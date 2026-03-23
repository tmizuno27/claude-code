const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 400, height: 620 });

  const css = fs.readFileSync(path.join(__dirname, 'popup.css'), 'utf-8');
  const popupJs = fs.readFileSync(path.join(__dirname, 'popup.js'), 'utf-8');

  // Build test page with injected URL
  const testHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <style>${css}</style>
</head>
<body>
  ${fs.readFileSync(path.join(__dirname, 'popup.html'), 'utf-8')
    .replace(/<!DOCTYPE html>[\s\S]*?<body>/, '')
    .replace(/<\/body>[\s\S]*/, '')
    .replace('<link rel="stylesheet" href="popup.css">', '')
    .replace('<script src="popup.js"></script>', '')
  }
  <script>
    // Mock chrome.tabs API
    window.chrome = {
      tabs: {
        query: function(opts, cb) {
          cb([{ url: 'https://nambei-oyaji.com' }]);
        }
      }
    };
    ${popupJs}
  </script>
</body>
</html>`;

  await page.setContent(testHtml, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 1000));

  // Screenshot initial
  await page.screenshot({ path: path.join(__dirname, 'ss-initial.png'), fullPage: true });
  console.log('SS 1: Initial');

  // Click analyze
  await page.click('#analyzeBtn');

  // Wait for results to appear
  await page.waitForFunction(() => {
    const results = document.getElementById('results');
    return results && results.style.display !== 'none';
  }, { timeout: 20000 }).catch(e => console.log('Timeout waiting for results:', e.message));

  await new Promise(r => setTimeout(r, 1500));

  // Screenshot results
  await page.screenshot({ path: path.join(__dirname, 'ss-results.png'), fullPage: true });
  console.log('SS 2: Results');

  // Check for errors
  const errorVisible = await page.evaluate(() => {
    const el = document.getElementById('errorState');
    return el && el.style.display !== 'none' ? document.getElementById('errorMsg')?.textContent : null;
  });
  if (errorVisible) console.log('Error:', errorVisible);

  await browser.close();
  console.log('Done!');
})();
