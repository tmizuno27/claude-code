import * as vscode from 'vscode';
import { execSync } from 'child_process';
import * as path from 'path';

const EMOJI_MAP: Record<string, string> = {
    feat: '\u2728', fix: '\uD83D\uDC1B', docs: '\uD83D\uDCDD', style: '\uD83D\uDC8E',
    refactor: '\u267B\uFE0F', perf: '\u26A1', test: '\uD83E\uDDEA', build: '\uD83D\uDCE6',
    ci: '\uD83D\uDE80', chore: '\uD83D\uDD27'
};

const TYPE_DESCRIPTIONS: Record<string, string> = {
    feat: 'A new feature',
    fix: 'A bug fix',
    docs: 'Documentation only changes',
    style: 'Code style changes (formatting, etc.)',
    refactor: 'Code refactoring',
    perf: 'Performance improvements',
    test: 'Adding or updating tests',
    build: 'Build system or dependencies',
    ci: 'CI configuration changes',
    chore: 'Other changes (maintenance, etc.)'
};

function getWorkspacePath(): string | undefined {
    return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
}

function getGitDiffStats(cwd: string): { files: string[]; insertions: number; deletions: number } {
    try {
        const statOutput = execSync('git diff --staged --stat', { cwd, encoding: 'utf8' });
        const nameOnly = execSync('git diff --staged --name-only', { cwd, encoding: 'utf8' });
        const files = nameOnly.trim().split('\n').filter(Boolean);
        const insertionMatch = statOutput.match(/(\d+) insertion/);
        const deletionMatch = statOutput.match(/(\d+) deletion/);
        return {
            files,
            insertions: insertionMatch ? parseInt(insertionMatch[1]) : 0,
            deletions: deletionMatch ? parseInt(deletionMatch[1]) : 0
        };
    } catch {
        return { files: [], insertions: 0, deletions: 0 };
    }
}

function detectType(files: string[]): string {
    const exts = files.map(f => path.extname(f).toLowerCase());
    const names = files.map(f => path.basename(f).toLowerCase());
    if (names.some(n => n.includes('test') || n.includes('spec'))) { return 'test'; }
    if (exts.every(e => e === '.md' || e === '.txt' || e === '.rst')) { return 'docs'; }
    if (names.some(n => n.includes('dockerfile') || n === 'package.json' || n.includes('webpack'))) { return 'build'; }
    if (names.some(n => n.includes('.yml') || n.includes('.yaml'))) { return 'ci'; }
    if (exts.every(e => e === '.css' || e === '.scss' || e === '.less')) { return 'style'; }
    return 'feat';
}

function detectScopes(files: string[], configScopes: string[]): string[] {
    if (configScopes.length > 0) { return configScopes; }
    const dirs = new Set(files.map(f => {
        const parts = f.split('/');
        return parts.length > 1 ? parts[0] : '';
    }).filter(Boolean));
    return [...dirs];
}

function buildMessage(type: string, scope: string, description: string, config: vscode.WorkspaceConfiguration): string {
    const template = config.get<string>('template', '{type}({scope}): {description}');
    const enableEmoji = config.get<boolean>('enableEmoji', false);
    let msg = template
        .replace('{type}', type)
        .replace('{scope}', scope)
        .replace('{description}', description);
    if (!scope) { msg = msg.replace('()', ''); }
    if (enableEmoji && EMOJI_MAP[type]) { msg = `${EMOJI_MAP[type]} ${msg}`; }
    return msg;
}

async function setScmMessage(message: string): Promise<void> {
    const gitExtension = vscode.extensions.getExtension('vscode.git');
    if (gitExtension) {
        const git = gitExtension.exports.getAPI(1);
        if (git.repositories.length > 0) {
            git.repositories[0].inputBox.value = message;
            vscode.window.showInformationMessage(`Commit message set: ${message}`);
            return;
        }
    }
    await vscode.env.clipboard.writeText(message);
    vscode.window.showInformationMessage(`Commit message copied: ${message}`);
}

export function activate(context: vscode.ExtensionContext): void {
    context.subscriptions.push(
        vscode.commands.registerCommand('commitCrafter.generate', async () => {
            const cwd = getWorkspacePath();
            if (!cwd) { vscode.window.showErrorMessage('No workspace folder open.'); return; }
            const stats = getGitDiffStats(cwd);
            if (stats.files.length === 0) {
                vscode.window.showWarningMessage('No staged changes found.');
                return;
            }
            const config = vscode.workspace.getConfiguration('commitCrafter');
            const detectedType = detectType(stats.files);
            const scopes = detectScopes(stats.files, config.get<string[]>('scopes', []));

            const typeItems = Object.entries(TYPE_DESCRIPTIONS).map(([key, desc]) => ({
                label: key === detectedType ? `$(star) ${key}` : key,
                description: desc,
                value: key
            }));
            const typePick = await vscode.window.showQuickPick(typeItems, {
                placeHolder: `Select commit type (suggested: ${detectedType})`
            });
            if (!typePick) { return; }

            let scope = '';
            if (scopes.length > 0) {
                const scopeItems = [{ label: '(none)', value: '' }, ...scopes.map(s => ({ label: s, value: s }))];
                const scopePick = await vscode.window.showQuickPick(scopeItems, { placeHolder: 'Select scope (optional)' });
                if (scopePick) { scope = scopePick.value; }
            }

            const maxLen = config.get<number>('maxSubjectLength', 50);
            const suggested = stats.files.length === 1
                ? `update ${path.basename(stats.files[0])}`
                : `update ${stats.files.length} files (+${stats.insertions}/-${stats.deletions})`;
            const desc = await vscode.window.showInputBox({
                prompt: `Commit description (max ${maxLen} chars)`,
                value: suggested,
                validateInput: v => v.length > maxLen ? `Too long (${v.length}/${maxLen})` : undefined
            });
            if (!desc) { return; }

            await setScmMessage(buildMessage(typePick.value, scope, desc, config));
        }),

        vscode.commands.registerCommand('commitCrafter.selectTemplate', async () => {
            const templates = [
                { label: 'feat: new feature', value: 'feat: ' },
                { label: 'fix: bug fix', value: 'fix: ' },
                { label: 'docs: documentation', value: 'docs: ' },
                { label: 'refactor: code refactoring', value: 'refactor: ' },
                { label: 'test: add tests', value: 'test: ' },
                { label: 'chore: maintenance', value: 'chore: ' },
            ];
            const pick = await vscode.window.showQuickPick(templates, { placeHolder: 'Select a template' });
            if (!pick) { return; }
            const desc = await vscode.window.showInputBox({ prompt: 'Enter description' });
            if (!desc) { return; }
            await setScmMessage(pick.value + desc);
        })
    );
}

export function deactivate(): void {}
