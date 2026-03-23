# M27 Paste & Transform

> Paste clipboard content with instant transformations. Convert case, encode/decode, format JSON, and sort lines -- all in one shortcut.

## Why This Extension?

Developers constantly copy-paste text that needs transformation -- variable names, encoded strings, JSON payloads, line lists. Paste & Transform lets you **paste and convert in one step** instead of switching to external tools.

## Features

- **Case Conversion** -- camelCase, snake_case, UPPER_CASE, kebab-case, PascalCase
- **JSON Operations** -- Format (pretty print) / Minify
- **Encoding/Decoding** -- Base64 encode/decode, URL encode/decode, HTML entities
- **Line Operations** -- Sort ascending/descending, remove duplicates, trim whitespace
- **Quick Pick Menu** -- Select transformation from a searchable list
- **Keyboard Shortcut** -- `Ctrl+Shift+Alt+V` for instant access

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 Paste & Transform"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-paste-and-transform
```

## Usage

1. Copy text to clipboard
2. Press `Ctrl+Shift+Alt+V` (or `Cmd+Shift+Alt+V` on macOS)
3. Select a transformation from the quick pick menu
4. Transformed text is inserted at cursor (or replaces selection)

## Keyboard Shortcuts

| Platform | Shortcut |
|----------|----------|
| Windows/Linux | `Ctrl+Shift+Alt+V` |
| macOS | `Cmd+Shift+Alt+V` |

## Available Transformations

| Category | Transformations |
|----------|----------------|
| Case | camelCase, snake_case, UPPER_CASE, kebab-case, PascalCase |
| JSON | Format (2-space indent), Minify |
| Encoding | Base64 encode/decode, URL encode/decode, HTML entities |
| Lines | Sort A-Z, Sort Z-A, Remove duplicates, Trim whitespace |

## Alternatives Comparison

| Feature | Paste & Transform | Change Case (ext) | Text Transformer (ext) |
|---------|:-----------------:|:-----------------:|:---------------------:|
| Paste + transform | Yes | No | No |
| Case conversion | Yes | Yes | Yes |
| Base64/URL encode | Yes | No | Limited |
| JSON format | Yes | No | No |
| Line operations | Yes | No | No |

## License

MIT
