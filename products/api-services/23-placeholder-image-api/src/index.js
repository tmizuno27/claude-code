const GRADIENTS = {
  blue: ['#667eea', '#764ba2'],
  sunset: ['#f093fb', '#f5576c'],
  ocean: ['#4facfe', '#00f2fe'],
  forest: ['#43e97b', '#38f9d7'],
  fire: ['#fa709a', '#fee140'],
  purple: ['#a18cd1', '#fbc2eb'],
  dark: ['#434343', '#000000'],
  sky: ['#89f7fe', '#66a6ff'],
  peach: ['#ffecd2', '#fcb69f'],
  mint: ['#a1c4fd', '#c2e9fb'],
};

const CATEGORIES = {
  avatar: { text: 'Avatar', bg: 'purple' },
  banner: { text: 'Banner', bg: 'sunset' },
  thumbnail: { text: 'Thumbnail', bg: 'ocean' },
  product: { text: 'Product', bg: 'mint' },
  hero: { text: 'Hero', bg: 'blue' },
  card: { text: 'Card', bg: 'forest' },
  icon: { text: 'Icon', bg: 'fire' },
  cover: { text: 'Cover', bg: 'sky' },
};

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-RapidAPI-Key',
};

function escapeXml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&apos;');
}

function buildSvg({ width, height, text, bg, color1, color2, textColor, fontSize, fontFamily, category }) {
  const gradientId = 'grad';
  let c1, c2;

  if (color1 && color2) {
    c1 = color1;
    c2 = color2;
  } else if (category && CATEGORIES[category]) {
    const g = GRADIENTS[CATEGORIES[category].bg];
    c1 = g[0];
    c2 = g[1];
    if (!text) text = CATEGORIES[category].text;
  } else if (bg && GRADIENTS[bg]) {
    c1 = GRADIENTS[bg][0];
    c2 = GRADIENTS[bg][1];
  } else if (bg === 'solid' && color1) {
    c1 = color1;
    c2 = color1;
  } else {
    c1 = GRADIENTS.blue[0];
    c2 = GRADIENTS.blue[1];
  }

  if (!text) text = `${width}x${height}`;
  const tc = textColor || '#ffffff';
  const fs = fontSize || Math.max(12, Math.min(72, Math.floor(Math.min(width, height) / 6)));
  const ff = fontFamily || 'Arial, Helvetica, sans-serif';
  const safeText = escapeXml(text);

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
  <defs>
    <linearGradient id="${gradientId}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:${c1};stop-opacity:1"/>
      <stop offset="100%" style="stop-color:${c2};stop-opacity:1"/>
    </linearGradient>
  </defs>
  <rect width="${width}" height="${height}" fill="url(#${gradientId})" rx="0" ry="0"/>
  <text x="50%" y="50%" dominant-baseline="central" text-anchor="middle" font-family="${ff}" font-size="${fs}" font-weight="600" fill="${tc}">${safeText}</text>
</svg>`;
}

async function svgToPng(svg, width, height) {
  // Cloudflare Workers don't have Canvas/sharp, so we return SVG wrapped as an
  // image data URI inside a minimal SVG that the browser renders as PNG-like.
  // For true raster PNG, we encode via a foreignObject approach that works in browsers.
  // In Workers environment, we provide the SVG with PNG content-type note.
  // Realistic approach: return SVG bytes with image/png content-type isn't valid,
  // so we use resvg-wasm or simply note the limitation.
  // Practical solution: encode a minimal valid PNG using the SVG colors.

  // Generate a simple single-color PNG programmatically (no dependencies).
  // This creates a valid minimal PNG with the gradient approximated as a solid color.
  return null; // Signal to use SVG fallback with note
}

function createPngFromSvg(svg) {
  // Return SVG with a wrapper that hints at PNG usage
  // In production, you'd use @resvg/resvg-wasm for true PNG conversion
  return null;
}

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    if (request.method !== 'GET') {
      return jsonResponse({ error: 'Method not allowed. Use GET.' }, 405);
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // Health check
    if (path === '/' || path === '/health') {
      return jsonResponse({
        service: 'Placeholder Image API',
        status: 'healthy',
        version: '1.0.0',
        endpoints: {
          image: '/image?width=300&height=200&text=Hello&bg=gradient_name&format=svg',
          gradients: '/gradients',
          categories: '/categories',
        },
      });
    }

    // List available gradients
    if (path === '/gradients') {
      return jsonResponse({
        gradients: Object.keys(GRADIENTS).map((name) => ({
          name,
          colors: GRADIENTS[name],
        })),
      });
    }

    // List available categories
    if (path === '/categories') {
      return jsonResponse({
        categories: Object.entries(CATEGORIES).map(([key, val]) => ({
          name: key,
          defaultText: val.text,
          gradient: val.bg,
        })),
      });
    }

    // Image generation
    if (path === '/image') {
      const params = url.searchParams;
      const width = Math.min(4000, Math.max(1, parseInt(params.get('width') || '400', 10)));
      const height = Math.min(4000, Math.max(1, parseInt(params.get('height') || '300', 10)));
      const text = params.get('text') || '';
      const bg = params.get('bg') || 'blue';
      const color1 = params.get('color1') || '';
      const color2 = params.get('color2') || '';
      const textColor = params.get('textColor') || '';
      const fontSize = params.get('fontSize') ? parseInt(params.get('fontSize'), 10) : 0;
      const fontFamily = params.get('fontFamily') || '';
      const category = params.get('category') || '';
      const format = (params.get('format') || 'svg').toLowerCase();

      if (isNaN(width) || isNaN(height) || width < 1 || height < 1) {
        return jsonResponse({ error: 'Invalid width or height. Must be positive integers (max 4000).' }, 400);
      }

      const svg = buildSvg({
        width,
        height,
        text,
        bg,
        color1: color1.startsWith('#') ? color1 : color1 ? `#${color1}` : '',
        color2: color2.startsWith('#') ? color2 : color2 ? `#${color2}` : '',
        textColor: textColor.startsWith('#') ? textColor : textColor ? `#${textColor}` : '',
        fontSize,
        fontFamily,
        category,
      });

      if (format === 'png') {
        // Return SVG with instruction header since true PNG rasterization
        // requires resvg-wasm (add as dependency for production)
        return new Response(svg, {
          status: 200,
          headers: {
            'Content-Type': 'image/svg+xml',
            'X-Note': 'PNG format requires resvg-wasm dependency. SVG returned as fallback. SVG is supported by all modern browsers.',
            'Cache-Control': 'public, max-age=86400',
            ...CORS_HEADERS,
          },
        });
      }

      return new Response(svg, {
        status: 200,
        headers: {
          'Content-Type': 'image/svg+xml',
          'Cache-Control': 'public, max-age=86400',
          ...CORS_HEADERS,
        },
      });
    }

    return jsonResponse({ error: 'Not found. Available endpoints: /image, /gradients, /categories' }, 404);
  },
};
