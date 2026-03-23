/**
 * PDF Generator API — Cloudflare Worker
 * Pure JS PDF generation (no Puppeteer dependency)
 * Builds PDF binary structure directly from HTML/Markdown/URL input
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-RapidAPI-Key, X-RapidAPI-Host',
};

// ─── PDF Builder ───────────────────────────────────────────

class PDFBuilder {
  constructor(options = {}) {
    this.pageWidth = options.pageWidth || 595.28;   // A4 points
    this.pageHeight = options.pageHeight || 841.89;
    this.marginTop = options.marginTop || 72;
    this.marginBottom = options.marginBottom || 72;
    this.marginLeft = options.marginLeft || 72;
    this.marginRight = options.marginRight || 72;
    this.fontSize = options.fontSize || 12;
    this.lineHeight = options.lineHeight || 1.4;
    this.headerText = options.header || '';
    this.footerText = options.footer || '';
    this.objects = [];
    this.pages = [];
  }

  /**
   * Convert plain text lines into multi-page PDF
   */
  buildFromLines(lines) {
    const usableWidth = this.pageWidth - this.marginLeft - this.marginRight;
    const usableHeight = this.pageHeight - this.marginTop - this.marginBottom;
    const leading = this.fontSize * this.lineHeight;
    const charsPerLine = Math.floor(usableWidth / (this.fontSize * 0.5));

    // Word-wrap lines
    const wrapped = [];
    for (const raw of lines) {
      if (raw.trim() === '') { wrapped.push(''); continue; }
      let remaining = raw;
      while (remaining.length > charsPerLine) {
        let cut = remaining.lastIndexOf(' ', charsPerLine);
        if (cut <= 0) cut = charsPerLine;
        wrapped.push(remaining.slice(0, cut));
        remaining = remaining.slice(cut).trimStart();
      }
      wrapped.push(remaining);
    }

    // Paginate
    const linesPerPage = Math.floor(usableHeight / leading);
    const pageChunks = [];
    for (let i = 0; i < wrapped.length; i += linesPerPage) {
      pageChunks.push(wrapped.slice(i, i + linesPerPage));
    }
    if (pageChunks.length === 0) pageChunks.push(['']);

    // Build PDF objects
    const offsets = [];
    let body = '';
    let objNum = 0;

    const addObj = (content) => {
      objNum++;
      offsets.push(body.length);
      body += `${objNum} 0 obj\n${content}\nendobj\n`;
      return objNum;
    };

    // 1 — Catalog
    const catalogId = addObj('<< /Type /Catalog /Pages 2 0 R >>');

    // 2 — Pages (placeholder, patched later)
    const pagesId = addObj('PAGES_PLACEHOLDER');

    // 3 — Font
    const fontId = addObj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>');

    // Build each page
    const pageIds = [];
    for (let p = 0; p < pageChunks.length; p++) {
      const chunk = pageChunks[p];
      let stream = '';

      // Header
      if (this.headerText) {
        stream += `BT /F1 9 Tf ${this.marginLeft} ${this.pageHeight - 36} Td (${pdfEscape(this.headerText)}) Tj ET\n`;
      }
      // Footer
      if (this.footerText) {
        const footerFinal = this.footerText.replace('{{page}}', String(p + 1)).replace('{{pages}}', String(pageChunks.length));
        stream += `BT /F1 9 Tf ${this.marginLeft} 30 Td (${pdfEscape(footerFinal)}) Tj ET\n`;
      }

      // Body text
      let y = this.pageHeight - this.marginTop;
      for (const line of chunk) {
        stream += `BT /F1 ${this.fontSize} Tf ${this.marginLeft} ${y.toFixed(2)} Td (${pdfEscape(line)}) Tj ET\n`;
        y -= leading;
      }

      const streamId = addObj(`<< /Length ${stream.length} >>\nstream\n${stream}endstream`);

      const pageId = addObj(
        `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${this.pageWidth} ${this.pageHeight}] ` +
        `/Contents ${streamId} 0 R /Resources << /Font << /F1 ${fontId} 0 R >> >> >>`
      );
      pageIds.push(pageId);
    }

    // Patch pages object
    const kidsStr = pageIds.map(id => `${id} 0 R`).join(' ');
    const pagesContent = `<< /Type /Pages /Kids [${kidsStr}] /Count ${pageIds.length} >>`;
    body = body.replace('PAGES_PLACEHOLDER', pagesContent);

    // Rebuild offsets after patch (simple recalc)
    const recalcOffsets = [];
    let searchFrom = 0;
    for (let i = 1; i <= objNum; i++) {
      const idx = body.indexOf(`${i} 0 obj\n`, searchFrom);
      recalcOffsets.push(idx);
      searchFrom = idx + 1;
    }

    // Cross-reference table
    const xrefOffset = body.length;
    let xref = `xref\n0 ${objNum + 1}\n0000000000 65535 f \n`;
    for (const off of recalcOffsets) {
      xref += `${String(off).padStart(10, '0')} 00000 n \n`;
    }
    xref += `trailer\n<< /Size ${objNum + 1} /Root ${catalogId} 0 R >>\nstartxref\n${xrefOffset}\n%%EOF\n`;

    return '%PDF-1.4\n' + body + xref;
  }
}

function pdfEscape(str) {
  return str.replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)');
}

// ─── HTML / Markdown to plain text ─────────────────────────

function stripHtml(html) {
  let text = html;
  // Block elements → newlines
  text = text.replace(/<br\s*\/?>/gi, '\n');
  text = text.replace(/<\/(p|div|h[1-6]|li|tr|blockquote)>/gi, '\n');
  text = text.replace(/<(hr)\s*\/?>/gi, '\n---\n');
  // Headings: extract text, uppercase
  text = text.replace(/<h([1-6])[^>]*>(.*?)<\/h\1>/gi, (_, _l, c) => '\n' + stripTags(c).toUpperCase() + '\n');
  // Lists
  text = text.replace(/<li[^>]*>/gi, '  - ');
  // Strip remaining tags
  text = stripTags(text);
  // Decode common entities
  text = text.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ');
  return text;
}

function stripTags(str) {
  return str.replace(/<[^>]*>/g, '');
}

function markdownToText(md) {
  let text = md;
  // Headers
  text = text.replace(/^#{1,6}\s+(.+)$/gm, (_, t) => t.toUpperCase());
  // Bold / italic
  text = text.replace(/\*\*(.+?)\*\*/g, '$1');
  text = text.replace(/\*(.+?)\*/g, '$1');
  text = text.replace(/__(.+?)__/g, '$1');
  text = text.replace(/_(.+?)_/g, '$1');
  // Links
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');
  // Images
  text = text.replace(/!\[([^\]]*)\]\([^)]+\)/g, '[$1]');
  // Code blocks
  text = text.replace(/```[\s\S]*?```/g, (m) => m.replace(/```\w*\n?/g, ''));
  // Inline code
  text = text.replace(/`(.+?)`/g, '$1');
  // Horizontal rules
  text = text.replace(/^[-*_]{3,}$/gm, '---');
  // Blockquotes
  text = text.replace(/^>\s?/gm, '  | ');
  return text;
}

// ─── Request handlers ──────────────────────────────────────

function parsePageOptions(body) {
  const sizes = {
    A4: [595.28, 841.89],
    A3: [841.89, 1190.55],
    Letter: [612, 792],
    Legal: [612, 1008],
  };
  const size = sizes[(body.page_size || 'A4')] || sizes.A4;
  return {
    pageWidth: body.orientation === 'landscape' ? size[1] : size[0],
    pageHeight: body.orientation === 'landscape' ? size[0] : size[1],
    marginTop: body.margin_top ?? 72,
    marginBottom: body.margin_bottom ?? 72,
    marginLeft: body.margin_left ?? 72,
    marginRight: body.margin_right ?? 72,
    fontSize: body.font_size ?? 12,
    lineHeight: body.line_height ?? 1.4,
    header: body.header || '',
    footer: body.footer || '',
  };
}

async function handleGenerate(body) {
  if (!body.html) return jsonError(400, 'Missing required field: html');
  const text = stripHtml(body.html);
  const lines = text.split('\n');
  const builder = new PDFBuilder(parsePageOptions(body));
  const pdf = builder.buildFromLines(lines);
  return new Response(pdf, {
    headers: { ...CORS_HEADERS, 'Content-Type': 'application/pdf', 'Content-Disposition': `inline; filename="${body.filename || 'document.pdf'}"` },
  });
}

async function handleFromMarkdown(body) {
  if (!body.markdown) return jsonError(400, 'Missing required field: markdown');
  const text = markdownToText(body.markdown);
  const lines = text.split('\n');
  const builder = new PDFBuilder(parsePageOptions(body));
  const pdf = builder.buildFromLines(lines);
  return new Response(pdf, {
    headers: { ...CORS_HEADERS, 'Content-Type': 'application/pdf', 'Content-Disposition': `inline; filename="${body.filename || 'document.pdf'}"` },
  });
}

async function handleFromUrl(body) {
  if (!body.url) return jsonError(400, 'Missing required field: url');
  let html;
  try {
    const resp = await fetch(body.url, { headers: { 'User-Agent': 'PDFGeneratorAPI/1.0' } });
    if (!resp.ok) return jsonError(502, `Failed to fetch URL: HTTP ${resp.status}`);
    html = await resp.text();
  } catch (e) {
    return jsonError(502, `Failed to fetch URL: ${e.message}`);
  }
  const text = stripHtml(html);
  const lines = text.split('\n');
  const builder = new PDFBuilder(parsePageOptions(body));
  const pdf = builder.buildFromLines(lines);
  return new Response(pdf, {
    headers: { ...CORS_HEADERS, 'Content-Type': 'application/pdf', 'Content-Disposition': `inline; filename="${body.filename || 'document.pdf'}"` },
  });
}

// ─── Utilities ─────────────────────────────────────────────

function jsonError(status, message) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
  });
}

function jsonOk(data) {
  return new Response(JSON.stringify(data), {
    headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
  });
}

// ─── Router ────────────────────────────────────────────────

export default {
  async fetch(request) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // Health check
    if (path === '/' && request.method === 'GET') {
      return jsonOk({
        name: 'PDF Generator API',
        version: '1.0.0',
        status: 'operational',
        endpoints: ['POST /generate', 'POST /from-markdown', 'POST /from-url'],
      });
    }

    if (request.method !== 'POST') {
      return jsonError(405, 'Method not allowed. Use POST.');
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return jsonError(400, 'Invalid JSON body');
    }

    try {
      switch (path) {
        case '/generate':
          return await handleGenerate(body);
        case '/from-markdown':
          return await handleFromMarkdown(body);
        case '/from-url':
          return await handleFromUrl(body);
        default:
          return jsonError(404, `Unknown endpoint: ${path}`);
      }
    } catch (e) {
      return jsonError(500, `Internal error: ${e.message}`);
    }
  },
};
