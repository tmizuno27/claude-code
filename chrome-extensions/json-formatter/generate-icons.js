const sharp = require('sharp');
const path = require('path');

const sizes = [16, 32, 48, 128];

function makeSVG(size) {
  const fs = Math.round(size * 0.5);
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
    <rect width="${size}" height="${size}" rx="${Math.round(size*0.18)}" fill="#1e293b"/>
    <text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle"
      font-family="Consolas,Monaco,monospace" font-size="${fs}" font-weight="bold" fill="#3b82f6">{ }</text>
  </svg>`;
}

(async () => {
  for (const s of sizes) {
    await sharp(Buffer.from(makeSVG(s)))
      .png()
      .toFile(path.join(__dirname, 'icons', `icon${s}.png`));
    console.log(`icon${s}.png created`);
  }
})();
