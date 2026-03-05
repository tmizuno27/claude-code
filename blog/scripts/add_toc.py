"""
全ブログ記事にクリック開閉式の目次（Table of Contents）を自動挿入するスクリプト。
- <details>/<summary>タグで開閉式
- H2/H3見出しからアンカーリンク付き目次を生成
- 記事本文の各見出しにid属性を付与
- 既に目次がある記事はスキップ
"""

import os
import re
import glob
import unicodedata

ARTICLES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "outputs", "articles", "2026-03-03"
)


def slugify(text: str) -> str:
    """日本語対応のスラッグ生成。見出しテキストからアンカーIDを作る。"""
    # 記号・装飾を除去
    text = re.sub(r'[【】\[\]「」『』（）\(\)：:、。！!？?・\u2014\u2015\u2026]', '', text)
    text = text.strip()
    # 半角英数とハイフンに正規化
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text


def extract_headings(content: str) -> list:
    """Markdown本文からH2/H3見出しを抽出する。"""
    headings = []
    for line in content.split('\n'):
        m = re.match(r'^(#{2,3})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            headings.append((level, text))
    return headings


def generate_toc_html(headings: list) -> str:
    """見出しリストからHTML目次を生成する。"""
    if not headings:
        return ""

    lines = []
    lines.append('<details class="toc-container">')
    lines.append('<summary>目次（クリックで開閉）</summary>')
    lines.append('<nav class="toc">')
    lines.append('<ol>')

    for level, text in headings:
        anchor = slugify(text)
        if level == 2:
            lines.append(f'  <li><a href="#{anchor}">{text}</a></li>')
        elif level == 3:
            # H3はインデント
            lines.append(f'  <li class="toc-h3"><a href="#{anchor}">{text}</a></li>')

    lines.append('</ol>')
    lines.append('</nav>')
    lines.append('</details>')
    lines.append('')

    return '\n'.join(lines)


def add_heading_ids(content: str, headings: list) -> str:
    """各見出し行の前にHTMLアンカーを挿入する。"""
    for level, text in headings:
        anchor = slugify(text)
        prefix = '#' * level
        # 見出し行を探してアンカー付きに変換
        old_line = f'{prefix} {text}'
        new_line = f'<span id="{anchor}"></span>\n\n{prefix} {text}'
        # 最初の出現のみ置換
        content = content.replace(old_line, new_line, 1)
    return content


def find_toc_insert_position(body: str) -> int:
    """目次の挿入位置を決定する。
    アフィリエイト開示文の後、または導入段落の後に挿入。
    """
    lines = body.split('\n')

    # H1タイトルの位置を見つける
    h1_idx = -1
    for i, line in enumerate(lines):
        if re.match(r'^#\s+', line):
            h1_idx = i
            break

    if h1_idx == -1:
        return 0

    # H1の後の最初の空行の後、最初のH2の前に挿入
    # アフィリエイト開示文があればその段落の後
    first_h2_idx = -1
    for i in range(h1_idx + 1, len(lines)):
        if re.match(r'^##\s+', lines[i]):
            first_h2_idx = i
            break

    if first_h2_idx == -1:
        return len('\n'.join(lines))

    # 最初のH2の直前（空行を1つ残す）
    insert_idx = first_h2_idx
    # 直前の空行を保持
    while insert_idx > 0 and lines[insert_idx - 1].strip() == '':
        insert_idx -= 1

    return len('\n'.join(lines[:insert_idx]))


def process_article(filepath: str) -> bool:
    """1記事を処理する。目次を挿入してファイルを上書き。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 既に目次がある場合はスキップ
    if '<details class="toc-container">' in content:
        return False

    # frontmatterとbodyを分離
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2]

    # 見出し抽出
    headings = extract_headings(body)
    if not headings:
        return False

    # 見出しにアンカーIDを付与
    body = add_heading_ids(body, headings)

    # 目次HTML生成
    toc = generate_toc_html(headings)

    # 挿入位置を決定（最初のH2の直前）
    lines = body.split('\n')
    first_h2_idx = -1
    for i, line in enumerate(lines):
        # spanタグの次の空行の次がH2
        if re.match(r'^##\s+', line):
            first_h2_idx = i
            break

    if first_h2_idx == -1:
        return False

    # H2の直前に目次を挿入
    before = '\n'.join(lines[:first_h2_idx])
    after = '\n'.join(lines[first_h2_idx:])
    body = before.rstrip('\n') + '\n\n' + toc + '\n' + after

    # 再構築
    new_content = '---' + frontmatter + '---' + body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    pattern = os.path.join(ARTICLES_DIR, "article-*.md")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"記事が見つかりません: {pattern}")
        return

    print(f"対象記事: {len(files)}本")
    processed = 0
    skipped = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        if process_article(filepath):
            print(f"  OK: {filename}")
            processed += 1
        else:
            print(f"  - {filename} (スキップ)")
            skipped += 1

    print(f"\n完了: {processed}本に目次を挿入、{skipped}本スキップ")


if __name__ == "__main__":
    main()
