"""
pdf_generator.py
================
Markdown形式のプロダクトファイルをプロフェッショナルなPDFに変換するスクリプト。

処理フロー:
1. コマンドライン引数でMarkdownファイルのパスを受け取る
2. Markdownファイルを読み込む
3. python-markdown で HTML に変換する
4. プロフェッショナルなCSSテンプレートを適用する
   - 日本語フォントサポート（Noto Sans JP / Google Fonts）
   - 表紙スタイリング
   - H2/H3ヘッダーから目次を自動生成
   - ページ番号
   - ビジネス文書レイアウト（A4サイズ）
5. WeasyPrint で PDF を生成する
6. outputs/products/pdf/{filename}.pdf に保存する
7. ファイルサイズとパスを出力する
"""

import sys
import re
import logging
import argparse
from pathlib import Path
from datetime import date

try:
    import markdown
except ImportError:
    markdown = None  # type: ignore

try:
    from weasyprint import HTML as WeasyHTML
    from weasyprint import CSS
except ImportError:
    WeasyHTML = None  # type: ignore
    CSS = None  # type: ignore

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# プロジェクトルート
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PDF_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "products" / "pdf"

# ---------------------------------------------------------------------------
# プロフェッショナルCSSテンプレート
# ---------------------------------------------------------------------------

PROFESSIONAL_CSS = """
/* === Google Fonts: Noto Sans JP === */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Serif+JP:wght@400;700&display=swap');

/* === ページ設定（A4） === */
@page {
    size: A4;
    margin: 25mm 20mm 25mm 25mm;
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-family: 'Noto Sans JP', sans-serif;
        font-size: 9pt;
        color: #666666;
    }
    @top-right {
        content: string(document-title);
        font-family: 'Noto Sans JP', sans-serif;
        font-size: 8pt;
        color: #999999;
    }
}

@page :first {
    margin: 0;
    @bottom-center { content: none; }
    @top-right { content: none; }
}

/* === リセット === */
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* === 基本フォント === */
body {
    font-family: 'Noto Sans JP', 'Yu Gothic', 'Hiragino Kaku Gothic Pro', 'Meiryo', sans-serif;
    font-size: 10.5pt;
    line-height: 1.85;
    color: #1a1a1a;
    word-break: break-all;
    overflow-wrap: break-word;
}

/* === 表紙ページ === */
.cover-page {
    page: first;
    width: 210mm;
    height: 297mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #1a237e 0%, #0d47a1 40%, #1565c0 70%, #1976d2 100%);
    color: white;
    text-align: center;
    padding: 40mm 20mm;
    position: relative;
    overflow: hidden;
}

.cover-page::before {
    content: '';
    position: absolute;
    top: -30mm;
    right: -30mm;
    width: 120mm;
    height: 120mm;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.05);
}

.cover-page::after {
    content: '';
    position: absolute;
    bottom: -20mm;
    left: -20mm;
    width: 90mm;
    height: 90mm;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.04);
}

.cover-label {
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 10pt;
    font-weight: 500;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.75);
    margin-bottom: 12mm;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 3mm 8mm;
    border-radius: 2mm;
}

.cover-title {
    font-family: 'Noto Serif JP', 'Yu Mincho', 'Hiragino Mincho Pro', serif;
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.4;
    color: #ffffff;
    margin-bottom: 10mm;
    text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    string-set: document-title content();
}

.cover-subtitle {
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 13pt;
    font-weight: 300;
    color: rgba(255, 255, 255, 0.85);
    margin-bottom: 20mm;
    line-height: 1.6;
}

.cover-divider {
    width: 50mm;
    height: 1px;
    background: rgba(255, 255, 255, 0.4);
    margin: 0 auto 12mm;
}

.cover-meta {
    font-size: 9.5pt;
    color: rgba(255, 255, 255, 0.65);
    line-height: 2;
}

.cover-meta strong {
    color: rgba(255, 255, 255, 0.9);
    font-weight: 500;
}

/* === 目次 === */
.toc-section {
    page-break-before: always;
    padding: 15mm 0 10mm;
}

.toc-title {
    font-family: 'Noto Serif JP', serif;
    font-size: 20pt;
    font-weight: 700;
    color: #1a237e;
    border-bottom: 3px solid #1a237e;
    padding-bottom: 4mm;
    margin-bottom: 10mm;
}

.toc-list {
    list-style: none;
    padding: 0;
}

.toc-item-h2 {
    display: flex;
    align-items: baseline;
    margin-bottom: 4mm;
    font-size: 10.5pt;
    font-weight: 500;
    color: #1a237e;
}

.toc-item-h3 {
    display: flex;
    align-items: baseline;
    margin-bottom: 3mm;
    padding-left: 8mm;
    font-size: 9.5pt;
    font-weight: 400;
    color: #424242;
}

.toc-text {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
}

.toc-dots {
    flex: 1;
    border-bottom: 1px dotted #cccccc;
    margin: 0 3mm;
    min-width: 10mm;
}

.toc-page {
    white-space: nowrap;
    font-size: 9pt;
    color: #666666;
}

/* === 本文コンテナ === */
.document-body {
    padding-top: 5mm;
}

/* === 見出し === */
h1 {
    font-family: 'Noto Serif JP', serif;
    font-size: 22pt;
    font-weight: 700;
    color: #1a237e;
    margin: 12mm 0 6mm;
    padding-bottom: 3mm;
    border-bottom: 3px solid #1a237e;
    page-break-after: avoid;
    line-height: 1.4;
    string-set: document-title content();
}

h2 {
    font-family: 'Noto Serif JP', serif;
    font-size: 16pt;
    font-weight: 700;
    color: #1a237e;
    margin: 10mm 0 4mm;
    padding: 3mm 4mm 3mm 6mm;
    border-left: 5px solid #1976d2;
    background: #f3f4fb;
    page-break-after: avoid;
    line-height: 1.4;
}

h3 {
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #283593;
    margin: 7mm 0 3mm;
    padding-bottom: 2mm;
    border-bottom: 1.5px solid #c5cae9;
    page-break-after: avoid;
    line-height: 1.4;
}

h4 {
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 11pt;
    font-weight: 700;
    color: #37474f;
    margin: 5mm 0 2mm;
    page-break-after: avoid;
}

/* === 段落 === */
p {
    margin-bottom: 4mm;
    text-align: justify;
    text-justify: inter-ideograph;
}

/* === リスト === */
ul, ol {
    margin: 3mm 0 4mm 8mm;
    padding-left: 5mm;
}

li {
    margin-bottom: 2mm;
    line-height: 1.7;
}

ul li::marker {
    color: #1976d2;
}

ol li::marker {
    color: #1976d2;
    font-weight: 700;
}

/* === テーブル === */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 5mm 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}

thead tr {
    background: #1a237e;
    color: white;
}

thead th {
    padding: 3mm 4mm;
    text-align: left;
    font-weight: 500;
    border: 1px solid #1a237e;
}

tbody tr:nth-child(even) {
    background: #f5f5f5;
}

tbody td {
    padding: 2.5mm 4mm;
    border: 1px solid #e0e0e0;
    vertical-align: top;
}

/* === コードブロック === */
pre {
    background: #263238;
    color: #eceff1;
    padding: 5mm;
    border-radius: 2mm;
    font-size: 8.5pt;
    overflow-x: auto;
    margin: 4mm 0;
    page-break-inside: avoid;
    font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
    line-height: 1.6;
}

code {
    font-family: 'Fira Code', 'Consolas', 'Courier New', monospace;
    font-size: 9pt;
    background: #e8eaf6;
    color: #283593;
    padding: 0.5mm 2mm;
    border-radius: 1mm;
}

pre code {
    background: none;
    color: inherit;
    padding: 0;
    font-size: inherit;
}

/* === 引用 === */
blockquote {
    border-left: 4px solid #1976d2;
    background: #e8eaf6;
    padding: 4mm 5mm;
    margin: 5mm 0;
    color: #37474f;
    font-style: italic;
    border-radius: 0 2mm 2mm 0;
    page-break-inside: avoid;
}

blockquote p {
    margin-bottom: 0;
}

/* === 水平線 === */
hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 6mm 0;
}

/* === 強調 === */
strong {
    font-weight: 700;
    color: #1a237e;
}

em {
    font-style: italic;
    color: #37474f;
}

/* === リンク === */
a {
    color: #1565c0;
    text-decoration: none;
}

/* === 注意ボックス === */
.note-box {
    background: #fff9c4;
    border: 1px solid #f9a825;
    border-left: 4px solid #f9a825;
    padding: 4mm 5mm;
    margin: 5mm 0;
    border-radius: 0 2mm 2mm 0;
    page-break-inside: avoid;
}

/* === ページ区切り === */
.page-break {
    page-break-before: always;
}

/* === フッター補助 === */
.document-footer {
    margin-top: 15mm;
    padding-top: 5mm;
    border-top: 1px solid #e0e0e0;
    font-size: 8.5pt;
    color: #999999;
    text-align: center;
}
"""

# ---------------------------------------------------------------------------
# 目次生成
# ---------------------------------------------------------------------------

RE_H2_H3 = re.compile(r"<(h[23])[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL)
RE_HTML_STRIP = re.compile(r"<[^>]+>")


def strip_html(text: str) -> str:
    """HTMLタグを除去する。"""
    return RE_HTML_STRIP.sub("", text).strip()


def generate_toc(html_body: str) -> tuple[str, str]:
    """
    本文HTMLからH2/H3見出しを抽出し、目次HTMLと
    アンカー付き本文HTMLを返す。

    Returns:
        (toc_html, body_html_with_anchors)
    """
    toc_items: list[tuple[str, str, str]] = []  # (level, anchor_id, text)
    counter: dict[str, int] = defaultdict(int)

    def add_anchor(m: re.Match) -> str:
        tag = m.group(1).lower()
        inner = m.group(2)
        text = strip_html(inner)
        # アンカーID生成（英数字と日本語をそのまま使用）
        safe = re.sub(r"[^\w\u3000-\u9fff\uff00-\uffef]", "-", text)[:40]
        counter[safe] += 1
        anchor_id = f"{safe}-{counter[safe]}" if counter[safe] > 1 else safe
        toc_items.append((tag, anchor_id, text))
        return f'<{tag} id="{anchor_id}">{inner}</{tag}>'

    body_with_anchors = RE_H2_H3.sub(add_anchor, html_body)

    if not toc_items:
        return "", body_with_anchors

    # 目次HTML構築
    toc_lines = ['<div class="toc-section">', '<div class="toc-title">目次</div>', '<ul class="toc-list">']
    for level, anchor_id, text in toc_items:
        css_class = "toc-item-h2" if level == "h2" else "toc-item-h3"
        toc_lines.append(
            f'<li class="{css_class}">'
            f'<span class="toc-text"><a href="#{anchor_id}">{text}</a></span>'
            f'<span class="toc-dots"></span>'
            f'<span class="toc-page"></span>'
            f"</li>"
        )
    toc_lines.append("</ul></div>")
    toc_html = "\n".join(toc_lines)

    return toc_html, body_with_anchors


from collections import defaultdict


# ---------------------------------------------------------------------------
# 表紙生成
# ---------------------------------------------------------------------------

def extract_cover_info(md_text: str) -> dict:
    """
    Markdownの先頭から表紙情報を抽出する。
    対応フォーマット:
        # タイトル
        ## サブタイトル（オプション）
        <!-- cover-meta
        author: 著者名
        date: 日付
        version: バージョン
        -->
    """
    info = {
        "title": "",
        "subtitle": "",
        "author": "",
        "doc_date": date.today().strftime("%Y年%m月%d日"),
        "version": "1.0",
        "label": "BUSINESS DOCUMENT",
    }

    lines = md_text.strip().split("\n")
    for line in lines[:10]:
        line = line.strip()
        if line.startswith("# ") and not info["title"]:
            info["title"] = line[2:].strip()
        elif line.startswith("## ") and not info["subtitle"]:
            info["subtitle"] = line[3:].strip()

    # メタコメントブロックを解析
    meta_match = re.search(
        r"<!--\s*cover-meta\s*(.*?)-->",
        md_text,
        re.DOTALL | re.IGNORECASE,
    )
    if meta_match:
        for meta_line in meta_match.group(1).strip().split("\n"):
            if ":" in meta_line:
                key, _, val = meta_line.partition(":")
                key = key.strip().lower()
                val = val.strip()
                if key == "author":
                    info["author"] = val
                elif key == "date":
                    info["doc_date"] = val
                elif key == "version":
                    info["version"] = val
                elif key == "label":
                    info["label"] = val

    if not info["title"]:
        info["title"] = "ビジネスドキュメント"

    return info


def build_cover_html(info: dict) -> str:
    """表紙のHTMLを構築する。"""
    subtitle_html = (
        f'<div class="cover-subtitle">{info["subtitle"]}</div>'
        if info["subtitle"]
        else ""
    )
    meta_lines = []
    if info["author"]:
        meta_lines.append(f'<strong>作成者：</strong>{info["author"]}')
    meta_lines.append(f'<strong>作成日：</strong>{info["doc_date"]}')
    meta_lines.append(f'<strong>バージョン：</strong>v{info["version"]}')
    meta_html = "<br>".join(meta_lines)

    return f"""
<div class="cover-page">
    <div class="cover-label">{info["label"]}</div>
    <div class="cover-title">{info["title"]}</div>
    {subtitle_html}
    <div class="cover-divider"></div>
    <div class="cover-meta">{meta_html}</div>
</div>
"""


# ---------------------------------------------------------------------------
# Markdown → HTML → PDF 変換
# ---------------------------------------------------------------------------

def md_to_html_full(md_text: str) -> str:
    """
    Markdownを完全なHTML文書に変換する。
    表紙・目次・本文を含む。
    """
    if markdown is None:
        raise ImportError("markdown ライブラリが見つかりません。pip install markdown を実行してください。")

    # 表紙情報を抽出
    cover_info = extract_cover_info(md_text)

    # cover-meta コメントを除去してから変換
    md_clean = re.sub(r"<!--\s*cover-meta\s*.*?-->", "", md_text, flags=re.DOTALL)

    # Markdown → HTML
    md_extensions = ["tables", "fenced_code", "nl2br", "attr_list", "def_list", "toc"]
    body_html = markdown.markdown(md_clean, extensions=md_extensions)

    # 目次と本文（アンカー付き）を生成
    toc_html, body_with_anchors = generate_toc(body_html)

    # 全体のHTMLを組み立て
    cover_html = build_cover_html(cover_info)

    full_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cover_info["title"]}</title>
    <style>
{PROFESSIONAL_CSS}
    </style>
</head>
<body>
    {cover_html}
    {toc_html}
    <div class="document-body">
        {body_with_anchors}
    </div>
    <div class="document-footer">
        {cover_info["title"]} &nbsp;|&nbsp; {cover_info["doc_date"]} &nbsp;|&nbsp; v{cover_info["version"]}
    </div>
</body>
</html>"""

    return full_html


def convert_md_to_pdf(md_path: Path) -> Path:
    """
    Markdownファイルを読み込み、PDFに変換して保存する。

    Args:
        md_path: 変換対象のMarkdownファイルパス

    Returns:
        生成されたPDFファイルのパス
    """
    if WeasyHTML is None:
        raise ImportError(
            "weasyprint ライブラリが見つかりません。pip install weasyprint を実行してください。"
        )

    logger.info("Markdownファイルを読み込んでいます: %s", md_path)
    md_text = md_path.read_text(encoding="utf-8")

    logger.info("HTMLへの変換を開始します...")
    full_html = md_to_html_full(md_text)

    # 出力先ディレクトリを作成
    PDF_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    pdf_path = PDF_OUTPUT_DIR / f"{md_path.stem}.pdf"

    logger.info("PDFを生成しています: %s", pdf_path)
    WeasyHTML(string=full_html, base_url=str(md_path.parent)).write_pdf(str(pdf_path))

    file_size_kb = pdf_path.stat().st_size / 1024
    logger.info("PDF生成完了!")
    print(f"\n[PDF生成完了]")
    print(f"  出力ファイル : {pdf_path}")
    print(f"  ファイルサイズ: {file_size_kb:.1f} KB")

    return pdf_path


# ---------------------------------------------------------------------------
# エントリーポイント
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="MarkdownファイルをプロフェッショナルなビジネスPDFに変換するスクリプト"
    )
    parser.add_argument(
        "markdown_file",
        type=str,
        help="変換するMarkdownファイルのパス",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="PDF出力先ディレクトリ（デフォルト: outputs/products/pdf/）",
    )
    args = parser.parse_args()

    md_path = Path(args.markdown_file).resolve()
    if not md_path.exists():
        logger.error("指定されたMarkdownファイルが見つかりません: %s", md_path)
        raise SystemExit(1)
    if not md_path.suffix.lower() in (".md", ".markdown"):
        logger.warning("拡張子がMarkdown形式ではありません: %s", md_path.suffix)

    # 出力先ディレクトリを上書き
    if args.output_dir:
        global PDF_OUTPUT_DIR
        PDF_OUTPUT_DIR = Path(args.output_dir).resolve()

    try:
        pdf_path = convert_md_to_pdf(md_path)
        sys.exit(0)
    except ImportError as exc:
        logger.error("依存ライブラリが不足しています: %s", exc)
        logger.error("次のコマンドを実行してください: pip install markdown weasyprint")
        raise SystemExit(1)
    except Exception as exc:
        logger.exception("PDF生成中にエラーが発生しました: %s", exc)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
