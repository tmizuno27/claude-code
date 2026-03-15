import { WORDLIST } from './wordlist.js';
import { checkStrength } from './strength.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Proxy-Secret',
  'Content-Type': 'application/json',
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
}

function error(message, status = 400) {
  return json({ error: message }, status);
}

/** Crypto-secure random integer in [0, max) */
function secureRandomInt(max) {
  const arr = new Uint32Array(1);
  crypto.getRandomValues(arr);
  return arr[0] % max;
}

/** Generate random bytes and return as array */
function randomBytes(length) {
  const buf = new Uint8Array(length);
  crypto.getRandomValues(buf);
  return buf;
}

// ── Password Generator ──

function generatePassword(length, { uppercase, lowercase, numbers, symbols }) {
  let charset = '';
  if (lowercase) charset += 'abcdefghijklmnopqrstuvwxyz';
  if (uppercase) charset += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  if (numbers) charset += '0123456789';
  if (symbols) charset += '!@#$%^&*()_+-=[]{}|;:,.<>?/~`';
  if (!charset) charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';

  let result = '';
  for (let i = 0; i < length; i++) {
    result += charset[secureRandomInt(charset.length)];
  }
  return result;
}

// ── UUID v4 Generator ──

function generateUUIDv4() {
  const bytes = randomBytes(16);
  bytes[6] = (bytes[6] & 0x0f) | 0x40; // version 4
  bytes[8] = (bytes[8] & 0x3f) | 0x80; // variant 10
  const hex = Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('');
  return `${hex.slice(0,8)}-${hex.slice(8,12)}-${hex.slice(12,16)}-${hex.slice(16,20)}-${hex.slice(20,32)}`;
}

// ── Token Generator ──

function generateToken(length, format) {
  if (format === 'base64') {
    const bytes = randomBytes(length);
    return btoa(String.fromCharCode(...bytes)).slice(0, length);
  }
  if (format === 'alphanumeric') {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) result += chars[secureRandomInt(chars.length)];
    return result;
  }
  // hex (default)
  const bytes = randomBytes(Math.ceil(length / 2));
  return Array.from(bytes, b => b.toString(16).padStart(2, '0')).join('').slice(0, length);
}

// ── PIN Generator ──

function generatePIN(length) {
  let pin = '';
  for (let i = 0; i < length; i++) pin += secureRandomInt(10).toString();
  return pin;
}

// ── Passphrase Generator ──

function generatePassphrase(wordCount, separator, capitalize) {
  const words = [];
  for (let i = 0; i < wordCount; i++) {
    let word = WORDLIST[secureRandomInt(WORDLIST.length)];
    if (capitalize) word = word.charAt(0).toUpperCase() + word.slice(1);
    words.push(word);
  }
  return words.join(separator);
}

// ── Router ──

function parseBool(val, defaultVal = true) {
  if (val === undefined || val === null) return defaultVal;
  return val === 'true' || val === '1';
}

function clamp(val, min, max, def) {
  const n = parseInt(val);
  if (isNaN(n)) return def;
  return Math.max(min, Math.min(max, n));
}

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;
  const params = url.searchParams;

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  // GET /
  if (path === '/' || path === '') {
    return json({
      name: 'Password & Random Data Generator API',
      version: '1.0.0',
      endpoints: [
        'GET /password',
        'GET /uuid',
        'GET /token',
        'GET /pin',
        'POST /passphrase',
        'GET /strength',
      ],
      documentation: 'https://password-generator-api.t-mizuno27.workers.dev/',
    });
  }

  // GET /password
  if (path === '/password' && request.method === 'GET') {
    const length = clamp(params.get('length'), 4, 256, 16);
    const count = clamp(params.get('count'), 1, 100, 1);
    const opts = {
      uppercase: parseBool(params.get('uppercase'), true),
      lowercase: parseBool(params.get('lowercase'), true),
      numbers: parseBool(params.get('numbers'), true),
      symbols: parseBool(params.get('symbols'), true),
    };
    const passwords = Array.from({ length: count }, () => generatePassword(length, opts));
    return json({
      passwords: count === 1 ? passwords[0] : passwords,
      count,
      length,
      options: opts,
    });
  }

  // GET /uuid
  if (path === '/uuid' && request.method === 'GET') {
    const version = parseInt(params.get('version') || '4');
    if (version !== 4) return error('Only UUID v4 is supported.');
    const count = clamp(params.get('count'), 1, 100, 1);
    const uuids = Array.from({ length: count }, () => generateUUIDv4());
    return json({
      uuids: count === 1 ? uuids[0] : uuids,
      count,
      version: 4,
    });
  }

  // GET /token
  if (path === '/token' && request.method === 'GET') {
    const length = clamp(params.get('length'), 1, 512, 32);
    const format = params.get('format') || 'hex';
    if (!['hex', 'base64', 'alphanumeric'].includes(format)) {
      return error('Format must be hex, base64, or alphanumeric.');
    }
    const count = clamp(params.get('count'), 1, 100, 1);
    const tokens = Array.from({ length: count }, () => generateToken(length, format));
    return json({
      tokens: count === 1 ? tokens[0] : tokens,
      count,
      length,
      format,
    });
  }

  // GET /pin
  if (path === '/pin' && request.method === 'GET') {
    const length = clamp(params.get('length'), 3, 20, 6);
    const count = clamp(params.get('count'), 1, 100, 1);
    const pins = Array.from({ length: count }, () => generatePIN(length));
    return json({
      pins: count === 1 ? pins[0] : pins,
      count,
      length,
    });
  }

  // POST /passphrase
  if (path === '/passphrase' && request.method === 'POST') {
    let body = {};
    try {
      body = await request.json();
    } catch {
      // use defaults
    }
    const words = clamp(body.words, 2, 20, 4);
    const separator = typeof body.separator === 'string' ? body.separator.slice(0, 5) : '-';
    const capitalize = body.capitalize !== false;
    const count = clamp(body.count, 1, 100, 1);
    const passphrases = Array.from({ length: count }, () => generatePassphrase(words, separator, capitalize));
    return json({
      passphrases: count === 1 ? passphrases[0] : passphrases,
      count,
      words,
      separator,
      capitalize,
      wordlist_size: WORDLIST.length,
    });
  }

  // GET /strength
  if (path === '/strength' && request.method === 'GET') {
    const password = params.get('password');
    if (!password) return error('Query parameter "password" is required.');
    const result = checkStrength(password);
    return json({ password_length: password.length, ...result });
  }

  return error('Not found.', 404);
}

export default {
  fetch: handleRequest,
};
