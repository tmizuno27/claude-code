"""
全ブログ記事にクリック開閉式の目次（Table of Contents）を自動挿入するスクリプト。
- <details>/<summary>タグで開閉式
- H2/H3見出しからアンカーリンク付き目次を生成
- 記事本文の各見出しにid属性を付与
- 既存の目次・アンカーがある場合はクリーンアップして再生成
"""

import os
import re
import glob


# 目次から除外する見出しパターン
EXCLUDE_HEADINGS = [
    '著者プロフィール',
    'Rank Math 設定用',
    'Rank Math 設定用メタ情報',
]

ARTICLES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "outputs", "articles", "2026-03-03"
)


def slugify(text: str) -> str:
    """日本語対応のスラッグ生成。見出しテキストからアンカーIDを作る。"""
    text = re.sub(r'[【】\[\]「」『』（）\(\)：:、。！!？?・\u2014\u2015\u2026]', '', text)
    text = text.strip()
    text = text.lower()
    text = re.sub(r'\s+', '-', text)
    text = re.sub(r'-+', '-', text)
    text = text.strip('-')
    return text


def should_exclude(text: str) -> bool:
    """目次から除外すべき見出しかチェック。"""
    for pattern in EXCLUDE_HEADINGS:
        if pattern in text:
            return True
    return False


def extract_headings(content: str) -> list:
    """Markdown本文からH2/H3見出しを抽出する（メタ系セクション除外）。"""
    headings = []
    exclude_mode = False
    for line in content.split('\n'):
        m = re.match(r'^(#{2,3})\s+(.+)$', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            # 除外対象のH2以降はすべて除外
            if level == 2 and should_exclude(text):
                exclude_mode = True
                continue
            if level == 2:
                exclude_mode = False
            if not exclude_mode:
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
            lines.append(f'  <li class="toc-h3"><a href="#{anchor}">{text}</a></li>')

    lines.append('</ol>')
    lines.append('</nav>')
    lines.append('</details>')

    return '\n'.join(lines)


def clean_existing_toc(body: str) -> str:
    """既存の目次ブロックとアンカーspanを除去する。"""
    # 目次ブロック除去
    body = re.sub(
        r'\n*<details class="toc-container">.*?</details>\n*',
        '\n\n',
        body,
        flags=re.DOTALL
    )
    # アンカーspan除去
    body = re.sub(r'\n*<span id="[^"]*"></span>\n*', '\n\n', body)
    # 連続空行を2つまでに
    body = re.sub(r'\n{3,}', '\n\n', body)
    return body


def process_article(filepath: str) -> bool:
    """1記事を処理する。目次を挿入してファイルを上書き。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # frontmatterとbodyを分離
    parts = content.split('---', 2)
    if len(parts) < 3:
        return False

    frontmatter = parts[1]
    body = parts[2]

    # 既存のTOC・アンカーをクリーンアップ
    body = clean_existing_toc(body)

    # 見出し抽出
    headings = extract_headings(body)
    if not headings:
        return False

    # 目次HTML生成
    toc = generate_toc_html(headings)

    # 本文を行ごとに処理
    lines = body.split('\n')
    result_lines = []
    first_h2_found = False
    toc_inserted = False

    for line in lines:
        # 最初のH2の直前にTOCを挿入
        if not toc_inserted and re.match(r'^##\s+', line):
            result_lines.append(toc)
            result_lines.append('')
            toc_inserted = True

        # H2/H3にアンカーspanを付与
        m = re.match(r'^(#{2,3})\s+(.+)$', line)
        if m:
            anchor = slugify(m.group(2).strip())
            result_lines.append(f'<span id="{anchor}"></span>')
            result_lines.append('')
            result_lines.append(line)
        else:
            result_lines.append(line)

    body = '\n'.join(result_lines)

    # 連続空行を整理
    body = re.sub(r'\n{3,}', '\n\n', body)

    # 再構築
    new_content = '---' + frontmatter + '---' + body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


def main():
    pattern = os.path.join(ARTICLES_DIR, "article-*.md")
    files = sorted(glob.glob(pattern))

    if not files:
        print(f"No articles found: {pattern}")
        return

    print(f"Target: {len(files)} articles")
    processed = 0
    skipped = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        if process_article(filepath):
            print(f"  OK: {filename}")
            processed += 1
        else:
            print(f"  SKIP: {filename}")
            skipped += 1

    print(f"\nDone: {processed} processed, {skipped} skipped")


if __name__ == "__main__":
    main()
