import * as vscode from 'vscode';

// TODO: FoldingRangeProvider for custom region markers
// TODO: Fold all import/require blocks
// TODO: Fold all function/class bodies
// TODO: Save/load fold state presets per file
// TODO: Named regions: // #region Name ... // #endregion

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('smartFolding.foldImports', () => {
      vscode.window.showInformationMessage('Smart Folding: Not yet implemented');
    }),
    vscode.commands.registerCommand('smartFolding.foldFunctions', () => {
      vscode.window.showInformationMessage('Smart Folding: Not yet implemented');
    }),
    vscode.commands.registerCommand('smartFolding.savePreset', () => {
      vscode.window.showInformationMessage('Smart Folding: Not yet implemented');
    }),
    vscode.commands.registerCommand('smartFolding.loadPreset', () => {
      vscode.window.showInformationMessage('Smart Folding: Not yet implemented');
    }),
  );
}

export function deactivate() {}
