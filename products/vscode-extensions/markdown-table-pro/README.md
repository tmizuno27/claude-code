# M27 Markdown Table Pro

> The ultimate Markdown table editor. Format, sort, convert CSV, and manage columns -- all inside VS Code.

## Why This Extension?

Editing Markdown tables by hand is painful. Markdown Table Pro gives you **one-click formatting**, column sorting, CSV import/export, and structural editing -- making tables as easy to work with as spreadsheets.

## Features

- **Auto-Format** -- Align columns with proper padding in one click
- **Sort Columns** -- Sort by any column (ascending, descending, or numeric)
- **CSV Import** -- Convert CSV data to formatted Markdown tables
- **CSV Export** -- Export Markdown tables to CSV
- **Column Operations** -- Add, remove, and move columns
- **Row Operations** -- Add and remove rows
- **Rename Headers** -- Rename column headers inline
- **Format on Save** -- Optionally auto-format tables when saving

## Installation

1. Open VS Code
2. Go to Extensions (`Ctrl+Shift+X`)
3. Search for **"M27 Markdown Table Pro"**
4. Click **Install**

Or from the command line:
```
ext install miccho27.m27-markdown-table-pro
```

## Usage

1. Place cursor inside a Markdown table
2. Open Command Palette (`Ctrl+Shift+P`)
3. Run **"Markdown Table: Format"** to align columns
4. Run **"Markdown Table: Sort"** and select a column
5. Run **"Markdown Table: Import CSV"** to create a table from CSV

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `markdownTable.formatOnSave` | `false` | Auto-format tables on save |
| `markdownTable.defaultAlignment` | `left` | Default column alignment |

## Alternatives Comparison

| Feature | Markdown Table Pro | Markdown All in One | Table Formatter (ext) |
|---------|:-----------------:|:------------------:|:--------------------:|
| Sort columns | Yes | No | No |
| CSV import/export | Yes | No | No |
| Column operations | Yes | No | No |
| Format on save | Yes | Yes | Yes |
| Lightweight | Yes | No | Yes |

## License

MIT
