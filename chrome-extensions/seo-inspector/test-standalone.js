const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 400, height: 620 });

  // Read popup files
  const html = fs.readFileSync(path.join(__dirname, 'popup.html'), 'utf-8');
  const css = fs.readFileSync(path.join(__dirname, 'popup.css'), 'utf-8');

  // Modified JS that doesn't use chrome.tabs API
  const testUrl = 'https://nambei-oyaji.com';

  const modifiedHtml = html
    .replace('<link rel="stylesheet" href="popup.css">', `<style>${css}</style>`)
    .replace('<script src="popup.js"></script>', `
      <script>
        const API_BASE = 'https://seo-analyzer-api.t-mizuno27.workers.dev';
        const $ = (id) => document.getElementById(id);
        let currentUrl = '${testUrl}';

        document.addEventListener('DOMContentLoaded', () => {
          document.getElementById('urlText').textContent = currentUrl;
          document.getElementById('analyzeBtn').addEventListener('click', analyze);
          document.getElementById('retryBtn').addEventListener('click', analyze);
        });

        ${fs.readFileSync(path.join(__dirname, 'popup.js'), 'utf-8')
          .replace(/const API_BASE.*/, '')
          .replace(/const \$ =.*/, '')
          .replace(/let currentUrl.*/, '')
          .replace(/document\.addEventListener\('DOMContentLoaded'[\s\S]*?\}\);/, '')
        }
      </script>
    `);

  await page.setContent(modifiedHtml, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 500));

  // Screenshot: initial state
  await page.screenshot({ path: path.join(__dirname, 'screenshot-initial.png'), fullPage: true });
  console.log('Screenshot 1: Initial state');

  // Click analyze
  await page.click('#analyzeBtn');
  await new Promise(r => setTimeout(r, 1000));

  // Screenshot: loading
  await page.screenshot({ path: path.join(__dirname, 'screenshot-loading.png'), fullPage: true });
  console.log('Screenshot 2: Loading state');

  // Wait for results
  await page.waitForSelector('#results', { visible: true, timeout: 15000 }).catch(() => {});
  await new Promise(r => setTimeout(r, 2000));

  // Screenshot: results
  await page.screenshot({ path: path.join(__dirname, 'screenshot-results.png'), fullPage: true });
  console.log('Screenshot 3: Results');

  await browser.close();
  console.log('Done!');
})();
