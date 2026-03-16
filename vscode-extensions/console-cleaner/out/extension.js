"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const path = __importStar(require("path"));
const DEBUG_PATTERN = /^(\s*)(console\.(log|error|warn|info|debug|trace|dir|table|time|timeEnd|group|groupEnd|assert|count|clear)\s*\(.*\)\s*;?|debugger\s*;?|print\s*\(.*\)\s*;?)(\s*\/\/\s*keep)?/;
const COMMENTED_DEBUG_PATTERN = /^(\s*)\/\/\s*(console\.(log|error|warn|info|debug|trace|dir|table|time|timeEnd|group|groupEnd|assert|count|clear)\s*\(.*\)\s*;?|debugger\s*;?|print\s*\(.*\)\s*;?)/;
const SCAN_GLOBS = '**/*.{js,ts,jsx,tsx,mjs,cjs,py,vue,svelte}';
const EXCLUDE_GLOBS = '**/node_modules/**,**/dist/**,**/out/**,**/.next/**,**/vendor/**';
class ConsoleCleanerProvider {
    _onDidChangeTreeData = new vscode.EventEmitter();
    onDidChangeTreeData = this._onDidChangeTreeData.event;
    fileGroups = [];
    async scan() {
        this.fileGroups = [];
        const files = await vscode.workspace.findFiles(SCAN_GLOBS, EXCLUDE_GLOBS, 5000);
        for (const uri of files) {
            try {
                const doc = await vscode.workspace.openTextDocument(uri);
                const statements = [];
                for (let i = 0; i < doc.lineCount; i++) {
                    const lineText = doc.lineAt(i).text;
                    const match = DEBUG_PATTERN.exec(lineText);
                    const commentMatch = COMMENTED_DEBUG_PATTERN.exec(lineText);
                    if (match && !match[4]) {
                        statements.push({ uri, line: i, text: lineText.trim(), hasKeep: false, isCommented: false });
                    }
                    else if (match && match[4]) {
                        statements.push({ uri, line: i, text: lineText.trim(), hasKeep: true, isCommented: false });
                    }
                    else if (commentMatch) {
                        statements.push({ uri, line: i, text: lineText.trim(), hasKeep: false, isCommented: true });
                    }
                }
                if (statements.length > 0) {
                    this.fileGroups.push({ uri, statements });
                }
            }
            catch {
                // skip binary / unreadable files
            }
        }
        this._onDidChangeTreeData.fire();
    }
    getCount() {
        return this.fileGroups.reduce((sum, fg) => sum + fg.statements.filter((s) => !s.hasKeep && !s.isCommented).length, 0);
    }
    getTreeItem(element) {
        if ('statements' in element) {
            const item = new vscode.TreeItem(path.basename(element.uri.fsPath), vscode.TreeItemCollapsibleState.Expanded);
            item.description = `${element.statements.length} statements`;
            item.resourceUri = element.uri;
            item.contextValue = 'file';
            return item;
        }
        const item = new vscode.TreeItem(`L${element.line + 1}: ${element.text}`, vscode.TreeItemCollapsibleState.None);
        if (element.hasKeep) {
            item.description = '// keep';
            item.iconPath = new vscode.ThemeIcon('lock');
        }
        else if (element.isCommented) {
            item.description = 'commented';
            item.iconPath = new vscode.ThemeIcon('comment');
        }
        else {
            item.iconPath = new vscode.ThemeIcon('warning');
        }
        item.command = {
            command: 'vscode.open',
            title: 'Go to statement',
            arguments: [element.uri, { selection: new vscode.Range(element.line, 0, element.line, 0) }],
        };
        return item;
    }
    getChildren(element) {
        if (!element) {
            return this.fileGroups;
        }
        if ('statements' in element) {
            return element.statements;
        }
        return [];
    }
    getFileGroup(uri) {
        return this.fileGroups.find((fg) => fg.uri.toString() === uri.toString());
    }
    getAllStatements() {
        return this.fileGroups.flatMap((fg) => fg.statements);
    }
}
async function processStatements(statements, mode) {
    const byFile = new Map();
    for (const s of statements) {
        const key = s.uri.toString();
        if (!byFile.has(key)) {
            byFile.set(key, []);
        }
        byFile.get(key).push(s);
    }
    for (const [, stmts] of byFile) {
        const doc = await vscode.workspace.openTextDocument(stmts[0].uri);
        const edit = new vscode.WorkspaceEdit();
        // Process in reverse line order to avoid line number shifts
        const sorted = [...stmts].sort((a, b) => b.line - a.line);
        for (const stmt of sorted) {
            if (stmt.hasKeep) {
                continue;
            }
            const line = doc.lineAt(stmt.line);
            const range = line.rangeIncludingLineBreak;
            if (mode === 'remove' && !stmt.isCommented) {
                edit.delete(stmt.uri, range);
            }
            else if (mode === 'comment' && !stmt.isCommented) {
                const indent = line.text.match(/^(\s*)/)?.[1] || '';
                const content = line.text.trimStart();
                edit.replace(stmt.uri, line.range, `${indent}// ${content}`);
            }
            else if (mode === 'uncomment' && stmt.isCommented) {
                const newText = line.text.replace(/^(\s*)\/\/\s*/, '$1');
                edit.replace(stmt.uri, line.range, newText);
            }
        }
        await vscode.workspace.applyEdit(edit);
    }
}
let statusBarItem;
function updateStatusBar(count) {
    if (count > 0) {
        statusBarItem.text = `$(warning) ${count} debug`;
        statusBarItem.tooltip = `${count} debug statements found`;
        statusBarItem.show();
    }
    else {
        statusBarItem.text = '$(check) 0 debug';
        statusBarItem.tooltip = 'No debug statements';
        statusBarItem.show();
    }
}
let diagnosticCollection;
function updateDiagnostics(provider) {
    diagnosticCollection.clear();
    const byFile = new Map();
    for (const stmt of provider.getAllStatements()) {
        if (stmt.hasKeep || stmt.isCommented) {
            continue;
        }
        const key = stmt.uri.toString();
        if (!byFile.has(key)) {
            byFile.set(key, []);
        }
        const diag = new vscode.Diagnostic(new vscode.Range(stmt.line, 0, stmt.line, stmt.text.length), 'Debug statement found', vscode.DiagnosticSeverity.Warning);
        diag.source = 'Console Cleaner';
        byFile.get(key).push(diag);
    }
    for (const [uriStr, diags] of byFile) {
        diagnosticCollection.set(vscode.Uri.parse(uriStr), diags);
    }
}
function activate(context) {
    const provider = new ConsoleCleanerProvider();
    diagnosticCollection = vscode.languages.createDiagnosticCollection('consoleCleaner');
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 50);
    statusBarItem.command = 'consoleCleaner.refresh';
    vscode.window.registerTreeDataProvider('consoleCleanerView', provider);
    const refresh = async () => {
        await provider.scan();
        updateStatusBar(provider.getCount());
        updateDiagnostics(provider);
    };
    context.subscriptions.push(vscode.commands.registerCommand('consoleCleaner.refresh', refresh), vscode.commands.registerCommand('consoleCleaner.removeAll', async () => {
        await processStatements(provider.getAllStatements(), 'remove');
        await refresh();
        vscode.window.showInformationMessage('All debug statements removed.');
    }), vscode.commands.registerCommand('consoleCleaner.commentAll', async () => {
        await processStatements(provider.getAllStatements(), 'comment');
        await refresh();
        vscode.window.showInformationMessage('All debug statements commented out.');
    }), vscode.commands.registerCommand('consoleCleaner.uncommentAll', async () => {
        await processStatements(provider.getAllStatements(), 'uncomment');
        await refresh();
        vscode.window.showInformationMessage('All debug statements uncommented.');
    }), vscode.commands.registerCommand('consoleCleaner.removeInFile', async (fileGroup) => {
        if (fileGroup && 'statements' in fileGroup) {
            await processStatements(fileGroup.statements, 'remove');
            await refresh();
        }
    }), vscode.commands.registerCommand('consoleCleaner.commentInFile', async (fileGroup) => {
        if (fileGroup && 'statements' in fileGroup) {
            await processStatements(fileGroup.statements, 'comment');
            await refresh();
        }
    }), diagnosticCollection, statusBarItem);
    // Initial scan
    refresh();
    // Re-scan on save
    context.subscriptions.push(vscode.workspace.onDidSaveTextDocument(() => refresh()));
}
function deactivate() { }
//# sourceMappingURL=extension.js.map