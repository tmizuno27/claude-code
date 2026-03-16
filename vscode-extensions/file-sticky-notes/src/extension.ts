import * as vscode from 'vscode';

// TODO: Store notes in workspace globalState (file path + line + text)
// TODO: TreeView provider showing notes grouped by file
// TODO: Gutter decorations with note icon
// TODO: Hover provider showing note content
// TODO: Import/export notes as JSON

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('fileStickyNotes.add', () => {
      vscode.window.showInformationMessage('Sticky Notes: Not yet implemented');
    }),
    vscode.commands.registerCommand('fileStickyNotes.list', () => {
      vscode.window.showInformationMessage('Sticky Notes: Not yet implemented');
    }),
    vscode.commands.registerCommand('fileStickyNotes.remove', () => {
      vscode.window.showInformationMessage('Sticky Notes: Not yet implemented');
    }),
  );
}

export function deactivate() {}
