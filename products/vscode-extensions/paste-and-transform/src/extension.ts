import * as vscode from 'vscode';

interface TransformOption {
  label: string;
  description: string;
  transform: (text: string) => string;
}

function toCamelCase(text: string): string {
  return text
    .replace(/[-_\s]+(.)?/g, (_, c) => (c ? c.toUpperCase() : ''))
    .replace(/^[A-Z]/, (c) => c.toLowerCase());
}

function toSnakeCase(text: string): string {
  return text
    .replace(/([a-z])([A-Z])/g, '$1_$2')
    .replace(/[-\s]+/g, '_')
    .toLowerCase();
}

function toUpperCase(text: string): string {
  return toSnakeCase(text).toUpperCase();
}

function toKebabCase(text: string): string {
  return text
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[_\s]+/g, '-')
    .toLowerCase();
}

function toPascalCase(text: string): string {
  const camel = toCamelCase(text);
  return camel.charAt(0).toUpperCase() + camel.slice(1);
}

function jsonFormat(text: string): string {
  try {
    return JSON.stringify(JSON.parse(text), null, 2);
  } catch {
    return text;
  }
}

function jsonMinify(text: string): string {
  try {
    return JSON.stringify(JSON.parse(text));
  } catch {
    return text;
  }
}

function base64Encode(text: string): string {
  return Buffer.from(text, 'utf-8').toString('base64');
}

function base64Decode(text: string): string {
  try {
    return Buffer.from(text, 'base64').toString('utf-8');
  } catch {
    return text;
  }
}

function htmlEntityEncode(text: string): string {
  const map: Record<string, string> = {
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  };
  return text.replace(/[&<>"']/g, (c) => map[c] || c);
}

function htmlEntityDecode(text: string): string {
  const map: Record<string, string> = {
    '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'",
  };
  return text.replace(/&(?:amp|lt|gt|quot|#39);/g, (m) => map[m] || m);
}

function sortLinesAsc(text: string): string {
  return text.split('\n').sort((a, b) => a.localeCompare(b)).join('\n');
}

function sortLinesDesc(text: string): string {
  return text.split('\n').sort((a, b) => b.localeCompare(a)).join('\n');
}

function removeDuplicateLines(text: string): string {
  return [...new Set(text.split('\n'))].join('\n');
}

function trimWhitespace(text: string): string {
  return text.split('\n').map((line) => line.trim()).join('\n');
}

const transformOptions: TransformOption[] = [
  { label: 'camelCase', description: 'myVariableName', transform: toCamelCase },
  { label: 'snake_case', description: 'my_variable_name', transform: toSnakeCase },
  { label: 'UPPER_CASE', description: 'MY_VARIABLE_NAME', transform: toUpperCase },
  { label: 'kebab-case', description: 'my-variable-name', transform: toKebabCase },
  { label: 'PascalCase', description: 'MyVariableName', transform: toPascalCase },
  { label: 'JSON Format (2 space)', description: 'Pretty print JSON', transform: jsonFormat },
  { label: 'JSON Minify', description: 'Compact JSON', transform: jsonMinify },
  { label: 'Base64 Encode', description: 'Encode to Base64', transform: base64Encode },
  { label: 'Base64 Decode', description: 'Decode from Base64', transform: base64Decode },
  { label: 'URL Encode', description: 'encodeURIComponent', transform: (t) => encodeURIComponent(t) },
  { label: 'URL Decode', description: 'decodeURIComponent', transform: (t) => { try { return decodeURIComponent(t); } catch { return t; } } },
  { label: 'HTML Entity Encode', description: '&amp; &lt; &gt;', transform: htmlEntityEncode },
  { label: 'HTML Entity Decode', description: '& < >', transform: htmlEntityDecode },
  { label: 'Sort Lines (A-Z)', description: 'Ascending sort', transform: sortLinesAsc },
  { label: 'Sort Lines (Z-A)', description: 'Descending sort', transform: sortLinesDesc },
  { label: 'Remove Duplicate Lines', description: 'Keep unique lines', transform: removeDuplicateLines },
  { label: 'Trim Whitespace', description: 'Trim each line', transform: trimWhitespace },
];

export function activate(context: vscode.ExtensionContext) {
  const disposable = vscode.commands.registerCommand('pasteAndTransform.execute', async () => {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
      vscode.window.showWarningMessage('No active editor.');
      return;
    }

    const clipboard = await vscode.env.clipboard.readText();
    if (!clipboard) {
      vscode.window.showWarningMessage('Clipboard is empty.');
      return;
    }

    const picked = await vscode.window.showQuickPick(
      transformOptions.map((o) => ({ label: o.label, description: o.description })),
      { placeHolder: `Transform clipboard text (${clipboard.length} chars)` }
    );

    if (!picked) { return; }

    const option = transformOptions.find((o) => o.label === picked.label);
    if (!option) { return; }

    const result = option.transform(clipboard);

    await editor.edit((editBuilder) => {
      if (editor.selection.isEmpty) {
        editBuilder.insert(editor.selection.active, result);
      } else {
        editBuilder.replace(editor.selection, result);
      }
    });
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {}
