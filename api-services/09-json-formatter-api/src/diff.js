/**
 * Deep diff between two JSON objects.
 * Returns an array of differences with path, type (added/removed/changed), and values.
 */
export function jsonDiff(a, b, path = '') {
  const diffs = [];

  if (a === b) return diffs;

  const typeA = typeOf(a);
  const typeB = typeOf(b);

  if (typeA !== typeB) {
    diffs.push({ path: path || '(root)', type: 'changed', from: a, to: b });
    return diffs;
  }

  if (typeA === 'array') {
    const maxLen = Math.max(a.length, b.length);
    for (let i = 0; i < maxLen; i++) {
      const p = path ? `${path}[${i}]` : `[${i}]`;
      if (i >= a.length) {
        diffs.push({ path: p, type: 'added', value: b[i] });
      } else if (i >= b.length) {
        diffs.push({ path: p, type: 'removed', value: a[i] });
      } else {
        diffs.push(...jsonDiff(a[i], b[i], p));
      }
    }
    return diffs;
  }

  if (typeA === 'object') {
    const allKeys = new Set([...Object.keys(a), ...Object.keys(b)]);
    for (const key of allKeys) {
      const p = path ? `${path}.${key}` : key;
      if (!(key in a)) {
        diffs.push({ path: p, type: 'added', value: b[key] });
      } else if (!(key in b)) {
        diffs.push({ path: p, type: 'removed', value: a[key] });
      } else {
        diffs.push(...jsonDiff(a[key], b[key], p));
      }
    }
    return diffs;
  }

  // Primitives
  if (a !== b) {
    diffs.push({ path: path || '(root)', type: 'changed', from: a, to: b });
  }

  return diffs;
}

function typeOf(v) {
  if (v === null) return 'null';
  if (Array.isArray(v)) return 'array';
  return typeof v;
}
