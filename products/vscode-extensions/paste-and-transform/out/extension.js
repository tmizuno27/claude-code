"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
function toCamelCase(text) {
    return text
        .replace(/[-_\s]+(.)?/g, (_, c) => (c ? c.toUpperCase() : ''))
        .replace(/^[A-Z]/, (c) => c.toLowerCase());
}
function toSnakeCase(text) {
    return text
        .replace(/([a-z])([A-Z])/g, '$1_$2')
        .replace(/[-\s]+/g, '_')
        .toLowerCase();
}
function toUpperCase(text) {
    return toSnakeCase(text).toUpperCase();
}
function toKebabCase(text) {
    return text
        .replace(/([a-z])([A-Z])/g, '$1-$2')
        .replace(/[_\s]+/g, '-')
        .toLowerCase();
}
function toPascalCase(text) {
    const camel = toCamelCase(text);
    return camel.charAt(0).toUpperCase() + camel.slice(1);
}
function jsonFormat(text) {
    try {
        return JSON.stringify(JSON.parse(text), null, 2);
    }
    catch {
        return text;
    }
}
function jsonMinify(text) {
    try {
        return JSON.stringify(JSON.parse(text));
    }
    catch {
        return text;
    }
}
function base64Encode(text) {
    return Buffer.from(text, 'utf-8').toString('base64');
}
function base64Decode(text) {
    try {
        return Buffer.from(text, 'base64').toString('utf-8');
    }
    catch {
        return text;
    }
}
function htmlEntityEncode(text) {
    const map = {
        '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    };
    return text.replace(/[&<>"']/g, (c) => map[c] || c);
}
function htmlEntityDecode(text) {
    const map = {
        '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'",
    };
    return text.replace(/&(?:amp|lt|gt|quot|#39);/g, (m) => map[m] || m);
}
function sortLinesAsc(text) {
    return text.split('\n').sort((a, b) => a.localeCompare(b)).join('\n');
}
function sortLinesDesc(text) {
    return text.split('\n').sort((a, b) => b.localeCompare(a)).join('\n');
}
function removeDuplicateLines(text) {
    return [...new Set(text.split('\n'))].join('\n');
}
function trimWhitespace(text) {
    return text.split('\n').map((line) => line.trim()).join('\n');
}
const transformOptions = [
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
    { label: 'URL Decode', description: 'decodeURIComponent', transform: (t) => { try {
            return decodeURIComponent(t);
        }
        catch {
            return t;
        } } },
    { label: 'HTML Entity Encode', description: '&amp; &lt; &gt;', transform: htmlEntityEncode },
    { label: 'HTML Entity Decode', description: '& < >', transform: htmlEntityDecode },
    { label: 'Sort Lines (A-Z)', description: 'Ascending sort', transform: sortLinesAsc },
    { label: 'Sort Lines (Z-A)', description: 'Descending sort', transform: sortLinesDesc },
    { label: 'Remove Duplicate Lines', description: 'Keep unique lines', transform: removeDuplicateLines },
    { label: 'Trim Whitespace', description: 'Trim each line', transform: trimWhitespace },
];
function activate(context) {
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
        const picked = await vscode.window.showQuickPick(transformOptions.map((o) => ({ label: o.label, description: o.description })), { placeHolder: `Transform clipboard text (${clipboard.length} chars)` });
        if (!picked) {
            return;
        }
        const option = transformOptions.find((o) => o.label === picked.label);
        if (!option) {
            return;
        }
        const result = option.transform(clipboard);
        await editor.edit((editBuilder) => {
            if (editor.selection.isEmpty) {
                editBuilder.insert(editor.selection.active, result);
            }
            else {
                editBuilder.replace(editor.selection, result);
            }
        });
    });
    context.subscriptions.push(disposable);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map