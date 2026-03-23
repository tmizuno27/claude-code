# Doc Snapshot - Design Specification

## Overview
Take named snapshots of any document and compare/restore them later. Local version control without Git.

## Features

### 1. Take Snapshot
- Save current file content with timestamp and optional label
- Keyboard shortcut (Ctrl+Shift+S by default)
- Auto-snapshot on save (configurable)

### 2. List Snapshots
- QuickPick showing all snapshots for current file
- Display: label, timestamp, size, line count

### 3. Compare
- Diff current file against any snapshot (vscode.diff)
- Diff two snapshots against each other

### 4. Restore
- Replace current file content with snapshot
- Confirmation dialog before restore

### 5. Management
- Delete individual snapshots
- Max snapshots per file (default: 20, configurable)
- Clear all snapshots for file/workspace

## Storage
- `workspaceState` for per-workspace persistence
- Each snapshot: `{ filePath, content, label, timestamp }`

## Configuration
```json
{
  "docSnapshot.autoSnapshot": false,
  "docSnapshot.maxPerFile": 20,
  "docSnapshot.defaultLabel": "auto"
}
```
