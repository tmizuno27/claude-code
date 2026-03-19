import { md5 } from './md5.js';
import { bcryptHashPassword, bcryptCompare } from './bcrypt.js';
import { encode, decode } from './encoding.js';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Proxy-Secret',
  'Content-Type': 'application/json'
};

function json(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/hash-encoding-api/pricing" };
  }
  return new Response(JSON.stringify(data), { status, headers: CORS_HEADERS });
}

function error(message, status = 400) {
  return json({ error: message }, status);
}

function toHex(buffer) {
  return Array.from(new Uint8Array(buffer)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function toBase64(buffer) {
  return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}

const ALGO_MAP = {
  'sha1': 'SHA-1',
  'sha256': 'SHA-256',
  'sha384': 'SHA-384',
  'sha512': 'SHA-512'
};

async function handleHash(body) {
  const { text, algorithm = 'sha256' } = body;
  if (text === undefined || text === null) return error('Missing "text" field');

  const algo = algorithm.toLowerCase();
  const data = new TextEncoder().encode(text);

  if (algo === 'md5') {
    const hex = md5(text);
    const bytes = [];
    for (let i = 0; i < hex.length; i += 2) bytes.push(parseInt(hex.substring(i, i + 2), 16));
    return json({
      algorithm: 'md5',
      hex,
      base64: btoa(String.fromCharCode(...bytes)),
      length: text.length
    });
  }

  const webAlgo = ALGO_MAP[algo];
  if (!webAlgo) return error(`Unsupported algorithm: ${algorithm}. Supported: md5, sha1, sha256, sha384, sha512`);

  const hash = await crypto.subtle.digest(webAlgo, data);
  return json({
    algorithm: algo,
    hex: toHex(hash),
    base64: toBase64(hash),
    length: text.length
  });
}

async function handleHashFile(body) {
  const { data, algorithm = 'sha256' } = body;
  if (!data) return error('Missing "data" field (base64-encoded file content)');

  const algo = algorithm.toLowerCase();
  let bytes;
  try {
    bytes = Uint8Array.from(atob(data), c => c.charCodeAt(0));
  } catch {
    return error('Invalid base64 data');
  }

  if (algo === 'md5') {
    const hex = md5(bytes);
    const hashBytes = [];
    for (let i = 0; i < hex.length; i += 2) hashBytes.push(parseInt(hex.substring(i, i + 2), 16));
    return json({
      algorithm: 'md5',
      hex,
      base64: btoa(String.fromCharCode(...hashBytes)),
      file_size: bytes.length
    });
  }

  const webAlgo = ALGO_MAP[algo];
  if (!webAlgo) return error(`Unsupported algorithm: ${algorithm}. Supported: md5, sha1, sha256, sha384, sha512`);

  const hash = await crypto.subtle.digest(webAlgo, bytes);
  return json({
    algorithm: algo,
    hex: toHex(hash),
    base64: toBase64(hash),
    file_size: bytes.length
  });
}

async function handleHmac(body) {
  const { text, key: secretKey, algorithm = 'sha256' } = body;
  if (text === undefined || text === null) return error('Missing "text" field');
  if (!secretKey) return error('Missing "key" field');

  const algo = algorithm.toLowerCase();
  const webAlgo = ALGO_MAP[algo];
  if (!webAlgo) return error(`Unsupported algorithm: ${algorithm}. Supported: sha1, sha256, sha384, sha512`);

  const keyData = new TextEncoder().encode(secretKey);
  const cryptoKey = await crypto.subtle.importKey(
    'raw', keyData, { name: 'HMAC', hash: webAlgo }, false, ['sign']
  );
  const signature = await crypto.subtle.sign('HMAC', cryptoKey, new TextEncoder().encode(text));

  return json({
    algorithm: algo,
    hex: toHex(signature),
    base64: toBase64(signature)
  });
}

function handleEncode(body) {
  const { text, format } = body;
  if (text === undefined || text === null) return error('Missing "text" field');
  if (!format) return error('Missing "format" field');

  try {
    return json({ encoded: encode(text, format.toLowerCase()), format: format.toLowerCase() });
  } catch (e) {
    return error(e.message);
  }
}

function handleDecode(body) {
  const { text, format } = body;
  if (text === undefined || text === null) return error('Missing "text" field');
  if (!format) return error('Missing "format" field');

  try {
    return json({ decoded: decode(text, format.toLowerCase()), format: format.toLowerCase() });
  } catch (e) {
    return error(e.message);
  }
}

function handleBcrypt(body) {
  const { text, rounds = 10 } = body;
  if (text === undefined || text === null) return error('Missing "text" field');
  if (rounds < 4 || rounds > 31) return error('Rounds must be between 4 and 31');

  try {
    const hash = bcryptHashPassword(text, rounds);
    return json({ hash, rounds });
  } catch (e) {
    return error(e.message);
  }
}

function handleCompare(body) {
  const { text, hash } = body;
  if (text === undefined || text === null) return error('Missing "text" field');
  if (!hash) return error('Missing "hash" field');

  try {
    const match = bcryptCompare(text, hash);
    return json({ match });
  } catch (e) {
    return error(e.message);
  }
}

function handleRandom(url) {
  const params = new URL(url).searchParams;
  const length = Math.min(Math.max(parseInt(params.get('length') || '32', 10), 1), 1024);
  const format = (params.get('format') || 'hex').toLowerCase();

  const bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);

  let value;
  switch (format) {
    case 'hex':
      value = Array.from(bytes).map(b => b.toString(16).padStart(2, '0')).join('');
      break;
    case 'base64':
      value = btoa(String.fromCharCode(...bytes));
      break;
    default:
      return error('Unsupported format. Supported: hex, base64');
  }

  return json({ value, length, format });
}

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // GET endpoints
    if (request.method === 'GET') {
      if (path === '/') {
        return json({
          service: 'Hash & Encoding API',
          
        _premium: {
          message: "You are using the FREE tier of Hash Encoding API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/hash-encoding-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
          endpoints: [
            'POST /hash', 'POST /hash/file', 'POST /hmac',
            'POST /encode', 'POST /decode',
            'POST /bcrypt', 'POST /compare',
            'GET /random?length=32&format=hex'
          ]
        });
      }
      if (path === '/random') return handleRandom(request.url);
      if (path === '/health') return json({ status: 'ok' });
      return error('Not found', 404);
    }

    // POST endpoints
    if (request.method === 'POST') {
      let body;
      try {
        body = await request.json();
      } catch {
        return error('Invalid JSON body');
      }

      switch (path) {
        case '/hash': return handleHash(body);
        case '/hash/file': return handleHashFile(body);
        case '/hmac': return handleHmac(body);
        case '/encode': return handleEncode(body);
        case '/decode': return handleDecode(body);
        case '/bcrypt': return handleBcrypt(body);
        case '/compare': return handleCompare(body);
        default: return error('Not found', 404);
      }
    }

    return error('Method not allowed', 405);
  }
};
