# M27 File Sticky Notes

> Attach persistent, color-coded sticky notes to any line in any file. Your personal code annotation layer.

## Why This Extension?

Code comments clutter your source files and get committed to Git. File Sticky Notes gives you a **personal annotation layer** that lives outside your code -- perfect for code reviews, learning new codebases, or tracking TODOs.

## Features

- **Color-Coded Notes** -- Yellow, green, blue, and pink notes for different priorities
- **Line-Level Precision** -- Attach notes to specific lines
- **TreeView Sidebar** -- Browse all notes grouped by file
- **Gutter Icons** -- See which lines have notes at a glance
- **Hover Tooltips** -- Read notes by hovering over gutter icons
- **Search & Filter** -- Find notes by text content or color
- **Export/Import** -- Save to `.vscode/sticky-notes.json` for sharing
- **Persistent Storage** -- Notes survive VS Code restarts

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 File Sticky Notes"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-file-sticky-notes
```

## Usage

1. Right-click any line and select **"Add Sticky Note"**
2. Choose a color and enter your note
3. Open the **"Sticky Notes"** panel to browse all notes
4. Click any note to jump to its location

### Share Notes with Your Team
```
Export: Run "Sticky Notes: Export" -> saves to .vscode/sticky-notes.json
Import: Run "Sticky Notes: Import" -> loads from .vscode/sticky-notes.json
```

## Alternatives Comparison

| Feature | File Sticky Notes | Bookmarks (ext) | Todo Tree (ext) |
|---------|:-----------------:|:---------------:|:---------------:|
| Color-coded | Yes | No | Yes |
| Outside source code | Yes | Yes | No |
| Line-level | Yes | Yes | Yes |
| Export/Import | Yes | No | No |
| Gutter icons | Yes | Yes | Yes |

## License

MIT
