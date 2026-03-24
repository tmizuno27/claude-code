import * as vscode from 'vscode';

// ── Interfaces ──────────────────────────────────────────────

interface NamedRegion {
  name: string;
  startLine: number;
  endLine: number;
}

interface FoldPreset {
  name: string;
  foldedLines: number[];
}

interface PresetStore {
  [filePath: string]: FoldPreset[];
}

// ── Config helpers ──────────────────────────────────────────

function getConfig() {
  const cfg = vscode.workspace.getConfiguration('smartFolding');
  return {
    autoFoldImports: cfg.get<boolean>('autoFoldImports', false),
    rememberState: cfg.get<boolean>('rememberState', true),
    regionMarkers: cfg.get<string[]>('regionMarkers', ['#region', '#endregion']),
  };
}

// ── Line detection patterns ─────────────────────────────────

const IMPORT_PATTERNS = [
  /^\s*import\s/,
  /^\s*import\(/,
  /^\s*from\s+['"].*['"]\s+import/,
  /^\s*const\s+.*=\s*require\s*\(/,
  /^\s*let\s+.*=\s*require\s*\(/,
  /^\s*var\s+.*=\s*require\s*\(/,
  /^\s*#include\s/,
  /^\s*using\s/,
  /^\s*use\s/,
];

const FUNCTION_PATTERNS = [
  /^\s*(export\s+)?(async\s+)?function\s/,
  /^\s*(export\s+)?(const|let|var)\s+\w+\s*=\s*(async\s+)?\(/,
  /^\s*(export\s+)?(const|let|var)\s+\w+\s*=\s*(async\s+)?\w+\s*=>/,
  /^\s*(public|private|protected|static|async)\s+\w+\s*\(/,
  /^\s*def\s+\w+/,
  /^\s*fn\s+\w+/,
];

const CLASS_PATTERNS = [
  /^\s*(export\s+)?(abstract\s+)?class\s/,
  /^\s*(export\s+)?interface\s/,
  /^\s*(export\s+)?enum\s/,
  /^\s*(export\s+)?type\s+\w+\s*=/,
];

const COMMENT_PATTERNS = [
  /^\s*\/\*\*/,
  /^\s*\/\*/,
  /^\s*\/\/\s*$/,
];

// ── Utility: find contiguous block end ──────────────────────

function findBlockEnd(doc: vscode.TextDocument, startLine: number, patterns: RegExp[]): number {
  let line = startLine;
  // For imports: find contiguous import lines
  while (line + 1 < doc.lineCount) {
    const nextText = doc.lineAt(line + 1).text;
    if (nextText.trim() === '' && line + 2 < doc.lineCount && patterns.some((p) => p.test(doc.lineAt(line + 2).text))) {
      line += 2;
      continue;
    }
    if (patterns.some((p) => p.test(nextText))) {
      line++;
      continue;
    }
    break;
  }
  return line;
}

function findBraceBlockEnd(doc: vscode.TextDocument, startLine: number): number {
  let depth = 0;
  let foundOpen = false;
  for (let i = startLine; i < doc.lineCount; i++) {
    const text = doc.lineAt(i).text;
    for (const ch of text) {
      if (ch === '{') { depth++; foundOpen = true; }
      if (ch === '}') { depth--; }
      if (foundOpen && depth === 0) { return i; }
    }
  }
  // Python-style: use indentation
  if (!foundOpen) {
    const baseIndent = doc.lineAt(startLine).firstNonWhitespaceCharacterIndex;
    let lastContentLine = startLine;
    for (let i = startLine + 1; i < doc.lineCount; i++) {
      const line = doc.lineAt(i);
      if (line.isEmptyOrWhitespace) { continue; }
      if (line.firstNonWhitespaceCharacterIndex <= baseIndent) { break; }
      lastContentLine = i;
    }
    if (lastContentLine > startLine) { return lastContentLine; }
  }
  return startLine;
}

function findCommentEnd(doc: vscode.TextDocument, startLine: number): number {
  const text = doc.lineAt(startLine).text;
  if (text.trimStart().startsWith('//')) {
    // Single-line comment block
    let line = startLine;
    while (line + 1 < doc.lineCount && doc.lineAt(line + 1).text.trimStart().startsWith('//')) {
      line++;
    }
    return line;
  }
  // Multi-line comment /* or /**
  for (let i = startLine; i < doc.lineCount; i++) {
    if (doc.lineAt(i).text.includes('*/')) { return i; }
  }
  return startLine;
}

// ── Named Regions parsing ───────────────────────────────────

function parseNamedRegions(doc: vscode.TextDocument): NamedRegion[] {
  const cfg = getConfig();
  const startMarker = cfg.regionMarkers[0] || '#region';
  const endMarker = cfg.regionMarkers[1] || '#endregion';
  const regions: NamedRegion[] = [];
  const stack: { name: string; line: number }[] = [];

  for (let i = 0; i < doc.lineCount; i++) {
    const text = doc.lineAt(i).text;
    const startIdx = text.indexOf(startMarker);
    if (startIdx !== -1 && !text.includes(endMarker)) {
      const name = text.substring(startIdx + startMarker.length).trim() || `Region L${i + 1}`;
      stack.push({ name, line: i });
    } else if (text.includes(endMarker) && stack.length > 0) {
      const open = stack.pop()!;
      regions.push({ name: open.name, startLine: open.line, endLine: i });
    }
  }
  return regions;
}

// ── FoldingRangeProvider ────────────────────────────────────

class SmartFoldingRangeProvider implements vscode.FoldingRangeProvider {
  provideFoldingRanges(doc: vscode.TextDocument): vscode.FoldingRange[] {
    const ranges: vscode.FoldingRange[] = [];
    const regions = parseNamedRegions(doc);
    for (const r of regions) {
      const fr = new vscode.FoldingRange(r.startLine, r.endLine, vscode.FoldingRangeKind.Region);
      ranges.push(fr);
    }
    return ranges;
  }
}

// ── Regions TreeView ────────────────────────────────────────

class RegionItem extends vscode.TreeItem {
  constructor(public readonly region: NamedRegion, public readonly uri: vscode.Uri) {
    super(region.name, vscode.TreeItemCollapsibleState.None);
    this.description = `L${region.startLine + 1}–${region.endLine + 1}`;
    this.iconPath = new vscode.ThemeIcon('symbol-namespace');
    this.command = {
      command: 'vscode.open',
      title: 'Go to region',
      arguments: [uri, { selection: new vscode.Range(region.startLine, 0, region.startLine, 0) }],
    };
  }
}

class RegionsTreeProvider implements vscode.TreeDataProvider<RegionItem> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: RegionItem): vscode.TreeItem {
    return element;
  }

  getChildren(): RegionItem[] {
    const editor = vscode.window.activeTextEditor;
    if (!editor) { return []; }
    const doc = editor.document;
    const regions = parseNamedRegions(doc);
    return regions.map((r) => new RegionItem(r, doc.uri));
  }
}

// ── Fold-by-type commands ───────────────────────────────────

async function foldByType(type: 'imports' | 'functions' | 'classes' | 'comments'): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor.');
    return;
  }

  const doc = editor.document;
  const ranges: { start: number; end: number }[] = [];
  const visited = new Set<number>();

  for (let i = 0; i < doc.lineCount; i++) {
    if (visited.has(i)) { continue; }
    const text = doc.lineAt(i).text;
    if (doc.lineAt(i).isEmptyOrWhitespace) { continue; }

    let match = false;
    let end = i;

    if (type === 'imports' && IMPORT_PATTERNS.some((p) => p.test(text))) {
      match = true;
      end = findBlockEnd(doc, i, IMPORT_PATTERNS);
    } else if (type === 'functions' && FUNCTION_PATTERNS.some((p) => p.test(text))) {
      match = true;
      end = findBraceBlockEnd(doc, i);
    } else if (type === 'classes' && CLASS_PATTERNS.some((p) => p.test(text))) {
      match = true;
      end = findBraceBlockEnd(doc, i);
    } else if (type === 'comments' && COMMENT_PATTERNS.some((p) => p.test(text))) {
      match = true;
      end = findCommentEnd(doc, i);
    }

    if (match && end > i) {
      ranges.push({ start: i, end });
      for (let j = i; j <= end; j++) { visited.add(j); }
    }
  }

  if (ranges.length === 0) {
    vscode.window.showInformationMessage(`Smart Folding: No ${type} blocks found.`);
    return;
  }

  // Use editor fold command with explicit ranges
  for (const r of ranges) {
    editor.selection = new vscode.Selection(r.start, 0, r.start, 0);
    await vscode.commands.executeCommand('editor.fold', {
      selectionLines: [r.start],
      levels: 1,
    });
  }

  // Restore cursor to top of first fold
  if (ranges.length > 0) {
    editor.selection = new vscode.Selection(ranges[0].start, 0, ranges[0].start, 0);
    editor.revealRange(new vscode.Range(ranges[0].start, 0, ranges[0].start, 0));
  }

  vscode.window.showInformationMessage(`Smart Folding: Folded ${ranges.length} ${type} block(s).`);
}

// ── Fold Presets ────────────────────────────────────────────

function getFileKey(uri: vscode.Uri): string {
  return uri.fsPath;
}

async function savePreset(context: vscode.ExtensionContext): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor.');
    return;
  }

  const name = await vscode.window.showInputBox({
    prompt: 'Enter a name for this fold preset',
    placeHolder: 'e.g., Review Mode',
  });
  if (!name) { return; }

  // Get currently visible ranges to infer folded lines
  const visibleRanges = editor.visibleRanges;
  const doc = editor.document;
  const foldedLines: number[] = [];

  // Detect folded lines: lines not in any visible range
  const visibleLines = new Set<number>();
  for (const range of visibleRanges) {
    for (let i = range.start.line; i <= range.end.line; i++) {
      visibleLines.add(i);
    }
  }
  for (let i = 0; i < doc.lineCount; i++) {
    if (!visibleLines.has(i)) {
      foldedLines.push(i);
    }
  }

  const fileKey = getFileKey(doc.uri);
  const store: PresetStore = context.workspaceState.get('smartFolding.presets', {});
  if (!store[fileKey]) { store[fileKey] = []; }

  // Replace existing preset with same name
  store[fileKey] = store[fileKey].filter((p) => p.name !== name);
  store[fileKey].push({ name, foldedLines });

  await context.workspaceState.update('smartFolding.presets', store);
  vscode.window.showInformationMessage(`Smart Folding: Preset "${name}" saved (${foldedLines.length} hidden lines).`);
}

async function loadPreset(context: vscode.ExtensionContext): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor.');
    return;
  }

  const fileKey = getFileKey(editor.document.uri);
  const store: PresetStore = context.workspaceState.get('smartFolding.presets', {});
  const presets = store[fileKey] || [];

  if (presets.length === 0) {
    vscode.window.showInformationMessage('Smart Folding: No presets saved for this file.');
    return;
  }

  const picked = await vscode.window.showQuickPick(
    presets.map((p) => ({ label: p.name, description: `${p.foldedLines.length} hidden lines` })),
    { placeHolder: 'Select a fold preset to load' }
  );
  if (!picked) { return; }

  const preset = presets.find((p) => p.name === picked.label);
  if (!preset) { return; }

  // Unfold everything first
  await vscode.commands.executeCommand('editor.unfoldAll');

  // Fold at the start of each folded region
  if (preset.foldedLines.length > 0) {
    // Find contiguous folded ranges and fold at the start of each
    const starts = new Set<number>();
    for (const line of preset.foldedLines) {
      if (!preset.foldedLines.includes(line - 1)) {
        // This is the line BEFORE the fold; the fold header is line-1
        const headerLine = Math.max(0, line - 1);
        starts.add(headerLine);
      }
    }
    for (const startLine of starts) {
      await vscode.commands.executeCommand('editor.fold', {
        selectionLines: [startLine],
        levels: 1,
      });
    }
  }

  vscode.window.showInformationMessage(`Smart Folding: Preset "${picked.label}" loaded.`);
}

async function deletePreset(context: vscode.ExtensionContext): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor.');
    return;
  }

  const fileKey = getFileKey(editor.document.uri);
  const store: PresetStore = context.workspaceState.get('smartFolding.presets', {});
  const presets = store[fileKey] || [];

  if (presets.length === 0) {
    vscode.window.showInformationMessage('Smart Folding: No presets to delete.');
    return;
  }

  const picked = await vscode.window.showQuickPick(
    presets.map((p) => ({ label: p.name, description: `${p.foldedLines.length} hidden lines` })),
    { placeHolder: 'Select a preset to delete' }
  );
  if (!picked) { return; }

  store[fileKey] = presets.filter((p) => p.name !== picked.label);
  await context.workspaceState.update('smartFolding.presets', store);
  vscode.window.showInformationMessage(`Smart Folding: Preset "${picked.label}" deleted.`);
}

// ── Fold State Persistence ──────────────────────────────────

async function saveFoldState(context: vscode.ExtensionContext, editor: vscode.TextEditor): Promise<void> {
  if (!getConfig().rememberState) { return; }
  const doc = editor.document;
  const visibleLines = new Set<number>();
  for (const range of editor.visibleRanges) {
    for (let i = range.start.line; i <= range.end.line; i++) {
      visibleLines.add(i);
    }
  }
  const foldedLines: number[] = [];
  for (let i = 0; i < doc.lineCount; i++) {
    if (!visibleLines.has(i)) {
      foldedLines.push(i);
    }
  }

  const stateStore: Record<string, number[]> = context.workspaceState.get('smartFolding.foldState', {});
  stateStore[getFileKey(doc.uri)] = foldedLines;
  await context.workspaceState.update('smartFolding.foldState', stateStore);
}

async function restoreFoldState(context: vscode.ExtensionContext, editor: vscode.TextEditor): Promise<void> {
  if (!getConfig().rememberState) { return; }
  const stateStore: Record<string, number[]> = context.workspaceState.get('smartFolding.foldState', {});
  const foldedLines = stateStore[getFileKey(editor.document.uri)];
  if (!foldedLines || foldedLines.length === 0) { return; }

  const starts = new Set<number>();
  for (const line of foldedLines) {
    if (!foldedLines.includes(line - 1)) {
      starts.add(Math.max(0, line - 1));
    }
  }
  for (const startLine of starts) {
    await vscode.commands.executeCommand('editor.fold', {
      selectionLines: [startLine],
      levels: 1,
    });
  }
}

// ── Auto-fold imports on file open ──────────────────────────

async function autoFoldImports(editor: vscode.TextEditor): Promise<void> {
  if (!getConfig().autoFoldImports) { return; }
  const doc = editor.document;
  const visited = new Set<number>();

  for (let i = 0; i < doc.lineCount; i++) {
    if (visited.has(i) || doc.lineAt(i).isEmptyOrWhitespace) { continue; }
    if (IMPORT_PATTERNS.some((p) => p.test(doc.lineAt(i).text))) {
      const end = findBlockEnd(doc, i, IMPORT_PATTERNS);
      if (end > i) {
        await vscode.commands.executeCommand('editor.fold', {
          selectionLines: [i],
          levels: 1,
        });
        for (let j = i; j <= end; j++) { visited.add(j); }
      }
    }
  }
}

// ── Status Bar ──────────────────────────────────────────────

let statusBarItem: vscode.StatusBarItem;

function updateStatusBar(doc: vscode.TextDocument): void {
  const regions = parseNamedRegions(doc);
  if (regions.length > 0) {
    statusBarItem.text = `$(symbol-namespace) ${regions.length} regions`;
    statusBarItem.tooltip = `${regions.length} named region(s) in this file`;
  } else {
    statusBarItem.text = '$(symbol-namespace) 0 regions';
    statusBarItem.tooltip = 'No named regions';
  }
  statusBarItem.show();
}

// ── Activation ──────────────────────────────────────────────

export function activate(context: vscode.ExtensionContext) {
  const regionsTree = new RegionsTreeProvider();

  // Status bar
  statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 40);
  statusBarItem.command = 'smartFolding.foldRegions';

  // Register folding range provider for all languages
  context.subscriptions.push(
    vscode.languages.registerFoldingRangeProvider({ scheme: 'file' }, new SmartFoldingRangeProvider())
  );

  // TreeView
  vscode.window.registerTreeDataProvider('smartFoldingRegions', regionsTree);

  // Commands
  context.subscriptions.push(
    vscode.commands.registerCommand('smartFolding.foldImports', () => foldByType('imports')),
    vscode.commands.registerCommand('smartFolding.foldFunctions', () => foldByType('functions')),
    vscode.commands.registerCommand('smartFolding.foldClasses', () => foldByType('classes')),
    vscode.commands.registerCommand('smartFolding.foldComments', () => foldByType('comments')),
    vscode.commands.registerCommand('smartFolding.foldRegions', async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) { return; }
      const regions = parseNamedRegions(editor.document);
      if (regions.length === 0) {
        vscode.window.showInformationMessage('Smart Folding: No named regions found.');
        return;
      }
      for (const r of regions) {
        await vscode.commands.executeCommand('editor.fold', {
          selectionLines: [r.startLine],
          levels: 1,
        });
      }
      vscode.window.showInformationMessage(`Smart Folding: Folded ${regions.length} region(s).`);
    }),
    vscode.commands.registerCommand('smartFolding.savePreset', () => savePreset(context)),
    vscode.commands.registerCommand('smartFolding.loadPreset', () => loadPreset(context)),
    vscode.commands.registerCommand('smartFolding.deletePreset', () => deletePreset(context)),
    vscode.commands.registerCommand('smartFolding.refreshRegions', () => regionsTree.refresh()),
    statusBarItem,
  );

  // Update on editor change
  context.subscriptions.push(
    vscode.window.onDidChangeActiveTextEditor((editor) => {
      regionsTree.refresh();
      if (editor) {
        updateStatusBar(editor.document);
        // Restore fold state and auto-fold imports
        restoreFoldState(context, editor);
        autoFoldImports(editor);
      }
    }),
    vscode.workspace.onDidSaveTextDocument((doc) => {
      regionsTree.refresh();
      updateStatusBar(doc);
      // Save fold state on file save
      const editor = vscode.window.activeTextEditor;
      if (editor && editor.document.uri.toString() === doc.uri.toString()) {
        saveFoldState(context, editor);
      }
    }),
    vscode.workspace.onDidChangeTextDocument((e) => {
      const editor = vscode.window.activeTextEditor;
      if (editor && editor.document.uri.toString() === e.document.uri.toString()) {
        updateStatusBar(e.document);
      }
    }),
  );

  // Initial state
  if (vscode.window.activeTextEditor) {
    updateStatusBar(vscode.window.activeTextEditor.document);
    regionsTree.refresh();
    restoreFoldState(context, vscode.window.activeTextEditor);
    autoFoldImports(vscode.window.activeTextEditor);
  }
}

export function deactivate() {}
