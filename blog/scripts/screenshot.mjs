import puppeteer from 'puppeteer';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(__dirname, '..', 'design');

const url = 'https://nambei-oyaji.com/paraguay-food-culture/';

(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await browser.newPage();

  // Desktop view
  await page.setViewport({ width: 1400, height: 900 });
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 2000)); // Wait for JS to run
  await page.screenshot({ path: path.join(outDir, 'screenshot-desktop.png'), fullPage: true });
  console.log('Desktop screenshot saved');

  // Also take a cropped view of just the top area to see sidebar
  await page.screenshot({ path: path.join(outDir, 'screenshot-desktop-top.png'), fullPage: false });
  console.log('Desktop top screenshot saved');

  // Scroll down to see sidebar TOC (sticky)
  await page.evaluate(() => window.scrollTo(0, 3000));
  await new Promise(r => setTimeout(r, 1000));
  await page.screenshot({ path: path.join(outDir, 'screenshot-desktop-mid.png'), fullPage: false });
  console.log('Desktop mid screenshot saved');

  await browser.close();
})();
