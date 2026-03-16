# Console Cleaner

Find, remove, or comment out all debug statements across your workspace in one click.

## Features

- **TreeView sidebar** showing all `console.log`, `console.error`, `console.warn`, `debugger`, and `print()` statements
- **Remove All** / **Comment Out All** / **Uncomment All** commands
- **File-level operations** via context menu
- **`// keep` marker** to protect specific statements from removal
- **Diagnostic warnings** on debug statements
- **Status bar** showing count of debug statements

## Supported Patterns

- `console.log()`, `console.error()`, `console.warn()`, `console.info()`, `console.debug()`, `console.trace()`, `console.dir()`, `console.table()`, etc.
- `debugger`
- `print()` (Python)

## Usage

1. Open the "Console Cleaner" panel in the Activity Bar
2. Browse detected debug statements by file
3. Click a statement to jump to it
4. Use commands to remove/comment all at once

Add `// keep` to any line to protect it:
```js
console.log('Important debug info'); // keep
```

## Install

```
ext install miccho27.console-cleaner
```

## License

MIT
