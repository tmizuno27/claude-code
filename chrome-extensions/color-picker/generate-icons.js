const sharp = require('sharp');
const sizes = [16, 32, 48, 128];

async function generateIcon(size) {
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 100 100">
    <defs>
      <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stop-color="#ff0000"/>
        <stop offset="17%" stop-color="#ff8800"/>
        <stop offset="33%" stop-color="#ffff00"/>
        <stop offset="50%" stop-color="#00cc00"/>
        <stop offset="67%" stop-color="#0088ff"/>
        <stop offset="83%" stop-color="#8800ff"/>
        <stop offset="100%" stop-color="#ff00ff"/>
      </linearGradient>
    </defs>
    <circle cx="50" cy="50" r="45" fill="url(#g1)"/>
    <circle cx="50" cy="50" r="25" fill="#0f172a"/>
    <circle cx="50" cy="50" r="12" fill="#ffffff" opacity="0.9"/>
  </svg>`;
  await sharp(Buffer.from(svg)).resize(size, size).png().toFile(`icons/icon${size}.png`);
  console.log(`Generated icon${size}.png`);
}

Promise.all(sizes.map(generateIcon)).then(() => console.log('Done'));
