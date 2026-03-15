/**
 * CSV <-> JSON conversion utilities.
 */

export function csvToJson(csv, headers = true) {
  const lines = parseCSVLines(csv.trim());
  if (lines.length === 0) return [];

  if (headers) {
    const keys = lines[0];
    return lines.slice(1).map(row => {
      const obj = {};
      keys.forEach((key, i) => {
        obj[key] = row[i] !== undefined ? autoType(row[i]) : null;
      });
      return obj;
    });
  }

  return lines;
}

export function jsonToCsv(data) {
  if (!Array.isArray(data) || data.length === 0) {
    throw new Error('Input must be a non-empty JSON array');
  }

  const allKeys = [...new Set(data.flatMap(obj => Object.keys(obj)))];
  const header = allKeys.map(escapeCSV).join(',');
  const rows = data.map(obj =>
    allKeys.map(key => escapeCSV(obj[key] !== undefined ? String(obj[key]) : '')).join(',')
  );

  return [header, ...rows].join('\n');
}

function parseCSVLines(csv) {
  const lines = [];
  let current = [];
  let field = '';
  let inQuotes = false;

  for (let i = 0; i < csv.length; i++) {
    const ch = csv[i];

    if (inQuotes) {
      if (ch === '"') {
        if (csv[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += ch;
      }
    } else {
      if (ch === '"') {
        inQuotes = true;
      } else if (ch === ',') {
        current.push(field.trim());
        field = '';
      } else if (ch === '\n' || ch === '\r') {
        if (ch === '\r' && csv[i + 1] === '\n') i++;
        current.push(field.trim());
        if (current.some(f => f !== '')) lines.push(current);
        current = [];
        field = '';
      } else {
        field += ch;
      }
    }
  }

  current.push(field.trim());
  if (current.some(f => f !== '')) lines.push(current);

  return lines;
}

function escapeCSV(value) {
  const str = String(value);
  if (str.includes(',') || str.includes('"') || str.includes('\n')) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}

function autoType(value) {
  if (value === '') return null;
  if (value === 'true') return true;
  if (value === 'false') return false;
  const num = Number(value);
  if (!isNaN(num) && value.trim() !== '') return num;
  return value;
}
