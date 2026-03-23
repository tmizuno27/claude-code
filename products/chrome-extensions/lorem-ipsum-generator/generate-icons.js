const sharp = require('sharp');
const path = require('path');

const sizes = [16, 32, 48, 128];

async function generateIcon(size) {
  const svg = `
  <svg width="${size}" height="${size}" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
    <rect width="128" height="128" rx="28" fill="#0f172a"/>
    <text x="64" y="92" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="80" fill="#ec4899">T</text>
  </svg>`;

  await sharp(Buffer.from(svg))
    .resize(size, size)
    .png()
    .toFile(path.join(__dirname, 'icons', `icon${size}.png`));

  console.log(`Generated icon${size}.png`);
}

(async () => {
  for (const s of sizes) await generateIcon(s);
  console.log('Done!');
})();
