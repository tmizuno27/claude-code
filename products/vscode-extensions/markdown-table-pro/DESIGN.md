# Markdown Table Pro - Design Specification

## Overview
Format, sort, and convert Markdown tables with ease.

## Features

### 1. Auto-Format
- Align columns with consistent padding
- Fix separator row alignment (`:---`, `:---:`, `---:`)
- Format on save option

### 2. Sort
- Sort by any column (click column header in preview)
- Ascending / descending / numeric sort
- Multi-column sort

### 3. CSV Conversion
- Paste CSV → convert to Markdown table
- Select Markdown table → copy as CSV
- Import CSV file as table

### 4. Column Operations
- Add column (left/right)
- Remove column
- Move column (left/right)
- Rename header

### 5. Row Operations
- Add row (above/below)
- Delete row
- Move row (up/down)

## Commands
| Command | Description |
|---------|-------------|
| `markdownTablePro.format` | Format table at cursor |
| `markdownTablePro.sort` | Sort by selected column |
| `markdownTablePro.csvToTable` | Convert CSV to table |
| `markdownTablePro.tableToCsv` | Convert table to CSV |
