const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

let currentMode = "casual";

// Init
document.addEventListener("DOMContentLoaded", async () => {
  // Check API key
  chrome.runtime.sendMessage({ action: "hasKey" }, (res) => {
    if (!res?.hasKey) {
      $("#noKeyWarning").classList.remove("hidden");
    }
  });

  // Load usage info
  updateUsageBadge();

  // License key panel
  $("#licenseBtn").addEventListener("click", () => {
    $("#licensePanel").classList.toggle("hidden");
    chrome.runtime.sendMessage({ action: "getLicenseKey" }, (res) => {
      if (res?.key) {
        $("#licenseKeyInput").value = res.key;
        $("#licenseStatus").textContent = "Pro license active";
        $("#licenseStatus").className = "status ok";
      }
    });
  });

  $("#saveLicenseBtn").addEventListener("click", () => {
    const key = $("#licenseKeyInput").value.trim();
    if (!key || key.length < 8) {
      $("#licenseStatus").textContent = "Invalid license key";
      $("#licenseStatus").className = "status err";
      return;
    }
    chrome.runtime.sendMessage({ action: "saveLicenseKey", key }, (res) => {
      if (res?.success) {
        $("#licenseStatus").textContent = "License activated! Enjoy Pro.";
        $("#licenseStatus").className = "status ok";
        updateUsageBadge();
      }
    });
  });

  $("#removeLicenseBtn").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "removeLicenseKey" }, (res) => {
      if (res?.success) {
        $("#licenseKeyInput").value = "";
        $("#licenseStatus").textContent = "License removed";
        $("#licenseStatus").className = "status err";
        updateUsageBadge();
      }
    });
  });

  // Mode buttons
  $$(".mode-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      $$(".mode-btn").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentMode = btn.dataset.mode;
      chrome.storage.local.set({ lastMode: currentMode });
    });
  });

  // Load last mode
  chrome.storage.local.get("lastMode", (data) => {
    if (data.lastMode) {
      currentMode = data.lastMode;
      $$(".mode-btn").forEach((b) => {
        b.classList.toggle("active", b.dataset.mode === currentMode);
      });
    }
  });

  // Close upgrade overlay
  $("#closeUpgrade").addEventListener("click", () => {
    $("#upgradeOverlay").classList.add("hidden");
  });

  // Load last result from context menu
  chrome.storage.local.get("lastResult", (data) => {
    if (data.lastResult) {
      $("#inputText").value = data.lastResult.original;
      $("#resultText").textContent = data.lastResult.rewritten;
      $("#resultSection").classList.remove("hidden");
    }
  });

  // Settings toggle
  $("#settingsBtn").addEventListener("click", () => {
    $("#settingsPanel").classList.toggle("hidden");
  });

  // Toggle key visibility
  $("#toggleKeyVis").addEventListener("click", () => {
    const inp = $("#apiKeyInput");
    inp.type = inp.type === "password" ? "text" : "password";
  });

  // Save key
  $("#saveKeyBtn").addEventListener("click", () => {
    const key = $("#apiKeyInput").value.trim();
    if (!key || !key.startsWith("sk-")) {
      showStatus("Invalid API key format", false);
      return;
    }
    chrome.runtime.sendMessage({ action: "saveKey", key }, (res) => {
      if (res?.success) {
        showStatus("Key saved successfully", true);
        $("#apiKeyInput").value = "";
        $("#noKeyWarning").classList.add("hidden");
      }
    });
  });

  // Delete key
  $("#deleteKeyBtn").addEventListener("click", () => {
    chrome.runtime.sendMessage({ action: "deleteKey" }, (res) => {
      if (res?.success) {
        showStatus("Key deleted", true);
        $("#noKeyWarning").classList.remove("hidden");
      }
    });
  });

  // Rewrite
  $("#rewriteBtn").addEventListener("click", doRewrite);

  // Copy
  $("#copyBtn").addEventListener("click", () => {
    const text = $("#resultText").textContent;
    navigator.clipboard.writeText(text).then(() => {
      $("#copyBtn").textContent = "Copied!";
      setTimeout(() => { $("#copyBtn").textContent = "Copy to Clipboard"; }, 1500);
    });
  });

  // History toggle
  $("#historyBtn").addEventListener("click", () => {
    const panel = $("#historyPanel");
    const wasHidden = panel.classList.contains("hidden");
    panel.classList.toggle("hidden");
    if (wasHidden) loadHistory();
  });
});

function updateUsageBadge() {
  chrome.runtime.sendMessage({ action: "getUsageInfo" }, (res) => {
    if (!res) return;
    const badge = $("#usageBadge");
    if (res.isPro) {
      badge.textContent = "PRO";
      badge.className = "usage-badge pro";
    } else {
      badge.textContent = `${res.count}/${res.limit} today`;
      badge.className = "usage-badge" + (res.count >= res.limit ? " depleted" : "");
    }
  });
}

function showUpgradeModal() {
  $("#upgradeOverlay").classList.remove("hidden");
}

function showStatus(msg, ok) {
  const el = $("#keyStatus");
  el.textContent = msg;
  el.className = "status " + (ok ? "ok" : "err");
  setTimeout(() => { el.textContent = ""; el.className = "status"; }, 3000);
}

async function doRewrite() {
  const text = $("#inputText").value.trim();
  if (!text) return;

  $("#rewriteBtn").disabled = true;
  $("#resultSection").classList.add("hidden");
  $("#errorMsg").classList.add("hidden");
  $("#loading").classList.remove("hidden");

  chrome.runtime.sendMessage({ action: "rewrite", text, mode: currentMode }, (res) => {
    $("#loading").classList.add("hidden");
    $("#rewriteBtn").disabled = false;

    if (res?.error === "LIMIT_REACHED") {
      showUpgradeModal();
      updateUsageBadge();
      return;
    }

    if (res?.success) {
      $("#resultText").textContent = res.result;
      $("#resultSection").classList.remove("hidden");
      updateUsageBadge();
    } else {
      const errEl = $("#errorMsg");
      errEl.textContent = res?.error === "NO_API_KEY"
        ? "Please set your OpenAI API key in Settings."
        : (res?.error || "Unknown error");
      errEl.classList.remove("hidden");
    }
  });
}

function loadHistory() {
  chrome.runtime.sendMessage({ action: "getHistory" }, (res) => {
    const list = $("#historyList");
    const noHist = $("#noHistory");
    list.innerHTML = "";

    const history = res?.history || [];
    if (history.length === 0) {
      noHist.classList.remove("hidden");
      return;
    }
    noHist.classList.add("hidden");

    history.forEach((item) => {
      const div = document.createElement("div");
      div.className = "history-item";
      const time = new Date(item.timestamp).toLocaleString();
      div.innerHTML = `
        <div class="meta">
          <span>${time}</span>
          <span class="mode-tag">${item.mode}</span>
        </div>
        <div class="orig">${escHtml(item.original)}</div>
        <div class="rewr">${escHtml(item.rewritten)}</div>
      `;
      div.style.cursor = "pointer";
      div.addEventListener("click", () => {
        $("#inputText").value = item.original;
        $("#resultText").textContent = item.rewritten;
        $("#resultSection").classList.remove("hidden");
        $("#historyPanel").classList.add("hidden");
      });
      list.appendChild(div);
    });
  });
}

function escHtml(str) {
  const d = document.createElement("div");
  d.textContent = str;
  return d.innerHTML;
}
