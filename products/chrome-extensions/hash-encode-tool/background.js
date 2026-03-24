chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "hash-encode",
    title: "Hash & Encode: \"%s\"",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === "hash-encode" && info.selectionText) {
    // Store selected text so popup.js can retrieve it
    chrome.storage.local.set({ selectedText: info.selectionText });

    // Open popup.html in a small popup window (most reliable method)
    chrome.windows.create({
      url: chrome.runtime.getURL("popup.html"),
      type: "popup",
      width: 480,
      height: 600,
    });
  }
});
