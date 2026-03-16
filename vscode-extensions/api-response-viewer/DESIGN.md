# API Response Viewer - Design Specification

## Overview
Visualize JSON/XML API responses in an interactive tree view.

## Features

### 1. Tree View
- Collapsible nodes for objects and arrays
- Value type indicators (string, number, boolean, null, array, object)
- Array element count display

### 2. Copy JSON Path
- Right-click any node → copy path (e.g., `data.users[0].name`)
- Support dot notation and bracket notation

### 3. Search & Filter
- Search by key name or value
- Filter to show only matching branches
- Highlight search matches

### 4. Input Sources
- Parse from editor selection
- Parse from clipboard
- Parse from file

### 5. Response Comparison
- Compare two responses side by side
- Highlight added/removed/changed keys

## Commands
| Command | Description |
|---------|-------------|
| `apiResponseViewer.open` | Open selected text as tree |
| `apiResponseViewer.fromClipboard` | Open clipboard content as tree |
