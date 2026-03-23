const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1400, height: 900 });

  await page.goto('http://localhost:4567/dashboard', { waitUntil: 'networkidle0' });

  const inputs = await page.$$('input');
  await inputs[0].type('https://nambei-oyaji.com/wp-json/wp/v2');
  await inputs[1].type('t.mizuno27@gmail.com');
  await inputs[2].type('agNg 2624 4lL4 QoT9 EOOZ OEZr');

  await page.click('button');
  await page.waitForFunction(
    () => document.body.innerText.includes('\u5357\u7c73\u304a\u3084\u3058') || document.body.innerText.includes('error'),
    { timeout: 15000 }
  );
  await new Promise(r => setTimeout(r, 1000));
  await page.screenshot({ path: __dirname + '/connected.png' });

  const buttons = await page.$$('button');
  for (const btn of buttons) {
    const text = await btn.evaluate(el => el.textContent);
    if (text && text.includes('Analyze')) {
      await btn.click();
      break;
    }
  }

  await page.waitForFunction(
    () => document.body.innerText.includes('Total Posts') || document.body.innerText.includes('error'),
    { timeout: 30000 }
  );
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: __dirname + '/analysis-result.png', fullPage: true });

  await browser.close();
  console.log('Done');
})();
