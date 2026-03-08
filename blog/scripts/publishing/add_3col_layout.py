#!/usr/bin/env python3
"""記事ページに3カラムレイアウトを追加（デスクトップのみ）"""
import json, requests, sys
sys.stdout.reconfigure(encoding='utf-8')
from base64 import b64encode
from pathlib import Path

secrets = json.load(open(Path(__file__).parent.parent.parent / "config" / "secrets.json", encoding="utf-8"))
wp = secrets["wordpress"]
token = b64encode(f'{wp["username"]}:{wp["app_password"]}'.encode()).decode()
headers = {"Authorization": f"Basic {token}", "Content-Type": "application/json"}
base = "https://nambei-oyaji.com/wp-json/wp/v2"

# Get current single template
r = requests.get(f"{base}/templates/twentytwentyfive//single?context=edit", headers=headers)
content = r.json()["content"]["raw"]

# ============================================
# 1. Sidebar HTML (injected via wp:html block)
# ============================================
sidebar_html = '''
<!-- wp:html -->
<div class="nao-sidebar nao-sidebar-left" id="nao-sidebar-left">
  <div class="nao-sidebar-inner">
    <div class="nao-sidebar-section">
      <h4 class="nao-sidebar-heading">カテゴリー</h4>
      <ul class="nao-sidebar-list">
        <li><a href="/category/paraguay/">🇵🇾 パラグアイ生活<span class="nao-cat-count">6</span></a></li>
        <li><a href="/category/side-business/">💼 副業・稼ぎ方<span class="nao-cat-count">2</span></a></li>
        <li><a href="/category/ijuu-junbi/">✈️ 移住準備<span class="nao-cat-count">1</span></a></li>
      </ul>
    </div>
    <div class="nao-sidebar-section">
      <h4 class="nao-sidebar-heading">このブログについて</h4>
      <p class="nao-sidebar-text">パラグアイ在住の日本人が、海外移住・生活のリアルを発信しています。</p>
      <a href="/about/" class="nao-sidebar-link">プロフィールを見る →</a>
    </div>
  </div>
</div>
<!-- /wp:html -->

<!-- wp:html -->
<div class="nao-sidebar nao-sidebar-right" id="nao-sidebar-right">
  <div class="nao-sidebar-inner">
    <div class="nao-sidebar-section">
      <h4 class="nao-sidebar-heading">新着記事</h4>
      <ul class="nao-sidebar-posts">
        <li><a href="/category/paraguay/">パラグアイの食文化を在住者が解説</a></li>
        <li><a href="/kaigai-soukin-hikaku/">海外送金サービス徹底比較</a></li>
        <li><a href="/kaigai-ijuu-hatarakikata/">海外移住後の働き方</a></li>
        <li><a href="/kaigai-kosodate/">海外で子育て｜インター校事情</a></li>
        <li><a href="/paraguay-chian/">パラグアイの治安を本音で語る</a></li>
      </ul>
    </div>
    <div class="nao-sidebar-section nao-sidebar-sticky">
      <h4 class="nao-sidebar-heading">人気カテゴリー</h4>
      <div class="nao-sidebar-tags">
        <a href="/category/paraguay/" class="nao-tag">パラグアイ生活</a>
        <a href="/category/side-business/" class="nao-tag">副業・稼ぎ方</a>
        <a href="/category/ijuu-junbi/" class="nao-tag">移住準備</a>
      </div>
    </div>
  </div>
</div>
<!-- /wp:html -->'''

# ============================================
# 2. 3-column CSS (desktop only, 1200px+)
# ============================================
three_col_css = '''
<!-- wp:html -->
<style>
/* === 3-Column Layout (Desktop Only) === */
@media (min-width: 1200px) {
  /* Sidebars: hidden by default, shown on desktop */
  .nao-sidebar {
    display: block !important;
    position: fixed !important;
    top: 120px !important;
    width: 220px !important;
    max-height: calc(100vh - 160px) !important;
    overflow-y: auto !important;
    z-index: 10 !important;
    /* Thin scrollbar */
    scrollbar-width: thin;
    scrollbar-color: #d2d2d7 transparent;
  }
  .nao-sidebar::-webkit-scrollbar { width: 4px; }
  .nao-sidebar::-webkit-scrollbar-thumb { background: #d2d2d7; border-radius: 4px; }

  .nao-sidebar-left {
    left: max(16px, calc((100vw - 1200px) / 2 - 40px)) !important;
  }
  .nao-sidebar-right {
    right: max(16px, calc((100vw - 1200px) / 2 - 40px)) !important;
  }

  .nao-sidebar-inner {
    padding: 0 8px;
  }

  .nao-sidebar-heading {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #86868b !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    margin: 0 0 12px 0 !important;
    padding: 0 !important;
    border: none !important;
    background: none !important;
  }

  .nao-sidebar-section {
    margin-bottom: 32px;
  }

  .nao-sidebar-list {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  .nao-sidebar-list li {
    margin: 0 !important;
    padding: 0 !important;
  }
  .nao-sidebar-list li::before {
    display: none !important;
  }
  .nao-sidebar-list li a {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    padding: 8px 10px !important;
    font-size: 13px !important;
    color: #1d1d1f !important;
    text-decoration: none !important;
    border-radius: 8px !important;
    transition: background 0.2s ease !important;
    background: none !important;
    background-image: none !important;
  }
  .nao-sidebar-list li a:hover {
    background: #f5f5f7 !important;
    background-image: none !important;
  }
  .nao-cat-count {
    font-size: 11px;
    color: #86868b;
    background: #f5f5f7;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 500;
  }

  .nao-sidebar-posts {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  .nao-sidebar-posts li {
    margin: 0 !important;
    padding: 0 !important;
  }
  .nao-sidebar-posts li::before {
    display: none !important;
  }
  .nao-sidebar-posts li a {
    display: block !important;
    padding: 8px 10px !important;
    font-size: 13px !important;
    line-height: 1.4 !important;
    color: #1d1d1f !important;
    text-decoration: none !important;
    border-radius: 8px !important;
    transition: background 0.2s ease !important;
    background: none !important;
    background-image: none !important;
  }
  .nao-sidebar-posts li a:hover {
    background: #f5f5f7 !important;
    background-image: none !important;
  }

  .nao-sidebar-text {
    font-size: 13px !important;
    line-height: 1.6 !important;
    color: #6e6e73 !important;
    margin: 0 0 12px 0 !important;
    padding: 0 !important;
  }

  .nao-sidebar-link {
    font-size: 13px !important;
    color: #0066CC !important;
    text-decoration: none !important;
    font-weight: 500 !important;
    background: none !important;
    background-image: none !important;
  }
  .nao-sidebar-link:hover {
    text-decoration: underline !important;
    background-image: none !important;
  }

  .nao-sidebar-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .nao-tag {
    display: inline-block !important;
    padding: 5px 12px !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    color: #1d1d1f !important;
    background: #f5f5f7 !important;
    background-image: none !important;
    border-radius: 980px !important;
    text-decoration: none !important;
    transition: background 0.2s ease, color 0.2s ease !important;
  }
  .nao-tag:hover {
    background: #e8e8ed !important;
    background-image: none !important;
    color: #0066CC !important;
  }

  /* Sticky section within sidebar */
  .nao-sidebar-sticky {
    position: sticky;
    top: 0;
  }
}

/* Hide sidebars on mobile/tablet */
@media (max-width: 1199px) {
  .nao-sidebar {
    display: none !important;
  }
}
</style>
<!-- /wp:html -->'''

# ============================================
# 3. Insert sidebar HTML right after header, CSS at end
# ============================================

# Add sidebar HTML after header template part
header_end = '<!-- wp:template-part {"slug":"header","theme":"twentytwentyfive"} /-->'
new_content = content.replace(
    header_end,
    header_end + "\n" + sidebar_html
)

# Add 3-col CSS at the end
new_content = new_content + "\n" + three_col_css

# Post update
r2 = requests.post(
    f"{base}/templates/twentytwentyfive//single",
    headers=headers,
    json={"content": new_content}
)
print(f"Status: {r2.status_code}")
if r2.status_code == 200:
    print("3-column layout applied successfully!")
else:
    print(f"Error: {r2.text[:500]}")
