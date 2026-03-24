import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

// ── Types ──

interface LocaleData {
  locale: string;
  uri: vscode.Uri;
  keys: Map<string, string>; // flattened dot-notation key → value
}

interface LocaleKeyItem {
  type: 'locale' | 'key';
  locale?: string;
  uri?: vscode.Uri;
  key?: string;
  value?: string;
  missing?: string[]; // locales where this key is missing
}

// ── Helpers ──

function getConfig() {
  const cfg = vscode.workspace.getConfiguration('i18nHelper');
  return {
    localesPath: cfg.get<string>('localesPath', 'src/locales'),
    defaultLocale: cfg.get<string>('defaultLocale', 'en'),
    functionPatterns: cfg.get<string[]>('functionPatterns', ['t', '$t', 'i18n.t']),
  };
}

function flattenJson(obj: Record<string, unknown>, prefix = ''): Map<string, string> {
  const result = new Map<string, string>();
  for (const [k, v] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${k}` : k;
    if (v !== null && typeof v === 'object' && !Array.isArray(v)) {
      for (const [fk, fv] of flattenJson(v as Record<string, unknown>, fullKey)) {
        result.set(fk, fv);
      }
    } else {
      result.set(fullKey, String(v));
    }
  }
  return result;
}

function unflattenJson(map: Map<string, string>): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of map) {
    const parts = key.split('.');
    let current: Record<string, unknown> = result;
    for (let i = 0; i < parts.length - 1; i++) {
      if (!(parts[i] in current) || typeof current[parts[i]] !== 'object') {
        current[parts[i]] = {};
      }
      current = current[parts[i]] as Record<string, unknown>;
    }
    current[parts[parts.length - 1]] = value;
  }
  return result;
}

function sortObjectKeys(obj: Record<string, unknown>): Record<string, unknown> {
  const sorted: Record<string, unknown> = {};
  for (const key of Object.keys(obj).sort()) {
    const val = obj[key];
    if (val !== null && typeof val === 'object' && !Array.isArray(val)) {
      sorted[key] = sortObjectKeys(val as Record<string, unknown>);
    } else {
      sorted[key] = val;
    }
  }
  return sorted;
}

function setNestedKey(obj: Record<string, unknown>, dottedKey: string, value: string): void {
  const parts = dottedKey.split('.');
  let current: Record<string, unknown> = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    if (!(parts[i] in current) || typeof current[parts[i]] !== 'object') {
      current[parts[i]] = {};
    }
    current = current[parts[i]] as Record<string, unknown>;
  }
  current[parts[parts.length - 1]] = value;
}

function deleteNestedKey(obj: Record<string, unknown>, dottedKey: string): boolean {
  const parts = dottedKey.split('.');
  let current: Record<string, unknown> = obj;
  for (let i = 0; i < parts.length - 1; i++) {
    if (!(parts[i] in current) || typeof current[parts[i]] !== 'object') {
      return false;
    }
    current = current[parts[i]] as Record<string, unknown>;
  }
  if (parts[parts.length - 1] in current) {
    delete current[parts[parts.length - 1]];
    return true;
  }
  return false;
}

// ── Locale Scanner ──

class LocaleScanner {
  private locales: LocaleData[] = [];

  getLocales(): LocaleData[] { return this.locales; }

  getAllKeys(): string[] {
    const keys = new Set<string>();
    for (const loc of this.locales) {
      for (const k of loc.keys.keys()) { keys.add(k); }
    }
    return [...keys].sort();
  }

  getLocalesDir(): string | undefined {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders || folders.length === 0) { return undefined; }
    const cfg = getConfig();
    return path.join(folders[0].uri.fsPath, cfg.localesPath);
  }

  async scan(): Promise<void> {
    this.locales = [];
    const dir = this.getLocalesDir();
    if (!dir || !fs.existsSync(dir)) { return; }

    const files = fs.readdirSync(dir).filter((f) => f.endsWith('.json'));
    for (const file of files) {
      const filePath = path.join(dir, file);
      try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const json = JSON.parse(content);
        const locale = path.basename(file, '.json');
        const keys = flattenJson(json);
        this.locales.push({ locale, uri: vscode.Uri.file(filePath), keys });
      } catch { /* skip invalid JSON */ }
    }
  }

  getMissingKeys(): Map<string, string[]> {
    // key → list of locales where it's missing
    const allKeys = this.getAllKeys();
    const localeNames = this.locales.map((l) => l.locale);
    const missing = new Map<string, string[]>();
    for (const key of allKeys) {
      const missingIn: string[] = [];
      for (const loc of this.locales) {
        if (!loc.keys.has(key)) { missingIn.push(loc.locale); }
      }
      if (missingIn.length > 0 && missingIn.length < localeNames.length) {
        missing.set(key, missingIn);
      }
    }
    return missing;
  }
}

// ── TreeView Provider ──

class I18nTreeProvider implements vscode.TreeDataProvider<LocaleKeyItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  constructor(private scanner: LocaleScanner) {}

  refresh(): void { this._onDidChangeTreeData.fire(); }

  getTreeItem(element: LocaleKeyItem): vscode.TreeItem {
    if (element.type === 'locale') {
      const item = new vscode.TreeItem(element.locale!, vscode.TreeItemCollapsibleState.Collapsed);
      const loc = this.scanner.getLocales().find((l) => l.locale === element.locale);
      item.description = loc ? `${loc.keys.size} keys` : '';
      item.iconPath = new vscode.ThemeIcon('globe');
      item.contextValue = 'locale';
      if (element.uri) {
        item.command = { command: 'vscode.open', title: 'Open', arguments: [element.uri] };
      }
      return item;
    }

    // key item
    const item = new vscode.TreeItem(element.key!, vscode.TreeItemCollapsibleState.None);
    if (element.missing && element.missing.length > 0) {
      item.description = `missing in: ${element.missing.join(', ')}`;
      item.iconPath = new vscode.ThemeIcon('warning', new vscode.ThemeColor('editorWarning.foreground'));
    } else {
      item.description = element.value && element.value.length > 40
        ? element.value.substring(0, 40) + '...'
        : element.value;
      item.iconPath = new vscode.ThemeIcon('symbol-string');
    }
    item.tooltip = element.value || '';
    return item;
  }

  getChildren(element?: LocaleKeyItem): LocaleKeyItem[] {
    if (!element) {
      // Root: show locales + missing keys section
      const locales = this.scanner.getLocales();
      const items: LocaleKeyItem[] = locales.map((l) => ({
        type: 'locale' as const,
        locale: l.locale,
        uri: l.uri,
      }));
      return items;
    }

    if (element.type === 'locale') {
      const loc = this.scanner.getLocales().find((l) => l.locale === element.locale);
      if (!loc) { return []; }
      const missing = this.scanner.getMissingKeys();
      return [...loc.keys.entries()].sort((a, b) => a[0].localeCompare(b[0])).map(([key, value]) => ({
        type: 'key' as const,
        key,
        value,
        missing: missing.get(key)?.filter((m) => m !== element.locale),
      }));
    }

    return [];
  }
}

// ── Completion Provider ──

class I18nCompletionProvider implements vscode.CompletionItemProvider {
  constructor(private scanner: LocaleScanner) {}

  provideCompletionItems(
    document: vscode.TextDocument,
    position: vscode.Position
  ): vscode.CompletionItem[] | undefined {
    const lineText = document.lineAt(position).text;
    const linePrefix = lineText.substring(0, position.character);

    // Check if we're inside a translation function call
    const cfg = getConfig();
    const patterns = cfg.functionPatterns.map((p) =>
      p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    );
    const regex = new RegExp(`(?:${patterns.join('|')})\\(['\`"]([^'\`"]*)$`);
    const match = regex.exec(linePrefix);
    if (!match) { return undefined; }

    const typedPrefix = match[1];
    const defaultLocale = this.scanner.getLocales().find((l) => l.locale === cfg.defaultLocale);
    const allKeys = this.scanner.getAllKeys();

    return allKeys
      .filter((key) => key.startsWith(typedPrefix) || key.includes(typedPrefix))
      .map((key) => {
        const item = new vscode.CompletionItem(key, vscode.CompletionItemKind.Text);
        const value = defaultLocale?.keys.get(key);
        item.detail = value || '';
        item.documentation = new vscode.MarkdownString(
          this.scanner.getLocales()
            .map((l) => `**${l.locale}**: ${l.keys.get(key) || '*(missing)*'}`)
            .join('\n\n')
        );
        // Replace only the part after the opening quote
        const startChar = position.character - typedPrefix.length;
        item.range = new vscode.Range(position.line, startChar, position.line, position.character);
        return item;
      });
  }
}

// ── Hover Provider ──

class I18nHoverProvider implements vscode.HoverProvider {
  constructor(private scanner: LocaleScanner) {}

  provideHover(
    document: vscode.TextDocument,
    position: vscode.Position
  ): vscode.Hover | undefined {
    const lineText = document.lineAt(position).text;
    const cfg = getConfig();
    const patterns = cfg.functionPatterns.map((p) =>
      p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
    );
    const regex = new RegExp(`(?:${patterns.join('|')})\\(['\`"]([^'\`"]+)['\`"]\\)`, 'g');

    let match: RegExpExecArray | null;
    while ((match = regex.exec(lineText)) !== null) {
      const keyStart = match.index + match[0].indexOf(match[1]);
      const keyEnd = keyStart + match[1].length;
      if (position.character >= keyStart && position.character <= keyEnd) {
        const key = match[1];
        const lines = this.scanner.getLocales().map((l) => {
          const val = l.keys.get(key);
          return val ? `**${l.locale}**: ${val}` : `**${l.locale}**: *(missing)*`;
        });
        if (lines.length === 0) { return undefined; }
        const md = new vscode.MarkdownString(lines.join('\n\n'));
        return new vscode.Hover(md, new vscode.Range(position.line, keyStart, position.line, keyEnd));
      }
    }
    return undefined;
  }
}

// ── Diagnostics ──

function updateDiagnostics(scanner: LocaleScanner, collection: vscode.DiagnosticCollection): void {
  collection.clear();
  const missing = scanner.getMissingKeys();
  if (missing.size === 0) { return; }

  // Show diagnostics on each locale file for keys it's missing
  for (const loc of scanner.getLocales()) {
    const diags: vscode.Diagnostic[] = [];
    for (const [key, missingLocales] of missing) {
      if (missingLocales.includes(loc.locale)) {
        const diag = new vscode.Diagnostic(
          new vscode.Range(0, 0, 0, 0),
          `Missing translation key: "${key}"`,
          vscode.DiagnosticSeverity.Warning
        );
        diag.source = 'i18n Helper';
        diag.code = key;
        diags.push(diag);
      }
    }
    if (diags.length > 0) {
      collection.set(loc.uri, diags);
    }
  }
}

// ── Code Action Provider (Quick Fix) ──

class I18nCodeActionProvider implements vscode.CodeActionProvider {
  constructor(private scanner: LocaleScanner) {}

  provideCodeActions(
    document: vscode.TextDocument,
    _range: vscode.Range,
    context: vscode.CodeActionContext
  ): vscode.CodeAction[] {
    const actions: vscode.CodeAction[] = [];
    for (const diag of context.diagnostics) {
      if (diag.source !== 'i18n Helper' || !diag.code) { continue; }
      const key = String(diag.code);
      const action = new vscode.CodeAction(
        `Add missing key "${key}" with placeholder`,
        vscode.CodeActionKind.QuickFix
      );
      action.command = {
        command: 'i18nHelper.addMissingKey',
        title: 'Add missing key',
        arguments: [key, document.uri],
      };
      action.diagnostics = [diag];
      action.isPreferred = true;
      actions.push(action);
    }
    return actions;
  }
}

// ── Commands ──

async function findMissingTranslations(scanner: LocaleScanner): Promise<void> {
  const missing = scanner.getMissingKeys();
  if (missing.size === 0) {
    vscode.window.showInformationMessage('All translation keys are complete across all locales.');
    return;
  }

  let report = `# Missing Translations Report\n\n`;
  report += `| Key | Missing in |\n|-----|------------|\n`;
  for (const [key, locales] of missing) {
    report += `| \`${key}\` | ${locales.join(', ')} |\n`;
  }
  report += `\n**Total**: ${missing.size} keys with missing translations\n`;

  const doc = await vscode.workspace.openTextDocument({ content: report, language: 'markdown' });
  await vscode.window.showTextDocument(doc);
}

async function sortKeysInAllLocales(scanner: LocaleScanner): Promise<void> {
  const dir = scanner.getLocalesDir();
  if (!dir) { return; }

  let count = 0;
  for (const loc of scanner.getLocales()) {
    try {
      const content = fs.readFileSync(loc.uri.fsPath, 'utf-8');
      const json = JSON.parse(content);
      const sorted = sortObjectKeys(json);
      fs.writeFileSync(loc.uri.fsPath, JSON.stringify(sorted, null, 2) + '\n', 'utf-8');
      count++;
    } catch { /* skip */ }
  }
  vscode.window.showInformationMessage(`Sorted keys in ${count} locale file(s).`);
}

async function addKeyToAllLocales(scanner: LocaleScanner): Promise<void> {
  const key = await vscode.window.showInputBox({
    prompt: 'Enter the translation key (dot-notation supported, e.g. "common.save")',
    placeHolder: 'common.save',
  });
  if (!key) { return; }

  const value = await vscode.window.showInputBox({
    prompt: `Enter the default value for "${key}"`,
    placeHolder: 'Save',
  });
  if (value === undefined) { return; }

  for (const loc of scanner.getLocales()) {
    try {
      const content = fs.readFileSync(loc.uri.fsPath, 'utf-8');
      const json = JSON.parse(content);
      setNestedKey(json, key, loc.locale === getConfig().defaultLocale ? value : `[TODO:${loc.locale}] ${value}`);
      fs.writeFileSync(loc.uri.fsPath, JSON.stringify(json, null, 2) + '\n', 'utf-8');
    } catch { /* skip */ }
  }
  vscode.window.showInformationMessage(`Added "${key}" to ${scanner.getLocales().length} locale file(s).`);
}

async function addMissingKey(scanner: LocaleScanner, key: string): Promise<void> {
  // Find the default locale's value for this key
  const cfg = getConfig();
  const defaultLoc = scanner.getLocales().find((l) => l.locale === cfg.defaultLocale);
  const defaultValue = defaultLoc?.keys.get(key) || '';

  for (const loc of scanner.getLocales()) {
    if (loc.keys.has(key)) { continue; }
    try {
      const content = fs.readFileSync(loc.uri.fsPath, 'utf-8');
      const json = JSON.parse(content);
      setNestedKey(json, key, `[TODO:${loc.locale}] ${defaultValue}`);
      fs.writeFileSync(loc.uri.fsPath, JSON.stringify(json, null, 2) + '\n', 'utf-8');
    } catch { /* skip */ }
  }
  vscode.window.showInformationMessage(`Added placeholder for "${key}" in missing locales.`);
}

async function renameKeyInAllLocales(scanner: LocaleScanner): Promise<void> {
  const allKeys = scanner.getAllKeys();
  const oldKey = await vscode.window.showQuickPick(allKeys, {
    placeHolder: 'Select the key to rename',
  });
  if (!oldKey) { return; }

  const newKey = await vscode.window.showInputBox({
    prompt: `Rename "${oldKey}" to:`,
    value: oldKey,
  });
  if (!newKey || newKey === oldKey) { return; }

  for (const loc of scanner.getLocales()) {
    try {
      const content = fs.readFileSync(loc.uri.fsPath, 'utf-8');
      const json = JSON.parse(content);
      const flat = flattenJson(json);
      if (flat.has(oldKey)) {
        const value = flat.get(oldKey)!;
        deleteNestedKey(json, oldKey);
        setNestedKey(json, newKey, value);
        fs.writeFileSync(loc.uri.fsPath, JSON.stringify(json, null, 2) + '\n', 'utf-8');
      }
    } catch { /* skip */ }
  }
  vscode.window.showInformationMessage(`Renamed "${oldKey}" → "${newKey}" across all locales.`);
}

async function deleteKeyFromAllLocales(scanner: LocaleScanner): Promise<void> {
  const allKeys = scanner.getAllKeys();
  const key = await vscode.window.showQuickPick(allKeys, {
    placeHolder: 'Select the key to delete',
  });
  if (!key) { return; }

  const confirm = await vscode.window.showWarningMessage(
    `Delete "${key}" from all locale files?`,
    { modal: true },
    'Delete'
  );
  if (confirm !== 'Delete') { return; }

  for (const loc of scanner.getLocales()) {
    try {
      const content = fs.readFileSync(loc.uri.fsPath, 'utf-8');
      const json = JSON.parse(content);
      deleteNestedKey(json, key);
      fs.writeFileSync(loc.uri.fsPath, JSON.stringify(json, null, 2) + '\n', 'utf-8');
    } catch { /* skip */ }
  }
  vscode.window.showInformationMessage(`Deleted "${key}" from all locale files.`);
}

// ── Activation ──

export function activate(context: vscode.ExtensionContext) {
  const scanner = new LocaleScanner();
  const treeProvider = new I18nTreeProvider(scanner);
  const diagnosticCollection = vscode.languages.createDiagnosticCollection('i18nHelper');
  const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 40);
  statusBarItem.command = 'i18nHelper.findMissing';

  vscode.window.registerTreeDataProvider('i18nHelperView', treeProvider);

  const refresh = async () => {
    await scanner.scan();
    treeProvider.refresh();
    updateDiagnostics(scanner, diagnosticCollection);

    const missing = scanner.getMissingKeys();
    if (missing.size > 0) {
      statusBarItem.text = `$(warning) i18n: ${missing.size} missing`;
      statusBarItem.tooltip = `${missing.size} keys with missing translations`;
    } else {
      statusBarItem.text = `$(globe) i18n: OK`;
      statusBarItem.tooltip = 'All translations complete';
    }
    statusBarItem.show();
  };

  // Register completion provider for common file types
  const selector: vscode.DocumentSelector = [
    { scheme: 'file', language: 'javascript' },
    { scheme: 'file', language: 'typescript' },
    { scheme: 'file', language: 'javascriptreact' },
    { scheme: 'file', language: 'typescriptreact' },
    { scheme: 'file', language: 'vue' },
    { scheme: 'file', language: 'svelte' },
    { scheme: 'file', language: 'html' },
  ];

  context.subscriptions.push(
    // Commands
    vscode.commands.registerCommand('i18nHelper.findMissing', () => findMissingTranslations(scanner)),
    vscode.commands.registerCommand('i18nHelper.sortKeys', async () => {
      await sortKeysInAllLocales(scanner);
      await refresh();
    }),
    vscode.commands.registerCommand('i18nHelper.addKey', async () => {
      await addKeyToAllLocales(scanner);
      await refresh();
    }),
    vscode.commands.registerCommand('i18nHelper.renameKey', async () => {
      await renameKeyInAllLocales(scanner);
      await refresh();
    }),
    vscode.commands.registerCommand('i18nHelper.deleteKey', async () => {
      await deleteKeyFromAllLocales(scanner);
      await refresh();
    }),
    vscode.commands.registerCommand('i18nHelper.refresh', refresh),
    vscode.commands.registerCommand('i18nHelper.addMissingKey', async (key: string) => {
      await addMissingKey(scanner, key);
      await refresh();
    }),

    // Providers
    vscode.languages.registerCompletionItemProvider(selector, new I18nCompletionProvider(scanner), "'", '"', '`', '.'),
    vscode.languages.registerHoverProvider(selector, new I18nHoverProvider(scanner)),
    vscode.languages.registerCodeActionsProvider({ scheme: 'file', pattern: '**/*.json' }, new I18nCodeActionProvider(scanner)),

    // File watchers
    vscode.workspace.onDidSaveTextDocument((doc) => {
      if (doc.fileName.endsWith('.json')) { refresh(); }
    }),
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('i18nHelper')) { refresh(); }
    }),

    // Disposables
    diagnosticCollection,
    statusBarItem,
  );

  // Initial scan
  refresh();
}

export function deactivate() {}
