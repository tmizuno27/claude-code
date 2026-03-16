import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

// --- Types ---

type NoteColor = 'yellow' | 'green' | 'blue' | 'pink';

interface StickyNote {
  id: string;
  filePath: string;
  line: number;
  text: string;
  color: NoteColor;
  createdAt: string;
}

interface FileGroup {
  filePath: string;
  notes: StickyNote[];
}

// --- Constants ---

const STORAGE_KEY = 'fileStickyNotes.notes';

const COLOR_MAP: Record<NoteColor, { bg: string; gutter: string; icon: string }> = {
  yellow: { bg: 'rgba(255, 235, 59, 0.15)', gutter: 'rgba(255, 235, 59, 0.8)', icon: '📝' },
  green:  { bg: 'rgba(76, 175, 80, 0.15)',   gutter: 'rgba(76, 175, 80, 0.8)',   icon: '📗' },
  blue:   { bg: 'rgba(33, 150, 243, 0.15)',   gutter: 'rgba(33, 150, 243, 0.8)',  icon: '📘' },
  pink:   { bg: 'rgba(233, 30, 99, 0.15)',    gutter: 'rgba(233, 30, 99, 0.8)',   icon: '📕' },
};

// --- Note Store ---

class NoteStore {
  private notes: StickyNote[] = [];
  private _onDidChange = new vscode.EventEmitter<void>();
  readonly onDidChange = this._onDidChange.event;

  constructor(private context: vscode.ExtensionContext) {
    this.notes = context.workspaceState.get<StickyNote[]>(STORAGE_KEY) || [];
  }

  private save(): void {
    this.context.workspaceState.update(STORAGE_KEY, this.notes);
    this._onDidChange.fire();
  }

  getAll(): StickyNote[] { return [...this.notes]; }

  getByFile(filePath: string): StickyNote[] {
    return this.notes.filter((n) => n.filePath === filePath);
  }

  getByFileLine(filePath: string, line: number): StickyNote | undefined {
    return this.notes.find((n) => n.filePath === filePath && n.line === line);
  }

  add(filePath: string, line: number, text: string, color: NoteColor): StickyNote {
    const note: StickyNote = {
      id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      filePath, line, text, color,
      createdAt: new Date().toISOString(),
    };
    this.notes.push(note);
    this.save();
    return note;
  }

  update(id: string, text: string, color?: NoteColor): void {
    const note = this.notes.find((n) => n.id === id);
    if (note) {
      note.text = text;
      if (color) { note.color = color; }
      this.save();
    }
  }

  remove(id: string): void {
    this.notes = this.notes.filter((n) => n.id !== id);
    this.save();
  }

  removeByFileLine(filePath: string, line: number): void {
    this.notes = this.notes.filter((n) => !(n.filePath === filePath && n.line === line));
    this.save();
  }

  getFileGroups(): FileGroup[] {
    const map = new Map<string, StickyNote[]>();
    for (const note of this.notes) {
      if (!map.has(note.filePath)) { map.set(note.filePath, []); }
      map.get(note.filePath)!.push(note);
    }
    return [...map.entries()].map(([filePath, notes]) => ({
      filePath,
      notes: notes.sort((a, b) => a.line - b.line),
    }));
  }

  search(query: string): StickyNote[] {
    const lower = query.toLowerCase();
    return this.notes.filter((n) => n.text.toLowerCase().includes(lower));
  }

  filterByColor(color: NoteColor): StickyNote[] {
    return this.notes.filter((n) => n.color === color);
  }

  exportJSON(): string {
    return JSON.stringify(this.notes, null, 2);
  }

  importJSON(json: string): number {
    try {
      const imported = JSON.parse(json) as StickyNote[];
      if (!Array.isArray(imported)) { return 0; }
      let count = 0;
      for (const note of imported) {
        if (note.filePath && typeof note.line === 'number' && note.text) {
          this.notes.push({
            id: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
            filePath: note.filePath,
            line: note.line,
            text: note.text,
            color: note.color || 'yellow',
            createdAt: note.createdAt || new Date().toISOString(),
          });
          count++;
        }
      }
      this.save();
      return count;
    } catch {
      return 0;
    }
  }
}

// --- TreeView Provider ---

class StickyNotesTreeProvider implements vscode.TreeDataProvider<FileGroup | StickyNote> {
  private _onDidChangeTreeData = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this._onDidChangeTreeData.event;

  constructor(private store: NoteStore) {
    store.onDidChange(() => this._onDidChangeTreeData.fire());
  }

  refresh(): void {
    this._onDidChangeTreeData.fire();
  }

  getTreeItem(element: FileGroup | StickyNote): vscode.TreeItem {
    if ('notes' in element) {
      // FileGroup
      const label = vscode.workspace.workspaceFolders
        ? path.relative(vscode.workspace.workspaceFolders[0].uri.fsPath, element.filePath)
        : path.basename(element.filePath);
      const item = new vscode.TreeItem(label, vscode.TreeItemCollapsibleState.Expanded);
      item.description = `${element.notes.length} note${element.notes.length > 1 ? 's' : ''}`;
      item.iconPath = new vscode.ThemeIcon('file');
      item.contextValue = 'fileGroup';
      return item;
    }

    // StickyNote
    const preview = element.text.length > 50 ? element.text.substring(0, 50) + '...' : element.text;
    const item = new vscode.TreeItem(`L${element.line + 1}: ${preview}`, vscode.TreeItemCollapsibleState.None);
    item.description = element.color;
    item.tooltip = `${element.text}\n\n${element.color} | ${new Date(element.createdAt).toLocaleString()}`;
    item.contextValue = 'stickyNote';

    const colorIcons: Record<NoteColor, string> = { yellow: 'bookmark', green: 'pass', blue: 'info', pink: 'heart' };
    const colorTheme: Record<NoteColor, string> = { yellow: 'editorWarning.foreground', green: 'testing.iconPassed', blue: 'editorInfo.foreground', pink: 'editorError.foreground' };
    item.iconPath = new vscode.ThemeIcon(colorIcons[element.color], new vscode.ThemeColor(colorTheme[element.color]));

    item.command = {
      command: 'vscode.open',
      title: 'Go to note',
      arguments: [
        vscode.Uri.file(element.filePath),
        { selection: new vscode.Range(element.line, 0, element.line, 0) },
      ],
    };

    return item;
  }

  getChildren(element?: FileGroup | StickyNote): (FileGroup | StickyNote)[] {
    if (!element) { return this.store.getFileGroups(); }
    if ('notes' in element) { return element.notes; }
    return [];
  }
}

// --- Decorations ---

class DecorationManager {
  private decorationTypes = new Map<NoteColor, vscode.TextEditorDecorationType>();

  constructor() {
    for (const [color, config] of Object.entries(COLOR_MAP) as [NoteColor, typeof COLOR_MAP[NoteColor]][]) {
      this.decorationTypes.set(color, vscode.window.createTextEditorDecorationType({
        backgroundColor: config.bg,
        isWholeLine: true,
        overviewRulerColor: config.gutter,
        overviewRulerLane: vscode.OverviewRulerLane.Right,
        gutterIconSize: 'contain',
        before: {
          contentText: config.icon,
          margin: '0 4px 0 0',
        },
      }));
    }
  }

  update(editor: vscode.TextEditor, store: NoteStore): void {
    const filePath = editor.document.uri.fsPath;
    const notes = store.getByFile(filePath);

    const byColor = new Map<NoteColor, vscode.DecorationOptions[]>();
    for (const color of ['yellow', 'green', 'blue', 'pink'] as NoteColor[]) {
      byColor.set(color, []);
    }

    for (const note of notes) {
      if (note.line < editor.document.lineCount) {
        const line = editor.document.lineAt(note.line);
        byColor.get(note.color)!.push({
          range: line.range,
          hoverMessage: new vscode.MarkdownString(`**${note.color.toUpperCase()} Note** _(L${note.line + 1})_\n\n${note.text}\n\n---\n_${new Date(note.createdAt).toLocaleString()}_`),
        });
      }
    }

    for (const [color, decorations] of byColor) {
      editor.setDecorations(this.decorationTypes.get(color)!, decorations);
    }
  }

  dispose(): void {
    for (const dt of this.decorationTypes.values()) { dt.dispose(); }
  }
}

// --- Activation ---

export function activate(context: vscode.ExtensionContext) {
  const store = new NoteStore(context);
  const treeProvider = new StickyNotesTreeProvider(store);
  const decorationManager = new DecorationManager();

  vscode.window.registerTreeDataProvider('stickyNotesView', treeProvider);

  // Refresh decorations for all visible editors
  function refreshDecorations(): void {
    for (const editor of vscode.window.visibleTextEditors) {
      decorationManager.update(editor, store);
    }
  }

  // --- Commands ---

  // Add note at current line
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.add', async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showWarningMessage('No active editor.');
        return;
      }

      const text = await vscode.window.showInputBox({
        prompt: 'Enter sticky note text',
        placeHolder: 'Your note here...',
      });
      if (!text) { return; }

      const colorPick = await vscode.window.showQuickPick(
        [
          { label: '$(bookmark) Yellow', description: 'Default', value: 'yellow' as NoteColor },
          { label: '$(pass) Green', description: 'Done / OK', value: 'green' as NoteColor },
          { label: '$(info) Blue', description: 'Info / Reference', value: 'blue' as NoteColor },
          { label: '$(heart) Pink', description: 'Important', value: 'pink' as NoteColor },
        ],
        { placeHolder: 'Select note color' }
      );

      const color: NoteColor = (colorPick as any)?.value || 'yellow';
      const line = editor.selection.active.line;
      const filePath = editor.document.uri.fsPath;

      store.add(filePath, line, text, color);
      refreshDecorations();
      vscode.window.showInformationMessage(`Sticky note added at line ${line + 1}.`);
    })
  );

  // Remove note at current line
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.remove', async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showWarningMessage('No active editor.');
        return;
      }

      const filePath = editor.document.uri.fsPath;
      const line = editor.selection.active.line;
      const note = store.getByFileLine(filePath, line);

      if (!note) {
        vscode.window.showWarningMessage('No sticky note on this line.');
        return;
      }

      store.remove(note.id);
      refreshDecorations();
      vscode.window.showInformationMessage('Sticky note removed.');
    })
  );

  // List all notes via QuickPick
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.list', async () => {
      const notes = store.getAll();
      if (notes.length === 0) {
        vscode.window.showInformationMessage('No sticky notes in this workspace.');
        return;
      }

      const items = notes.map((n) => {
        const relPath = vscode.workspace.workspaceFolders
          ? path.relative(vscode.workspace.workspaceFolders[0].uri.fsPath, n.filePath)
          : path.basename(n.filePath);
        return {
          label: `$(${n.color === 'yellow' ? 'bookmark' : n.color === 'green' ? 'pass' : n.color === 'blue' ? 'info' : 'heart'}) ${n.text}`,
          description: `${relPath}:${n.line + 1}`,
          detail: `${n.color} | ${new Date(n.createdAt).toLocaleString()}`,
          note: n,
        };
      });

      const picked = await vscode.window.showQuickPick(items, { placeHolder: 'Select a note to jump to' });
      if (picked) {
        const doc = await vscode.workspace.openTextDocument(picked.note.filePath);
        const editor = await vscode.window.showTextDocument(doc);
        const pos = new vscode.Position(picked.note.line, 0);
        editor.selection = new vscode.Selection(pos, pos);
        editor.revealRange(new vscode.Range(pos, pos), vscode.TextEditorRevealType.InCenter);
      }
    })
  );

  // Edit note from tree view
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.edit', async (note: StickyNote) => {
      if (!note || !note.id) { return; }

      const newText = await vscode.window.showInputBox({
        prompt: 'Edit sticky note text',
        value: note.text,
      });
      if (newText === undefined) { return; }

      const colorPick = await vscode.window.showQuickPick(
        [
          { label: '$(bookmark) Yellow', value: 'yellow' as NoteColor },
          { label: '$(pass) Green', value: 'green' as NoteColor },
          { label: '$(info) Blue', value: 'blue' as NoteColor },
          { label: '$(heart) Pink', value: 'pink' as NoteColor },
        ],
        { placeHolder: `Current: ${note.color}. Select new color (or ESC to keep)` }
      );

      store.update(note.id, newText, (colorPick as any)?.value);
      refreshDecorations();
      vscode.window.showInformationMessage('Sticky note updated.');
    })
  );

  // Delete note from tree view
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.delete', (note: StickyNote) => {
      if (!note || !note.id) { return; }
      store.remove(note.id);
      refreshDecorations();
      vscode.window.showInformationMessage('Sticky note deleted.');
    })
  );

  // Search notes
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.search', async () => {
      const query = await vscode.window.showInputBox({ prompt: 'Search notes by text' });
      if (!query) { return; }

      const results = store.search(query);
      if (results.length === 0) {
        vscode.window.showInformationMessage(`No notes matching "${query}".`);
        return;
      }

      const items = results.map((n) => ({
        label: n.text,
        description: `${path.basename(n.filePath)}:${n.line + 1} (${n.color})`,
        note: n,
      }));

      const picked = await vscode.window.showQuickPick(items, { placeHolder: `${results.length} result(s)` });
      if (picked) {
        const doc = await vscode.workspace.openTextDocument(picked.note.filePath);
        const editor = await vscode.window.showTextDocument(doc);
        const pos = new vscode.Position(picked.note.line, 0);
        editor.selection = new vscode.Selection(pos, pos);
        editor.revealRange(new vscode.Range(pos, pos), vscode.TextEditorRevealType.InCenter);
      }
    })
  );

  // Filter by color
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.filterByColor', async () => {
      const colorPick = await vscode.window.showQuickPick(
        ['yellow', 'green', 'blue', 'pink'].map((c) => ({ label: c })),
        { placeHolder: 'Filter by color' }
      );
      if (!colorPick) { return; }

      const results = store.filterByColor(colorPick.label as NoteColor);
      if (results.length === 0) {
        vscode.window.showInformationMessage(`No ${colorPick.label} notes.`);
        return;
      }

      const items = results.map((n) => ({
        label: n.text,
        description: `${path.basename(n.filePath)}:${n.line + 1}`,
        note: n,
      }));

      const picked = await vscode.window.showQuickPick(items, { placeHolder: `${results.length} ${colorPick.label} note(s)` });
      if (picked) {
        const doc = await vscode.workspace.openTextDocument(picked.note.filePath);
        const editor = await vscode.window.showTextDocument(doc);
        const pos = new vscode.Position(picked.note.line, 0);
        editor.selection = new vscode.Selection(pos, pos);
        editor.revealRange(new vscode.Range(pos, pos), vscode.TextEditorRevealType.InCenter);
      }
    })
  );

  // Export to JSON
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.export', async () => {
      const notes = store.getAll();
      if (notes.length === 0) {
        vscode.window.showWarningMessage('No notes to export.');
        return;
      }

      const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
      if (!workspaceFolder) {
        vscode.window.showWarningMessage('No workspace folder open.');
        return;
      }

      const vscodeDir = path.join(workspaceFolder.uri.fsPath, '.vscode');
      if (!fs.existsSync(vscodeDir)) { fs.mkdirSync(vscodeDir, { recursive: true }); }

      const outPath = path.join(vscodeDir, 'sticky-notes.json');
      fs.writeFileSync(outPath, store.exportJSON(), 'utf-8');

      const doc = await vscode.workspace.openTextDocument(outPath);
      await vscode.window.showTextDocument(doc);
      vscode.window.showInformationMessage(`Exported ${notes.length} notes to .vscode/sticky-notes.json`);
    })
  );

  // Import from JSON
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.import', async () => {
      const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
      if (!workspaceFolder) {
        vscode.window.showWarningMessage('No workspace folder open.');
        return;
      }

      const defaultPath = path.join(workspaceFolder.uri.fsPath, '.vscode', 'sticky-notes.json');
      let jsonContent: string;

      if (fs.existsSync(defaultPath)) {
        jsonContent = fs.readFileSync(defaultPath, 'utf-8');
      } else {
        const uris = await vscode.window.showOpenDialog({
          filters: { 'JSON': ['json'] },
          canSelectMany: false,
        });
        if (!uris || uris.length === 0) { return; }
        jsonContent = fs.readFileSync(uris[0].fsPath, 'utf-8');
      }

      const count = store.importJSON(jsonContent);
      if (count > 0) {
        refreshDecorations();
        vscode.window.showInformationMessage(`Imported ${count} notes.`);
      } else {
        vscode.window.showWarningMessage('No valid notes found in JSON file.');
      }
    })
  );

  // --- Event Listeners ---

  context.subscriptions.push(
    vscode.window.onDidChangeActiveTextEditor((editor) => {
      if (editor) { decorationManager.update(editor, store); }
    }),
    vscode.window.onDidChangeVisibleTextEditors(() => refreshDecorations()),
    vscode.workspace.onDidOpenTextDocument(() => {
      setTimeout(refreshDecorations, 100);
    }),
  );

  // Initial decoration
  refreshDecorations();
}

export function deactivate() {}
