chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "hash-encode",
    title: "Hash & Encode: \"%s\"",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener(async (info) => {
  if (info.menuItemId === "hash-encode" && info.selectionText) {
    await chrome.storage.local.set({ selectedText: info.selectionText });

    try {
      await chrome.action.openPopup();
    } catch {
      // Fallback: open popup.html in a new window if openPopup() is unavailable
      chrome.windows.create({
        url: chrome.runtime.getURL("popup.html"),
        type: "popup",
        width: 420,
        height: 560,
      });
    }
  }
});
