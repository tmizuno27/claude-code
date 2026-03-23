// Freemium constants
const FREE_DAILY_LIMIT = 5;
const GUMROAD_URL = "https://tatsuya27.gumroad.com/l/ai-text-rewriter-pro";

// Usage tracking
async function getUsageToday() {
  const data = await chrome.storage.local.get("rewriter_usage");
  const usage = data.rewriter_usage || { count: 0, date: "" };
  const today = new Date().toISOString().slice(0, 10);
  if (usage.date !== today) return { count: 0, date: today };
  return usage;
}

async function incrementUsage() {
  const usage = await getUsageToday();
  usage.count++;
  await chrome.storage.local.set({ rewriter_usage: usage });
  return usage;
}

async function isPro() {
  const data = await chrome.storage.sync.get("rewriter_license_key");
  const key = data.rewriter_license_key;
  return !!(key && key.length >= 8);
}

// Context menu setup
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "rewrite-with-ai",
    title: "Rewrite with AI",
    contexts: ["selection"]
  });
});

// Simple XOR obfuscation for API key storage (not true encryption, but deters casual inspection)
function obfuscate(text) {
  const key = "ai-text-rewriter-v1";
  return Array.from(text)
    .map((c, i) => String.fromCharCode(c.charCodeAt(0) ^ key.charCodeAt(i % key.length)))
    .join("");
}

const deobfuscate = obfuscate; // XOR is symmetric

async function getApiKey() {
  const data = await chrome.storage.local.get("openai_api_key_enc");
  if (!data.openai_api_key_enc) return null;
  return deobfuscate(data.openai_api_key_enc);
}

async function callOpenAI(text, mode) {
  const apiKey = await getApiKey();
  if (!apiKey) throw new Error("NO_API_KEY");

  const prompts = {
    casual: "Rewrite the following text in a casual, friendly tone. Keep the same meaning.",
    professional: "Rewrite the following text in a professional, business-appropriate tone. Keep the same meaning.",
    shorter: "Rewrite the following text to be shorter and more concise. Keep the key meaning.",
    longer: "Rewrite the following text with more detail and elaboration. Expand on the ideas.",
    grammar: "Fix only the grammar and spelling errors in the following text. Do not change the tone or meaning."
  };

  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: "gpt-4o-mini",
      messages: [
        { role: "system", content: prompts[mode] + " Return only the rewritten text, nothing else." },
        { role: "user", content: text }
      ],
      temperature: 0.7,
      max_tokens: 2048
    })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error?.message || `API error ${res.status}`);
  }

  const json = await res.json();
  return json.choices[0].message.content.trim();
}

// Save to history
async function saveHistory(original, rewritten, mode) {
  const data = await chrome.storage.local.get("history");
  const history = data.history || [];
  history.unshift({ original, rewritten, mode, timestamp: Date.now() });
  if (history.length > 10) history.length = 10;
  await chrome.storage.local.set({ history });
}

// Context menu click
chrome.contextMenus.onClicked.addListener(async (info, tab) => {
  if (info.menuItemId !== "rewrite-with-ai") return;

  const text = info.selectionText;
  if (!text) return;

  // Get last used mode or default
  const data = await chrome.storage.local.get("lastMode");
  const mode = data.lastMode || "professional";

  try {
    const pro = await isPro();
    if (!pro) {
      const usage = await getUsageToday();
      if (usage.count >= FREE_DAILY_LIMIT) {
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: (url) => {
            const toast = document.createElement("div");
            toast.innerHTML = `Daily limit reached (5 rewrites). <a href="${url}" target="_blank" style="color:#fbbf24;text-decoration:underline;">Upgrade to Pro</a>`;
            toast.style.cssText = "position:fixed;bottom:20px;right:20px;background:#ef4444;color:white;padding:12px 20px;border-radius:8px;font-family:-apple-system,sans-serif;font-weight:600;font-size:14px;z-index:999999;box-shadow:0 4px 20px rgba(0,0,0,0.3);";
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 5000);
          },
          args: [GUMROAD_URL]
        });
        return;
      }
    }
    const result = await callOpenAI(text, mode);
    if (!pro) await incrementUsage();
    await saveHistory(text, result, mode);
    // Send result to popup via storage (user opens popup to see it)
    await chrome.storage.local.set({ lastResult: { original: text, rewritten: result, mode } });
    // Also copy to clipboard via content script
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (rewritten) => {
        navigator.clipboard.writeText(rewritten);
        // Show toast notification
        const toast = document.createElement("div");
        toast.textContent = "Rewritten text copied to clipboard!";
        toast.style.cssText = "position:fixed;bottom:20px;right:20px;background:#f59e0b;color:#0f172a;padding:12px 20px;border-radius:8px;font-family:-apple-system,sans-serif;font-weight:600;font-size:14px;z-index:999999;box-shadow:0 4px 20px rgba(0,0,0,0.3);";
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
      },
      args: [result]
    });
  } catch (e) {
    if (e.message === "NO_API_KEY") {
      await chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
          const toast = document.createElement("div");
          toast.textContent = "Please set your OpenAI API key in the extension settings.";
          toast.style.cssText = "position:fixed;bottom:20px;right:20px;background:#ef4444;color:white;padding:12px 20px;border-radius:8px;font-family:-apple-system,sans-serif;font-weight:600;font-size:14px;z-index:999999;box-shadow:0 4px 20px rgba(0,0,0,0.3);";
          document.body.appendChild(toast);
          setTimeout(() => toast.remove(), 4000);
        }
      });
    }
  }
});

// Message handler for popup
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg.action === "rewrite") {
    (async () => {
      const pro = await isPro();
      if (!pro) {
        const usage = await getUsageToday();
        if (usage.count >= FREE_DAILY_LIMIT) {
          sendResponse({ success: false, error: "LIMIT_REACHED", limit: FREE_DAILY_LIMIT, gumroadUrl: GUMROAD_URL });
          return;
        }
      }
      try {
        const result = await callOpenAI(msg.text, msg.mode);
        await saveHistory(msg.text, result, msg.mode);
        if (!pro) await incrementUsage();
        const usage = await getUsageToday();
        sendResponse({ success: true, result, usage: { count: usage.count, limit: FREE_DAILY_LIMIT, isPro: pro } });
      } catch (e) {
        sendResponse({ success: false, error: e.message });
      }
    })();
    return true; // async
  }
  if (msg.action === "getUsageInfo") {
    (async () => {
      const pro = await isPro();
      const usage = await getUsageToday();
      sendResponse({ count: usage.count, limit: FREE_DAILY_LIMIT, isPro: pro, gumroadUrl: GUMROAD_URL });
    })();
    return true;
  }
  if (msg.action === "saveLicenseKey") {
    chrome.storage.sync.set({ rewriter_license_key: msg.key }).then(() => sendResponse({ success: true }));
    return true;
  }
  if (msg.action === "getLicenseKey") {
    chrome.storage.sync.get("rewriter_license_key").then((data) => sendResponse({ key: data.rewriter_license_key || "" }));
    return true;
  }
  if (msg.action === "removeLicenseKey") {
    chrome.storage.sync.remove("rewriter_license_key").then(() => sendResponse({ success: true }));
    return true;
  }
  if (msg.action === "saveKey") {
    const enc = obfuscate(msg.key);
    chrome.storage.local.set({ openai_api_key_enc: enc }).then(() => sendResponse({ success: true }));
    return true;
  }
  if (msg.action === "hasKey") {
    chrome.storage.local.get("openai_api_key_enc").then((data) => {
      sendResponse({ hasKey: !!data.openai_api_key_enc });
    });
    return true;
  }
  if (msg.action === "deleteKey") {
    chrome.storage.local.remove("openai_api_key_enc").then(() => sendResponse({ success: true }));
    return true;
  }
  if (msg.action === "getHistory") {
    chrome.storage.local.get("history").then((data) => sendResponse({ history: data.history || [] }));
    return true;
  }
});
