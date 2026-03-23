chrome.runtime.onMessage.addListener((msg, sender) => {
  if (msg.type === 'json-detected' && sender.tab) {
    chrome.action.setBadgeText({
      tabId: sender.tab.id,
      text: msg.valid ? 'JSON' : 'ERR'
    });
    chrome.action.setBadgeBackgroundColor({
      tabId: sender.tab.id,
      color: msg.valid ? '#3b82f6' : '#dc2626'
    });
  }
});
