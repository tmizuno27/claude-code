const sharp = require("sharp");
const path = require("path");

const sizes = [16, 32, 48, 128];

async function generateIcon(size) {
  const s = size;
  const cx = s / 2;
  const cy = s / 2;
  const r = s * 0.38;
  const stroke = Math.max(1.5, s * 0.06);
  const fontSize = Math.round(s * 0.32);

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${s}" height="${s}" viewBox="0 0 ${s} ${s}">
    <rect width="${s}" height="${s}" rx="${s * 0.18}" fill="#0f172a"/>
    <circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#06b6d4" stroke-width="${stroke}"/>
    <text x="${cx}" y="${cy}" text-anchor="middle" dominant-baseline="central"
          font-family="Arial,sans-serif" font-weight="bold" font-size="${fontSize}" fill="#06b6d4">#</text>
  </svg>`;

  await sharp(Buffer.from(svg)).png().toFile(path.join(__dirname, "icons", `icon${size}.png`));
  console.log(`Generated icon${size}.png`);
}

Promise.all(sizes.map(generateIcon)).then(() => console.log("Done"));
