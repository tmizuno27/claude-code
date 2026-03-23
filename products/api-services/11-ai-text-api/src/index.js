const MODEL = "@cf/meta/llama-3.1-8b-instruct";

const RATE_LIMIT_WINDOW = 60_000;
const RATE_LIMIT_MAX = 30;
const MAX_TEXT_LENGTH = 5000;
const MAX_PROMPT_LENGTH = 1000;

const rateLimitMap = new Map();

function checkRateLimit(ip) {
  const now = Date.now();
  let entry = rateLimitMap.get(ip);
  if (!entry || now - entry.windowStart > RATE_LIMIT_WINDOW) {
    entry = { windowStart: now, count: 0 };
    rateLimitMap.set(ip, entry);
  }
  entry.count++;
  if (entry.count > RATE_LIMIT_MAX) {
    return false;
  }
  return true;
}

function cleanupRateLimit() {
  if (rateLimitMap.size > 10000) {
    const now = Date.now();
    for (const [ip, entry] of rateLimitMap) {
      if (now - entry.windowStart > RATE_LIMIT_WINDOW * 2) {
        rateLimitMap.delete(ip);
      }
    }
  }
}

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-RapidAPI-Key",
};

function json(data, status = 200) {
  if (status === 200 && typeof data === "object" && !Array.isArray(data)) {
    data._upgrade = { note: "Upgrade for higher limits & priority support", url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/ai-text-api/pricing" };
  }
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json", ...CORS_HEADERS },
  });
}

function errorResponse(message, status = 400) {
  return json({ error: message }, status);
}

async function runAI(env, messages, max_tokens = 512, temperature = 0.7) {
  const result = await env.AI.run(MODEL, {
    messages,
    max_tokens,
    temperature,
  });
  return result.response;
}

async function handleGenerate(body, env) {
  const { prompt, max_tokens = 512, temperature = 0.7 } = body;
  if (!prompt) return errorResponse("prompt is required");
  if (typeof prompt !== "string") return errorResponse("prompt must be a string");
  if (prompt.length > MAX_PROMPT_LENGTH)
    return errorResponse(`prompt exceeds ${MAX_PROMPT_LENGTH} characters`);
  if (max_tokens < 1 || max_tokens > 2048)
    return errorResponse("max_tokens must be between 1 and 2048");
  if (temperature < 0 || temperature > 2)
    return errorResponse("temperature must be between 0 and 2");

  const text = await runAI(
    env,
    [
      { role: "system", content: "You are a helpful assistant. Generate text based on the user's prompt. Be creative, accurate, and concise." },
      { role: "user", content: prompt },
    ],
    max_tokens,
    temperature
  );
  return json({ result: text, model: MODEL, usage: { prompt_length: prompt.length } });
}

async function handleSummarize(body, env) {
  const { text, max_length = 200 } = body;
  if (!text) return errorResponse("text is required");
  if (typeof text !== "string") return errorResponse("text must be a string");
  if (text.length > MAX_TEXT_LENGTH)
    return errorResponse(`text exceeds ${MAX_TEXT_LENGTH} characters`);

  const result = await runAI(env, [
    { role: "system", content: `You are a summarization expert. Summarize the following text concisely in approximately ${max_length} words or fewer. Output only the summary, nothing else.` },
    { role: "user", content: text },
  ], 512, 0.3);
  return json({ result, model: MODEL, original_length: text.length });
}

async function handleTranslate(body, env) {
  const { text, source_lang = "auto", target_lang } = body;
  if (!text) return errorResponse("text is required");
  if (!target_lang) return errorResponse("target_lang is required");
  if (typeof text !== "string") return errorResponse("text must be a string");
  if (text.length > MAX_TEXT_LENGTH)
    return errorResponse(`text exceeds ${MAX_TEXT_LENGTH} characters`);

  const sourcePart = source_lang === "auto" ? "" : ` from ${source_lang}`;
  const result = await runAI(env, [
    { role: "system", content: `You are a professional translator. Translate the following text${sourcePart} to ${target_lang}. Output only the translation, nothing else.` },
    { role: "user", content: text },
  ], 1024, 0.3);
  return json({ result, model: MODEL, source_lang, target_lang });
}

async function handleSentiment(body, env) {
  const { text } = body;
  if (!text) return errorResponse("text is required");
  if (typeof text !== "string") return errorResponse("text must be a string");
  if (text.length > MAX_TEXT_LENGTH)
    return errorResponse(`text exceeds ${MAX_TEXT_LENGTH} characters`);

  const result = await runAI(env, [
    { role: "system", content: 'You are a sentiment analysis expert. Analyze the sentiment of the given text. Respond with a JSON object containing: "sentiment" (positive, negative, or neutral), "confidence" (0-1), and "explanation" (brief reason). Output only valid JSON.' },
    { role: "user", content: text },
  ], 256, 0.2);

  let parsed;
  try {
    parsed = JSON.parse(result);
  } catch {
    parsed = { raw: result };
  }
  return json({ result: parsed, model: MODEL });
}

async function handleRewrite(body, env) {
  const { text, tone = "professional" } = body;
  if (!text) return errorResponse("text is required");
  if (typeof text !== "string") return errorResponse("text must be a string");
  if (text.length > MAX_TEXT_LENGTH)
    return errorResponse(`text exceeds ${MAX_TEXT_LENGTH} characters`);
  const validTones = ["formal", "casual", "professional", "simple"];
  if (!validTones.includes(tone))
    return errorResponse(`tone must be one of: ${validTones.join(", ")}`);

  const toneInstructions = {
    formal: "Use formal, polished language suitable for official documents.",
    casual: "Use friendly, conversational language as if talking to a friend.",
    professional: "Use clear, professional business language.",
    simple: "Use simple, easy-to-understand language. Avoid jargon.",
  };

  const result = await runAI(env, [
    { role: "system", content: `You are a writing expert. Rewrite the following text in a ${tone} tone. ${toneInstructions[tone]} Output only the rewritten text, nothing else.` },
    { role: "user", content: text },
  ], 1024, 0.5);
  return json({ result, model: MODEL, tone });
}

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // Rate limiting
    cleanupRateLimit();
    const ip = request.headers.get("cf-connecting-ip") || "unknown";
    if (!checkRateLimit(ip)) {
      return errorResponse("Rate limit exceeded. Max 30 requests per minute.", 429);
    }

    // GET /
    if (path === "/" && request.method === "GET") {
      return json({
        name: "AI Text API",
        
        _premium: {
          message: "You are using the FREE tier of AI Text API. Upgrade to Pro for higher rate limits, priority support, and advanced features.",
          upgrade_url: "https://rapidapi.com/miccho27-5OJaGGbBiO/api/ai-text-api/pricing",
          plans: ["Pro ($5.99/mo)", "Ultra ($14.99/mo)", "Mega ($49.99/mo)"]
        },
        description: "Text generation, summarization, translation, sentiment analysis, and rewriting powered by Cloudflare Workers AI",
        model: MODEL,
        endpoints: [
          { method: "POST", path: "/generate", description: "Generate text from a prompt" },
          { method: "POST", path: "/summarize", description: "Summarize text" },
          { method: "POST", path: "/translate", description: "Translate text between languages" },
          { method: "POST", path: "/sentiment", description: "Analyze text sentiment" },
          { method: "POST", path: "/rewrite", description: "Rewrite text in a different tone" },
        ],
        limits: {
          rate: "30 requests/minute per IP",
          max_prompt: MAX_PROMPT_LENGTH,
          max_text: MAX_TEXT_LENGTH,
        },
      });
    }

    // POST endpoints
    if (request.method !== "POST") {
      return errorResponse("Method not allowed", 405);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return errorResponse("Invalid JSON body");
    }

    try {
      switch (path) {
        case "/generate":
          return await handleGenerate(body, env);
        case "/summarize":
          return await handleSummarize(body, env);
        case "/translate":
          return await handleTranslate(body, env);
        case "/sentiment":
          return await handleSentiment(body, env);
        case "/rewrite":
          return await handleRewrite(body, env);
        default:
          return errorResponse("Not found", 404);
      }
    } catch (err) {
      return errorResponse(`Internal error: ${err.message}`, 500);
    }
  },
};
