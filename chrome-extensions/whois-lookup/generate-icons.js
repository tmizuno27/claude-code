const sharp = require('sharp');
const path = require('path');

const sizes = [16, 32, 48, 128];

async function generateIcon(size) {
  const svg = `<svg width="${size}" height="${size}" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#7c3aed"/>
        <stop offset="100%" style="stop-color:#8b5cf6"/>
      </linearGradient>
    </defs>
    <rect width="128" height="128" rx="28" fill="url(#bg)"/>
    <!-- Globe -->
    <circle cx="64" cy="58" r="30" fill="none" stroke="white" stroke-width="4"/>
    <ellipse cx="64" cy="58" rx="14" ry="30" fill="none" stroke="white" stroke-width="3"/>
    <line x1="34" y1="58" x2="94" y2="58" stroke="white" stroke-width="3"/>
    <line x1="38" y1="44" x2="90" y2="44" stroke="white" stroke-width="2.5"/>
    <line x1="38" y1="72" x2="90" y2="72" stroke="white" stroke-width="2.5"/>
    <!-- Search/WHOIS indicator -->
    <circle cx="84" cy="82" r="12" fill="none" stroke="white" stroke-width="4"/>
    <line x1="92" y1="90" x2="102" y2="100" stroke="white" stroke-width="5" stroke-linecap="round"/>
    <!-- "W" text -->
    <text x="64" y="112" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="18" fill="rgba(255,255,255,0.8)">WHOIS</text>
  </svg>`;

  await sharp(Buffer.from(svg))
    .resize(size, size)
    .png()
    .toFile(path.join(__dirname, 'icons', `icon${size}.png`));

  console.log(`Generated icon${size}.png`);
}

Promise.all(sizes.map(generateIcon)).then(() => console.log('Done'));
