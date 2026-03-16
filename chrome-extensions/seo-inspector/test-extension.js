const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const extPath = path.resolve(__dirname);

  const browser = await puppeteer.launch({
    headless: false,
    args: [
      `--disable-extensions-except=${extPath}`,
      `--load-extension=${extPath}`,
      '--no-sandbox'
    ]
  });

  // Navigate to a test page
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto('https://nambei-oyaji.com', { waitUntil: 'networkidle2', timeout: 30000 });

  // Wait for page to load
  await new Promise(r => setTimeout(r, 2000));

  // Get extension ID
  const targets = await browser.targets();
  const extTarget = targets.find(t => t.type() === 'service_worker' && t.url().includes('chrome-extension://'));

  if (!extTarget) {
    console.log('Extension not found. Checking all targets:');
    targets.forEach(t => console.log(`  ${t.type()}: ${t.url()}`));

    // Try to find extension page target
    const extPageTarget = targets.find(t => t.url().includes('chrome-extension://'));
    if (extPageTarget) {
      const extId = extPageTarget.url().match(/chrome-extension:\/\/([^/]+)/)?.[1];
      console.log('Found extension ID:', extId);
    }
  } else {
    const extId = extTarget.url().match(/chrome-extension:\/\/([^/]+)/)?.[1];
    console.log('Extension ID:', extId);

    // Open popup directly
    const popupPage = await browser.newPage();
    await popupPage.setViewport({ width: 400, height: 600 });
    await popupPage.goto(`chrome-extension://${extId}/popup.html`, { waitUntil: 'domcontentloaded' });

    await new Promise(r => setTimeout(r, 1000));

    // Take screenshot of popup
    await popupPage.screenshot({
      path: path.join(__dirname, 'screenshot-popup-initial.png'),
      fullPage: true
    });
    console.log('Screenshot saved: screenshot-popup-initial.png');
  }

  // Keep browser open for manual inspection
  console.log('Browser is open. Press Ctrl+C to close.');

  // Auto-close after 60 seconds
  await new Promise(r => setTimeout(r, 60000));
  await browser.close();
})();
