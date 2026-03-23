const sharp = require('sharp');
const path = require('path');

const sizes = [16, 32, 48, 128];

async function generateIcon(size) {
  const svg = `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#0a84ff"/>
          <stop offset="100%" stop-color="#5e5ce6"/>
        </linearGradient>
      </defs>
      <rect width="${size}" height="${size}" rx="${size * 0.2}" fill="url(#g)"/>
      <circle cx="${size * 0.42}" cy="${size * 0.42}" r="${size * 0.22}" fill="none" stroke="white" stroke-width="${Math.max(size * 0.08, 1.5)}" stroke-linecap="round"/>
      <line x1="${size * 0.42 + size * 0.22 * Math.cos(Math.PI / 4)}" y1="${size * 0.42 + size * 0.22 * Math.sin(Math.PI / 4)}" x2="${size * 0.78}" y2="${size * 0.78}" stroke="white" stroke-width="${Math.max(size * 0.08, 1.5)}" stroke-linecap="round"/>
    </svg>`;

  const outPath = path.join(__dirname, 'icons', `icon${size}.png`);
  await sharp(Buffer.from(svg)).png().toFile(outPath);
  console.log(`Generated: icon${size}.png`);
}

Promise.all(sizes.map(generateIcon)).then(() => console.log('Done!'));
