# M27 Smart Folding

> Fold code by type -- imports, functions, classes, or comments. Save fold presets and auto-fold on open.

## Why This Extension?

VS Code's built-in folding only works with indentation levels. Smart Folding lets you **fold by semantic type** -- collapse all imports, fold every function, hide all comments -- and save your preferred fold state as a preset.

## Features

- **Fold by Type** -- Fold all imports/requires, functions, classes, or comments separately
- **Named Regions** -- `#region` / `#endregion` support with TreeView browser
- **Fold Presets** -- Save and restore fold configurations
- **Auto-Fold on Open** -- Automatically fold imports (or other types) when opening a file
- **TreeView Panel** -- Browse all named regions in the sidebar
- **Multi-Language** -- Works with JavaScript, TypeScript, Python, Java, Go, and more

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 Smart Folding"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-smart-folding
```

## Usage

1. Open any source file
2. Open Command Palette (`Ctrl+Shift+P`)
3. Run **"Smart Folding: Fold All Imports"** to collapse import blocks
4. Run **"Smart Folding: Fold All Functions"** to collapse function bodies
5. Run **"Smart Folding: Save Preset"** to remember the current fold state

### Named Regions
```js
// #region API Handlers
function getUsers() { ... }
function createUser() { ... }
// #endregion
```

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `smartFolding.autoFoldImports` | `false` | Auto-fold imports on file open |
| `smartFolding.autoFoldComments` | `false` | Auto-fold comments on file open |

## Alternatives Comparison

| Feature | Smart Folding | Better Folding (ext) | Region Folding (ext) |
|---------|:------------:|:-------------------:|:-------------------:|
| Fold by type | Yes | Limited | No |
| Named regions | Yes | Yes | Yes |
| Fold presets | Yes | No | No |
| Auto-fold | Yes | No | No |
| TreeView panel | Yes | No | No |

## License

MIT
