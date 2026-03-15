// ============================================================
// QR Code Generator API — Cloudflare Worker
// Pure JavaScript implementation (no Node.js dependencies)
// ============================================================

// --------------- QR Code Encoder (Pure JS) ---------------

const ECL = { L: 1, M: 0, Q: 3, H: 2 };

const MODE_BYTE = 4;

// Error correction codewords per block and block counts for versions 1-40
// Format: [totalCodewords, ecCodewordsPerBlock, group1Blocks, group1DataCW, group2Blocks, group2DataCW]
const EC_TABLE = {
  L: [
    [26,7,1,19,0,0],[44,10,1,34,0,0],[70,15,1,55,0,0],[100,20,1,80,0,0],
    [134,26,1,108,0,0],[172,18,2,68,0,0],[196,20,2,78,0,0],[242,24,2,97,0,0],
    [292,30,2,116,0,0],[346,18,2,68,2,69],[404,20,4,81,0,0],[466,24,2,92,2,93],
    [532,26,4,107,0,0],[581,30,3,115,1,116],[655,22,5,87,1,88],[733,24,5,98,1,99],
    [815,28,1,107,5,108],[901,30,5,120,1,121],[991,28,3,113,4,114],[1085,28,3,107,5,108],
    [1156,28,4,116,4,117],[1258,28,2,111,7,112],[1364,30,4,121,5,122],[1474,30,6,117,4,118],
    [1588,26,8,106,4,107],[1706,28,10,114,2,115],[1828,30,8,122,4,123],[1921,30,3,117,10,118],
    [2051,30,7,116,7,117],[2185,30,5,115,10,116],[2323,30,13,115,3,116],[2465,30,17,115,0,0],
    [2611,30,17,115,1,116],[2761,30,13,115,6,116],[2876,30,12,121,7,122],[3034,30,6,121,14,122],
    [3196,30,17,122,4,123],[3362,30,4,122,18,123],[3532,30,20,117,4,118],[3706,30,19,118,6,119],
  ],
  M: [
    [26,10,1,16,0,0],[44,16,1,28,0,0],[70,26,1,44,0,0],[100,18,2,32,0,0],
    [134,24,2,43,0,0],[172,16,4,27,0,0],[196,18,4,31,0,0],[242,22,2,38,2,39],
    [292,22,3,36,2,37],[346,26,4,43,1,44],[404,30,1,50,4,51],[466,22,6,36,2,37],
    [532,22,8,37,1,38],[581,24,4,40,5,41],[655,24,5,41,5,42],[733,28,7,45,3,46],
    [815,28,10,46,1,47],[901,26,9,43,4,44],[991,26,3,44,11,45],[1085,26,3,41,13,42],
    [1156,26,17,42,0,0],[1258,28,17,46,0,0],[1364,28,4,47,14,48],[1474,28,6,45,14,46],
    [1588,28,8,47,13,48],[1706,28,19,46,4,47],[1828,28,22,45,3,46],[1921,28,3,45,23,46],
    [2051,28,21,45,7,46],[2185,28,19,47,10,48],[2323,28,2,46,29,47],[2465,28,10,46,23,47],
    [2611,28,14,46,21,47],[2761,28,14,46,23,47],[2876,28,12,47,26,48],[3034,28,6,47,34,48],
    [3196,28,29,46,14,47],[3362,28,13,46,32,47],[3532,28,40,47,7,48],[3706,28,18,47,31,48],
  ],
  Q: [
    [26,13,1,13,0,0],[44,22,1,22,0,0],[70,18,2,17,0,0],[100,26,2,24,0,0],
    [134,18,2,15,2,16],[172,24,4,19,0,0],[196,18,2,14,4,15],[242,22,4,18,2,19],
    [292,20,4,16,4,17],[346,24,6,19,2,20],[404,28,4,22,4,23],[466,26,4,20,6,21],
    [532,24,8,20,4,21],[581,20,11,16,5,17],[655,30,5,24,7,25],[733,24,15,19,2,20],
    [815,28,1,22,15,23],[901,28,17,22,1,23],[991,26,17,21,4,22],[1085,30,15,24,5,25],
    [1156,28,17,22,6,23],[1258,30,7,24,16,25],[1364,30,11,24,14,25],[1474,30,11,24,16,25],
    [1588,30,7,24,22,25],[1706,28,28,22,6,23],[1828,30,8,23,26,24],[1921,30,4,24,31,25],
    [2051,30,1,23,37,24],[2185,30,15,24,25,25],[2323,30,42,24,1,25],[2465,30,10,24,35,25],
    [2611,30,29,24,19,25],[2761,30,44,24,7,25],[2876,30,39,24,14,25],[3034,30,46,24,10,25],
    [3196,30,49,24,10,25],[3362,30,48,24,14,25],[3532,30,43,24,22,25],[3706,30,34,24,34,25],
  ],
  H: [
    [26,17,1,9,0,0],[44,28,1,16,0,0],[70,22,2,13,0,0],[100,16,4,9,0,0],
    [134,22,2,11,2,12],[172,28,4,15,0,0],[196,26,4,13,1,14],[242,26,4,14,2,15],
    [292,24,4,12,4,13],[346,28,6,15,2,16],[404,24,3,12,8,13],[466,28,7,14,4,15],
    [532,22,12,11,4,12],[581,24,11,12,5,13],[655,24,11,12,7,13],[733,30,3,15,13,16],
    [815,28,2,14,17,15],[901,28,2,14,19,15],[991,26,9,13,16,14],[1085,28,15,15,10,16],
    [1156,30,19,16,6,17],[1258,24,34,13,0,0],[1364,30,16,15,14,16],[1474,30,30,16,2,17],
    [1588,30,22,15,13,16],[1706,30,33,16,4,17],[1828,30,12,15,28,16],[1921,30,11,15,31,16],
    [2051,30,19,15,26,16],[2185,30,23,15,25,16],[2323,30,23,15,28,16],[2465,30,19,15,35,16],
    [2611,30,11,15,46,16],[2761,30,59,16,1,17],[2876,30,22,15,41,16],[3034,30,2,15,64,16],
    [3196,30,24,15,46,16],[3362,30,42,15,32,16],[3532,30,10,15,67,16],[3706,30,20,15,61,16],
  ],
};

const ALIGNMENT_POSITIONS = [
  [],[], [6,18], [6,22], [6,26], [6,30], [6,34],
  [6,22,38], [6,24,42], [6,26,46], [6,28,50], [6,30,54], [6,32,58], [6,34,62],
  [6,26,46,66], [6,26,48,70], [6,26,50,74], [6,30,54,78], [6,30,56,82], [6,30,58,86], [6,34,62,90],
  [6,28,50,72,94], [6,26,50,74,98], [6,30,54,78,102], [6,28,54,80,106], [6,32,58,84,110], [6,30,58,86,114], [6,34,62,90,118],
  [6,26,50,74,98,122], [6,30,54,78,102,126], [6,26,52,78,104,130], [6,30,56,82,108,134], [6,34,60,86,112,138], [6,30,58,86,114,142], [6,34,62,90,118,146],
  [6,30,54,78,102,126,150], [6,24,50,76,102,128,154], [6,28,54,80,106,132,158], [6,32,58,84,110,136,162], [6,26,54,82,110,138,166], [6,30,58,86,114,142,170],
];

// GF(256) arithmetic for Reed-Solomon
const GF_EXP = new Uint8Array(512);
const GF_LOG = new Uint8Array(256);
{
  let x = 1;
  for (let i = 0; i < 255; i++) {
    GF_EXP[i] = x;
    GF_LOG[x] = i;
    x = (x << 1) ^ (x >= 128 ? 0x11d : 0);
  }
  for (let i = 255; i < 512; i++) GF_EXP[i] = GF_EXP[i - 255];
}

function gfMul(a, b) {
  if (a === 0 || b === 0) return 0;
  return GF_EXP[GF_LOG[a] + GF_LOG[b]];
}

function rsGenPoly(nsym) {
  let g = [1];
  for (let i = 0; i < nsym; i++) {
    const ng = new Array(g.length + 1).fill(0);
    for (let j = 0; j < g.length; j++) {
      ng[j] ^= g[j];
      ng[j + 1] ^= gfMul(g[j], GF_EXP[i]);
    }
    g = ng;
  }
  return g;
}

function rsEncode(data, nsym) {
  const gen = rsGenPoly(nsym);
  const res = new Uint8Array(data.length + nsym);
  res.set(data);
  for (let i = 0; i < data.length; i++) {
    const coef = res[i];
    if (coef !== 0) {
      for (let j = 0; j < gen.length; j++) {
        res[i + j] ^= gfMul(gen[j], coef);
      }
    }
  }
  return res.slice(data.length);
}

function getVersion(dataLen, ecLevel) {
  const ecKey = ['M','L','H','Q'][ecLevel];
  const table = EC_TABLE[ecKey];
  for (let v = 0; v < 40; v++) {
    const [total, ecCWPerBlock, g1Blocks, g1Data, g2Blocks, g2Data] = table[v];
    const capacity = g1Blocks * g1Data + g2Blocks * g2Data;
    if (dataLen <= capacity) return v + 1;
  }
  return -1;
}

function getCharCountBits(version) {
  if (version <= 9) return 8;
  if (version <= 26) return 16;
  return 16;
}

function encodeData(text, ecLevel) {
  const data = new TextEncoder().encode(text);
  const version = getVersion(data.length + 3, ecLevel); // rough estimate
  if (version < 0) throw new Error('Text too long for QR code');

  const ecKey = ['M','L','H','Q'][ecLevel];
  const [total, ecCWPerBlock, g1Blocks, g1Data, g2Blocks, g2Data] = EC_TABLE[ecKey][version - 1];
  const totalDataCW = g1Blocks * g1Data + g2Blocks * g2Data;

  // Build bit stream
  const bits = [];
  function pushBits(val, len) {
    for (let i = len - 1; i >= 0; i--) bits.push((val >> i) & 1);
  }

  pushBits(MODE_BYTE, 4);
  pushBits(data.length, getCharCountBits(version));
  for (const b of data) pushBits(b, 8);

  // Terminator
  const remaining = totalDataCW * 8 - bits.length;
  pushBits(0, Math.min(4, remaining));

  // Pad to byte boundary
  while (bits.length % 8 !== 0) bits.push(0);

  // Pad bytes
  const padBytes = [0xEC, 0x11];
  let padIdx = 0;
  while (bits.length < totalDataCW * 8) {
    pushBits(padBytes[padIdx % 2], 8);
    padIdx++;
  }

  // Convert to bytes
  const dataBytes = new Uint8Array(totalDataCW);
  for (let i = 0; i < totalDataCW; i++) {
    let byte = 0;
    for (let j = 0; j < 8; j++) byte = (byte << 1) | bits[i * 8 + j];
    dataBytes[i] = byte;
  }

  // Split into blocks and compute EC
  const blocks = [];
  const ecBlocks = [];
  let offset = 0;

  for (let i = 0; i < g1Blocks; i++) {
    const block = dataBytes.slice(offset, offset + g1Data);
    blocks.push(block);
    ecBlocks.push(rsEncode(block, ecCWPerBlock));
    offset += g1Data;
  }
  for (let i = 0; i < g2Blocks; i++) {
    const block = dataBytes.slice(offset, offset + g2Data);
    blocks.push(block);
    ecBlocks.push(rsEncode(block, ecCWPerBlock));
    offset += g2Data;
  }

  // Interleave data blocks
  const interleaved = [];
  const maxDataLen = Math.max(g1Data, g2Data || 0);
  for (let i = 0; i < maxDataLen; i++) {
    for (const block of blocks) {
      if (i < block.length) interleaved.push(block[i]);
    }
  }
  // Interleave EC blocks
  for (let i = 0; i < ecCWPerBlock; i++) {
    for (const block of ecBlocks) {
      if (i < block.length) interleaved.push(block[i]);
    }
  }

  return { version, data: new Uint8Array(interleaved) };
}

function createMatrix(version) {
  const size = version * 4 + 17;
  const matrix = Array.from({ length: size }, () => new Int8Array(size)); // 0=unset, 1=black, -1=white
  const reserved = Array.from({ length: size }, () => new Uint8Array(size)); // 1=reserved

  function setModule(row, col, val) {
    matrix[row][col] = val ? 1 : -1;
    reserved[row][col] = 1;
  }

  // Finder patterns
  function drawFinder(row, col) {
    for (let r = -1; r <= 7; r++) {
      for (let c = -1; c <= 7; c++) {
        const rr = row + r, cc = col + c;
        if (rr < 0 || rr >= size || cc < 0 || cc >= size) continue;
        const inOuter = r === 0 || r === 6 || c === 0 || c === 6;
        const inInner = r >= 2 && r <= 4 && c >= 2 && c <= 4;
        const inBorder = r === -1 || r === 7 || c === -1 || c === 7;
        setModule(rr, cc, !inBorder && (inOuter || inInner));
      }
    }
  }

  drawFinder(0, 0);
  drawFinder(0, size - 7);
  drawFinder(size - 7, 0);

  // Timing patterns
  for (let i = 8; i < size - 8; i++) {
    setModule(6, i, i % 2 === 0);
    setModule(i, 6, i % 2 === 0);
  }

  // Alignment patterns
  if (version >= 2) {
    const pos = ALIGNMENT_POSITIONS[version];
    for (const r of pos) {
      for (const c of pos) {
        if (reserved[r][c]) continue;
        for (let dr = -2; dr <= 2; dr++) {
          for (let dc = -2; dc <= 2; dc++) {
            const isBlack = Math.abs(dr) === 2 || Math.abs(dc) === 2 || (dr === 0 && dc === 0);
            setModule(r + dr, c + dc, isBlack);
          }
        }
      }
    }
  }

  // Dark module
  setModule(size - 8, 8, true);

  // Reserve format info areas
  for (let i = 0; i < 8; i++) {
    if (!reserved[8][i]) { reserved[8][i] = 1; matrix[8][i] = 0; }
    if (!reserved[8][size - 1 - i]) { reserved[8][size - 1 - i] = 1; matrix[8][size - 1 - i] = 0; }
    if (!reserved[i][8]) { reserved[i][8] = 1; matrix[i][8] = 0; }
    if (!reserved[size - 1 - i][8]) { reserved[size - 1 - i][8] = 1; matrix[size - 1 - i][8] = 0; }
  }
  if (!reserved[8][8]) { reserved[8][8] = 1; matrix[8][8] = 0; }

  // Reserve version info areas (version >= 7)
  if (version >= 7) {
    for (let i = 0; i < 6; i++) {
      for (let j = 0; j < 3; j++) {
        reserved[i][size - 11 + j] = 1;
        reserved[size - 11 + j][i] = 1;
      }
    }
  }

  return { matrix, reserved, size };
}

function placeData(matrix, reserved, size, data) {
  const bits = [];
  for (const byte of data) {
    for (let i = 7; i >= 0; i--) bits.push((byte >> i) & 1);
  }

  let bitIdx = 0;
  let upward = true;

  for (let right = size - 1; right >= 1; right -= 2) {
    if (right === 6) right = 5; // skip timing column

    const rows = upward
      ? Array.from({ length: size }, (_, i) => size - 1 - i)
      : Array.from({ length: size }, (_, i) => i);

    for (const row of rows) {
      for (const col of [right, right - 1]) {
        if (!reserved[row][col]) {
          if (bitIdx < bits.length) {
            matrix[row][col] = bits[bitIdx] ? 1 : -1;
          } else {
            matrix[row][col] = -1;
          }
          bitIdx++;
        }
      }
    }
    upward = !upward;
  }
}

const FORMAT_INFO_STRINGS = [
  0x77c4, 0x72f3, 0x7daa, 0x789d, 0x662f, 0x6318, 0x6c41, 0x6976,
  0x5412, 0x5125, 0x5e7c, 0x5b4b, 0x45f9, 0x40ce, 0x4f97, 0x4aa0,
  0x355f, 0x3068, 0x3f31, 0x3a06, 0x24b4, 0x2183, 0x2eda, 0x2bed,
  0x1689, 0x13be, 0x1ce7, 0x19d0, 0x0762, 0x0255, 0x0d0c, 0x083b,
];

function getFormatInfo(ecLevel, maskPattern) {
  const idx = (ecLevel << 3) | maskPattern;
  return FORMAT_INFO_STRINGS[idx];
}

const VERSION_INFO = [
  0,0,0,0,0,0,0,
  0x07C94, 0x085BC, 0x09A99, 0x0A4D3, 0x0BBF6, 0x0C762, 0x0D847, 0x0E60D,
  0x0F928, 0x10B78, 0x1145D, 0x12A17, 0x13532, 0x149A6, 0x15683, 0x168C9,
  0x177EC, 0x18EC4, 0x191E1, 0x1AFAB, 0x1B08E, 0x1CC1A, 0x1D33F, 0x1ED75,
  0x1F250, 0x209D5, 0x216F0, 0x228BA, 0x2379F, 0x24B0B, 0x2542E, 0x26A64,
  0x27541, 0x28C69,
];

function applyFormatInfo(matrix, size, ecLevel, maskPattern) {
  const info = getFormatInfo(ecLevel, maskPattern);

  for (let i = 0; i < 15; i++) {
    const bit = ((info >> i) & 1) ? 1 : -1;

    // Around top-left finder
    if (i < 6) matrix[8][i] = bit;
    else if (i === 6) matrix[8][7] = bit;
    else if (i === 7) matrix[8][8] = bit;
    else if (i === 8) matrix[7][8] = bit;
    else matrix[14 - i][8] = bit;

    // Other copy
    if (i < 8) matrix[size - 1 - i][8] = bit;
    else matrix[8][size - 15 + i] = bit;
  }
}

function applyVersionInfo(matrix, size, version) {
  if (version < 7) return;
  const info = VERSION_INFO[version];
  for (let i = 0; i < 18; i++) {
    const bit = ((info >> i) & 1) ? 1 : -1;
    const row = Math.floor(i / 3);
    const col = size - 11 + (i % 3);
    matrix[row][col] = bit;
    matrix[col][row] = bit;
  }
}

const MASK_FUNCTIONS = [
  (r, c) => (r + c) % 2 === 0,
  (r, c) => r % 2 === 0,
  (r, c) => c % 3 === 0,
  (r, c) => (r + c) % 3 === 0,
  (r, c) => (Math.floor(r / 2) + Math.floor(c / 3)) % 2 === 0,
  (r, c) => ((r * c) % 2 + (r * c) % 3) === 0,
  (r, c) => ((r * c) % 2 + (r * c) % 3) % 2 === 0,
  (r, c) => ((r + c) % 2 + (r * c) % 3) % 2 === 0,
];

function applyMask(matrix, reserved, size, maskIdx) {
  const fn = MASK_FUNCTIONS[maskIdx];
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      if (!reserved[r][c] && fn(r, c)) {
        matrix[r][c] = matrix[r][c] === 1 ? -1 : 1;
      }
    }
  }
}

function scorePenalty(matrix, size) {
  let penalty = 0;

  // Rule 1: runs of same color
  for (let r = 0; r < size; r++) {
    let count = 1;
    for (let c = 1; c < size; c++) {
      if (matrix[r][c] === matrix[r][c - 1]) { count++; }
      else { if (count >= 5) penalty += count - 2; count = 1; }
    }
    if (count >= 5) penalty += count - 2;
  }
  for (let c = 0; c < size; c++) {
    let count = 1;
    for (let r = 1; r < size; r++) {
      if (matrix[r][c] === matrix[r - 1][c]) { count++; }
      else { if (count >= 5) penalty += count - 2; count = 1; }
    }
    if (count >= 5) penalty += count - 2;
  }

  // Rule 2: 2x2 blocks
  for (let r = 0; r < size - 1; r++) {
    for (let c = 0; c < size - 1; c++) {
      const v = matrix[r][c];
      if (v === matrix[r][c + 1] && v === matrix[r + 1][c] && v === matrix[r + 1][c + 1]) {
        penalty += 3;
      }
    }
  }

  // Rule 3: finder-like patterns (simplified)
  // Rule 4: proportion
  let dark = 0;
  for (let r = 0; r < size; r++) for (let c = 0; c < size; c++) if (matrix[r][c] === 1) dark++;
  const pct = (dark * 100) / (size * size);
  penalty += Math.abs(Math.round(pct / 5) * 5 - 50) * 2;

  return penalty;
}

function generateQR(text, ecLevel) {
  const { version, data } = encodeData(text, ecLevel);
  const { matrix: baseMatrix, reserved, size } = createMatrix(version);

  placeData(baseMatrix, reserved, size, data);

  let bestMask = 0;
  let bestPenalty = Infinity;
  let bestMatrix = null;

  for (let m = 0; m < 8; m++) {
    // Deep copy matrix
    const mat = baseMatrix.map(row => Int8Array.from(row));
    applyMask(mat, reserved, size, m);
    applyFormatInfo(mat, size, ecLevel, m);
    applyVersionInfo(mat, size, version);

    const penalty = scorePenalty(mat, size);
    if (penalty < bestPenalty) {
      bestPenalty = penalty;
      bestMask = m;
      bestMatrix = mat;
    }
  }

  return { matrix: bestMatrix, size };
}

// --------------- PNG Encoder (minimal, uncompressed) ---------------

function crc32(buf) {
  let crc = 0xFFFFFFFF;
  for (let i = 0; i < buf.length; i++) {
    crc ^= buf[i];
    for (let j = 0; j < 8; j++) crc = (crc >>> 1) ^ (crc & 1 ? 0xEDB88320 : 0);
  }
  return (crc ^ 0xFFFFFFFF) >>> 0;
}

function adler32(buf) {
  let a = 1, b = 0;
  for (let i = 0; i < buf.length; i++) {
    a = (a + buf[i]) % 65521;
    b = (b + a) % 65521;
  }
  return ((b << 16) | a) >>> 0;
}

function createDeflateStored(data) {
  // Store blocks (max 65535 bytes each)
  const blocks = [];
  let offset = 0;
  while (offset < data.length) {
    const isLast = offset + 65535 >= data.length;
    const len = Math.min(65535, data.length - offset);
    const block = new Uint8Array(5 + len);
    block[0] = isLast ? 1 : 0;
    block[1] = len & 0xFF;
    block[2] = (len >> 8) & 0xFF;
    block[3] = ~len & 0xFF;
    block[4] = (~len >> 8) & 0xFF;
    block.set(data.subarray(offset, offset + len), 5);
    blocks.push(block);
    offset += len;
  }

  const totalLen = blocks.reduce((s, b) => s + b.length, 0);
  const result = new Uint8Array(2 + totalLen + 4); // zlib header + data + adler32
  result[0] = 0x78; // CMF
  result[1] = 0x01; // FLG
  let pos = 2;
  for (const block of blocks) {
    result.set(block, pos);
    pos += block.length;
  }
  const adl = adler32(data);
  result[pos] = (adl >> 24) & 0xFF;
  result[pos + 1] = (adl >> 16) & 0xFF;
  result[pos + 2] = (adl >> 8) & 0xFF;
  result[pos + 3] = adl & 0xFF;
  return result;
}

function encodePNG(qrMatrix, qrSize, pixelSize, fgColor, bgColor) {
  const imgSize = qrSize * pixelSize + 8 * pixelSize; // 4 module quiet zone on each side
  const totalSize = imgSize;

  // Build raw image data (filter byte + RGB per pixel per row)
  const rawData = new Uint8Array(totalSize * (1 + totalSize * 3));
  let idx = 0;

  const fg = [
    parseInt(fgColor.substring(0, 2), 16),
    parseInt(fgColor.substring(2, 4), 16),
    parseInt(fgColor.substring(4, 6), 16),
  ];
  const bg = [
    parseInt(bgColor.substring(0, 2), 16),
    parseInt(bgColor.substring(2, 4), 16),
    parseInt(bgColor.substring(4, 6), 16),
  ];

  for (let y = 0; y < totalSize; y++) {
    rawData[idx++] = 0; // filter: none
    const moduleY = Math.floor(y / pixelSize) - 4;
    for (let x = 0; x < totalSize; x++) {
      const moduleX = Math.floor(x / pixelSize) - 4;
      let color = bg;
      if (moduleY >= 0 && moduleY < qrSize && moduleX >= 0 && moduleX < qrSize) {
        if (qrMatrix[moduleY][moduleX] === 1) color = fg;
      }
      rawData[idx++] = color[0];
      rawData[idx++] = color[1];
      rawData[idx++] = color[2];
    }
  }

  const compressed = createDeflateStored(rawData);

  // Build PNG
  const pngParts = [];

  // Signature
  pngParts.push(new Uint8Array([137, 80, 78, 71, 13, 10, 26, 10]));

  function writeChunk(type, data) {
    const len = new Uint8Array(4);
    new DataView(len.buffer).setUint32(0, data.length);
    const typeBytes = new TextEncoder().encode(type);
    const crcData = new Uint8Array(4 + data.length);
    crcData.set(typeBytes);
    crcData.set(data, 4);
    const crcVal = crc32(crcData);
    const crcBytes = new Uint8Array(4);
    new DataView(crcBytes.buffer).setUint32(0, crcVal);
    pngParts.push(len, typeBytes, data, crcBytes);
  }

  // IHDR
  const ihdr = new Uint8Array(13);
  const ihdrView = new DataView(ihdr.buffer);
  ihdrView.setUint32(0, totalSize);
  ihdrView.setUint32(4, totalSize);
  ihdr[8] = 8;  // bit depth
  ihdr[9] = 2;  // color type: RGB
  ihdr[10] = 0; // compression
  ihdr[11] = 0; // filter
  ihdr[12] = 0; // interlace
  writeChunk('IHDR', ihdr);

  // IDAT
  writeChunk('IDAT', compressed);

  // IEND
  writeChunk('IEND', new Uint8Array(0));

  // Concat
  const totalLen = pngParts.reduce((s, p) => s + p.length, 0);
  const png = new Uint8Array(totalLen);
  let offset = 0;
  for (const part of pngParts) {
    png.set(part, offset);
    offset += part.length;
  }
  return png;
}

// --------------- SVG Generator ---------------

function generateSVG(qrMatrix, qrSize, pixelSize, fgColor, bgColor) {
  const quiet = 4;
  const totalModules = qrSize + quiet * 2;
  const totalSize = totalModules * pixelSize;

  let svg = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  svg += `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${totalModules} ${totalModules}" width="${totalSize}" height="${totalSize}" shape-rendering="crispEdges">\n`;
  svg += `<rect width="${totalModules}" height="${totalModules}" fill="#${bgColor}"/>\n`;

  for (let r = 0; r < qrSize; r++) {
    for (let c = 0; c < qrSize; c++) {
      if (qrMatrix[r][c] === 1) {
        svg += `<rect x="${c + quiet}" y="${r + quiet}" width="1" height="1" fill="#${fgColor}"/>\n`;
      }
    }
  }

  svg += `</svg>`;
  return svg;
}

// --------------- Rate Limiter (in-memory, per-worker-instance) ---------------

const rateLimitMap = new Map();
const WINDOW_MS = 60000;

function checkRateLimit(ip, limit) {
  const now = Date.now();
  let entry = rateLimitMap.get(ip);
  if (!entry || now - entry.start >= WINDOW_MS) {
    entry = { start: now, count: 0 };
    rateLimitMap.set(ip, entry);
  }
  entry.count++;

  // Cleanup old entries periodically
  if (rateLimitMap.size > 10000) {
    for (const [key, val] of rateLimitMap) {
      if (now - val.start >= WINDOW_MS) rateLimitMap.delete(key);
    }
  }

  return {
    remaining: Math.max(0, limit - entry.count),
    reset: Math.ceil((entry.start + WINDOW_MS - now) / 1000),
    exceeded: entry.count > limit,
  };
}

// --------------- Request Handler ---------------

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

function errorResponse(status, message) {
  return new Response(
    JSON.stringify({ error: message, status }),
    {
      status,
      headers: { 'Content-Type': 'application/json', ...corsHeaders() },
    }
  );
}

export default {
  async fetch(request, env) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (request.method !== 'GET') {
      return errorResponse(405, 'Method not allowed');
    }

    const url = new URL(request.url);

    // Root: API info
    if (url.pathname === '/' || url.pathname === '') {
      return new Response(
        JSON.stringify({
          name: 'QR Code Generator API',
          version: '1.0.0',
          endpoints: {
            generate: '/generate?text=hello&size=300&format=png',
          },
          parameters: {
            text: 'Required. The text/URL to encode.',
            size: 'Image size in pixels (default: 300, max: 1000). For PNG/base64 only.',
            format: 'Output format: png, svg, base64 (default: png)',
            color: 'Foreground color hex without # (default: 000000)',
            bgcolor: 'Background color hex without # (default: ffffff)',
            error_correction: 'Error correction level: L, M, Q, H (default: M)',
          },
        }),
        {
          headers: { 'Content-Type': 'application/json', ...corsHeaders() },
        }
      );
    }

    if (url.pathname !== '/generate') {
      return errorResponse(404, 'Not found. Use /generate endpoint.');
    }

    // Rate limiting
    const ip = request.headers.get('CF-Connecting-IP') || request.headers.get('X-Forwarded-For') || 'unknown';
    const rateLimit = parseInt(env.RATE_LIMIT_PER_MINUTE || '60');
    const rl = checkRateLimit(ip, rateLimit);

    const rlHeaders = {
      'X-RateLimit-Limit': String(rateLimit),
      'X-RateLimit-Remaining': String(rl.remaining),
      'X-RateLimit-Reset': String(rl.reset),
    };

    if (rl.exceeded) {
      return new Response(
        JSON.stringify({ error: 'Rate limit exceeded. Try again later.', status: 429 }),
        { status: 429, headers: { 'Content-Type': 'application/json', 'Retry-After': String(rl.reset), ...rlHeaders, ...corsHeaders() } }
      );
    }

    // Parse parameters
    const text = url.searchParams.get('text');
    if (!text) {
      return errorResponse(400, 'Missing required parameter: text');
    }
    if (text.length > 4296) {
      return errorResponse(400, 'Text too long. Maximum 4296 characters.');
    }

    const maxSize = parseInt(env.MAX_QR_SIZE || '1000');
    const defaultSize = parseInt(env.DEFAULT_QR_SIZE || '300');
    let size = parseInt(url.searchParams.get('size') || String(defaultSize));
    if (isNaN(size) || size < 10 || size > maxSize) {
      return errorResponse(400, `Invalid size. Must be between 10 and ${maxSize}.`);
    }

    const format = (url.searchParams.get('format') || 'png').toLowerCase();
    if (!['png', 'svg', 'base64'].includes(format)) {
      return errorResponse(400, 'Invalid format. Must be png, svg, or base64.');
    }

    const color = (url.searchParams.get('color') || '000000').replace('#', '');
    const bgcolor = (url.searchParams.get('bgcolor') || 'ffffff').replace('#', '');
    if (!/^[0-9a-fA-F]{6}$/.test(color) || !/^[0-9a-fA-F]{6}$/.test(bgcolor)) {
      return errorResponse(400, 'Invalid color. Use 6-digit hex (e.g., ff0000).');
    }

    const ecParam = (url.searchParams.get('error_correction') || 'M').toUpperCase();
    if (!['L', 'M', 'Q', 'H'].includes(ecParam)) {
      return errorResponse(400, 'Invalid error_correction. Must be L, M, Q, or H.');
    }
    const ecLevel = ECL[ecParam];

    // Generate QR code
    let qr;
    try {
      qr = generateQR(text, ecLevel);
    } catch (e) {
      return errorResponse(400, e.message || 'Failed to generate QR code.');
    }

    const headers = { ...rlHeaders, ...corsHeaders(), 'Cache-Control': 'public, max-age=86400' };

    if (format === 'svg') {
      const svg = generateSVG(qr.matrix, qr.size, Math.max(1, Math.round(size / (qr.size + 8))), color, bgcolor);
      return new Response(svg, {
        headers: { ...headers, 'Content-Type': 'image/svg+xml' },
      });
    }

    const pixelSize = Math.max(1, Math.round(size / (qr.size + 8)));
    const pngData = encodePNG(qr.matrix, qr.size, pixelSize, color, bgcolor);

    if (format === 'base64') {
      // Convert to base64
      let binary = '';
      for (let i = 0; i < pngData.length; i++) binary += String.fromCharCode(pngData[i]);
      const base64 = btoa(binary);
      return new Response(
        JSON.stringify({
          data: base64,
          data_uri: `data:image/png;base64,${base64}`,
          mime_type: 'image/png',
          size: pngData.length,
        }),
        {
          headers: { ...headers, 'Content-Type': 'application/json' },
        }
      );
    }

    // PNG
    return new Response(pngData, {
      headers: { ...headers, 'Content-Type': 'image/png' },
    });
  },
};
