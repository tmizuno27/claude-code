// popup.js — Tab Manager & Session Saver

document.addEventListener("DOMContentLoaded", init);

// --- State ---
let allTabs = [];
let dragSrcIndex = null;

// --- Init ---
async function init() {
  loadTheme();
  await updateProBadge();
  setupNavigation();
  setupEventListeners();
  await loadTabs();
}

// --- Theme ---
function loadTheme() {
  const theme = localStorage.getItem("theme") || "light";
  document.body.setAttribute("data-theme", theme);
  updateThemeIcon(theme);
}

function toggleTheme() {
  const current = document.body.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.body.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const icon = document.querySelector(".icon-theme");
  icon.textContent = theme === "dark" ? "\u2600" : "\u263E";
}

// --- Navigation ---
function setupNavigation() {
  const navTabs = document.querySelectorAll(".nav-tab");
  navTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      navTabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
      const panelId = `panel-${tab.dataset.tab}`;
      document.getElementById(panelId).classList.add("active");

      if (tab.dataset.tab === "sessions") {
        loadSessions();
      } else {
        loadTabs();
      }
    });
  });
}

// --- Event Listeners ---
function setupEventListeners() {
  document.getElementById("btn-theme").addEventListener("click", toggleTheme);
  document.getElementById("btn-pro").addEventListener("click", togglePro);
  document.getElementById("search-tabs").addEventListener("input", filterTabs);
  document.getElementById("btn-close-duplicates").addEventListener("click", closeDuplicates);
  document.getElementById("btn-save-session").addEventListener("click", saveSession);
  document.getElementById("btn-export").addEventListener("click", exportSessions);
  document.getElementById("btn-import").addEventListener("click", () => {
    document.getElementById("import-file").click();
  });
  document.getElementById("import-file").addEventListener("change", importSessions);
}

// --- Pro Status ---
async function togglePro() {
  const isPro = await sendMessage({ action: "getProStatus" });
  await sendMessage({ action: "setProStatus", isPro: !isPro });
  await updateProBadge();
  showToast(isPro ? "Switched to Free plan" : "Pro unlocked!");
}

async function updateProBadge() {
  const isPro = await sendMessage({ action: "getProStatus" });
  const btn = document.getElementById("btn-pro");
  btn.textContent = isPro ? "PRO" : "FREE";
  btn.classList.toggle("pro-active", isPro);
}

// --- Tabs ---
async function loadTabs() {
  allTabs = await sendMessage({ action: "getTabs" });
  renderTabs(allTabs);
}

function renderTabs(tabs) {
  const list = document.getElementById("tab-list");
  const countLabel = document.getElementById("tab-count-label");
  countLabel.textContent = `${tabs.length} tab${tabs.length !== 1 ? "s" : ""}`;

  const duplicateUrls = findDuplicateUrls(tabs);

  list.innerHTML = "";
  tabs.forEach((tab, index) => {
    const isDuplicate = duplicateUrls.has(normalizeUrl(tab.url));
    const li = createTabElement(tab, index, isDuplicate);
    list.appendChild(li);
  });
}

function createTabElement(tab, index, isDuplicate) {
  const li = document.createElement("li");
  li.className = `tab-item${isDuplicate ? " duplicate" : ""}`;
  li.draggable = true;
  li.dataset.index = index;

  const favicon = tab.favIconUrl
    ? `<img class="tab-favicon" src="${escapeHtml(tab.favIconUrl)}" alt="" onerror="this.className='tab-favicon-placeholder'">`
    : '<div class="tab-favicon-placeholder"></div>';

  li.innerHTML = `
    ${favicon}
    <div class="tab-info">
      <div class="tab-title">${escapeHtml(tab.title)}</div>
      <div class="tab-url">${escapeHtml(tab.url)}</div>
    </div>
    <button class="tab-close" data-tab-id="${tab.id}" title="Close tab">&times;</button>
  `;

  // Click to switch
  li.addEventListener("click", (e) => {
    if (e.target.closest(".tab-close")) return;
    sendMessage({ action: "switchToTab", tabId: tab.id });
  });

  // Close button
  li.querySelector(".tab-close").addEventListener("click", async (e) => {
    e.stopPropagation();
    await sendMessage({ action: "closeTab", tabId: tab.id });
    await loadTabs();
  });

  // Drag events
  li.addEventListener("dragstart", (e) => {
    dragSrcIndex = index;
    li.classList.add("dragging");
    e.dataTransfer.effectAllowed = "move";
  });

  li.addEventListener("dragend", () => {
    li.classList.remove("dragging");
    document.querySelectorAll(".drag-over").forEach((el) => el.classList.remove("drag-over"));
  });

  li.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    li.classList.add("drag-over");
  });

  li.addEventListener("dragleave", () => {
    li.classList.remove("drag-over");
  });

  li.addEventListener("drop", (e) => {
    e.preventDefault();
    li.classList.remove("drag-over");
    const targetIndex = index;
    if (dragSrcIndex !== null && dragSrcIndex !== targetIndex) {
      const moved = allTabs.splice(dragSrcIndex, 1)[0];
      allTabs.splice(targetIndex, 0, moved);
      renderTabs(allTabs);

      // Reorder actual Chrome tabs
      chrome.tabs.move(moved.id, { index: targetIndex });
    }
    dragSrcIndex = null;
  });

  return li;
}

function filterTabs() {
  const query = document.getElementById("search-tabs").value.toLowerCase();
  if (!query) {
    renderTabs(allTabs);
    return;
  }
  const filtered = allTabs.filter(
    (t) => t.title.toLowerCase().includes(query) || t.url.toLowerCase().includes(query)
  );
  renderTabs(filtered);
}

async function closeDuplicates() {
  const result = await sendMessage({ action: "closeDuplicates" });
  if (result.success) {
    showToast(`Closed ${result.closed} duplicate tab${result.closed !== 1 ? "s" : ""}`);
    await loadTabs();
  }
}

// --- Sessions ---
async function loadSessions() {
  const sessions = await sendMessage({ action: "getSessions" });
  const list = document.getElementById("session-list");
  const empty = document.getElementById("session-empty");

  list.innerHTML = "";

  if (sessions.length === 0) {
    empty.style.display = "block";
    return;
  }

  empty.style.display = "none";

  sessions.forEach((session) => {
    const li = document.createElement("li");
    li.className = "session-item";

    const date = new Date(session.createdAt);
    const dateStr = date.toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });

    li.innerHTML = `
      <div class="session-info">
        <div class="session-name">${escapeHtml(session.name)}</div>
        <div class="session-meta">${session.tabCount} tabs &middot; ${dateStr}</div>
      </div>
      <div class="session-actions">
        <button class="session-btn restore" data-id="${session.id}">Restore</button>
        <button class="session-btn delete" data-id="${session.id}">Delete</button>
      </div>
    `;

    li.querySelector(".restore").addEventListener("click", async () => {
      const result = await sendMessage({ action: "restoreSession", sessionId: session.id });
      if (result.success) {
        showToast(`Restored ${result.tabCount} tabs`);
      } else {
        showToast(result.error);
      }
    });

    li.querySelector(".delete").addEventListener("click", async () => {
      await sendMessage({ action: "deleteSession", sessionId: session.id });
      showToast("Session deleted");
      await loadSessions();
    });

    list.appendChild(li);
  });
}

async function saveSession() {
  const input = document.getElementById("session-name");
  const name = input.value.trim();
  if (!name) {
    showToast("Enter a session name");
    input.focus();
    return;
  }

  const result = await sendMessage({ action: "saveSession", name });
  if (result.success) {
    showToast(`Session "${name}" saved`);
    input.value = "";
    await loadSessions();
  } else {
    showToast(result.error);
  }
}

async function exportSessions() {
  const result = await sendMessage({ action: "exportSessions" });
  if (!result.success) {
    showToast(result.error);
    return;
  }

  const blob = new Blob([result.data], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "tab-manager-sessions.json";
  a.click();
  URL.revokeObjectURL(url);
  showToast("Sessions exported");
}

async function importSessions(e) {
  const file = e.target.files[0];
  if (!file) return;

  const text = await file.text();
  const result = await sendMessage({ action: "importSessions", data: text });
  if (result.success) {
    showToast(`Imported ${result.added} session${result.added !== 1 ? "s" : ""}`);
    await loadSessions();
  } else {
    showToast(result.error);
  }
  e.target.value = "";
}

// --- Utilities ---
function sendMessage(message) {
  return new Promise((resolve) => {
    chrome.runtime.sendMessage(message, (response) => {
      resolve(response);
    });
  });
}

function showToast(text) {
  const toast = document.getElementById("toast");
  toast.textContent = text;
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 2500);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function normalizeUrl(url) {
  try {
    const u = new URL(url);
    return `${u.origin}${u.pathname}${u.search}`;
  } catch {
    return url;
  }
}

function findDuplicateUrls(tabs) {
  const counts = new Map();
  for (const tab of tabs) {
    const key = normalizeUrl(tab.url);
    counts.set(key, (counts.get(key) || 0) + 1);
  }
  const duplicates = new Set();
  for (const [key, count] of counts) {
    if (count > 1) duplicates.add(key);
  }
  return duplicates;
}
