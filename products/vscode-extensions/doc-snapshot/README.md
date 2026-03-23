# M27 Doc Snapshot

> Lightweight local version history for any file. Take snapshots, compare diffs, and restore -- no Git required.

## Why This Extension?

Sometimes you need quick version control for files that aren't in a Git repo -- config files, notes, scratch files, or experimental changes. Doc Snapshot gives you **instant snapshots** with comparison and restore, all stored locally.

## Features

- **Named Snapshots** -- Save snapshots with custom labels for easy identification
- **Visual Diff** -- Compare current file with any snapshot using VS Code's built-in diff viewer
- **Snapshot-to-Snapshot Comparison** -- Compare any two snapshots against each other
- **One-Click Restore** -- Revert file content from any snapshot
- **Auto-Snapshot on Save** -- Optionally capture a snapshot every time you save
- **Configurable Limits** -- Set max snapshots per file to manage storage
- **Workspace Cleanup** -- Clear snapshots per file or for the entire workspace

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 Doc Snapshot"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-doc-snapshot
```

## Usage

1. Open any file
2. Run **"Doc Snapshot: Take Snapshot"** from Command Palette (`Ctrl+Shift+P`)
3. Enter a label (e.g., "before refactor")
4. Later, run **"Doc Snapshot: Compare"** to see what changed
5. Run **"Doc Snapshot: Restore"** to revert if needed

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `docSnapshot.maxSnapshots` | `20` | Maximum snapshots per file |
| `docSnapshot.autoSnapshotOnSave` | `false` | Auto-capture on save |

## Alternatives Comparison

| Feature | Doc Snapshot | Local History (ext) | Git |
|---------|:----------:|:------------------:|:---:|
| No Git required | Yes | Yes | No |
| Named labels | Yes | No | Yes |
| Snapshot comparison | Yes | Yes | Yes |
| Auto-snapshot | Yes | Yes | N/A |
| Lightweight | Yes | Yes | No |

## License

MIT
