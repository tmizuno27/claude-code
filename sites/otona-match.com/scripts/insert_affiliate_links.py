import sys
import re
import requests
from requests.auth import HTTPBasicAuth

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://otona-match.com/?rest_route=/wp/v2"
USERNAME = "t.mizuno27@gmail.com"
APP_PASSWORD = "P4A1 P4eh Nk0z 29An hS6H 9OHq"

auth = HTTPBasicAuth(USERNAME, APP_PASSWORD)

MARRISH_URL = "https://px.a8.net/svt/ejp?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA"
MARRISH_IMG = "https://www10.a8.net/0.gif?a8mat=4AZGCF+DRY4GQ+3N2M+67JUA"
MARRISH_LINK_TAG = f'<a href="{MARRISH_URL}" rel="nofollow" target="_blank">マリッシュ</a>'
MARRISH_IMG_TAG = f'<img src="{MARRISH_IMG}" width="1" height="1" style="border:none;" />'

PCMAX_URL = "https://px.a8.net/svt/ejp?a8mat=4AZGCF+EGCW9M+YQK+631SY"
PCMAX_IMG = "https://www16.a8.net/0.gif?a8mat=4AZGCF+EGCW9M+YQK+631SY"
PCMAX_LINK_TAG = f'<a href="{PCMAX_URL}" rel="nofollow" target="_blank">PCMAX</a>'
PCMAX_IMG_TAG = f'<img src="{PCMAX_IMG}" width="1" height="1" style="border:none;" />'


def get_post(post_id):
    url = f"https://otona-match.com/?rest_route=/wp/v2/posts/{post_id}&context=edit"
    resp = requests.get(url, auth=auth)
    if resp.status_code == 200:
        return resp.json()
    else:
        print(f"  ERROR: GET failed {resp.status_code} - {resp.text[:200]}")
        return None


def update_post(post_id, content):
    url = f"https://otona-match.com/?rest_route=/wp/v2/posts/{post_id}"
    resp = requests.post(url, auth=auth, json={"content": content})
    if resp.status_code == 200:
        return True
    else:
        print(f"  ERROR: POST failed {resp.status_code} - {resp.text[:200]}")
        return False


def is_inside_tag(text, match_start, match_end):
    """マッチ箇所がHTMLタグ内（属性値など）にあるかチェック"""
    # マッチより前の文字列で最後の < と > を探す
    before = text[:match_start]
    last_open = before.rfind('<')
    last_close = before.rfind('>')
    if last_open > last_close:
        # タグの中にいる
        return True
    return False


def is_inside_heading(text, match_start):
    """h1/h2/h3タグ内にあるかチェック"""
    before = text[:match_start]
    # 直近の開きタグを探す
    tag_pattern = re.compile(r'<(h[123]|/h[123]|a[^>]*|/a)[^>]*>', re.IGNORECASE)
    tags = list(tag_pattern.finditer(before))
    if not tags:
        return False
    last_tag = tags[-1]
    tag_name = last_tag.group(1).lower()
    if tag_name in ('h1', 'h2', 'h3'):
        return True
    return False


def is_inside_a_tag(text, match_start):
    """aタグ内（リンクテキストor属性）にあるかチェック"""
    before = text[:match_start]
    # aタグと/aタグのスタック
    open_count = len(re.findall(r'<a\b', before, re.IGNORECASE))
    close_count = len(re.findall(r'</a>', before, re.IGNORECASE))
    return open_count > close_count


def already_has_affiliate(text, affiliate_domain="px.a8.net"):
    """px.a8.netリンクが既にあるかチェック（各案件のURL含む）"""
    return affiliate_domain in text


def replace_keyword(content, keyword, link_tag, affiliate_url, max_replace=2):
    """
    content内のkeywordをlink_tagに置換する。
    - 既にaタグ内 / h1/h2/h3内 / alt属性内 / 既に同じアフィリエイトURLがある箇所はスキップ
    - 最大max_replace回まで
    返り値: (new_content, replace_count)
    """
    count = 0
    result = []
    pos = 0
    text = content

    # keyword のパターン（大文字小文字区別なしで marrish も対応）
    pattern = re.compile(re.escape(keyword), re.IGNORECASE if keyword.lower() == 'marrish' else 0)

    for m in pattern.finditer(text):
        if count >= max_replace:
            break
        start, end = m.start(), m.end()

        # タグ属性内チェック
        if is_inside_tag(text, start, end):
            continue
        # aタグ内チェック
        if is_inside_a_tag(text, start):
            continue
        # 見出し内チェック
        if is_inside_heading(text, start):
            continue

        # 前後50文字でアフィリエイトURL重複チェック（同じURLが既にある）
        context_start = max(0, start - 200)
        context_end = min(len(text), end + 200)
        context = text[context_start:context_end]
        if affiliate_url in context:
            continue

        result.append(text[pos:start])
        # keywordがマッチしたテキストをlink_tagで置換
        result.append(link_tag)
        pos = end
        count += 1

    result.append(text[pos:])
    return ''.join(result), count


def add_tracking_img(content, img_tag, img_url):
    """記事末尾にトラッキング画像を追加（重複チェック）"""
    if img_url in content:
        return content, False
    return content + '\n' + img_tag, True


def process_post(post_id, marrish=False, pcmax=False):
    print(f"\n=== 記事ID {post_id} 処理開始 ===")
    post = get_post(post_id)
    if not post:
        return

    title = post.get('title', {}).get('rendered', '')
    print(f"  タイトル: {title}")

    content = post.get('content', {}).get('raw', '')
    if not content:
        print("  ERROR: raw contentが取得できませんでした")
        return

    original_len = len(content)
    total_replacements = 0

    if marrish:
        # 「マリッシュ」と「marrish」両方置換
        content, c1 = replace_keyword(content, 'マリッシュ', MARRISH_LINK_TAG, MARRISH_URL, max_replace=2)
        print(f"  マリッシュ 置換数: {c1}")
        remaining = 2 - c1
        if remaining > 0:
            content, c2 = replace_keyword(content, 'marrish', f'<a href="{MARRISH_URL}" rel="nofollow" target="_blank">marrish</a>', MARRISH_URL, max_replace=remaining)
            print(f"  marrish 置換数: {c2}")
        else:
            c2 = 0
        total_replacements += c1 + c2

        content, added = add_tracking_img(content, MARRISH_IMG_TAG, MARRISH_IMG)
        print(f"  マリッシュ tracking img 追加: {'YES' if added else 'スキップ（重複）'}")

    if pcmax:
        content, c3 = replace_keyword(content, 'PCMAX', PCMAX_LINK_TAG, PCMAX_URL, max_replace=2)
        print(f"  PCMAX 置換数: {c3}")
        total_replacements += c3

        content, added = add_tracking_img(content, PCMAX_IMG_TAG, PCMAX_IMG)
        print(f"  PCMAX tracking img 追加: {'YES' if added else 'スキップ（重複）'}")

    if len(content) == original_len and total_replacements == 0:
        print("  変更なし（置換対象が見つからなかった）")
        return

    success = update_post(post_id, content)
    if success:
        print(f"  投稿更新 SUCCESS")
    else:
        print(f"  投稿更新 FAILED")


if __name__ == "__main__":
    # 1. 記事ID 191: マリッシュ
    process_post(191, marrish=True)

    # 2. 記事ID 146: マリッシュ
    process_post(146, marrish=True)

    # 3. 記事ID 15: PCMAX
    process_post(15, pcmax=True)

    # 4. 記事ID 14: マリッシュ + PCMAX
    process_post(14, marrish=True, pcmax=True)

    # 5. 記事ID 13: PCMAX
    process_post(13, pcmax=True)

    print("\n=== 全処理完了 ===")
