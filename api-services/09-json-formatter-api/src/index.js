import { jsonDiff } from './diff.js';
import { transform } from './transform.js';
import { csvToJson, jsonToCsv } from './csv.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Proxy-Secret',
  'Content-Type': 'application/json',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
}

function error(message, status = 400) {
  return json({ error: message }, status);
}

async function getBody(request) {
  const text = await request.text();
  if (!text) throw new Error('Request body is empty');
  return JSON.parse(text);
}

/** Recursively compute depth and key count */
function jsonStats(data) {
  const raw = typeof data === 'string' ? data : JSON.stringify(data);
  const parsed = typeof data === 'string' ? JSON.parse(data) : data;

  let keys = 0;
  function countKeys(obj) {
    if (obj && typeof obj === 'object') {
      if (Array.isArray(obj)) {
        obj.forEach(countKeys);
      } else {
        const k = Object.keys(obj);
        keys += k.length;
        k.forEach(key => countKeys(obj[key]));
      }
    }
  }

  function getDepth(obj) {
    if (!obj || typeof obj !== 'object') return 0;
    if (Array.isArray(obj)) {
      if (obj.length === 0) return 1;
      return 1 + Math.max(...obj.map(getDepth));
    }
    const vals = Object.values(obj);
    if (vals.length === 0) return 1;
    return 1 + Math.max(...vals.map(getDepth));
  }

  countKeys(parsed);
  return { keys, depth: getDepth(parsed), size_bytes: new TextEncoder().encode(raw).length };
}

async function handleFormat(request) {
  const body = await getBody(request);
  const { data, indent = 2 } = body;
  if (data === undefined) return error('Missing "data" field');

  const parsed = typeof data === 'string' ? JSON.parse(data) : data;
  const formatted = JSON.stringify(parsed, null, indent);
  return json({ formatted });
}

async function handleMinify(request) {
  const body = await getBody(request);
  const { data } = body;
  if (data === undefined) return error('Missing "data" field');

  const parsed = typeof data === 'string' ? JSON.parse(data) : data;
  const minified = JSON.stringify(parsed);
  return json({ minified });
}

async function handleValidate(request) {
  const body = await getBody(request);
  const { data } = body;
  if (data === undefined) return error('Missing "data" field');

  const errors = [];
  let parsed;

  if (typeof data === 'string') {
    try {
      parsed = JSON.parse(data);
    } catch (e) {
      return json({
        valid: false,
        errors: [{ message: e.message, position: extractPosition(e.message) }],
        stats: null,
      });
    }
  } else {
    parsed = data;
  }

  return json({ valid: true, errors: [], stats: jsonStats(parsed) });
}

function extractPosition(msg) {
  const match = msg.match(/position (\d+)/);
  return match ? parseInt(match[1], 10) : null;
}

async function handleDiff(request) {
  const body = await getBody(request);
  const { a, b } = body;
  if (a === undefined || b === undefined) return error('Missing "a" or "b" field');

  const diffs = jsonDiff(a, b);
  return json({
    equal: diffs.length === 0,
    total_differences: diffs.length,
    differences: diffs,
  });
}

async function handleTransform(request) {
  const body = await getBody(request);
  const { data, query } = body;
  if (data === undefined || !query) return error('Missing "data" or "query" field');

  const result = transform(data, query);
  return json({ result });
}

async function handleCsvToJson(request) {
  const body = await getBody(request);
  const { csv, headers = true } = body;
  if (!csv) return error('Missing "csv" field');

  const result = csvToJson(csv, headers);
  return json({ data: result, rows: result.length });
}

async function handleJsonToCsv(request) {
  const body = await getBody(request);
  const { data } = body;
  if (!data) return error('Missing "data" field');

  const csvStr = jsonToCsv(data);
  return json({ csv: csvStr });
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === 'GET' && (path === '/' || path === '')) {
      return json({
        service: 'JSON Formatter & Validator API',
        version: '1.0.0',
        endpoints: ['/format', '/minify', '/validate', '/diff', '/transform', '/csv-to-json', '/json-to-csv'],
      });
    }

    if (request.method !== 'POST') {
      return error('Method not allowed. Use POST.', 405);
    }

    try {
      switch (path) {
        case '/format': return await handleFormat(request);
        case '/minify': return await handleMinify(request);
        case '/validate': return await handleValidate(request);
        case '/diff': return await handleDiff(request);
        case '/transform': return await handleTransform(request);
        case '/csv-to-json': return await handleCsvToJson(request);
        case '/json-to-csv': return await handleJsonToCsv(request);
        default: return error('Not found', 404);
      }
    } catch (e) {
      return error(e.message, 400);
    }
  },
};
