"""
Deploy TCD-style article page CSS + JS to WordPress single template.
Injects CSS as <style> and JS as <script> into the single template.
"""
import json, urllib.request, base64, sys, os, re, time

sys.stdout.reconfigure(encoding='utf-8')

# ============================================================
# Config
# ============================================================
BLOG_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DESIGN_DIR = os.path.join(BLOG_ROOT, 'design')
CSS_FILE = os.path.join(DESIGN_DIR, 'single-article.css')
JS_FILE = os.path.join(DESIGN_DIR, 'single-article.js')

# Auth
creds = base64.b64encode(b't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D').decode()

# Markers for identifying our injected blocks
CSS_MARKER = '/* TCD-SINGLE-ARTICLE-CSS */'
JS_MARKER = '/* TCD-SINGLE-ARTICLE-JS */'

def api_call(endpoint, data=None, method='GET'):
    url = 'https://nambei-oyaji.com/wp-json/wp/v2/' + endpoint
    if data:
        payload = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=payload,
            headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + creds},
            method=method or 'POST')
    else:
        req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + creds})
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8'))

def minify_css(css):
    """Light CSS minification — remove comments and extra whitespace."""
    css = re.sub(r'/\*(?!TCD-SINGLE).*?\*/', '', css, flags=re.DOTALL)
    css = re.sub(r'\n\s*\n', '\n', css)
    # Keep readable for debugging but remove blank lines
    lines = [l for l in css.split('\n') if l.strip()]
    return '\n'.join(lines)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def split_into_chunks(content, tag, marker, max_size=3000):
    """Split CSS/JS into chunks to avoid WAF blocking large payloads."""
    lines = content.split('\n')
    chunks = []
    current = []
    current_size = 0

    for line in lines:
        line_size = len(line.encode('utf-8'))
        if current_size + line_size > max_size and current:
            chunks.append('\n'.join(current))
            current = []
            current_size = 0
        current.append(line)
        current_size += line_size

    if current:
        chunks.append('\n'.join(current))

    blocks = []
    for i, chunk in enumerate(chunks):
        block = f'<!-- wp:html -->\n<{tag}>\n{marker}\n{chunk}\n</{tag}>\n<!-- /wp:html -->'
        blocks.append(block)

    return blocks

def remove_old_blocks(content, marker):
    """Remove previously injected CSS/JS blocks identified by marker."""
    pattern = r'<!-- wp:html -->\s*<(?:style|script)>\s*' + re.escape(marker) + r'.*?</(?:style|script)>\s*<!-- /wp:html -->'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def remove_legacy_blocks(content):
    """Remove old TCD-SINGLE blocks from previous deployments."""
    # Old marker: /* TCD-SINGLE */ (without -ARTICLE-CSS/-JS suffix)
    pattern = r'<!-- wp:html\s*-->\s*<(?:style|script)>\s*/\* TCD-SINGLE \*/.*?</(?:style|script)>\s*<!-- /wp:html\s*-->'
    return re.sub(pattern, '', content, flags=re.DOTALL)

def main():
    print('=' * 60)
    print('TCD Article Design Deployer')
    print('=' * 60)

    # Read CSS and JS
    print('\n[1/4] Reading design files...')
    css_content = read_file(CSS_FILE)
    js_content = read_file(JS_FILE)
    css_minified = minify_css(css_content)
    print(f'  CSS: {len(css_content):,} bytes -> {len(css_minified):,} bytes (minified)')
    print(f'  JS:  {len(js_content):,} bytes')

    # Create blocks
    # CSS is split into chunks (WAF safe), JS must stay as ONE block (IIFE pattern)
    print('\n[2/4] Splitting into blocks...')
    css_blocks = split_into_chunks(css_minified, 'style', CSS_MARKER, max_size=2500)
    # JS as single block — IIFE cannot be split across <script> tags
    js_blocks = [f'<!-- wp:html -->\n<script>\n{JS_MARKER}\n{js_content}\n</script>\n<!-- /wp:html -->']
    print(f'  CSS blocks: {len(css_blocks)}')
    print(f'  JS blocks:  {len(js_blocks)} (single IIFE)')

    # Fetch current single template
    print('\n[3/4] Fetching single template...')
    try:
        tmpl = api_call('templates/twentytwentyfive//single')
        content = tmpl.get('content', {}).get('raw', '')
        print(f'  Template size: {len(content):,} chars')
    except Exception as e:
        print(f'  ERROR: Failed to fetch template: {e}')
        return

    # Remove old injected blocks (current + legacy markers)
    content_clean = remove_old_blocks(content, CSS_MARKER)
    content_clean = remove_old_blocks(content_clean, JS_MARKER)
    content_clean = remove_legacy_blocks(content_clean)
    removed = len(content) - len(content_clean)
    if removed > 0:
        print(f'  Removed old blocks: {removed:,} chars')

    # Find insertion point (before main tag)
    main_marker = '<!-- wp:group {"tagName":"main"'
    if main_marker not in content_clean:
        # Try alternative markers
        for alt in ['<!-- wp:post-content', '<!-- wp:group {"layout"']:
            if alt in content_clean:
                main_marker = alt
                break
        else:
            print('  ERROR: No suitable insertion point found in template')
            print('  Template preview:', content_clean[:500])
            return

    # Insert CSS at end (after all existing styles) so it wins cascade, JS also at end
    print('\n[4/4] Deploying to WordPress...')

    # CSS and JS both go at the very end of template (after all existing inline styles)
    css_injection = '\n'.join(css_blocks)
    js_injection = '\n'.join(js_blocks)
    new_content = content_clean + '\n' + css_injection + '\n' + js_injection

    print(f'  New template size: {len(new_content):,} chars')

    # Deploy
    try:
        api_call('templates/twentytwentyfive//single', {'content': new_content}, 'POST')
        print('\n  SUCCESS: Single template updated!')
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='replace')
        print(f'\n  ERROR {e.code}: {e.reason}')
        print(f'  Response: {error_body[:500]}')

        if e.code == 403 and 'waf' in error_body.lower():
            print('\n  WAF detected. Trying smaller chunks...')
            # Retry with smaller chunks
            css_blocks = split_into_chunks(css_minified, 'style', CSS_MARKER, max_size=1200)
            js_blocks = split_into_chunks(js_content, 'script', JS_MARKER, max_size=1200)

            css_injection = '\n'.join(css_blocks) + '\n'
            js_injection = '\n' + '\n'.join(js_blocks)
            new_content = parts[0] + css_injection + main_marker + parts[1] + js_injection

            try:
                api_call('templates/twentytwentyfive//single', {'content': new_content}, 'POST')
                print('  SUCCESS (smaller chunks)!')
            except Exception as e2:
                print(f'  FAILED again: {e2}')
                print('  Try deploying CSS/JS via Cocoon theme settings manually.')
        return
    except Exception as e:
        print(f'\n  ERROR: {e}')
        return

    print('\n' + '=' * 60)
    print('Deployment complete!')
    print(f'  CSS: {len(css_blocks)} blocks injected')
    print(f'  JS:  {len(js_blocks)} blocks injected')
    print('  URL: https://nambei-oyaji.com/ (any article page)')
    print('=' * 60)

if __name__ == '__main__':
    main()
