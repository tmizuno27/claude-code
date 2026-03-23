/**
 * Markdown Converter API — Cloudflare Worker
 * Pure JS implementation (no external dependencies)
 * Supports: GFM tables, task lists, strikethrough, code block syntax highlighting classes, TOC generation
 */

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-RapidAPI-Proxy-Secret, X-RapidAPI-Key',
};

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...CORS_HEADERS },
  });
}

function errorResponse(message, status = 400) {
  return jsonResponse({ error: message }, status);
}

// ─── Markdown → HTML ───

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function parseInline(text) {
  // Images (before links)
  text = text.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1">');
  // Links
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  // Bold + italic
  text = text.replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>');
  text = text.replace(/___(.+?)___/g, '<strong><em>$1</em></strong>');
  // Bold
  text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/__(.+?)__/g, '<strong>$1</strong>');
  // Italic
  text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
  text = text.replace(/_(.+?)_/g, '<em>$1</em>');
  // Strikethrough (GFM)
  text = text.replace(/~~(.+?)~~/g, '<del>$1</del>');
  // Inline code
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');
  // Line break
  text = text.replace(/  $/gm, '<br>');
  return text;
}

function parseTable(lines) {
  if (lines.length < 2) return null;
  const parseRow = (line) =>
    line.replace(/^\|/, '').replace(/\|$/, '').split('|').map((c) => c.trim());

  const headers = parseRow(lines[0]);
  const sepLine = lines[1].trim();
  if (!/^\|?[\s:]*-+[\s:]*(\|[\s:]*-+[\s:]*)*\|?$/.test(sepLine)) return null;

  const aligns = parseRow(lines[1]).map((c) => {
    const left = c.startsWith(':');
    const right = c.endsWith(':');
    if (left && right) return 'center';
    if (right) return 'right';
    if (left) return 'left';
    return '';
  });

  let html = '<table>\n<thead>\n<tr>\n';
  headers.forEach((h, i) => {
    const align = aligns[i] ? ` style="text-align:${aligns[i]}"` : '';
    html += `<th${align}>${parseInline(h)}</th>\n`;
  });
  html += '</tr>\n</thead>\n<tbody>\n';

  for (let r = 2; r < lines.length; r++) {
    const cells = parseRow(lines[r]);
    html += '<tr>\n';
    cells.forEach((c, i) => {
      const align = aligns[i] ? ` style="text-align:${aligns[i]}"` : '';
      html += `<td${align}>${parseInline(c)}</td>\n`;
    });
    html += '</tr>\n';
  }
  html += '</tbody>\n</table>';
  return html;
}

function markdownToHtml(md) {
  const lines = md.replace(/\r\n/g, '\n').split('\n');
  const output = [];
  let i = 0;
  let inList = null; // 'ul' | 'ol' | null
  let listIndent = 0;

  function closeList() {
    if (inList) {
      output.push(`</${inList}>`);
      inList = null;
    }
  }

  while (i < lines.length) {
    const line = lines[i];

    // Fenced code block
    const fenceMatch = line.match(/^```(\w*)/);
    if (fenceMatch) {
      closeList();
      const lang = fenceMatch[1];
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].startsWith('```')) {
        codeLines.push(escapeHtml(lines[i]));
        i++;
      }
      i++; // skip closing ```
      const langClass = lang ? ` class="language-${lang}"` : '';
      output.push(`<pre><code${langClass}>${codeLines.join('\n')}</code></pre>`);
      continue;
    }

    // Table detection
    if (i + 1 < lines.length && /^\|/.test(line) && /^\|?[\s:]*-+/.test(lines[i + 1])) {
      closeList();
      const tableLines = [];
      while (i < lines.length && (lines[i].includes('|') || /^\s*$/.test(lines[i]))) {
        if (/^\s*$/.test(lines[i])) break;
        tableLines.push(lines[i]);
        i++;
      }
      const tableHtml = parseTable(tableLines);
      if (tableHtml) {
        output.push(tableHtml);
      }
      continue;
    }

    // Heading
    const headingMatch = line.match(/^(#{1,6})\s+(.+)/);
    if (headingMatch) {
      closeList();
      const level = headingMatch[1].length;
      const text = headingMatch[2].replace(/\s+#+\s*$/, '');
      const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
      output.push(`<h${level} id="${id}">${parseInline(text)}</h${level}>`);
      i++;
      continue;
    }

    // Horizontal rule
    if (/^(\*{3,}|-{3,}|_{3,})\s*$/.test(line)) {
      closeList();
      output.push('<hr>');
      i++;
      continue;
    }

    // Blockquote
    if (line.startsWith('> ')) {
      closeList();
      const quoteLines = [];
      while (i < lines.length && lines[i].startsWith('> ')) {
        quoteLines.push(lines[i].slice(2));
        i++;
      }
      output.push(`<blockquote>${parseInline(quoteLines.join('\n'))}</blockquote>`);
      continue;
    }

    // Task list (GFM)
    const taskMatch = line.match(/^(\s*)[-*+]\s+\[([ xX])\]\s+(.*)/);
    if (taskMatch) {
      if (inList !== 'ul') {
        closeList();
        inList = 'ul';
        output.push('<ul class="task-list">');
      }
      const checked = taskMatch[2] !== ' ' ? ' checked' : '';
      output.push(`<li class="task-list-item"><input type="checkbox" disabled${checked}> ${parseInline(taskMatch[3])}</li>`);
      i++;
      continue;
    }

    // Unordered list
    const ulMatch = line.match(/^(\s*)[-*+]\s+(.*)/);
    if (ulMatch) {
      if (inList !== 'ul') {
        closeList();
        inList = 'ul';
        output.push('<ul>');
      }
      output.push(`<li>${parseInline(ulMatch[2])}</li>`);
      i++;
      continue;
    }

    // Ordered list
    const olMatch = line.match(/^(\s*)\d+\.\s+(.*)/);
    if (olMatch) {
      if (inList !== 'ol') {
        closeList();
        inList = 'ol';
        output.push('<ol>');
      }
      output.push(`<li>${parseInline(olMatch[2])}</li>`);
      i++;
      continue;
    }

    // Empty line
    if (/^\s*$/.test(line)) {
      closeList();
      i++;
      continue;
    }

    // Paragraph
    closeList();
    const paraLines = [];
    while (i < lines.length && !/^\s*$/.test(lines[i]) && !/^#{1,6}\s/.test(lines[i]) && !/^```/.test(lines[i]) && !/^[-*+]\s/.test(lines[i]) && !/^\d+\.\s/.test(lines[i]) && !/^\|/.test(lines[i]) && !/^>/.test(lines[i]) && !/^(\*{3,}|-{3,}|_{3,})\s*$/.test(lines[i])) {
      paraLines.push(lines[i]);
      i++;
    }
    if (paraLines.length > 0) {
      output.push(`<p>${parseInline(paraLines.join('\n'))}</p>`);
    }
  }
  closeList();
  return output.join('\n');
}

// ─── HTML → Markdown ───

function htmlToMarkdown(html) {
  let md = html;

  // Pre/code blocks first (protect content)
  md = md.replace(/<pre><code(?:\s+class="language-(\w+)")?>([\s\S]*?)<\/code><\/pre>/gi, (_, lang, code) => {
    const decoded = code.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"');
    return `\n\`\`\`${lang || ''}\n${decoded}\n\`\`\`\n`;
  });

  // Headings
  md = md.replace(/<h([1-6])[^>]*>([\s\S]*?)<\/h\1>/gi, (_, level, text) => {
    return '\n' + '#'.repeat(parseInt(level)) + ' ' + stripTags(text).trim() + '\n';
  });

  // Bold
  md = md.replace(/<(strong|b)>([\s\S]*?)<\/\1>/gi, '**$2**');
  // Italic
  md = md.replace(/<(em|i)>([\s\S]*?)<\/\1>/gi, '*$2*');
  // Strikethrough
  md = md.replace(/<del>([\s\S]*?)<\/del>/gi, '~~$1~~');
  // Inline code
  md = md.replace(/<code>([\s\S]*?)<\/code>/gi, '`$1`');

  // Links
  md = md.replace(/<a\s+href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/gi, '[$2]($1)');
  // Images
  md = md.replace(/<img\s+[^>]*src="([^"]*)"[^>]*alt="([^"]*)"[^>]*\/?>/gi, '![$2]($1)');
  md = md.replace(/<img\s+[^>]*alt="([^"]*)"[^>]*src="([^"]*)"[^>]*\/?>/gi, '![$1]($2)');

  // Tables
  md = md.replace(/<table[\s\S]*?<\/table>/gi, (table) => {
    const rows = [];
    const rowMatches = table.match(/<tr[\s\S]*?<\/tr>/gi) || [];
    rowMatches.forEach((row, idx) => {
      const cells = (row.match(/<(?:td|th)[^>]*>([\s\S]*?)<\/(?:td|th)>/gi) || []).map((c) =>
        stripTags(c.replace(/<\/?(?:td|th)[^>]*>/gi, '')).trim()
      );
      rows.push('| ' + cells.join(' | ') + ' |');
      if (idx === 0) {
        rows.push('| ' + cells.map(() => '---').join(' | ') + ' |');
      }
    });
    return '\n' + rows.join('\n') + '\n';
  });

  // Task list items
  md = md.replace(/<li[^>]*class="task-list-item"[^>]*><input[^>]*checked[^>]*>\s*([\s\S]*?)<\/li>/gi, '- [x] $1\n');
  md = md.replace(/<li[^>]*class="task-list-item"[^>]*><input[^>]*>\s*([\s\S]*?)<\/li>/gi, '- [ ] $1\n');

  // Ordered list
  let olCounter = 0;
  md = md.replace(/<ol[^>]*>/gi, () => { olCounter = 0; return '\n'; });
  md = md.replace(/<\/ol>/gi, '\n');
  md = md.replace(/<li>([\s\S]*?)<\/li>/gi, (match, content) => {
    // Check if we're likely in an ol context (rough heuristic: if olCounter was reset)
    // Since we process sequentially, we handle ul/ol via tags
    return `- ${stripTags(content).trim()}\n`;
  });

  // Re-do ordered lists more carefully
  md = md.replace(/\n(\d+\. [^\n]+\n)+/g, (m) => m); // keep as-is if already numbered

  // Unordered list
  md = md.replace(/<ul[^>]*>/gi, '\n');
  md = md.replace(/<\/ul>/gi, '\n');

  // Blockquote
  md = md.replace(/<blockquote>([\s\S]*?)<\/blockquote>/gi, (_, content) => {
    return stripTags(content).trim().split('\n').map((l) => '> ' + l).join('\n') + '\n';
  });

  // Horizontal rule
  md = md.replace(/<hr\s*\/?>/gi, '\n---\n');

  // Paragraphs
  md = md.replace(/<p>([\s\S]*?)<\/p>/gi, '\n$1\n');

  // Line breaks
  md = md.replace(/<br\s*\/?>/gi, '  \n');

  // Strip remaining tags
  md = stripTags(md);

  // Decode entities
  md = md.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

  // Clean up excessive newlines
  md = md.replace(/\n{3,}/g, '\n\n').trim();

  return md;
}

function stripTags(html) {
  return html.replace(/<[^>]+>/g, '');
}

// ─── TOC Generation ───

function generateToc(md) {
  const lines = md.replace(/\r\n/g, '\n').split('\n');
  const toc = [];
  let inCodeBlock = false;

  for (const line of lines) {
    if (/^```/.test(line)) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    if (inCodeBlock) continue;

    const match = line.match(/^(#{1,6})\s+(.+)/);
    if (match) {
      const level = match[1].length;
      const text = match[2].replace(/\s+#+\s*$/, '');
      const id = text.toLowerCase().replace(/[^\w\s-]/g, '').replace(/\s+/g, '-');
      const indent = '  '.repeat(level - 1);
      toc.push({ level, text, id, markdown: `${indent}- [${text}](#${id})` });
    }
  }

  return {
    items: toc.map(({ level, text, id }) => ({ level, text, id })),
    markdown: toc.map((t) => t.markdown).join('\n'),
    html: markdownToHtml(toc.map((t) => t.markdown).join('\n')),
  };
}

// ─── Router ───

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: CORS_HEADERS });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // Health / info
    if (path === '/' && request.method === 'GET') {
      return jsonResponse({
        name: 'Markdown Converter API',
        version: '1.0.0',
        endpoints: [
          { method: 'POST', path: '/md-to-html', description: 'Convert Markdown to HTML' },
          { method: 'POST', path: '/html-to-md', description: 'Convert HTML to Markdown' },
          { method: 'POST', path: '/toc', description: 'Generate Table of Contents from Markdown' },
        ],
      });
    }

    if (request.method !== 'POST') {
      return errorResponse('Method not allowed. Use POST.', 405);
    }

    let body;
    try {
      body = await request.json();
    } catch {
      return errorResponse('Invalid JSON body.', 400);
    }

    switch (path) {
      case '/md-to-html': {
        const { markdown } = body;
        if (!markdown || typeof markdown !== 'string') {
          return errorResponse('Missing or invalid "markdown" field.');
        }
        try {
          const html = markdownToHtml(markdown);
          return jsonResponse({ html });
        } catch (e) {
          return errorResponse(`Conversion failed: ${e.message}`, 500);
        }
      }

      case '/html-to-md': {
        const { html } = body;
        if (!html || typeof html !== 'string') {
          return errorResponse('Missing or invalid "html" field.');
        }
        try {
          const markdown = htmlToMarkdown(html);
          return jsonResponse({ markdown });
        } catch (e) {
          return errorResponse(`Conversion failed: ${e.message}`, 500);
        }
      }

      case '/toc': {
        const { markdown } = body;
        if (!markdown || typeof markdown !== 'string') {
          return errorResponse('Missing or invalid "markdown" field.');
        }
        try {
          const toc = generateToc(markdown);
          return jsonResponse({ toc });
        } catch (e) {
          return errorResponse(`TOC generation failed: ${e.message}`, 500);
        }
      }

      default:
        return errorResponse(`Unknown endpoint: ${path}`, 404);
    }
  },
};
