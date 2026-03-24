import * as vscode from 'vscode';
import * as fs from 'fs';

// ---------------------------------------------------------------------------
// Table model
// ---------------------------------------------------------------------------

interface MarkdownTable {
  headerRow: string[];
  separatorAligns: ('left' | 'center' | 'right' | 'none')[];
  dataRows: string[][];
}

// ---------------------------------------------------------------------------
// Parsing helpers
// ---------------------------------------------------------------------------

function parseCells(line: string): string[] {
  const trimmed = line.trim();
  const stripped = trimmed.startsWith('|') ? trimmed.slice(1) : trimmed;
  const end = stripped.endsWith('|') ? stripped.slice(0, -1) : stripped;
  return end.split('|').map((c) => c.trim());
}

function parseAlignment(cell: string): 'left' | 'center' | 'right' | 'none' {
  const t = cell.trim();
  const left = t.startsWith(':');
  const right = t.endsWith(':');
  if (left && right) { return 'center'; }
  if (right) { return 'right'; }
  if (left) { return 'left'; }
  return 'none';
}

function isSeparatorRow(line: string): boolean {
  const cells = parseCells(line);
  return cells.length > 0 && cells.every((c) => /^:?-{1,}:?$/.test(c.trim()));
}

function parseTable(lines: string[]): MarkdownTable | null {
  if (lines.length < 2) { return null; }
  if (!isSeparatorRow(lines[1])) { return null; }

  const headerRow = parseCells(lines[0]);
  const sepCells = parseCells(lines[1]);
  const separatorAligns = sepCells.map(parseAlignment);
  const colCount = headerRow.length;

  const dataRows: string[][] = [];
  for (let i = 2; i < lines.length; i++) {
    const cells = parseCells(lines[i]);
    // Pad or trim to match column count
    const row = Array.from({ length: colCount }, (_, j) => cells[j] ?? '');
    dataRows.push(row);
  }

  return { headerRow, separatorAligns, dataRows };
}

// ---------------------------------------------------------------------------
// Formatting / serialization
// ---------------------------------------------------------------------------

function buildSeparator(align: 'left' | 'center' | 'right' | 'none', width: number): string {
  const inner = '-'.repeat(Math.max(width, 3));
  switch (align) {
    case 'left': return ':' + inner.slice(1);
    case 'right': return inner.slice(1) + ':';
    case 'center': return ':' + inner.slice(2) + ':';
    default: return inner;
  }
}

function padCell(text: string, width: number, align: 'left' | 'center' | 'right' | 'none'): string {
  const diff = width - text.length;
  if (diff <= 0) { return text; }
  switch (align) {
    case 'right': return ' '.repeat(diff) + text;
    case 'center': {
      const left = Math.floor(diff / 2);
      return ' '.repeat(left) + text + ' '.repeat(diff - left);
    }
    default: return text + ' '.repeat(diff);
  }
}

function formatTable(table: MarkdownTable): string {
  const colCount = table.headerRow.length;
  // Ensure align array matches
  const aligns = Array.from({ length: colCount }, (_, i) => table.separatorAligns[i] ?? 'none');

  // Calculate column widths
  const widths: number[] = [];
  for (let c = 0; c < colCount; c++) {
    let max = table.headerRow[c].length;
    for (const row of table.dataRows) {
      max = Math.max(max, (row[c] ?? '').length);
    }
    widths.push(Math.max(max, 3));
  }

  const headerLine = '| ' + table.headerRow.map((h, i) => padCell(h, widths[i], aligns[i])).join(' | ') + ' |';
  const sepLine = '| ' + aligns.map((a, i) => buildSeparator(a, widths[i])).join(' | ') + ' |';
  const dataLines = table.dataRows.map(
    (row) => '| ' + row.map((cell, i) => padCell(cell, widths[i], aligns[i])).join(' | ') + ' |'
  );

  return [headerLine, sepLine, ...dataLines].join('\n');
}

// ---------------------------------------------------------------------------
// Find table range around cursor
// ---------------------------------------------------------------------------

function findTableRange(doc: vscode.TextDocument, pos: vscode.Position): vscode.Range | null {
  const lineCount = doc.lineCount;
  let startLine = pos.line;
  let endLine = pos.line;

  // Check current line looks like a table row
  const curText = doc.lineAt(pos.line).text.trim();
  if (!curText.includes('|')) { return null; }

  // Expand up
  while (startLine > 0) {
    const prev = doc.lineAt(startLine - 1).text.trim();
    if (!prev.includes('|')) { break; }
    startLine--;
  }

  // Expand down
  while (endLine < lineCount - 1) {
    const next = doc.lineAt(endLine + 1).text.trim();
    if (!next.includes('|')) { break; }
    endLine++;
  }

  // Need at least header + separator
  if (endLine - startLine < 1) { return null; }

  return new vscode.Range(startLine, 0, endLine, doc.lineAt(endLine).text.length);
}

function getTableAtCursor(editor: vscode.TextEditor): { range: vscode.Range; table: MarkdownTable } | null {
  const range = findTableRange(editor.document, editor.selection.active);
  if (!range) { return null; }

  const lines: string[] = [];
  for (let i = range.start.line; i <= range.end.line; i++) {
    lines.push(editor.document.lineAt(i).text);
  }

  const table = parseTable(lines);
  if (!table) { return null; }
  return { range, table };
}

/** Determine which column index the cursor is in based on pipe positions. */
function getCursorColumnIndex(editor: vscode.TextEditor): number {
  const line = editor.document.lineAt(editor.selection.active.line).text;
  const charPos = editor.selection.active.character;
  let col = -1;
  for (let i = 0; i < charPos; i++) {
    if (line[i] === '|') { col++; }
  }
  return Math.max(col, 0);
}

/** Determine which data-row index the cursor is on (0-based, header=-1, separator=-2). */
function getCursorRowIndex(editor: vscode.TextEditor, tableStartLine: number): number {
  const curLine = editor.selection.active.line;
  const offset = curLine - tableStartLine;
  if (offset === 0) { return -1; } // header
  if (offset === 1) { return -2; } // separator
  return offset - 2;
}

// ---------------------------------------------------------------------------
// CSV helpers
// ---------------------------------------------------------------------------

function csvToRows(csv: string): string[][] {
  const lines = csv.split(/\r?\n/).filter((l) => l.trim().length > 0);
  return lines.map((line) => {
    // Simple CSV parse (handles quoted fields)
    const cells: string[] = [];
    let current = '';
    let inQuotes = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (inQuotes) {
        if (ch === '"' && line[i + 1] === '"') {
          current += '"';
          i++;
        } else if (ch === '"') {
          inQuotes = false;
        } else {
          current += ch;
        }
      } else {
        if (ch === '"') {
          inQuotes = true;
        } else if (ch === ',') {
          cells.push(current.trim());
          current = '';
        } else {
          current += ch;
        }
      }
    }
    cells.push(current.trim());
    return cells;
  });
}

function rowsToCsv(header: string[], rows: string[][]): string {
  const escape = (s: string) => {
    if (s.includes(',') || s.includes('"') || s.includes('\n')) {
      return '"' + s.replace(/"/g, '""') + '"';
    }
    return s;
  };
  const lines = [header.map(escape).join(',')];
  for (const row of rows) {
    lines.push(row.map(escape).join(','));
  }
  return lines.join('\n');
}

function rowsToTable(rows: string[][]): MarkdownTable {
  const header = rows[0] ?? [];
  const colCount = header.length;
  const aligns: ('none')[] = Array.from({ length: colCount }, () => 'none');
  const dataRows = rows.slice(1).map((r) =>
    Array.from({ length: colCount }, (_, i) => r[i] ?? '')
  );
  return { headerRow: header, separatorAligns: aligns, dataRows };
}

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

async function cmdFormat(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) {
    vscode.window.showWarningMessage('No Markdown table found at cursor.');
    return;
  }
  const formatted = formatTable(result.table);
  await editor.edit((eb) => eb.replace(result.range, formatted));
}

async function cmdSort(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) {
    vscode.window.showWarningMessage('No Markdown table found at cursor.');
    return;
  }

  const { table } = result;
  const colItems = table.headerRow.map((h, i) => ({ label: h || `Column ${i + 1}`, index: i }));
  const picked = await vscode.window.showQuickPick(colItems, { placeHolder: 'Select column to sort by' });
  if (!picked) { return; }

  const dirPick = await vscode.window.showQuickPick(
    [
      { label: 'Ascending (A-Z / 0-9)', value: 'asc' },
      { label: 'Descending (Z-A / 9-0)', value: 'desc' },
      { label: 'Numeric Ascending', value: 'num-asc' },
      { label: 'Numeric Descending', value: 'num-desc' },
    ],
    { placeHolder: 'Sort direction' }
  );
  if (!dirPick) { return; }

  const col = picked.index;
  const sorted = [...table.dataRows];

  if (dirPick.value.startsWith('num')) {
    const mult = dirPick.value === 'num-asc' ? 1 : -1;
    sorted.sort((a, b) => mult * (parseFloat(a[col] || '0') - parseFloat(b[col] || '0')));
  } else {
    const mult = dirPick.value === 'asc' ? 1 : -1;
    sorted.sort((a, b) => mult * (a[col] ?? '').localeCompare(b[col] ?? ''));
  }

  table.dataRows = sorted;
  const formatted = formatTable(table);
  await editor.edit((eb) => eb.replace(result.range, formatted));
}

async function cmdCsvToTable(editor: vscode.TextEditor) {
  // Use selection if available, otherwise clipboard
  let csv: string;
  if (!editor.selection.isEmpty) {
    csv = editor.document.getText(editor.selection);
  } else {
    csv = await vscode.env.clipboard.readText();
  }

  if (!csv || !csv.trim()) {
    vscode.window.showWarningMessage('No CSV data found in selection or clipboard.');
    return;
  }

  const rows = csvToRows(csv);
  if (rows.length < 1) {
    vscode.window.showWarningMessage('Could not parse CSV data.');
    return;
  }

  const table = rowsToTable(rows);
  const formatted = formatTable(table);

  await editor.edit((eb) => {
    if (!editor.selection.isEmpty) {
      eb.replace(editor.selection, formatted);
    } else {
      eb.insert(editor.selection.active, formatted + '\n');
    }
  });
}

async function cmdTableToCsv(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) {
    vscode.window.showWarningMessage('No Markdown table found at cursor.');
    return;
  }

  const csv = rowsToCsv(result.table.headerRow, result.table.dataRows);
  await vscode.env.clipboard.writeText(csv);
  vscode.window.showInformationMessage(`Table copied as CSV (${result.table.dataRows.length} rows).`);
}

async function cmdImportCsvFile(editor: vscode.TextEditor) {
  const uris = await vscode.window.showOpenDialog({
    canSelectMany: false,
    filters: { 'CSV Files': ['csv'], 'All Files': ['*'] },
  });
  if (!uris || uris.length === 0) { return; }

  const content = fs.readFileSync(uris[0].fsPath, 'utf-8');
  const rows = csvToRows(content);
  if (rows.length < 1) {
    vscode.window.showWarningMessage('Could not parse CSV file.');
    return;
  }

  const table = rowsToTable(rows);
  const formatted = formatTable(table);
  await editor.edit((eb) => eb.insert(editor.selection.active, formatted + '\n'));
}

// ---------------------------------------------------------------------------
// Column operations
// ---------------------------------------------------------------------------

async function cmdAddColumnLeft(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const col = getCursorColumnIndex(editor);
  const { table, range } = result;

  const name = await vscode.window.showInputBox({ prompt: 'New column header' });
  if (name === undefined) { return; }

  table.headerRow.splice(col, 0, name || '');
  table.separatorAligns.splice(col, 0, 'none');
  for (const row of table.dataRows) { row.splice(col, 0, ''); }

  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdAddColumnRight(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const col = getCursorColumnIndex(editor) + 1;
  const { table, range } = result;

  const name = await vscode.window.showInputBox({ prompt: 'New column header' });
  if (name === undefined) { return; }

  table.headerRow.splice(col, 0, name || '');
  table.separatorAligns.splice(col, 0, 'none');
  for (const row of table.dataRows) { row.splice(col, 0, ''); }

  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdRemoveColumn(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const { table, range } = result;

  const items = table.headerRow.map((h, i) => ({ label: h || `Column ${i + 1}`, index: i }));
  const picked = await vscode.window.showQuickPick(items, { placeHolder: 'Select column to remove' });
  if (!picked) { return; }

  const col = picked.index;
  table.headerRow.splice(col, 1);
  table.separatorAligns.splice(col, 1);
  for (const row of table.dataRows) { row.splice(col, 1); }

  if (table.headerRow.length === 0) {
    await editor.edit((eb) => eb.replace(range, ''));
  } else {
    await editor.edit((eb) => eb.replace(range, formatTable(table)));
  }
}

async function cmdMoveColumnLeft(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const col = getCursorColumnIndex(editor);
  if (col <= 0) { return; }
  const { table, range } = result;

  swap(table.headerRow, col, col - 1);
  swap(table.separatorAligns, col, col - 1);
  for (const row of table.dataRows) { swap(row, col, col - 1); }

  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdMoveColumnRight(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const col = getCursorColumnIndex(editor);
  const { table, range } = result;
  if (col >= table.headerRow.length - 1) { return; }

  swap(table.headerRow, col, col + 1);
  swap(table.separatorAligns, col, col + 1);
  for (const row of table.dataRows) { swap(row, col, col + 1); }

  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdRenameHeader(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const { table, range } = result;

  const items = table.headerRow.map((h, i) => ({ label: h || `Column ${i + 1}`, index: i }));
  const picked = await vscode.window.showQuickPick(items, { placeHolder: 'Select column to rename' });
  if (!picked) { return; }

  const newName = await vscode.window.showInputBox({ prompt: 'New header name', value: picked.label });
  if (newName === undefined) { return; }

  table.headerRow[picked.index] = newName;
  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

// ---------------------------------------------------------------------------
// Row operations
// ---------------------------------------------------------------------------

async function cmdAddRowAbove(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const { table, range } = result;
  const rowIdx = getCursorRowIndex(editor, range.start.line);
  const insertAt = Math.max(rowIdx, 0);
  const emptyRow = Array.from({ length: table.headerRow.length }, () => '');
  table.dataRows.splice(insertAt, 0, emptyRow);
  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdAddRowBelow(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const { table, range } = result;
  const rowIdx = getCursorRowIndex(editor, range.start.line);
  const insertAt = Math.max(rowIdx + 1, 1);
  const emptyRow = Array.from({ length: table.headerRow.length }, () => '');
  table.dataRows.splice(Math.min(insertAt, table.dataRows.length), 0, emptyRow);
  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdDeleteRow(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const { table, range } = result;
  const rowIdx = getCursorRowIndex(editor, range.start.line);
  if (rowIdx < 0 || rowIdx >= table.dataRows.length) {
    vscode.window.showWarningMessage('Cursor is not on a data row.');
    return;
  }
  table.dataRows.splice(rowIdx, 1);
  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdMoveRowUp(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const { table, range } = result;
  const rowIdx = getCursorRowIndex(editor, range.start.line);
  if (rowIdx <= 0) { return; }
  swap(table.dataRows, rowIdx, rowIdx - 1);
  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

async function cmdMoveRowDown(editor: vscode.TextEditor) {
  const result = getTableAtCursor(editor);
  if (!result) { return vscode.window.showWarningMessage('No Markdown table found at cursor.'); }
  const { table, range } = result;
  const rowIdx = getCursorRowIndex(editor, range.start.line);
  if (rowIdx < 0 || rowIdx >= table.dataRows.length - 1) { return; }
  swap(table.dataRows, rowIdx, rowIdx + 1);
  await editor.edit((eb) => eb.replace(range, formatTable(table)));
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------

function swap<T>(arr: T[], i: number, j: number): void {
  [arr[i], arr[j]] = [arr[j], arr[i]];
}

// ---------------------------------------------------------------------------
// Format on save
// ---------------------------------------------------------------------------

function formatAllTables(doc: vscode.TextDocument): vscode.TextEdit[] {
  const edits: vscode.TextEdit[] = [];
  let i = 0;

  while (i < doc.lineCount) {
    const line = doc.lineAt(i).text.trim();
    if (!line.includes('|')) { i++; continue; }

    // Find contiguous table lines
    const start = i;
    while (i < doc.lineCount && doc.lineAt(i).text.trim().includes('|')) { i++; }
    const end = i - 1;

    if (end - start < 1) { continue; }

    const lines: string[] = [];
    for (let j = start; j <= end; j++) { lines.push(doc.lineAt(j).text); }
    const table = parseTable(lines);
    if (!table) { continue; }

    const range = new vscode.Range(start, 0, end, doc.lineAt(end).text.length);
    const formatted = formatTable(table);
    if (formatted !== lines.join('\n')) {
      edits.push(vscode.TextEdit.replace(range, formatted));
    }
  }

  return edits;
}

// ---------------------------------------------------------------------------
// Activation
// ---------------------------------------------------------------------------

export function activate(context: vscode.ExtensionContext) {
  const reg = (cmd: string, fn: (editor: vscode.TextEditor) => Promise<unknown>) => {
    return vscode.commands.registerTextEditorCommand(cmd, (e) => { fn(e); });
  };

  context.subscriptions.push(
    // Core commands
    reg('markdownTablePro.format', cmdFormat),
    reg('markdownTablePro.sort', cmdSort),
    reg('markdownTablePro.csvToTable', cmdCsvToTable),
    reg('markdownTablePro.tableToCsv', cmdTableToCsv),
    reg('markdownTablePro.importCsvFile', cmdImportCsvFile),

    // Column operations
    reg('markdownTablePro.addColumnLeft', cmdAddColumnLeft),
    reg('markdownTablePro.addColumnRight', cmdAddColumnRight),
    reg('markdownTablePro.removeColumn', cmdRemoveColumn),
    reg('markdownTablePro.moveColumnLeft', cmdMoveColumnLeft),
    reg('markdownTablePro.moveColumnRight', cmdMoveColumnRight),
    reg('markdownTablePro.renameHeader', cmdRenameHeader),

    // Row operations
    reg('markdownTablePro.addRowAbove', cmdAddRowAbove),
    reg('markdownTablePro.addRowBelow', cmdAddRowBelow),
    reg('markdownTablePro.deleteRow', cmdDeleteRow),
    reg('markdownTablePro.moveRowUp', cmdMoveRowUp),
    reg('markdownTablePro.moveRowDown', cmdMoveRowDown),

    // Format on save
    vscode.languages.registerDocumentFormattingEditProvider('markdown', {
      provideDocumentFormattingEdits(doc) {
        return formatAllTables(doc);
      },
    }),

    vscode.workspace.onWillSaveTextDocument((event) => {
      const config = vscode.workspace.getConfiguration('markdownTablePro');
      if (!config.get<boolean>('formatOnSave', false)) { return; }
      if (event.document.languageId !== 'markdown') { return; }
      event.waitUntil(Promise.resolve(formatAllTables(event.document)));
    }),
  );
}

export function deactivate() {}
