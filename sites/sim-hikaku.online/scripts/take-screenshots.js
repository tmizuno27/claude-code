const puppeteer = require('puppeteer');
const path = require('path');

const articles = [
  { slug: 'yoto-betsu-kakuyasu-sim-erabikata', name: 'yoto-betsu-kakuyasu-sim-erabikata' },
  { slug: 'kakuyasu-sim-ryokin-hikaku-ichiran', name: 'kakuyasu-sim-ryokin-hikaku-ichiran' },
];

const screenshotDir = path.join(__dirname, 'images', 'screenshots');

(async () => {
  const browser = await puppeteer.launch({ headless: true });

  for (const article of articles) {
    const url = `https://sim-hikaku.online/${article.slug}/`;
    console.log(`Taking screenshot: ${url}`);

    // Desktop
    const pageD = await browser.newPage();
    await pageD.setViewport({ width: 1280, height: 800 });
    try {
      await pageD.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
      await pageD.screenshot({
        path: path.join(screenshotDir, `${article.name}-desktop.png`),
        fullPage: true,
      });
      console.log(`  Desktop OK`);
    } catch (e) {
      console.error(`  Desktop FAIL: ${e.message}`);
    }
    await pageD.close();

    // Mobile
    const pageM = await browser.newPage();
    await pageM.setViewport({ width: 375, height: 812 });
    await pageM.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1');
    try {
      await pageM.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
      await pageM.screenshot({
        path: path.join(screenshotDir, `${article.name}-mobile.png`),
        fullPage: true,
      });
      console.log(`  Mobile OK`);
    } catch (e) {
      console.error(`  Mobile FAIL: ${e.message}`);
    }
    await pageM.close();
  }

  await browser.close();
  console.log('Done!');
})();
