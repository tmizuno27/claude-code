const SUPPORTED_LANGUAGES = [
  'en','es','fr','de','it','pt','nl','pl','ru','zh','ja','ko','ar','hi','tr','vi','th','id',
  'cs','ro','da','fi','hu','no','sv','uk','bg','el','hr','sk','sl','sr','lt','lv','et','mt',
  'ga','cy','af','sw','ha','ig','yo','zu'
];

const RATE_LIMIT_MAX = 30;
const RATE_LIMIT_WINDOW = 60000;
const RATE_LIMIT_MAX_ENTRIES = 10000;

const rateLimitMap = new Map();

function rateLimit(ip) {
  const now = Date.now();
  // Size-based cleanup
  if (rateLimitMap.size > RATE_LIMIT_MAX_ENTRIES) {
    for (const [key, entry] of rateLimitMap) {
      if (now - entry.start > RATE_LIMIT_WINDOW) rateLimitMap.delete(key);
      if (rateLimitMap.size <= RATE_LIMIT_MAX_ENTRIES / 2) break;
    }
  }
  const entry = rateLimitMap.get(ip);
  if (!entry || now - entry.start > RATE_LIMIT_WINDOW) {
    rateLimitMap.set(ip, { start: now, count: 1 });
    return true;
  }
  entry.count++;
  return entry.count <= RATE_LIMIT_MAX;
}

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...corsHeaders() },
  });
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    const ip = request.headers.get('cf-connecting-ip') || 'unknown';
    if (!rateLimit(ip)) {
      return json({ error: 'Rate limit exceeded. Max 30 requests per minute.' }, 429);
    }

    const url = new URL(request.url);
    const path = url.pathname;

    try {
      if (path === '/' && request.method === 'GET') {
        return json({
          name: 'ai-translate-api',
          
        _premium: {
          message: "You are using the FREE tier of AI Translate API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/ai-translate-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
          description: 'Translation API powered by Cloudflare Workers AI',
          endpoints: {
            'GET /': 'API info',
            'POST /translate': 'Translate text',
            'POST /detect': 'Detect language',
            'POST /batch': 'Batch translate (max 10)',
            'GET /languages': 'List supported languages',
          },
          supported_languages: SUPPORTED_LANGUAGES,
          model: '@cf/meta/m2m100-1.2b',
        });
      }

      if (path === '/languages' && request.method === 'GET') {
        return json({ languages: SUPPORTED_LANGUAGES, count: SUPPORTED_LANGUAGES.length });
      }

      if (path === '/translate' && request.method === 'POST') {
        const body = await request.json();
        const { text, source_lang, target_lang } = body;
        if (!text || !source_lang || !target_lang) {
          return json({ error: 'Missing required fields: text, source_lang, target_lang' }, 400);
        }
        if (!SUPPORTED_LANGUAGES.includes(source_lang) || !SUPPORTED_LANGUAGES.includes(target_lang)) {
          return json({ error: 'Unsupported language code' }, 400);
        }
        const result = await env.AI.run('@cf/meta/m2m100-1.2b', { text, source_lang, target_lang });
        return json({
          translated_text: result.translated_text,
          source_lang,
          target_lang,
          model: '@cf/meta/m2m100-1.2b',
        });
      }

      if (path === '/detect' && request.method === 'POST') {
        const body = await request.json();
        const { text } = body;
        if (!text) {
          return json({ error: 'Missing required field: text' }, 400);
        }
        const result = await env.AI.run('@cf/meta/llama-3.1-8b-instruct', {
          messages: [
            {
              role: 'system',
              content: 'You are a language detection tool. Respond with ONLY a JSON object: {"detected_language":"<ISO 639-1 code>","confidence":<0.0-1.0>}. No other text.',
            },
            {
              role: 'user',
              content: `Detect the language of this text: "${text}"`,
            },
          ],
        });
        try {
          const parsed = JSON.parse(result.response);
          return json({ detected_language: parsed.detected_language, confidence: parsed.confidence });
        } catch {
          return json({ detected_language: result.response.trim(), confidence: null });
        }
      }

      if (path === '/batch' && request.method === 'POST') {
        const body = await request.json();
        const { texts, source_lang, target_lang } = body;
        if (!texts || !Array.isArray(texts) || !source_lang || !target_lang) {
          return json({ error: 'Missing required fields: texts (array), source_lang, target_lang' }, 400);
        }
        if (texts.length > 10) {
          return json({ error: 'Maximum 10 texts per request' }, 400);
        }
        if (!SUPPORTED_LANGUAGES.includes(source_lang) || !SUPPORTED_LANGUAGES.includes(target_lang)) {
          return json({ error: 'Unsupported language code' }, 400);
        }
        const translations = await Promise.all(
          texts.map(async (text) => {
            const result = await env.AI.run('@cf/meta/m2m100-1.2b', { text, source_lang, target_lang });
            return { original: text, translated_text: result.translated_text };
          })
        );
        return json({ translations, source_lang, target_lang, model: '@cf/meta/m2m100-1.2b' });
      }

      return json({ error: 'Not found' }, 404);
    } catch (err) {
      return json({ error: 'Internal server error', message: err.message }, 500);
    }
  },
};
