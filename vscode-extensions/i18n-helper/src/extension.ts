import * as vscode from 'vscode';

// TODO: Scan locales/ directory for JSON translation files
// TODO: CompletionProvider for translation keys in code
// TODO: Find keys present in one locale but missing in others
// TODO: Sort keys alphabetically in all locale files
// TODO: Add new key to all locale files at once

export function activate(context: vscode.ExtensionContext) {
  context.subscriptions.push(
    vscode.commands.registerCommand('i18nHelper.findMissing', () => {
      vscode.window.showInformationMessage('i18n Helper: Not yet implemented');
    }),
    vscode.commands.registerCommand('i18nHelper.sortKeys', () => {
      vscode.window.showInformationMessage('i18n Helper: Not yet implemented');
    }),
    vscode.commands.registerCommand('i18nHelper.addKey', () => {
      vscode.window.showInformationMessage('i18n Helper: Not yet implemented');
    }),
  );
}

export function deactivate() {}
