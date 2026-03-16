import * as vscode from 'vscode';

// TODO: Store snapshots in globalState (filePath + content + timestamp + label)
// TODO: QuickPick to select snapshot for comparison
// TODO: Use vscode.diff to show side-by-side comparison
// TODO: Restore snapshot (replace file content)
// TODO: Auto-snapshot on save (configurable)
// TODO: Max snapshots per file limit

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('docSnapshot.take', () => {
      vscode.window.showInformationMessage('Doc Snapshot: Not yet implemented');
    }),
    vscode.commands.registerCommand('docSnapshot.list', () => {
      vscode.window.showInformationMessage('Doc Snapshot: Not yet implemented');
    }),
    vscode.commands.registerCommand('docSnapshot.compare', () => {
      vscode.window.showInformationMessage('Doc Snapshot: Not yet implemented');
    }),
    vscode.commands.registerCommand('docSnapshot.restore', () => {
      vscode.window.showInformationMessage('Doc Snapshot: Not yet implemented');
    }),
  );
}

export function deactivate() {}
