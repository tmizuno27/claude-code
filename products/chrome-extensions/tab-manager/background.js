// background.js — Tab Manager & Session Saver

const FREE_SESSION_LIMIT = 3;

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  const handlers = {
    getTabs: handleGetTabs,
    saveSession: handleSaveSession,
    getSessions: handleGetSessions,
    deleteSession: handleDeleteSession,
    restoreSession: handleRestoreSession,
    closeDuplicates: handleCloseDuplicates,
    closeTab: handleCloseTab,
    switchToTab: handleSwitchToTab,
    exportSessions: handleExportSessions,
    importSessions: handleImportSessions,
    getProStatus: handleGetProStatus,
    setProStatus: handleSetProStatus,
  };

  const handler = handlers[message.action];
  if (handler) {
    handler(message).then(sendResponse).catch((err) => {
      sendResponse({ success: false, error: err.message });
    });
    return true;
  }
});

async function handleGetTabs() {
  const tabs = await chrome.tabs.query({ currentWindow: true });
  return tabs.map(toTabInfo);
}

async function handleSaveSession(message) {
  const isPro = await getProStatus();
  const { sessions = [] } = await chrome.storage.local.get("sessions");

  if (!isPro && sessions.length >= FREE_SESSION_LIMIT) {
    return {
      success: false,
      error: `Free plan allows up to ${FREE_SESSION_LIMIT} sessions. Upgrade to Pro for unlimited sessions.`,
    };
  }

  const tabs = await chrome.tabs.query({ currentWindow: true });
  const session = {
    id: crypto.randomUUID(),
    name: message.name,
    tabs: tabs.map(toTabInfo),
    createdAt: new Date().toISOString(),
    tabCount: tabs.length,
  };

  const updated = [...sessions, session];
  await chrome.storage.local.set({ sessions: updated });
  return { success: true, session };
}

async function handleGetSessions() {
  const { sessions = [] } = await chrome.storage.local.get("sessions");
  return sessions;
}

async function handleDeleteSession(message) {
  const { sessions = [] } = await chrome.storage.local.get("sessions");
  const updated = sessions.filter((s) => s.id !== message.sessionId);
  await chrome.storage.local.set({ sessions: updated });
  return { success: true };
}

async function handleRestoreSession(message) {
  const { sessions = [] } = await chrome.storage.local.get("sessions");
  const session = sessions.find((s) => s.id === message.sessionId);
  if (!session) {
    return { success: false, error: "Session not found" };
  }

  for (const tab of session.tabs) {
    await chrome.tabs.create({ url: tab.url, active: false });
  }
  return { success: true, tabCount: session.tabs.length };
}

async function handleCloseDuplicates() {
  const tabs = await chrome.tabs.query({ currentWindow: true });
  const seen = new Map();
  const duplicateIds = [];

  for (const tab of tabs) {
    const normalizedUrl = normalizeUrl(tab.url);
    if (seen.has(normalizedUrl)) {
      duplicateIds.push(tab.id);
    } else {
      seen.set(normalizedUrl, tab.id);
    }
  }

  if (duplicateIds.length > 0) {
    await chrome.tabs.remove(duplicateIds);
  }
  return { success: true, closed: duplicateIds.length };
}

async function handleCloseTab(message) {
  await chrome.tabs.remove(message.tabId);
  return { success: true };
}

async function handleSwitchToTab(message) {
  await chrome.tabs.update(message.tabId, { active: true });
  return { success: true };
}

async function handleExportSessions() {
  const isPro = await getProStatus();
  if (!isPro) {
    return {
      success: false,
      error: "Export is a Pro feature. Upgrade to unlock.",
    };
  }
  const { sessions = [] } = await chrome.storage.local.get("sessions");
  return { success: true, data: JSON.stringify(sessions, null, 2) };
}

async function handleImportSessions(message) {
  const isPro = await getProStatus();
  if (!isPro) {
    return {
      success: false,
      error: "Import is a Pro feature. Upgrade to unlock.",
    };
  }

  try {
    const imported = JSON.parse(message.data);
    if (!Array.isArray(imported)) {
      return { success: false, error: "Invalid format: expected an array" };
    }
    const { sessions = [] } = await chrome.storage.local.get("sessions");
    const existingIds = new Set(sessions.map((s) => s.id));
    const newSessions = imported.filter((s) => !existingIds.has(s.id));
    const merged = [...sessions, ...newSessions];
    await chrome.storage.local.set({ sessions: merged });
    return { success: true, added: newSessions.length };
  } catch {
    return { success: false, error: "Invalid JSON data" };
  }
}

async function handleGetProStatus() {
  return getProStatus();
}

async function handleSetProStatus(message) {
  await chrome.storage.local.set({ isPro: message.isPro });
  return { success: true };
}

async function getProStatus() {
  const { isPro = false } = await chrome.storage.local.get("isPro");
  return isPro;
}

function toTabInfo(tab) {
  return {
    id: tab.id,
    title: tab.title || "Untitled",
    url: tab.url || "",
    favIconUrl: tab.favIconUrl || "",
    pinned: tab.pinned || false,
  };
}

function normalizeUrl(url) {
  try {
    const u = new URL(url);
    return `${u.origin}${u.pathname}${u.search}`;
  } catch {
    return url;
  }
}
