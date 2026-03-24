import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

const SECRET_KEYWORDS = ['password', 'secret', 'token', 'key', 'api_key', 'apikey', 'auth', 'credential', 'private'];

interface EnvEntry {
  key: string;
  value: string;
  line: number;
}

interface EnvFile {
  uri: vscode.Uri;
  entries: EnvEntry[];
}

function parseEnvContent(content: string): EnvEntry[] {
  const entries: EnvEntry[] = [];
  const lines = content.split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line || line.startsWith('#')) { continue; }
    const eqIdx = line.indexOf('=');
    if (eqIdx === -1) { continue; }
    const key = line.substring(0, eqIdx).trim();
    const value = line.substring(eqIdx + 1).trim().replace(/^["']|["']$/g, '');
    entries.push({ key, value, line: i });
  }
  return entries;
}

function detectValueType(value: string): string {
  if (!value) { return 'empty'; }
  if (/^https?:\/\//.test(value)) { return 'URL'; }
  if (/^(true|false)$/i.test(value)) { return 'boolean'; }
  if (/^\d+(\.\d+)?$/.test(value)) { return 'number'; }
  if (/^[a-f0-9]{32,}$/i.test(value)) { return 'hash'; }
  return 'string';
}

function isSecretKey(key: string): boolean {
  const lower = key.toLowerCase();
  return SECRET_KEYWORDS.some((kw) => lower.includes(kw));
}

class EnvLensProvider implements vscode.TreeDataProvider<EnvFile | EnvEntry> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;
  private envFiles: EnvFile[] = [];

  async scan(): Promise<void> {
    this.envFiles = [];
    const files = await vscode.workspace.findFiles('**/.env*', '**/node_modules/**', 100);
    for (const uri of files) {
      const basename = path.basename(uri.fsPath);
      if (!basename.startsWith('.env')) { continue; }
      try {
        const content = (await vscode.workspace.fs.readFile(uri)).toString();
        const entries = parseEnvContent(content);
        if (entries.length > 0) {
          this.envFiles.push({ uri, entries });
        }
      } catch { /* skip */ }
    }
    this._onDidChangeTreeData.fire();
  }

  getEnvFiles(): EnvFile[] { return this.envFiles; }

  getTreeItem(element: EnvFile | EnvEntry): vscode.TreeItem {
    if ('entries' in element) {
      const item = new vscode.TreeItem(
        path.basename(element.uri.fsPath),
        vscode.TreeItemCollapsibleState.Expanded
      );
      item.description = `${element.entries.length} keys`;
      item.resourceUri = element.uri;
      item.contextValue = 'envFile';
      item.command = {
        command: 'vscode.open',
        title: 'Open',
        arguments: [element.uri],
      };
      return item;
    }

    const valueType = detectValueType(element.value);
    const isSecret = isSecretKey(element.key);
    const displayValue = isSecret ? '********' : (element.value.length > 30 ? element.value.substring(0, 30) + '...' : element.value);
    const item = new vscode.TreeItem(`${element.key}`, vscode.TreeItemCollapsibleState.None);
    item.description = `${displayValue} [${valueType}]`;

    if (isSecret) {
      item.iconPath = new vscode.ThemeIcon('shield', new vscode.ThemeColor('editorWarning.foreground'));
    } else {
      const iconMap: Record<string, string> = { URL: 'link', number: 'symbol-number', boolean: 'symbol-boolean', hash: 'key', empty: 'circle-slash' };
      item.iconPath = new vscode.ThemeIcon(iconMap[valueType] || 'symbol-string');
    }

    return item;
  }

  getChildren(element?: EnvFile | EnvEntry): (EnvFile | EnvEntry)[] {
    if (!element) { return this.envFiles; }
    if ('entries' in element) { return element.entries; }
    return [];
  }
}

const valueTypeDecorationType = vscode.window.createTextEditorDecorationType({
  after: { margin: '0 0 0 1em', fontStyle: 'italic' },
});
const secretDecorationType = vscode.window.createTextEditorDecorationType({
  backgroundColor: 'rgba(255, 200, 0, 0.15)',
  after: { contentText: ' ⚠ potential secret', color: 'rgba(255, 170, 0, 0.8)', fontStyle: 'italic', margin: '0 0 0 1em' },
});

function updateDecorations(editor: vscode.TextEditor): void {
  if (!path.basename(editor.document.fileName).startsWith('.env')) { return; }

  const content = editor.document.getText();
  const entries = parseEnvContent(content);
  const typeDecorations: vscode.DecorationOptions[] = [];
  const secretDecorations: vscode.DecorationOptions[] = [];

  for (const entry of entries) {
    const line = editor.document.lineAt(entry.line);
    const range = line.range;
    const vType = detectValueType(entry.value);

    if (isSecretKey(entry.key)) {
      secretDecorations.push({ range });
    } else {
      typeDecorations.push({
        range,
        renderOptions: { after: { contentText: `  [${vType}]`, color: 'rgba(150, 150, 150, 0.7)' } },
      });
    }
  }

  editor.setDecorations(valueTypeDecorationType, typeDecorations);
  editor.setDecorations(secretDecorationType, secretDecorations);
}

async function compareEnvFiles(envFiles: EnvFile[]): Promise<void> {
  if (envFiles.length < 2) {
    vscode.window.showWarningMessage('Need at least 2 .env files to compare.');
    return;
  }

  const picks = envFiles.map((f) => ({ label: path.basename(f.uri.fsPath), uri: f.uri }));

  const first = await vscode.window.showQuickPick(picks, { placeHolder: 'Select first .env file' });
  if (!first) { return; }

  const second = await vscode.window.showQuickPick(
    picks.filter((p) => p.uri.toString() !== first.uri.toString()),
    { placeHolder: 'Select second .env file' }
  );
  if (!second) { return; }

  // Generate comparison content
  const fileA = envFiles.find((f) => f.uri.toString() === first.uri.toString())!;
  const fileB = envFiles.find((f) => f.uri.toString() === second.uri.toString())!;
  const keysA = new Set(fileA.entries.map((e) => e.key));
  const keysB = new Set(fileB.entries.map((e) => e.key));

  const onlyA = [...keysA].filter((k) => !keysB.has(k));
  const onlyB = [...keysB].filter((k) => !keysA.has(k));
  const common = [...keysA].filter((k) => keysB.has(k));

  let report = `# ENV Comparison: ${first.label} vs ${second.label}\n\n`;
  report += `## Common keys (${common.length})\n`;
  for (const k of common) { report += `- ${k}\n`; }
  report += `\n## Only in ${first.label} (${onlyA.length})\n`;
  for (const k of onlyA) { report += `- ${k}\n`; }
  report += `\n## Only in ${second.label} (${onlyB.length})\n`;
  for (const k of onlyB) { report += `- ${k}\n`; }

  const doc = await vscode.workspace.openTextDocument({ content: report, language: 'markdown' });
  await vscode.window.showTextDocument(doc);
}

async function generateExample(envFiles: EnvFile[]): Promise<void> {
  const picks = envFiles.map((f) => ({ label: path.basename(f.uri.fsPath), uri: f.uri, entries: f.entries }));
  const selected = await vscode.window.showQuickPick(picks, { placeHolder: 'Select source .env file' });
  if (!selected) { return; }

  let content = '# Generated by ENV Lens\n';
  for (const entry of selected.entries) {
    const placeholder = isSecretKey(entry.key) ? 'your-secret-here' : detectValueType(entry.value) === 'URL' ? 'https://example.com' : '';
    content += `${entry.key}=${placeholder}\n`;
  }

  const dir = path.dirname(selected.uri.fsPath);
  const outPath = path.join(dir, '.env.example');
  fs.writeFileSync(outPath, content, 'utf-8');
  const doc = await vscode.workspace.openTextDocument(outPath);
  await vscode.window.showTextDocument(doc);
  vscode.window.showInformationMessage(`Generated ${outPath}`);
}

export function activate(context: vscode.ExtensionContext) {
  const provider = new EnvLensProvider();
  vscode.window.registerTreeDataProvider('envLensView', provider);

  const refresh = () => provider.scan();

  context.subscriptions.push(
    vscode.commands.registerCommand('envLens.refresh', refresh),
    vscode.commands.registerCommand('envLens.compare', () => compareEnvFiles(provider.getEnvFiles())),
    vscode.commands.registerCommand('envLens.generateExample', () => generateExample(provider.getEnvFiles())),
  );

  // Decorations on active editor
  context.subscriptions.push(
    vscode.window.onDidChangeActiveTextEditor((editor) => { if (editor) { updateDecorations(editor); } }),
    vscode.workspace.onDidChangeTextDocument((e) => {
      const editor = vscode.window.activeTextEditor;
      if (editor && editor.document === e.document) { updateDecorations(editor); }
    }),
    vscode.workspace.onDidSaveTextDocument(() => refresh()),
  );

  refresh();
  if (vscode.window.activeTextEditor) { updateDecorations(vscode.window.activeTextEditor); }
}

export function deactivate() {}
