# M27 Debug Log Cleaner

> Remove, comment out, or audit all debug statements across your entire workspace in one click.

## Why This Extension?

Shipping code with `console.log` and `debugger` statements is embarrassing and potentially a security risk. Debug Log Cleaner finds **every debug statement** in your project and lets you remove them all instantly -- or keep the ones you need.

## Features

- **TreeView Sidebar** -- Browse all debug statements organized by file
- **One-Click Cleanup** -- Remove All / Comment Out All / Uncomment All
- **File-Level Operations** -- Clean individual files via context menu
- **Keep Marker** -- Add `// keep` to protect important debug statements
- **Diagnostic Warnings** -- See inline warnings on debug statements
- **Status Bar Counter** -- Always know how many debug statements remain
- **Multi-Language** -- Supports JavaScript, TypeScript, Python, and more

## Supported Patterns

| Pattern | Language |
|---------|----------|
| `console.log()`, `console.error()`, `console.warn()`, `console.info()`, `console.debug()`, `console.trace()`, `console.dir()`, `console.table()` | JS/TS |
| `debugger` | JS/TS |
| `print()` | Python |

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 Debug Log Cleaner"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-console-cleaner-tool
```

## Usage

1. Open the **"Console Cleaner"** panel in the Activity Bar
2. Browse detected debug statements by file
3. Click any statement to jump to its location
4. Use toolbar buttons to Remove All / Comment Out All

### Protect Important Logs
```js
console.log('Critical monitoring data'); // keep
```
Lines with `// keep` are excluded from cleanup operations.

## Alternatives Comparison

| Feature | Debug Log Cleaner | ESLint no-console | Remove Console Log (ext) |
|---------|:-----------------:|:-----------------:|:-----------------------:|
| TreeView browser | Yes | No | No |
| Comment out option | Yes | No | No |
| Keep marker | Yes | N/A | No |
| Python print() | Yes | No | No |
| Status bar count | Yes | No | No |

## License

MIT
