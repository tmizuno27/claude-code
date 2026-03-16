import * as vscode from 'vscode';

// TODO: Parse markdown tables from selection/cursor
// TODO: Auto-align columns with padding
// TODO: Sort by column (asc/desc/numeric)
// TODO: CSV ↔ Markdown table conversion
// TODO: Add/remove column commands

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('markdownTablePro.format', () => {
      vscode.window.showInformationMessage('Markdown Table Pro: Not yet implemented');
    }),
    vscode.commands.registerCommand('markdownTablePro.sort', () => {
      vscode.window.showInformationMessage('Markdown Table Pro: Not yet implemented');
    }),
    vscode.commands.registerCommand('markdownTablePro.csvToTable', () => {
      vscode.window.showInformationMessage('Markdown Table Pro: Not yet implemented');
    }),
    vscode.commands.registerCommand('markdownTablePro.tableToCsv', () => {
      vscode.window.showInformationMessage('Markdown Table Pro: Not yet implemented');
    }),
  );
}

export function deactivate() {}
