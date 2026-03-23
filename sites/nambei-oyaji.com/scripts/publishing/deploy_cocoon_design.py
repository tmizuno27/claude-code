"""
Deploy TCD-style article page CSS + JS to Cocoon theme via WordPress widgets.
- CSS → content-top widget (custom_html-2)
- JS → sidebar widget (custom_html-3)
"""
import json, urllib.request, base64, sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

BLOG_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DESIGN_DIR = os.path.join(BLOG_ROOT, 'design')
CSS_FILE = os.path.join(DESIGN_DIR, 'single-article-cocoon.css')
JS_FILE = os.path.join(DESIGN_DIR, 'single-article-cocoon.js')

creds = base64.b64encode(b't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D').decode()

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
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
    lines = [l.strip() for l in css.split('\n') if l.strip()]
    return '\n'.join(lines)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def update_widget(widget_id, content):
    """Update a custom_html widget content."""
    data = {
        'instance': {
            'raw': {
                'content': content
            }
        }
    }
    return api_call(f'widgets/{widget_id}', data, 'PUT')

def main():
    print('=' * 60)
    print('Cocoon Design Deployer')
    print('=' * 60)

    # Read files
    print('\n[1/3] Reading design files...')
    css_content = read_file(CSS_FILE)
    js_content = read_file(JS_FILE)
    css_minified = minify_css(css_content)
    print(f'  CSS: {len(css_content):,} -> {len(css_minified):,} bytes')
    print(f'  JS:  {len(js_content):,} bytes')

    # Deploy CSS to content-top widget
    print('\n[2/3] Deploying CSS to content-top widget...')
    css_html = f'<style>\n{css_minified}\n</style>'
    try:
        update_widget('custom_html-2', css_html)
        print('  SUCCESS: CSS deployed to custom_html-2 (content-top)')
    except Exception as e:
        print(f'  ERROR: {e}')
        # Try smaller payload
        if hasattr(e, 'read'):
            print(f'  Response: {e.read().decode("utf-8", errors="replace")[:500]}')
        return

    # Deploy JS to sidebar widget
    print('\n[3/3] Deploying JS to sidebar widget...')
    js_html = f'<script>\n{js_content}\n</script>'
    try:
        update_widget('custom_html-3', js_html)
        print('  SUCCESS: JS deployed to custom_html-3 (sidebar)')
    except Exception as e:
        print(f'  ERROR: {e}')
        if hasattr(e, 'read'):
            print(f'  Response: {e.read().decode("utf-8", errors="replace")[:500]}')
        return

    print('\n' + '=' * 60)
    print('Deployment complete!')
    print('  CSS: content-top widget (loads on all pages)')
    print('  JS:  sidebar widget (loads on pages with sidebar)')
    print('  URL: https://nambei-oyaji.com/paraguay-food-culture/')
    print('=' * 60)

if __name__ == '__main__':
    main()
