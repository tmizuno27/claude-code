import * as vscode from 'vscode';

// TODO: Implement commit message generation from git diff
// TODO: Implement conventional commit templates (feat, fix, docs, etc.)
// TODO: Implement QuickPick for type/scope/description
// TODO: Implement SCM input box integration

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('commitCrafter.generate', () => {
      vscode.window.showInformationMessage('Commit Crafter: Not yet implemented');
    }),
    vscode.commands.registerCommand('commitCrafter.selectTemplate', () => {
      vscode.window.showInformationMessage('Commit Crafter: Not yet implemented');
    }),
  );
}

export function deactivate() {}
