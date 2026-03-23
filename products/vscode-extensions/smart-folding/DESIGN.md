# Smart Folding - Design Specification

## Overview
Enhanced code folding with named regions, type-based folding, and fold state presets.

## Features

### 1. Fold by Type
- Fold all imports/requires
- Fold all functions
- Fold all classes
- Fold all comments/JSDoc

### 2. Named Regions
- Custom `// #region Name` / `// #endregion` markers
- TreeView showing all named regions
- Jump to region from sidebar

### 3. Fold Presets
- Save current fold state as named preset
- Load preset to restore fold state
- Per-file and per-workspace presets

### 4. Smart Defaults
- Auto-fold imports on file open (configurable)
- Remember fold state per file across sessions

## Configuration
```json
{
  "smartFolding.autoFoldImports": false,
  "smartFolding.rememberState": true,
  "smartFolding.regionMarkers": ["#region", "#endregion"]
}
```
