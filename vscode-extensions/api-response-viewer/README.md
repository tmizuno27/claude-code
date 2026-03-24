# M27 API Response Viewer

> Instantly visualize, search, and compare JSON/XML API responses inside VS Code.

## Why This Extension?

Stop switching between VS Code and browser-based JSON viewers. API Response Viewer gives you a **collapsible tree view** with powerful search, filtering, and comparison -- all without leaving your editor.

## Features

- **Interactive Tree View** -- Expand/collapse JSON and XML structures with type indicators (string, number, boolean, null, array, object)
- **Search & Filter** -- Find keys or values instantly across deeply nested data
- **Copy Path / Copy Value** -- Click any node to copy its JSON path or value to clipboard
- **Side-by-Side Comparison** -- Compare two API responses to spot differences
- **Multiple Input Sources** -- Load from editor selection, clipboard, or file
- **Syntax Highlighting** -- Color-coded types for quick scanning

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 API Response Viewer"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-api-response-viewer
```

## Usage

1. Select JSON text in your editor (or copy it to clipboard)
2. Open Command Palette (`Ctrl+Shift+P`)
3. Run **"API Response Viewer: Open"**
4. Explore the tree, search, and copy paths

### Compare Two Responses
1. Load the first response
2. Run **"API Response Viewer: Compare"**
3. Load the second response
4. View differences highlighted side by side

## Alternatives Comparison

| Feature | API Response Viewer | JSON Viewer (others) | Browser Tools |
|---------|:------------------:|:-------------------:|:------------:|
| Tree view | Yes | Yes | Yes |
| Search & filter | Yes | Limited | Yes |
| Copy JSON path | Yes | No | No |
| Compare responses | Yes | No | No |
| Works in VS Code | Yes | Yes | No |

## License

MIT
