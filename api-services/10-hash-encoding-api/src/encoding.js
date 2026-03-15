// Encoding/Decoding utilities

const HTML_ENTITIES = {
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
};

const HTML_DECODE_MAP = {
  '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"', '&#39;': "'",
  '&apos;': "'", '&#x27;': "'", '&#x2F;': '/', '&nbsp;': ' '
};

export function encode(text, format) {
  switch (format) {
    case 'base64':
      return btoa(unescape(encodeURIComponent(text)));
    case 'url':
      return encodeURIComponent(text);
    case 'html':
      return text.replace(/[&<>"']/g, c => HTML_ENTITIES[c]);
    case 'hex':
      return Array.from(new TextEncoder().encode(text))
        .map(b => b.toString(16).padStart(2, '0'))
        .join('');
    default:
      throw new Error(`Unsupported format: ${format}. Supported: base64, url, html, hex`);
  }
}

export function decode(text, format) {
  switch (format) {
    case 'base64':
      return decodeURIComponent(escape(atob(text)));
    case 'url':
      return decodeURIComponent(text);
    case 'html':
      return text.replace(/&(?:amp|lt|gt|quot|apos|nbsp|#39|#x27|#x2F);/g,
        m => HTML_DECODE_MAP[m] || m);
    case 'hex': {
      const bytes = [];
      for (let i = 0; i < text.length; i += 2) {
        bytes.push(parseInt(text.substring(i, i + 2), 16));
      }
      return new TextDecoder().decode(new Uint8Array(bytes));
    }
    default:
      throw new Error(`Unsupported format: ${format}. Supported: base64, url, html, hex`);
  }
}
