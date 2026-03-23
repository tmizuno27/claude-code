# File Sticky Notes - Design Specification

## Overview
Attach virtual sticky notes to any file or line number. Notes persist across sessions via workspace state.

## Features

### 1. Add Notes
- Right-click context menu "Add Sticky Note" on any line
- Input box for note text + optional color (yellow/green/blue/pink)
- Notes stored as: `{ filePath, line, text, color, createdAt }`

### 2. TreeView Sidebar
- Notes grouped by file
- Click to jump to annotated line
- Delete/edit from context menu

### 3. Visual Indicators
- Gutter icon on annotated lines
- Hover shows note content
- Line highlight with note color

### 4. Persistence
- Stored in `workspaceState` (per-workspace)
- Export to `.vscode/sticky-notes.json`
- Import from JSON

### 5. Search & Filter
- Search notes by text
- Filter by color
- Filter by file

## Commands
| Command | Description |
|---------|-------------|
| `fileStickyNotes.add` | Add note at current line |
| `fileStickyNotes.list` | Show all notes |
| `fileStickyNotes.remove` | Remove note at current line |
