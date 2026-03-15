/**
 * Lightweight JMESPath-like query engine.
 * Supports: dot notation, array index, wildcard [*], nested paths.
 * Examples: "items[*].name", "users[0].email", "config.database.host"
 */
export function transform(data, query) {
  const tokens = tokenize(query);
  return evaluate(data, tokens);
}

function tokenize(query) {
  const tokens = [];
  let i = 0;
  while (i < query.length) {
    if (query[i] === '.') {
      i++;
      continue;
    }
    if (query[i] === '[') {
      const end = query.indexOf(']', i);
      if (end === -1) throw new Error(`Unmatched bracket at position ${i}`);
      const inner = query.slice(i + 1, end);
      if (inner === '*') {
        tokens.push({ type: 'wildcard' });
      } else if (inner.startsWith('?')) {
        tokens.push({ type: 'filter', expr: inner.slice(1) });
      } else {
        tokens.push({ type: 'index', value: parseInt(inner, 10) });
      }
      i = end + 1;
      continue;
    }
    // Read key
    let key = '';
    while (i < query.length && query[i] !== '.' && query[i] !== '[') {
      key += query[i];
      i++;
    }
    if (key) tokens.push({ type: 'key', value: key });
  }
  return tokens;
}

function evaluate(data, tokens) {
  let current = data;

  for (let i = 0; i < tokens.length; i++) {
    const token = tokens[i];

    if (current === null || current === undefined) return null;

    if (token.type === 'key') {
      if (typeof current === 'object' && !Array.isArray(current)) {
        current = current[token.value];
      } else {
        return null;
      }
    } else if (token.type === 'index') {
      if (Array.isArray(current)) {
        current = current[token.value];
      } else {
        return null;
      }
    } else if (token.type === 'wildcard') {
      if (!Array.isArray(current)) return null;
      const remaining = tokens.slice(i + 1);
      if (remaining.length === 0) return current;
      return current.map(item => evaluate(item, remaining)).filter(v => v !== null);
    } else if (token.type === 'filter') {
      if (!Array.isArray(current)) return null;
      const [key, val] = token.expr.split('==').map(s => s.trim());
      const cleanVal = val.replace(/^['"]|['"]$/g, '');
      current = current.filter(item => String(item[key]) === cleanVal);
    }
  }

  return current;
}
