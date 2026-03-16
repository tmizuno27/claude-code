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
function detectType(value) {
    if (value === null || value === undefined) {
        return 'null';
    }
    if (Array.isArray(value)) {
        return 'array';
    }
    if (typeof value === 'object') {
        return 'object';
    }
    if (typeof value === 'number') {
        return 'number';
    }
    if (typeof value === 'boolean') {
        return 'boolean';
    }
    return 'string';
}
function buildPath(parent, key, isArrayItem) {
    if (!parent) {
        return key;
    }
    if (isArrayItem) {
        return `${parent}[${key}]`;
    }
    return /^[a-zA-Z_$][a-zA-Z0-9_$]*$/.test(key) ? `${parent}.${key}` : `${parent}["${key}"]`;
}
// ─── Tree Data Provider ───────────────────────────────────
class ResponseTreeItem extends vscode.TreeItem {
    node;
    children;
    constructor(node, children) {
        const hasChildren = node.type === 'object' || node.type === 'array';
        super(ResponseTreeItem.buildLabel(node), hasChildren
            ? vscode.TreeItemCollapsibleState.Collapsed
            : vscode.TreeItemCollapsibleState.None);
        this.node = node;
        this.children = children;
        this.tooltip = `${node.path}\nType: ${node.type}`;
        this.description = ResponseTreeItem.buildDescription(node);
        this.contextValue = 'responseNode';
        this.iconPath = ResponseTreeItem.buildIcon(node.type);
    }
    static buildLabel(node) {
        return node.key;
    }
    static buildDescription(node) {
        switch (node.type) {
            case 'array':
                return `Array(${node.childCount ?? 0})`;
            case 'object':
                return `{${node.childCount ?? 0} keys}`;
            case 'string':
                return `"${String(node.value)}"`;
            case 'null':
                return 'null';
            default:
                return String(node.value);
        }
    }
    static buildIcon(type) {
        switch (type) {
            case 'object': return new vscode.ThemeIcon('symbol-object');
            case 'array': return new vscode.ThemeIcon('symbol-array');
            case 'string': return new vscode.ThemeIcon('symbol-string');
            case 'number': return new vscode.ThemeIcon('symbol-number');
            case 'boolean': return new vscode.ThemeIcon('symbol-boolean');
            case 'null': return new vscode.ThemeIcon('symbol-null');
        }
    }
}
class ResponseTreeProvider {
    _onDidChangeTreeData = new vscode.EventEmitter();
    onDidChangeTreeData = this._onDidChangeTreeData.event;
    rootItems = [];
    allItems = [];
    filterText = '';
    setData(json) {
        this.rootItems = this.buildTree(json, '', '', false);
        this.allItems = this.flattenAll(this.rootItems);
        this.filterText = '';
        this._onDidChangeTreeData.fire();
    }
    setFilter(text) {
        this.filterText = text.toLowerCase();
        this._onDidChangeTreeData.fire();
    }
    clearFilter() {
        this.filterText = '';
        this._onDidChangeTreeData.fire();
    }
    getTreeItem(element) {
        if (this.filterText && this.matchesFilter(element)) {
            const item = new ResponseTreeItem(element.node, element.children);
            item.collapsibleState = element.children.length > 0
                ? vscode.TreeItemCollapsibleState.Expanded
                : vscode.TreeItemCollapsibleState.None;
            return item;
        }
        return element;
    }
    getChildren(element) {
        const items = element ? element.children : this.rootItems;
        if (!this.filterText) {
            return items;
        }
        return items.filter((item) => this.subtreeMatchesFilter(item));
    }
    matchesFilter(item) {
        const node = item.node;
        const filter = this.filterText;
        if (node.key.toLowerCase().includes(filter)) {
            return true;
        }
        if (node.type !== 'object' && node.type !== 'array') {
            if (String(node.value).toLowerCase().includes(filter)) {
                return true;
            }
        }
        return false;
    }
    subtreeMatchesFilter(item) {
        if (this.matchesFilter(item)) {
            return true;
        }
        return item.children.some((child) => this.subtreeMatchesFilter(child));
    }
    flattenAll(items) {
        const result = [];
        for (const item of items) {
            result.push(item);
            result.push(...this.flattenAll(item.children));
        }
        return result;
    }
    buildTree(value, key, parentPath, isArrayItem) {
        const type = detectType(value);
        const path = key ? buildPath(parentPath, key, isArrayItem) : '';
        if (type === 'object' && value !== null) {
            const obj = value;
            const keys = Object.keys(obj);
            const node = { key: key || '{}', value, path: path || '$', type: 'object', childCount: keys.length };
            const children = keys.flatMap((k) => this.buildTree(obj[k], k, path || '$', false));
            const item = new ResponseTreeItem(node, children);
            return key ? [item] : children;
        }
        if (type === 'array') {
            const arr = value;
            const node = { key: key || '[]', value, path: path || '$', type: 'array', childCount: arr.length };
            const children = arr.flatMap((v, i) => this.buildTree(v, String(i), path || '$', true));
            const item = new ResponseTreeItem(node, children);
            return key ? [item] : children;
        }
        const node = { key: key || String(value), value, path: path || '$', type };
        return [new ResponseTreeItem(node, [])];
    }
}
// ─── XML Parser (simple) ─────────────────────────────────
function tryParseXmlToJson(text) {
    const trimmed = text.trim();
    if (!trimmed.startsWith('<')) {
        return null;
    }
    try {
        const result = {};
        const tagRegex = /<(\w+)([^>]*)>([\s\S]*?)<\/\1>/g;
        let match;
        let found = false;
        while ((match = tagRegex.exec(trimmed)) !== null) {
            found = true;
            const [, tagName, , content] = match;
            const inner = content.trim();
            if (/<\w/.test(inner)) {
                const nested = tryParseXmlToJson(inner);
                result[tagName] = nested ?? inner;
            }
            else {
                // Try to parse as number/boolean
                if (inner === 'true') {
                    result[tagName] = true;
                }
                else if (inner === 'false') {
                    result[tagName] = false;
                }
                else if (inner === '' || inner === 'null') {
                    result[tagName] = null;
                }
                else if (!isNaN(Number(inner)) && inner !== '') {
                    result[tagName] = Number(inner);
                }
                else {
                    result[tagName] = inner;
                }
            }
        }
        return found ? result : null;
    }
    catch {
        return null;
    }
}
// ─── Parse Input ──────────────────────────────────────────
function parseInput(text) {
    const trimmed = text.trim();
    // Try JSON first
    try {
        return JSON.parse(trimmed);
    }
    catch {
        // Not JSON
    }
    // Try XML
    const xmlResult = tryParseXmlToJson(trimmed);
    if (xmlResult !== null) {
        return xmlResult;
    }
    throw new Error('Input is not valid JSON or XML.');
}
function compareObjects(a, b, path = '$') {
    const result = { added: [], removed: [], changed: [], unchanged: [] };
    if (typeof a !== typeof b || Array.isArray(a) !== Array.isArray(b)) {
        result.changed.push({ path, oldValue: a, newValue: b });
        return result;
    }
    if (Array.isArray(a) && Array.isArray(b)) {
        const maxLen = Math.max(a.length, b.length);
        for (let i = 0; i < maxLen; i++) {
            const itemPath = `${path}[${i}]`;
            if (i >= a.length) {
                result.added.push(itemPath);
            }
            else if (i >= b.length) {
                result.removed.push(itemPath);
            }
            else {
                const sub = compareObjects(a[i], b[i], itemPath);
                result.added.push(...sub.added);
                result.removed.push(...sub.removed);
                result.changed.push(...sub.changed);
                result.unchanged.push(...sub.unchanged);
            }
        }
        return result;
    }
    if (a !== null && b !== null && typeof a === 'object' && typeof b === 'object') {
        const objA = a;
        const objB = b;
        const allKeys = new Set([...Object.keys(objA), ...Object.keys(objB)]);
        for (const key of allKeys) {
            const keyPath = /^[a-zA-Z_$][a-zA-Z0-9_$]*$/.test(key) ? `${path}.${key}` : `${path}["${key}"]`;
            if (!(key in objA)) {
                result.added.push(keyPath);
            }
            else if (!(key in objB)) {
                result.removed.push(keyPath);
            }
            else {
                const sub = compareObjects(objA[key], objB[key], keyPath);
                result.added.push(...sub.added);
                result.removed.push(...sub.removed);
                result.changed.push(...sub.changed);
                result.unchanged.push(...sub.unchanged);
            }
        }
        return result;
    }
    if (a === b) {
        result.unchanged.push(path);
    }
    else {
        result.changed.push({ path, oldValue: a, newValue: b });
    }
    return result;
}
function formatDiffReport(diff) {
    const lines = ['# API Response Comparison\n'];
    if (diff.added.length) {
        lines.push(`## Added (${diff.added.length})`);
        diff.added.forEach((p) => lines.push(`+ ${p}`));
        lines.push('');
    }
    if (diff.removed.length) {
        lines.push(`## Removed (${diff.removed.length})`);
        diff.removed.forEach((p) => lines.push(`- ${p}`));
        lines.push('');
    }
    if (diff.changed.length) {
        lines.push(`## Changed (${diff.changed.length})`);
        diff.changed.forEach((c) => lines.push(`~ ${c.path}: ${JSON.stringify(c.oldValue)} → ${JSON.stringify(c.newValue)}`));
        lines.push('');
    }
    lines.push(`## Summary`);
    lines.push(`- Added: ${diff.added.length}`);
    lines.push(`- Removed: ${diff.removed.length}`);
    lines.push(`- Changed: ${diff.changed.length}`);
    lines.push(`- Unchanged: ${diff.unchanged.length}`);
    return lines.join('\n');
}
// ─── Activation ───────────────────────────────────────────
function activate(context) {
    const treeProvider = new ResponseTreeProvider();
    const treeView = vscode.window.createTreeView('apiResponseTree', {
        treeDataProvider: treeProvider,
        showCollapseAll: true,
    });
    // Store last two parsed values for comparison
    let lastParsed = null;
    let previousParsed = null;
    function loadData(data) {
        previousParsed = lastParsed;
        lastParsed = data;
        treeProvider.setData(data);
        treeView.title = 'Response Tree';
    }
    // Command: Open from editor selection
    const openCmd = vscode.commands.registerCommand('apiResponseViewer.open', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showWarningMessage('No active editor.');
            return;
        }
        const selection = editor.selection;
        let text;
        if (selection.isEmpty) {
            text = editor.document.getText();
        }
        else {
            text = editor.document.getText(selection);
        }
        if (!text.trim()) {
            vscode.window.showWarningMessage('No text selected or document is empty.');
            return;
        }
        try {
            const data = parseInput(text);
            loadData(data);
            vscode.window.showInformationMessage('API Response loaded into tree view.');
        }
        catch (err) {
            vscode.window.showErrorMessage(`Failed to parse: ${err instanceof Error ? err.message : String(err)}`);
        }
    });
    // Command: Open from clipboard
    const clipboardCmd = vscode.commands.registerCommand('apiResponseViewer.fromClipboard', async () => {
        const text = await vscode.env.clipboard.readText();
        if (!text.trim()) {
            vscode.window.showWarningMessage('Clipboard is empty.');
            return;
        }
        try {
            const data = parseInput(text);
            loadData(data);
            vscode.window.showInformationMessage('API Response loaded from clipboard.');
        }
        catch (err) {
            vscode.window.showErrorMessage(`Failed to parse clipboard: ${err instanceof Error ? err.message : String(err)}`);
        }
    });
    // Command: Copy JSON path
    const copyPathCmd = vscode.commands.registerCommand('apiResponseViewer.copyPath', async (item) => {
        if (!item?.node?.path) {
            return;
        }
        await vscode.env.clipboard.writeText(item.node.path);
        vscode.window.showInformationMessage(`Copied: ${item.node.path}`);
    });
    // Command: Copy value
    const copyValueCmd = vscode.commands.registerCommand('apiResponseViewer.copyValue', async (item) => {
        if (!item?.node) {
            return;
        }
        const val = item.node.type === 'object' || item.node.type === 'array'
            ? JSON.stringify(item.node.value, null, 2)
            : String(item.node.value);
        await vscode.env.clipboard.writeText(val);
        vscode.window.showInformationMessage('Value copied to clipboard.');
    });
    // Command: Search/filter
    const searchCmd = vscode.commands.registerCommand('apiResponseViewer.search', async () => {
        const query = await vscode.window.showInputBox({
            prompt: 'Search keys and values',
            placeHolder: 'e.g. "name", "200", "error"',
        });
        if (query === undefined) {
            return;
        }
        if (query === '') {
            treeProvider.clearFilter();
            vscode.window.showInformationMessage('Filter cleared.');
        }
        else {
            treeProvider.setFilter(query);
            vscode.window.showInformationMessage(`Filtered by: "${query}"`);
        }
    });
    // Command: Clear filter
    const clearFilterCmd = vscode.commands.registerCommand('apiResponseViewer.clearFilter', () => {
        treeProvider.clearFilter();
        vscode.window.showInformationMessage('Filter cleared.');
    });
    // Command: Open from file
    const fromFileCmd = vscode.commands.registerCommand('apiResponseViewer.fromFile', async () => {
        const uris = await vscode.window.showOpenDialog({
            canSelectMany: false,
            filters: { 'JSON/XML': ['json', 'xml', 'txt'] },
            openLabel: 'Open API Response',
        });
        if (!uris || uris.length === 0) {
            return;
        }
        try {
            const content = await vscode.workspace.fs.readFile(uris[0]);
            const text = Buffer.from(content).toString('utf-8');
            const data = parseInput(text);
            loadData(data);
            vscode.window.showInformationMessage(`Loaded from ${uris[0].fsPath}`);
        }
        catch (err) {
            vscode.window.showErrorMessage(`Failed to load file: ${err instanceof Error ? err.message : String(err)}`);
        }
    });
    // Command: Compare two responses
    const compareCmd = vscode.commands.registerCommand('apiResponseViewer.compare', async () => {
        if (!previousParsed || !lastParsed) {
            vscode.window.showWarningMessage('Load at least two responses to compare. Use "Open Response" or "View from Clipboard" twice.');
            return;
        }
        const diff = compareObjects(previousParsed, lastParsed);
        const report = formatDiffReport(diff);
        const doc = await vscode.workspace.openTextDocument({
            content: report,
            language: 'markdown',
        });
        await vscode.window.showTextDocument(doc, { preview: true });
    });
    context.subscriptions.push(treeView, openCmd, clipboardCmd, copyPathCmd, copyValueCmd, searchCmd, clearFilterCmd, fromFileCmd, compareCmd);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map