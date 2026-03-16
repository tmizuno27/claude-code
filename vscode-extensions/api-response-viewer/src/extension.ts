import * as vscode from 'vscode';

// TODO: Parse JSON/XML from selection or clipboard
// TODO: TreeView with collapsible nodes for objects/arrays
// TODO: Copy JSON path on click
// TODO: Search/filter within response
// TODO: Syntax highlighting for values (string/number/boolean/null)

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('apiResponseViewer.open', () => {
      vscode.window.showInformationMessage('API Response Viewer: Not yet implemented');
    }),
    vscode.commands.registerCommand('apiResponseViewer.fromClipboard', () => {
      vscode.window.showInformationMessage('API Response Viewer: Not yet implemented');
    }),
  );
}

export function deactivate() {}
