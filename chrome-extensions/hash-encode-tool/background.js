chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "hash-encode",
    title: "Hash & Encode: \"%s\"",
    contexts: ["selection"],
  });
});

chrome.contextMenus.onClicked.addListener((info) => {
  if (info.menuItemId === "hash-encode" && info.selectionText) {
    chrome.storage.local.set({ selectedText: info.selectionText }, () => {
      chrome.action.openPopup();
    });
  }
});
