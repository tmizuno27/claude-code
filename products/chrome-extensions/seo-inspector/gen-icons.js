const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  const sizes = [16, 32, 48, 128];

  for (const size of sizes) {
    await page.setViewport({ width: size, height: size });
    await page.setContent(`
      <html><body style="margin:0;padding:0;background:transparent;">
        <canvas id="c" width="${size}" height="${size}"></canvas>
        <script>
          const size = ${size};
          const canvas = document.getElementById('c');
          const ctx = canvas.getContext('2d');
          const grad = ctx.createLinearGradient(0, 0, size, size);
          grad.addColorStop(0, '#0a84ff');
          grad.addColorStop(1, '#5e5ce6');
          const r = size * 0.2;
          ctx.beginPath();
          ctx.moveTo(r, 0); ctx.lineTo(size-r, 0);
          ctx.quadraticCurveTo(size, 0, size, r);
          ctx.lineTo(size, size-r);
          ctx.quadraticCurveTo(size, size, size-r, size);
          ctx.lineTo(r, size);
          ctx.quadraticCurveTo(0, size, 0, size-r);
          ctx.lineTo(0, r);
          ctx.quadraticCurveTo(0, 0, r, 0);
          ctx.closePath();
          ctx.fillStyle = grad;
          ctx.fill();
          ctx.strokeStyle = '#fff';
          ctx.lineWidth = Math.max(size * 0.08, 1.5);
          ctx.lineCap = 'round';
          const cx = size*0.42, cy = size*0.42, cr = size*0.22;
          ctx.beginPath(); ctx.arc(cx, cy, cr, 0, Math.PI*2); ctx.stroke();
          ctx.beginPath();
          ctx.moveTo(cx+cr*Math.cos(Math.PI/4), cy+cr*Math.sin(Math.PI/4));
          ctx.lineTo(size*0.78, size*0.78);
          ctx.stroke();
        </script>
      </body></html>
    `);

    await page.waitForTimeout(200);
    const canvas = await page.$('#c');
    const dataUrl = await page.evaluate(el => el.toDataURL('image/png'), canvas);
    const base64 = dataUrl.replace(/^data:image\/png;base64,/, '');
    const outPath = path.join(__dirname, 'icons', `icon${size}.png`);
    fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
    console.log(`Generated: icon${size}.png`);
  }

  await browser.close();
  console.log('Done!');
})();
