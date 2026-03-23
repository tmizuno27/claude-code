import * as vscode from 'vscode';
import * as path from 'path';

interface Snapshot {
  filePath: string;
  content: string;
  label: string;
  timestamp: number;
  lineCount: number;
  size: number;
}

const STORAGE_KEY = 'docSnapshot.snapshots';

function getSnapshots(context: vscode.ExtensionContext): Snapshot[] {
  return context.workspaceState.get<Snapshot[]>(STORAGE_KEY, []);
}

function saveSnapshots(context: vscode.ExtensionContext, snapshots: Snapshot[]): Thenable<void> {
  return context.workspaceState.update(STORAGE_KEY, snapshots);
}

function getSnapshotsForFile(context: vscode.ExtensionContext, filePath: string): Snapshot[] {
  return getSnapshots(context).filter((s) => s.filePath === filePath);
}

function formatTimestamp(ts: number): string {
  const d = new Date(ts);
  return d.toLocaleString();
}

function formatSize(bytes: number): string {
  if (bytes < 1024) { return `${bytes} B`; }
  if (bytes < 1024 * 1024) { return `${(bytes / 1024).toFixed(1)} KB`; }
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function enforceMaxSnapshots(context: vscode.ExtensionContext, filePath: string): void {
  const config = vscode.workspace.getConfiguration('docSnapshot');
  const max = config.get<number>('maxPerFile', 20);
  const all = getSnapshots(context);
  const forFile = all.filter((s) => s.filePath === filePath);

  if (forFile.length > max) {
    // Remove oldest beyond limit
    const sorted = forFile.sort((a, b) => a.timestamp - b.timestamp);
    const toRemove = sorted.slice(0, forFile.length - max);
    const removeSet = new Set(toRemove.map((s) => s.timestamp));
    const filtered = all.filter((s) => !(s.filePath === filePath && removeSet.has(s.timestamp)));
    saveSnapshots(context, filtered);
  }
}

async function pickSnapshot(
  context: vscode.ExtensionContext,
  filePath: string,
  title: string
): Promise<Snapshot | undefined> {
  const snapshots = getSnapshotsForFile(context, filePath)
    .sort((a, b) => b.timestamp - a.timestamp);

  if (snapshots.length === 0) {
    vscode.window.showInformationMessage('No snapshots found for this file.');
    return undefined;
  }

  const items = snapshots.map((s) => ({
    label: s.label,
    description: `${formatTimestamp(s.timestamp)} | ${s.lineCount} lines | ${formatSize(s.size)}`,
    snapshot: s,
  }));

  const picked = await vscode.window.showQuickPick(items, { placeHolder: title });
  return picked?.snapshot;
}

function getActiveFilePath(): string | undefined {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor.');
    return undefined;
  }
  if (editor.document.uri.scheme !== 'file') {
    vscode.window.showWarningMessage('Snapshots only work with saved files.');
    return undefined;
  }
  return editor.document.uri.fsPath;
}

async function takeSnapshot(context: vscode.ExtensionContext, askLabel: boolean = true): Promise<void> {
  const editor = vscode.window.activeTextEditor;
  if (!editor) {
    vscode.window.showWarningMessage('No active editor.');
    return;
  }

  const filePath = getActiveFilePath();
  if (!filePath) { return; }

  const content = editor.document.getText();
  const config = vscode.workspace.getConfiguration('docSnapshot');
  const defaultLabel = config.get<string>('defaultLabel', 'auto');

  let label = defaultLabel;
  if (askLabel) {
    const input = await vscode.window.showInputBox({
      prompt: 'Snapshot label (leave empty for auto)',
      value: '',
    });
    if (input === undefined) { return; } // cancelled
    label = input || `${defaultLabel}-${Date.now()}`;
  } else {
    label = `${defaultLabel}-${Date.now()}`;
  }

  const snapshot: Snapshot = {
    filePath,
    content,
    label,
    timestamp: Date.now(),
    lineCount: editor.document.lineCount,
    size: Buffer.byteLength(content, 'utf-8'),
  };

  const all = getSnapshots(context);
  all.push(snapshot);
  await saveSnapshots(context, all);
  enforceMaxSnapshots(context, filePath);

  vscode.window.showInformationMessage(`Snapshot "${label}" saved.`);
}

export function activate(context: vscode.ExtensionContext) {
  // Take Snapshot
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.take', () => takeSnapshot(context, true))
  );

  // List Snapshots
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.list', async () => {
      const filePath = getActiveFilePath();
      if (!filePath) { return; }

      const snapshots = getSnapshotsForFile(context, filePath)
        .sort((a, b) => b.timestamp - a.timestamp);

      if (snapshots.length === 0) {
        vscode.window.showInformationMessage('No snapshots for this file.');
        return;
      }

      const items = snapshots.map((s) => ({
        label: s.label,
        description: `${formatTimestamp(s.timestamp)} | ${s.lineCount} lines | ${formatSize(s.size)}`,
      }));

      const picked = await vscode.window.showQuickPick(items, {
        placeHolder: `${snapshots.length} snapshot(s) for ${path.basename(filePath)}`,
      });

      if (!picked) { return; }

      const actions = ['Compare with Current', 'Restore', 'Delete'];
      const action = await vscode.window.showQuickPick(actions, {
        placeHolder: `"${picked.label}" — Choose action`,
      });

      if (!action) { return; }

      const snap = snapshots.find((s) => s.label === picked.label && s.timestamp.toString() === (picked.description?.split(' | ')[0] ? '' : ''));
      // Re-find by label + matching description
      const matchedSnap = snapshots.find((s) =>
        s.label === picked.label &&
        picked.description?.startsWith(formatTimestamp(s.timestamp))
      );

      if (!matchedSnap) { return; }

      if (action === 'Compare with Current') {
        await showDiff(matchedSnap, filePath);
      } else if (action === 'Restore') {
        await restoreSnapshot(matchedSnap);
      } else if (action === 'Delete') {
        await deleteSnapshot(context, matchedSnap);
      }
    })
  );

  // Compare with Snapshot
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.compare', async () => {
      const filePath = getActiveFilePath();
      if (!filePath) { return; }

      const snapshot = await pickSnapshot(context, filePath, 'Select snapshot to compare with current file');
      if (!snapshot) { return; }

      await showDiff(snapshot, filePath);
    })
  );

  // Compare Two Snapshots
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.compareTwoSnapshots', async () => {
      const filePath = getActiveFilePath();
      if (!filePath) { return; }

      const snap1 = await pickSnapshot(context, filePath, 'Select FIRST snapshot (left)');
      if (!snap1) { return; }

      const snap2 = await pickSnapshot(context, filePath, 'Select SECOND snapshot (right)');
      if (!snap2) { return; }

      const uri1 = vscode.Uri.parse(`doc-snapshot:${snap1.label}@${snap1.timestamp}`);
      const uri2 = vscode.Uri.parse(`doc-snapshot:${snap2.label}@${snap2.timestamp}`);

      snapshotContentProvider.set(uri1.toString(), snap1.content);
      snapshotContentProvider.set(uri2.toString(), snap2.content);

      await vscode.commands.executeCommand(
        'vscode.diff',
        uri1,
        uri2,
        `${snap1.label} <-> ${snap2.label}`
      );
    })
  );

  // Restore Snapshot
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.restore', async () => {
      const filePath = getActiveFilePath();
      if (!filePath) { return; }

      const snapshot = await pickSnapshot(context, filePath, 'Select snapshot to restore');
      if (!snapshot) { return; }

      await restoreSnapshot(snapshot);
    })
  );

  // Delete Snapshot
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.delete', async () => {
      const filePath = getActiveFilePath();
      if (!filePath) { return; }

      const snapshot = await pickSnapshot(context, filePath, 'Select snapshot to delete');
      if (!snapshot) { return; }

      await deleteSnapshot(context, snapshot);
    })
  );

  // Clear All Snapshots for File
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.clearFile', async () => {
      const filePath = getActiveFilePath();
      if (!filePath) { return; }

      const count = getSnapshotsForFile(context, filePath).length;
      if (count === 0) {
        vscode.window.showInformationMessage('No snapshots for this file.');
        return;
      }

      const confirm = await vscode.window.showWarningMessage(
        `Delete all ${count} snapshot(s) for ${path.basename(filePath)}?`,
        { modal: true },
        'Delete All'
      );

      if (confirm !== 'Delete All') { return; }

      const all = getSnapshots(context).filter((s) => s.filePath !== filePath);
      await saveSnapshots(context, all);
      vscode.window.showInformationMessage(`Cleared ${count} snapshot(s).`);
    })
  );

  // Clear All Snapshots in Workspace
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.clearWorkspace', async () => {
      const all = getSnapshots(context);
      if (all.length === 0) {
        vscode.window.showInformationMessage('No snapshots in workspace.');
        return;
      }

      const confirm = await vscode.window.showWarningMessage(
        `Delete ALL ${all.length} snapshot(s) in this workspace?`,
        { modal: true },
        'Delete All'
      );

      if (confirm !== 'Delete All') { return; }

      await saveSnapshots(context, []);
      vscode.window.showInformationMessage(`Cleared ${all.length} snapshot(s).`);
    })
  );

  // Auto-snapshot on save
  context.subscriptions.push(
    vscode.workspace.onDidSaveTextDocument(async (doc) => {
      const config = vscode.workspace.getConfiguration('docSnapshot');
      if (!config.get<boolean>('autoSnapshot', false)) { return; }
      if (doc.uri.scheme !== 'file') { return; }

      const filePath = doc.uri.fsPath;
      const content = doc.getText();
      const defaultLabel = config.get<string>('defaultLabel', 'auto');

      const snapshot: Snapshot = {
        filePath,
        content,
        label: `${defaultLabel}-${Date.now()}`,
        timestamp: Date.now(),
        lineCount: doc.lineCount,
        size: Buffer.byteLength(content, 'utf-8'),
      };

      const all = getSnapshots(context);
      all.push(snapshot);
      await saveSnapshots(context, all);
      enforceMaxSnapshots(context, filePath);
    })
  );

  // Register TextDocumentContentProvider for snapshot diffs
  context.subscriptions.push(
    vscode.workspace.registerTextDocumentContentProvider('doc-snapshot', snapshotContentProvider)
  );
}

// Virtual document provider for showing snapshot content in diff
const snapshotContentProvider = new (class implements vscode.TextDocumentContentProvider {
  private contents = new Map<string, string>();

  set(uri: string, content: string): void {
    this.contents.set(uri, content);
  }

  provideTextDocumentContent(uri: vscode.Uri): string {
    return this.contents.get(uri.toString()) || '';
  }
})();

async function showDiff(snapshot: Snapshot, currentFilePath: string): Promise<void> {
  const snapshotUri = vscode.Uri.parse(
    `doc-snapshot:${encodeURIComponent(snapshot.label)}@${snapshot.timestamp}`
  );
  snapshotContentProvider.set(snapshotUri.toString(), snapshot.content);

  const currentUri = vscode.Uri.file(currentFilePath);

  await vscode.commands.executeCommand(
    'vscode.diff',
    snapshotUri,
    currentUri,
    `${snapshot.label} (${formatTimestamp(snapshot.timestamp)}) <-> Current`
  );
}

async function restoreSnapshot(snapshot: Snapshot): Promise<void> {
  const confirm = await vscode.window.showWarningMessage(
    `Restore "${snapshot.label}" from ${formatTimestamp(snapshot.timestamp)}? This will replace the current file content.`,
    { modal: true },
    'Restore'
  );

  if (confirm !== 'Restore') { return; }

  const editor = vscode.window.activeTextEditor;
  if (!editor) { return; }

  const fullRange = new vscode.Range(
    editor.document.positionAt(0),
    editor.document.positionAt(editor.document.getText().length)
  );

  await editor.edit((editBuilder) => {
    editBuilder.replace(fullRange, snapshot.content);
  });

  vscode.window.showInformationMessage(`Restored "${snapshot.label}".`);
}

async function deleteSnapshot(context: vscode.ExtensionContext, snapshot: Snapshot): Promise<void> {
  const all = getSnapshots(context).filter(
    (s) => !(s.filePath === snapshot.filePath && s.timestamp === snapshot.timestamp)
  );
  await saveSnapshots(context, all);
  vscode.window.showInformationMessage(`Deleted snapshot "${snapshot.label}".`);
}

export function deactivate() {}
