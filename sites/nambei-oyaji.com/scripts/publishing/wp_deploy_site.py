#!/usr/bin/env python3
"""
WordPress サイト一括デプロイスクリプト

「南米おやじのAI実践ラボ」の全固定ページ・カテゴリ・カスタムCSSを
WordPress REST API経由で一括作成・設定する。

使い方: python scripts/wp_deploy_site.py
"""

import json
import logging
import sys
import time
from base64 import b64encode
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "settings.json"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def wp_api(config):
    """WordPress API helper を返す"""
    wp = config["wordpress"]
    creds = b64encode(f"{wp['username']}:{wp['app_password']}".encode()).decode()
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
    }
    base = wp["rest_api_url"]
    return base, headers


def create_categories(base, headers):
    """カテゴリを作成し、IDマップを返す"""
    categories = [
        {"name": "AI活用", "slug": "ai", "description": "AIツール・AI副業の実践記録"},
        {"name": "パラグアイ生活", "slug": "paraguay", "description": "パラグアイ在住者のリアルな生活情報"},
        {"name": "副業・稼ぎ方", "slug": "side-business", "description": "海外からの副業・収益化ノウハウ"},
        {"name": "ツール比較", "slug": "tools", "description": "AI・副業ツールの正直レビュー"},
        {"name": "実験レポート", "slug": "report", "description": "月次収益・PVの実験報告"},
    ]

    cat_map = {}
    for cat in categories:
        r = requests.post(f"{base}/categories", headers=headers, json=cat, timeout=15)
        if r.status_code == 201:
            data = r.json()
            cat_map[cat["slug"]] = data["id"]
            logger.info(f"  カテゴリ作成: {cat['name']} (ID:{data['id']})")
        elif "term_exists" in r.text:
            existing_id = r.json().get("data", {}).get("term_id")
            if existing_id:
                cat_map[cat["slug"]] = existing_id
                logger.info(f"  カテゴリ既存: {cat['name']} (ID:{existing_id})")
        else:
            logger.warning(f"  カテゴリ作成失敗: {cat['name']} - {r.text[:200]}")
    return cat_map


def delete_default_content(base, headers):
    """デフォルトの「Hello world!」投稿と「Sample Page」を削除"""
    # Delete default post
    r = requests.delete(f"{base}/posts/1?force=true", headers=headers, timeout=15)
    if r.status_code == 200:
        logger.info("  デフォルト投稿「Hello world!」を削除")

    # Delete default page
    r = requests.delete(f"{base}/pages/2?force=true", headers=headers, timeout=15)
    if r.status_code == 200:
        logger.info("  デフォルトページ「Sample Page」を削除")


def create_page(base, headers, title, slug, content, status="publish", parent=0):
    """固定ページを作成"""
    data = {
        "title": title,
        "slug": slug,
        "content": content,
        "status": status,
        "parent": parent,
    }
    r = requests.post(f"{base}/pages", headers=headers, json=data, timeout=30)
    if r.status_code == 201:
        page = r.json()
        logger.info(f"  ページ作成: {title} (ID:{page['id']}) → {page['link']}")
        return page["id"]
    else:
        logger.error(f"  ページ作成失敗: {title} - {r.status_code} {r.text[:300]}")
        return None


def set_front_page(base, headers, page_id):
    """固定ページをフロントページに設定"""
    settings_url = base.replace("/wp/v2", "") + "/wp/v2/settings"
    data = {
        "show_on_front": "page",
        "page_on_front": page_id,
    }
    r = requests.post(settings_url, headers=headers, json=data, timeout=15)
    if r.status_code == 200:
        logger.info(f"  フロントページ設定: ID:{page_id}")
    else:
        logger.warning(f"  フロントページ設定失敗: {r.status_code} {r.text[:300]}")


def set_custom_css(base, headers, css):
    """カスタムCSSを設定 (カスタマイザー経由)"""
    customizer_url = base.replace("/wp/v2", "") + "/wp/v2/settings"
    # Cocoon theme stores custom CSS differently - try via custom CSS post type
    # First try the standard WordPress custom CSS approach
    data = {"custom_css_post_id": 0}

    # Create a custom CSS post
    css_post = {
        "title": "Custom CSS",
        "content": css,
        "status": "publish",
        "type": "custom_css",
    }
    # WordPress doesn't easily support custom CSS via REST API
    # Instead, we'll inject CSS into a reusable block or use a page approach
    logger.info("  カスタムCSS: 各ページのインラインスタイルとして埋め込み済み")


# ============================================
# PAGE CONTENT DEFINITIONS
# ============================================

def get_homepage_html():
    """トップページ HTML"""
    return """<!-- wp:html -->
<style>
:root {
  --nao-green-dark: #1B5E20;
  --nao-green: #2E7D32;
  --nao-green-light: #43A047;
  --nao-orange: #EF6C00;
  --nao-orange-light: #FF9800;
  --nao-gold: #FFB300;
  --nao-dark: #1A1A1A;
  --nao-text: #333333;
  --nao-text-light: #666666;
  --nao-bg: #FAFAF5;
  --nao-white: #FFFFFF;
  --nao-border: #E0DED6;
  --nao-shadow: 0 2px 16px rgba(0,0,0,0.08);
  --nao-radius: 12px;
}
.nao-home { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; color: var(--nao-text); line-height: 1.8; }
.nao-home *, .nao-home *::before, .nao-home *::after { box-sizing: border-box; }
.nao-full { width: 100vw; position: relative; left: 50%; transform: translateX(-50%); }
.nao-container { max-width: 1080px; margin: 0 auto; padding: 0 20px; }

/* HERO */
.nao-hero { background: linear-gradient(135deg, #0D3B0F 0%, var(--nao-green-dark) 40%, #1A472A 100%); padding: 100px 20px 90px; text-align: center; position: relative; overflow: hidden; }
.nao-hero::before { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(ellipse at 20% 50%, rgba(255,179,0,0.08) 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, rgba(67,160,71,0.12) 0%, transparent 50%); pointer-events: none; }
.nao-hero-content { position: relative; z-index: 1; max-width: 780px; margin: 0 auto; }
.nao-hero-badge { display: inline-block; background: rgba(255,179,0,0.15); border: 1px solid rgba(255,179,0,0.3); color: var(--nao-gold); font-size: 13px; font-weight: 600; padding: 6px 18px; border-radius: 50px; margin-bottom: 28px; }
.nao-hero h1 { color: var(--nao-white); font-size: clamp(32px, 6vw, 52px); font-weight: 900; line-height: 1.3; margin-bottom: 20px; }
.nao-hero h1 span { background: linear-gradient(90deg, var(--nao-gold), var(--nao-orange-light)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.nao-hero-sub { color: rgba(255,255,255,0.8); font-size: clamp(15px, 2.5vw, 18px); line-height: 1.9; margin-bottom: 40px; }
.nao-hero-buttons { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.nao-btn { display: inline-flex; align-items: center; gap: 8px; padding: 14px 32px; border-radius: 50px; font-size: 15px; font-weight: 700; text-decoration: none; transition: all 0.3s ease; border: none; cursor: pointer; }
.nao-btn-primary { background: linear-gradient(135deg, var(--nao-orange), var(--nao-orange-light)); color: var(--nao-white); box-shadow: 0 4px 20px rgba(239,108,0,0.35); }
.nao-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 28px rgba(239,108,0,0.45); color: #fff; }
.nao-btn-outline { background: transparent; color: var(--nao-white); border: 2px solid rgba(255,255,255,0.3); }
.nao-btn-outline:hover { border-color: rgba(255,255,255,0.6); background: rgba(255,255,255,0.05); color: #fff; }
.nao-hero-stats { display: flex; justify-content: center; gap: 48px; margin-top: 56px; padding-top: 36px; border-top: 1px solid rgba(255,255,255,0.1); }
.nao-hero-stat { text-align: center; }
.nao-hero-stat-num { display: block; color: var(--nao-gold); font-size: 28px; font-weight: 800; }
.nao-hero-stat-label { color: rgba(255,255,255,0.5); font-size: 12px; font-weight: 500; margin-top: 4px; display: block; }

/* FEATURES */
.nao-features { background: var(--nao-bg); padding: 72px 20px; }
.nao-features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; max-width: 1080px; margin: 0 auto; }
.nao-feature-card { background: var(--nao-white); border: 1px solid var(--nao-border); border-radius: var(--nao-radius); padding: 36px 28px; text-align: center; transition: all 0.3s ease; }
.nao-feature-card:hover { transform: translateY(-4px); box-shadow: var(--nao-shadow); }
.nao-feature-icon { font-size: 40px; margin-bottom: 16px; display: block; }
.nao-feature-card h3 { font-size: 18px; font-weight: 800; margin-bottom: 10px; color: var(--nao-dark); }
.nao-feature-card p { font-size: 14px; color: var(--nao-text-light); line-height: 1.8; margin: 0; }

/* SECTION HEADERS */
.nao-section-header { text-align: center; margin-bottom: 52px; }
.nao-section-label { display: inline-block; font-size: 13px; font-weight: 700; color: var(--nao-green); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; }
.nao-section-title { font-size: clamp(24px, 4vw, 36px); font-weight: 900; color: var(--nao-dark); line-height: 1.4; margin: 0; }
.nao-section-desc { font-size: 15px; color: var(--nao-text-light); max-width: 600px; margin: 12px auto 0; }

/* PILLARS */
.nao-pillars { background: var(--nao-white); padding: 80px 20px; }
.nao-pillars-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 32px; }
.nao-pillar-card { border-radius: var(--nao-radius); padding: 40px 32px; transition: transform 0.3s ease; }
.nao-pillar-card:hover { transform: translateY(-4px); }
.nao-pillar-card.--paraguay { background: linear-gradient(145deg, #E8F5E9 0%, #F1F8E9 100%); border: 1px solid #C8E6C9; }
.nao-pillar-card.--ai { background: linear-gradient(145deg, #FFF3E0 0%, #FFF8E1 100%); border: 1px solid #FFE0B2; }
.nao-pillar-emoji { font-size: 48px; margin-bottom: 20px; display: block; }
.nao-pillar-card h3 { font-size: 22px; font-weight: 800; margin-bottom: 12px; color: var(--nao-dark); }
.nao-pillar-card > p { font-size: 14px; color: var(--nao-text-light); margin-bottom: 24px; line-height: 1.8; }
.nao-pillar-topics { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }
.nao-pillar-topics li { font-size: 14px; color: var(--nao-text); padding-left: 24px; position: relative; }
.nao-pillar-topics li::before { content: '\\2713'; position: absolute; left: 0; font-weight: 700; }
.nao-pillar-card.--paraguay .nao-pillar-topics li::before { color: var(--nao-green); }
.nao-pillar-card.--ai .nao-pillar-topics li::before { color: var(--nao-orange); }

/* EXPERIMENT LOG */
.nao-log { background: var(--nao-white); padding: 80px 20px; }
.nao-log-timeline { max-width: 720px; margin: 0 auto; position: relative; padding-left: 40px; }
.nao-log-timeline::before { content: ''; position: absolute; left: 12px; top: 0; bottom: 0; width: 2px; background: linear-gradient(to bottom, var(--nao-green), var(--nao-orange)); border-radius: 2px; }
.nao-log-item { position: relative; margin-bottom: 36px; padding: 24px; background: var(--nao-bg); border-radius: var(--nao-radius); border: 1px solid var(--nao-border); }
.nao-log-item::before { content: ''; position: absolute; left: -34px; top: 30px; width: 12px; height: 12px; border-radius: 50%; background: var(--nao-green); border: 3px solid var(--nao-white); }
.nao-log-date { font-size: 12px; font-weight: 700; color: var(--nao-green); margin-bottom: 8px; }
.nao-log-item h4 { font-size: 16px; font-weight: 800; color: var(--nao-dark); margin: 0 0 8px 0; }
.nao-log-item p { font-size: 14px; color: var(--nao-text-light); line-height: 1.8; margin: 0; }

/* ABOUT */
.nao-about { background: var(--nao-bg); padding: 80px 20px; }
.nao-about-inner { max-width: 860px; margin: 0 auto; display: flex; gap: 48px; align-items: center; }
.nao-about-avatar { flex-shrink: 0; width: 180px; height: 180px; border-radius: 50%; background: linear-gradient(135deg, var(--nao-green-dark), var(--nao-green-light)); display: flex; align-items: center; justify-content: center; font-size: 72px; box-shadow: 0 8px 32px rgba(46,125,50,0.2); }
.nao-about-text h2 { font-size: 26px; font-weight: 900; color: var(--nao-dark); margin-bottom: 16px; }
.nao-about-text p { font-size: 15px; color: var(--nao-text-light); line-height: 2; margin-bottom: 12px; }
.nao-about-tags { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 20px; }
.nao-about-tag { display: inline-block; background: var(--nao-white); border: 1px solid var(--nao-border); border-radius: 50px; padding: 6px 16px; font-size: 13px; color: var(--nao-text-light); font-weight: 500; }

/* CTA */
.nao-cta { background: linear-gradient(135deg, var(--nao-dark) 0%, #2C2C2C 100%); padding: 72px 20px; text-align: center; }
.nao-cta-inner { max-width: 640px; margin: 0 auto; }
.nao-cta h2 { color: var(--nao-white); font-size: clamp(22px, 4vw, 32px); font-weight: 900; margin-bottom: 16px; }
.nao-cta p { color: rgba(255,255,255,0.6); font-size: 15px; margin-bottom: 32px; line-height: 1.8; }
.nao-cta-buttons { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.nao-btn-x { background: #000; color: #fff; box-shadow: 0 4px 16px rgba(0,0,0,0.3); }
.nao-btn-x:hover { background: #1A1A1A; transform: translateY(-2px); color: #fff; }

/* LATEST POSTS SECTION */
.nao-latest { background: var(--nao-bg); padding: 80px 20px; }
.nao-latest-note { text-align: center; padding: 40px; background: var(--nao-white); border-radius: var(--nao-radius); border: 2px dashed var(--nao-border); max-width: 600px; margin: 0 auto; }
.nao-latest-note p { color: var(--nao-text-light); font-size: 15px; margin: 0; line-height: 1.8; }

/* RESPONSIVE */
@media (max-width: 768px) {
  .nao-features-grid { grid-template-columns: 1fr; gap: 16px; }
  .nao-pillars-grid { grid-template-columns: 1fr; }
  .nao-about-inner { flex-direction: column; text-align: center; }
  .nao-about-tags { justify-content: center; }
  .nao-about-avatar { width: 140px; height: 140px; font-size: 56px; }
  .nao-hero-stats { gap: 24px; flex-wrap: wrap; }
  .nao-hero { padding: 72px 20px 64px; }
  .nao-log-timeline { padding-left: 32px; }
}
</style>

<div class="nao-home">

  <!-- HERO -->
  <section class="nao-hero nao-full">
    <div class="nao-hero-content">
      <div class="nao-hero-badge">&#127477;&#127486; パラグアイから発信中</div>
      <h1>南米おやじの<br><span>AI実践ラボ</span></h1>
      <p class="nao-hero-sub">
        パラグアイ在住の日本人が、AIを使って副業でどこまで稼げるか。<br>
        成功も失敗も、リアルな数字で全部見せる実験ログ。
      </p>
      <div class="nao-hero-buttons">
        <a href="/category/ai/" class="nao-btn nao-btn-primary">&#128214; 記事を読む</a>
        <a href="/about/" class="nao-btn nao-btn-outline">このサイトについて</a>
      </div>
      <div class="nao-hero-stats">
        <div class="nao-hero-stat">
          <span class="nao-hero-stat-num">&#127477;&#127486;</span>
          <span class="nao-hero-stat-label">パラグアイ在住</span>
        </div>
        <div class="nao-hero-stat">
          <span class="nao-hero-stat-num">AI</span>
          <span class="nao-hero-stat-label">完全AI活用</span>
        </div>
        <div class="nao-hero-stat">
          <span class="nao-hero-stat-num">&yen;0&rarr;</span>
          <span class="nao-hero-stat-label">ゼロから挑戦中</span>
        </div>
      </div>
    </div>
  </section>

  <!-- FEATURES -->
  <section class="nao-features nao-full">
    <div class="nao-features-grid">
      <div class="nao-feature-card">
        <span class="nao-feature-icon">&#128202;</span>
        <h3>リアルな数字で公開</h3>
        <p>収益・PV・かかった時間。都合の悪い数字も隠さず公開します。</p>
      </div>
      <div class="nao-feature-card">
        <span class="nao-feature-icon">&#129302;</span>
        <h3>AI徹底活用の実践記</h3>
        <p>ChatGPT、Claude、画像生成AI…最新ツールを試して本当に使えるものだけを紹介。</p>
      </div>
      <div class="nao-feature-card">
        <span class="nao-feature-icon">&#127758;</span>
        <h3>海外ならではの視点</h3>
        <p>南米パラグアイだからこそ見える世界。時差・言語・文化の壁を超えた副業のリアル。</p>
      </div>
    </div>
  </section>

  <!-- TWO PILLARS -->
  <section class="nao-pillars nao-full">
    <div class="nao-container">
      <div class="nao-section-header">
        <div class="nao-section-label">Contents</div>
        <h2 class="nao-section-title">2つのテーマで発信中</h2>
        <p class="nao-section-desc">パラグアイの生活情報と、AI副業の実践記録。この2本柱でお届けします。</p>
      </div>
      <div class="nao-pillars-grid">
        <div class="nao-pillar-card --paraguay">
          <span class="nao-pillar-emoji">&#127477;&#127486;</span>
          <h3>パラグアイ生活ガイド</h3>
          <p>移住10年超の経験を元に、ネットに出てこないリアルな情報を発信。</p>
          <ul class="nao-pillar-topics">
            <li>パラグアイ移住の費用とリアルな手続き</li>
            <li>現地の生活費を徹底公開（2026年版）</li>
            <li>永住権の取り方を完全ガイド</li>
            <li>日本人コミュニティと現地での暮らし</li>
          </ul>
        </div>
        <div class="nao-pillar-card --ai">
          <span class="nao-pillar-emoji">&#128640;</span>
          <h3>AI副業チャレンジ</h3>
          <p>AIツールを駆使して、海外から日本語で稼ぐ方法を実験中。</p>
          <ul class="nao-pillar-topics">
            <li>AI &times; ブログで月5万円を目指す全過程</li>
            <li>海外在住者におすすめの副業比較</li>
            <li>使って分かったAIツール正直レビュー</li>
            <li>デジタル商品の作り方と売り方</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- EXPERIMENT LOG -->
  <section class="nao-log nao-full">
    <div class="nao-container">
      <div class="nao-section-header">
        <div class="nao-section-label">Experiment Log</div>
        <h2 class="nao-section-title">実験ログ</h2>
        <p class="nao-section-desc">このサイト自体が実験です。立ち上げから収益化までの道のりを時系列で記録。</p>
      </div>
      <div class="nao-log-timeline">
        <div class="nao-log-item">
          <div class="nao-log-date">2026年3月 &mdash; Month 0</div>
          <h4>&#128295; プロジェクト始動</h4>
          <p>WordPressでサイト構築開始。AI（Claude）でコンテンツ自動生成の仕組みを作り、7つのAIエージェントを準備。目標は3ヶ月でデジタル商品2つ販売開始。</p>
        </div>
        <div class="nao-log-item">
          <div class="nao-log-date">Coming Soon &mdash; Month 1</div>
          <h4>&#128221; 最初の記事群を公開予定</h4>
          <p>パラグアイ系5記事 + AI副業系10記事を目標に執筆中。SEOで上位を取れるか？リアルタイムで報告します。</p>
        </div>
      </div>
    </div>
  </section>

  <!-- ABOUT PREVIEW -->
  <section class="nao-about nao-full" id="about">
    <div class="nao-container">
      <div class="nao-about-inner">
        <div class="nao-about-avatar">&#129492;</div>
        <div class="nao-about-text">
          <h2>南米おやじ について</h2>
          <p>パラグアイ在住の日本人。妻と娘2人の家族4人で南米に移住し、現地で暮らしています。</p>
          <p>「海外に住んでるおっさんが、AIの力を借りてどこまでやれるのか？」&mdash;&mdash;その答えを、このサイトで探していきます。</p>
          <div class="nao-about-tags">
            <span class="nao-about-tag">&#127477;&#127486; パラグアイ在住</span>
            <span class="nao-about-tag">&#129302; AI活用</span>
            <span class="nao-about-tag">&#128176; 副業実験中</span>
            <span class="nao-about-tag">&#128202; 数字で証明</span>
          </div>
          <div style="margin-top: 24px;">
            <a href="/about/" class="nao-btn nao-btn-primary" style="font-size: 14px; padding: 10px 24px;">プロフィールを詳しく見る &rarr;</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="nao-cta nao-full">
    <div class="nao-cta-inner">
      <h2>実験の続きが気になったら</h2>
      <p>毎週の実験報告・収益レポート・AI活用のTipsをXで発信中。<br>フォローして一緒に実験を見届けてください。</p>
      <div class="nao-cta-buttons">
        <a href="/category/ai/" class="nao-btn nao-btn-primary">記事一覧を見る &rarr;</a>
      </div>
    </div>
  </section>

</div>
<!-- /wp:html -->"""


def get_about_html():
    """プロフィールページ HTML"""
    return """<!-- wp:html -->
<style>
:root {
  --nao-green-dark: #1B5E20;
  --nao-green: #2E7D32;
  --nao-green-light: #43A047;
  --nao-orange: #EF6C00;
  --nao-orange-light: #FF9800;
  --nao-gold: #FFB300;
  --nao-dark: #1A1A1A;
  --nao-text: #333333;
  --nao-text-light: #666666;
  --nao-bg: #FAFAF5;
  --nao-white: #FFFFFF;
  --nao-border: #E0DED6;
  --nao-shadow: 0 2px 16px rgba(0,0,0,0.08);
  --nao-radius: 12px;
}
.nao-page { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; color: var(--nao-text); line-height: 1.8; }
.nao-page *, .nao-page *::before, .nao-page *::after { box-sizing: border-box; }
.nao-full { width: 100vw; position: relative; left: 50%; transform: translateX(-50%); }

/* PROFILE HERO */
.nao-profile-hero { background: linear-gradient(135deg, #0D3B0F 0%, var(--nao-green-dark) 40%, #1A472A 100%); padding: 80px 20px; text-align: center; }
.nao-profile-avatar { width: 160px; height: 160px; border-radius: 50%; background: linear-gradient(135deg, var(--nao-green), var(--nao-green-light)); display: flex; align-items: center; justify-content: center; font-size: 64px; margin: 0 auto 24px; box-shadow: 0 8px 32px rgba(0,0,0,0.3); border: 4px solid rgba(255,255,255,0.2); }
.nao-profile-hero h1 { color: var(--nao-white); font-size: 32px; font-weight: 900; margin-bottom: 8px; }
.nao-profile-hero .nao-subtitle { color: rgba(255,255,255,0.7); font-size: 16px; }
.nao-profile-tags { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-top: 20px; }
.nao-profile-tag { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2); color: rgba(255,255,255,0.8); border-radius: 50px; padding: 6px 16px; font-size: 13px; font-weight: 500; }

/* BIO SECTION */
.nao-bio { background: var(--nao-white); padding: 64px 20px; }
.nao-bio-inner { max-width: 760px; margin: 0 auto; }
.nao-bio h2 { font-size: 24px; font-weight: 900; color: var(--nao-dark); margin: 40px 0 16px; padding-bottom: 8px; border-bottom: 3px solid var(--nao-green); display: inline-block; }
.nao-bio h2:first-child { margin-top: 0; }
.nao-bio p { font-size: 15px; color: var(--nao-text); line-height: 2; margin-bottom: 16px; }

/* TIMELINE */
.nao-career { background: var(--nao-bg); padding: 64px 20px; }
.nao-career-inner { max-width: 760px; margin: 0 auto; }
.nao-career h2 { font-size: 24px; font-weight: 900; color: var(--nao-dark); margin-bottom: 32px; text-align: center; }
.nao-career-item { display: flex; gap: 24px; margin-bottom: 24px; padding: 24px; background: var(--nao-white); border-radius: var(--nao-radius); border: 1px solid var(--nao-border); }
.nao-career-year { flex-shrink: 0; font-size: 14px; font-weight: 800; color: var(--nao-green); min-width: 100px; padding-top: 2px; }
.nao-career-item h3 { font-size: 16px; font-weight: 800; color: var(--nao-dark); margin-bottom: 4px; }
.nao-career-item p { font-size: 14px; color: var(--nao-text-light); line-height: 1.7; margin: 0; }

/* SITE INFO */
.nao-site-info { background: var(--nao-white); padding: 64px 20px; }
.nao-site-info-inner { max-width: 760px; margin: 0 auto; }
.nao-site-info h2 { font-size: 24px; font-weight: 900; color: var(--nao-dark); margin-bottom: 24px; text-align: center; }
.nao-info-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
.nao-info-card { padding: 24px; background: var(--nao-bg); border-radius: var(--nao-radius); border: 1px solid var(--nao-border); text-align: center; }
.nao-info-card .icon { font-size: 32px; margin-bottom: 12px; display: block; }
.nao-info-card h3 { font-size: 16px; font-weight: 800; color: var(--nao-dark); margin-bottom: 8px; }
.nao-info-card p { font-size: 14px; color: var(--nao-text-light); line-height: 1.7; margin: 0; }

/* CTA */
.nao-about-cta { background: linear-gradient(135deg, var(--nao-dark) 0%, #2C2C2C 100%); padding: 56px 20px; text-align: center; }
.nao-about-cta h2 { color: var(--nao-white); font-size: 24px; font-weight: 900; margin-bottom: 16px; }
.nao-about-cta p { color: rgba(255,255,255,0.6); font-size: 15px; margin-bottom: 24px; }
.nao-about-cta a { display: inline-flex; align-items: center; gap: 8px; padding: 14px 32px; border-radius: 50px; font-size: 15px; font-weight: 700; text-decoration: none; background: linear-gradient(135deg, var(--nao-orange), var(--nao-orange-light)); color: #fff; box-shadow: 0 4px 20px rgba(239,108,0,0.35); transition: all 0.3s ease; }
.nao-about-cta a:hover { transform: translateY(-2px); color: #fff; }

@media (max-width: 768px) {
  .nao-career-item { flex-direction: column; gap: 8px; }
  .nao-info-grid { grid-template-columns: 1fr; }
  .nao-profile-hero { padding: 56px 20px; }
  .nao-profile-avatar { width: 120px; height: 120px; font-size: 48px; }
}
</style>

<div class="nao-page">

  <!-- PROFILE HERO -->
  <section class="nao-profile-hero nao-full">
    <div class="nao-profile-avatar">&#129492;</div>
    <h1>南米おやじ（水野 達也）</h1>
    <p class="nao-subtitle">パラグアイ在住 / AI副業実験家 / ブロガー</p>
    <div class="nao-profile-tags">
      <span class="nao-profile-tag">&#127477;&#127486; パラグアイ在住</span>
      <span class="nao-profile-tag">&#129302; AI活用歴 1年</span>
      <span class="nao-profile-tag">&#128176; 副業収益公開中</span>
    </div>
  </section>

  <!-- BIO -->
  <section class="nao-bio nao-full">
    <div class="nao-bio-inner">
      <h2>はじめまして</h2>
      <p>パラグアイ在住の日本人、南米おやじと申します。このサイト「南米おやじのAI実践ラボ」を運営しています。</p>
      <p>南米パラグアイに移住して10年以上。現地でいくつかのビジネスを経験し、2026年から本格的にAIを活用した副業実験をスタートしました。</p>

      <h2>なぜこのサイトを始めたのか</h2>
      <p>「海外に住んでるおっさんが、AIの力を借りてどこまで稼げるのか？」</p>
      <p>この素朴な疑問が、すべての始まりでした。ChatGPTやClaude、画像生成AIといったツールが次々と登場する中、「これを副業に使ったらどうなるんだろう？」と思ったのがきっかけです。</p>
      <p>ただの情報サイトではなく、<strong>実験ログ</strong>としてリアルな数字と過程を全部公開します。収益が0円の月も、失敗した施策も、すべて記録します。</p>

      <h2>このサイトで得られること</h2>
      <p>&#10004; AIを使った副業のリアルな実践記録（収益・PV・作業時間すべて公開）<br>
      &#10004; 海外在住者ならではの副業ノウハウ<br>
      &#10004; パラグアイの生活・移住に関するリアルな一次情報<br>
      &#10004; 本当に使えるAIツールの正直レビュー</p>
    </div>
  </section>

  <!-- CAREER -->
  <section class="nao-career nao-full">
    <div class="nao-career-inner">
      <h2>これまでの経歴</h2>
      <div class="nao-career-item">
        <div class="nao-career-year">2014-2015</div>
        <div>
          <h3>サッカークラブ設立（個人事業主）</h3>
          <p>瀬谷インターナショナルフットボール。ゼロから事業を立ち上げる経験を積む。</p>
        </div>
      </div>
      <div class="nao-career-item">
        <div class="nao-career-year">2015-2019</div>
        <div>
          <h3>パーソナルジム 店舗責任者</h3>
          <p>トゥエンティーフォーセブン。店舗運営・マネジメントを経験。</p>
        </div>
      </div>
      <div class="nao-career-item">
        <div class="nao-career-year">2020-2021</div>
        <div>
          <h3>リユース貿易 拠点責任者</h3>
          <p>三洋環境。海外貿易の現場で国際ビジネスを学ぶ。</p>
        </div>
      </div>
      <div class="nao-career-item">
        <div class="nao-career-year">2021-2023</div>
        <div>
          <h3>個別指導塾 教室長</h3>
          <p>D-ai。教育分野でのマネジメント経験。</p>
        </div>
      </div>
      <div class="nao-career-item">
        <div class="nao-career-year">2023-2025</div>
        <div>
          <h3>Amazon QA + チームマネージャー</h3>
          <p>Sutherland Global。リモートワーク×品質管理。</p>
        </div>
      </div>
      <div class="nao-career-item">
        <div class="nao-career-year">2025-現在</div>
        <div>
          <h3>フリーランス / AI副業実験家</h3>
          <p>オンラインセールス + AI活用のブログ運営。このサイトがまさにそれです。</p>
        </div>
      </div>
    </div>
  </section>

  <!-- SITE INFO -->
  <section class="nao-site-info nao-full">
    <div class="nao-site-info-inner">
      <h2>サイト情報</h2>
      <div class="nao-info-grid">
        <div class="nao-info-card">
          <span class="icon">&#128187;</span>
          <h3>運営環境</h3>
          <p>WordPress + ConoHa WING<br>テーマ: Cocoon<br>SEO: Rank Math</p>
        </div>
        <div class="nao-info-card">
          <span class="icon">&#129302;</span>
          <h3>AI活用</h3>
          <p>記事執筆補助: Claude API<br>KW調査: 自作ツール<br>画像: AI生成活用</p>
        </div>
        <div class="nao-info-card">
          <span class="icon">&#128200;</span>
          <h3>透明性</h3>
          <p>収益・PV・作業時間を<br>毎月レポートで公開</p>
        </div>
        <div class="nao-info-card">
          <span class="icon">&#128172;</span>
          <h3>お問い合わせ</h3>
          <p>ご質問・お仕事のご依頼は<br><a href="/contact/" style="color: var(--nao-green); font-weight: 700;">お問い合わせフォーム</a>から</p>
        </div>
      </div>
    </div>
  </section>

  <!-- CTA -->
  <section class="nao-about-cta nao-full">
    <h2>実験の行方が気になったら</h2>
    <p>最新の記事やレポートをチェックしてください</p>
    <a href="/category/ai/">記事一覧を見る &rarr;</a>
  </section>

</div>
<!-- /wp:html -->"""


def get_contact_html():
    """お問い合わせページ HTML"""
    return """<!-- wp:html -->
<style>
:root {
  --nao-green-dark: #1B5E20;
  --nao-green: #2E7D32;
  --nao-orange: #EF6C00;
  --nao-dark: #1A1A1A;
  --nao-text: #333333;
  --nao-text-light: #666666;
  --nao-bg: #FAFAF5;
  --nao-white: #FFFFFF;
  --nao-border: #E0DED6;
  --nao-radius: 12px;
}
.nao-contact { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; color: var(--nao-text); line-height: 1.8; max-width: 720px; margin: 0 auto; padding: 40px 20px; }
.nao-contact h2 { font-size: 28px; font-weight: 900; color: var(--nao-dark); margin-bottom: 16px; text-align: center; }
.nao-contact > p { text-align: center; color: var(--nao-text-light); font-size: 15px; margin-bottom: 40px; }
.nao-contact-form { background: var(--nao-white); border: 1px solid var(--nao-border); border-radius: var(--nao-radius); padding: 40px; }
.nao-form-group { margin-bottom: 24px; }
.nao-form-group label { display: block; font-size: 14px; font-weight: 700; color: var(--nao-dark); margin-bottom: 8px; }
.nao-form-group label .required { color: #e53935; margin-left: 4px; font-size: 12px; }
.nao-form-group input, .nao-form-group textarea, .nao-form-group select { width: 100%; padding: 12px 16px; border: 1px solid var(--nao-border); border-radius: 8px; font-size: 15px; font-family: inherit; transition: border-color 0.3s; background: var(--nao-bg); }
.nao-form-group input:focus, .nao-form-group textarea:focus, .nao-form-group select:focus { outline: none; border-color: var(--nao-green); box-shadow: 0 0 0 3px rgba(46,125,50,0.1); }
.nao-form-group textarea { min-height: 160px; resize: vertical; }
.nao-form-submit { display: block; width: 100%; padding: 16px; background: linear-gradient(135deg, var(--nao-green-dark), var(--nao-green)); color: #fff; border: none; border-radius: 50px; font-size: 16px; font-weight: 700; cursor: pointer; transition: all 0.3s; font-family: inherit; }
.nao-form-submit:hover { transform: translateY(-2px); box-shadow: 0 4px 20px rgba(46,125,50,0.3); }
.nao-contact-note { margin-top: 32px; padding: 20px; background: var(--nao-bg); border-radius: var(--nao-radius); border: 1px solid var(--nao-border); }
.nao-contact-note h3 { font-size: 15px; font-weight: 800; color: var(--nao-dark); margin-bottom: 8px; }
.nao-contact-note p { font-size: 13px; color: var(--nao-text-light); margin: 0; line-height: 1.8; }
</style>

<div class="nao-contact">
  <h2>お問い合わせ</h2>
  <p>ご質問・ご感想・お仕事のご依頼など、お気軽にどうぞ。<br>通常2-3営業日以内にご返信します。</p>

  <div class="nao-contact-form">
    <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
      <div class="nao-form-group">
        <label>お名前<span class="required">*必須</span></label>
        <input type="text" name="name" required placeholder="例: 山田 太郎">
      </div>
      <div class="nao-form-group">
        <label>メールアドレス<span class="required">*必須</span></label>
        <input type="email" name="email" required placeholder="例: your@email.com">
      </div>
      <div class="nao-form-group">
        <label>お問い合わせ種別</label>
        <select name="type">
          <option value="question">ご質問・ご相談</option>
          <option value="feedback">ご感想・フィードバック</option>
          <option value="business">お仕事のご依頼</option>
          <option value="other">その他</option>
        </select>
      </div>
      <div class="nao-form-group">
        <label>メッセージ<span class="required">*必須</span></label>
        <textarea name="message" required placeholder="お問い合わせ内容をご記入ください"></textarea>
      </div>
      <button type="submit" class="nao-form-submit">送信する</button>
    </form>
  </div>

  <div class="nao-contact-note">
    <h3>&#9888;&#65039; ご注意</h3>
    <p>
      ・いただいたメールアドレスは、ご返信の目的のみに使用します。<br>
      ・営業メールや迷惑メールはお断りしております。<br>
      ・パラグアイとの時差（日本より12時間遅れ）があるため、ご返信に少しお時間をいただく場合があります。
    </p>
  </div>
</div>
<!-- /wp:html -->"""


def get_privacy_html():
    """プライバシーポリシーページ HTML"""
    return """<!-- wp:html -->
<style>
:root {
  --nao-dark: #1A1A1A;
  --nao-text: #333333;
  --nao-text-light: #666666;
  --nao-bg: #FAFAF5;
  --nao-white: #FFFFFF;
  --nao-border: #E0DED6;
  --nao-green: #2E7D32;
  --nao-radius: 12px;
}
.nao-legal { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; color: var(--nao-text); line-height: 2; max-width: 760px; margin: 0 auto; padding: 40px 20px; }
.nao-legal h1 { font-size: 28px; font-weight: 900; color: var(--nao-dark); margin-bottom: 8px; text-align: center; }
.nao-legal .updated { text-align: center; color: var(--nao-text-light); font-size: 13px; margin-bottom: 40px; display: block; }
.nao-legal h2 { font-size: 20px; font-weight: 800; color: var(--nao-dark); margin: 36px 0 12px; padding-left: 12px; border-left: 4px solid var(--nao-green); }
.nao-legal p { font-size: 15px; margin-bottom: 12px; }
.nao-legal ul { padding-left: 24px; margin-bottom: 16px; }
.nao-legal li { font-size: 15px; margin-bottom: 6px; }
.nao-legal a { color: var(--nao-green); }
</style>

<div class="nao-legal">
  <h1>プライバシーポリシー</h1>
  <span class="updated">最終更新日: 2026年3月3日</span>

  <p>「南米おやじのAI実践ラボ」（以下「当サイト」、URL: https://nambei-oyaji.com）では、ユーザーのプライバシーを尊重し、個人情報の保護に努めています。</p>

  <h2>個人情報の収集</h2>
  <p>当サイトでは、お問い合わせフォームでのご連絡時に、以下の個人情報を取得する場合があります。</p>
  <ul>
    <li>お名前</li>
    <li>メールアドレス</li>
    <li>お問い合わせ内容</li>
  </ul>

  <h2>個人情報の利用目的</h2>
  <p>取得した個人情報は、以下の目的でのみ利用します。</p>
  <ul>
    <li>お問い合わせへのご返信</li>
    <li>サービスに関するご案内（ご本人の同意がある場合のみ）</li>
  </ul>

  <h2>個人情報の第三者提供</h2>
  <p>法令に基づく場合を除き、ご本人の同意なく個人情報を第三者に提供することはありません。</p>

  <h2>Cookieの使用</h2>
  <p>当サイトでは、ユーザー体験の向上や効果測定のためにCookieを使用しています。ブラウザの設定によりCookieの受け入れを拒否できますが、一部機能が利用できなくなる場合があります。</p>

  <h2>アクセス解析ツール</h2>
  <p>当サイトでは、Googleアナリティクス（GA4）を使用しています。Googleアナリティクスは、Cookieを使用してユーザーのアクセス情報を収集します。このデータは匿名で収集されており、個人を特定するものではありません。</p>
  <p>詳しくは<a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">Googleのサービスを使用するサイトやアプリから収集した情報のGoogleによる使用</a>をご覧ください。</p>

  <h2>広告について</h2>
  <p>当サイトでは、第三者配信の広告サービス（Google AdSense、A8.net等のアフィリエイトプログラム）を利用しています。</p>
  <p>これらの広告配信事業者は、ユーザーの興味に応じた広告を表示するためにCookieを使用することがあります。Google AdSenseにおける広告配信については、<a href="https://policies.google.com/technologies/ads" target="_blank" rel="noopener">Google広告に関するポリシー</a>をご覧ください。</p>

  <h2>アフィリエイトプログラム</h2>
  <p>当サイトは、以下のアフィリエイトプログラムに参加しています。</p>
  <ul>
    <li>A8.net</li>
    <li>もしもアフィリエイト</li>
  </ul>
  <p>記事内のリンクを通じて商品・サービスをお申し込みいただくと、当サイトに報酬が支払われる場合があります。</p>

  <h2>免責事項</h2>
  <p>当サイトの情報は、可能な限り正確な情報を提供するよう努めていますが、正確性や安全性を保証するものではありません。当サイトの情報を利用することで生じた損害について、一切の責任を負いかねます。</p>
  <p>また、当サイトからリンクやバナーなどで移動した先のサイトの情報やサービスについても責任を負いません。</p>

  <h2>著作権</h2>
  <p>当サイトのコンテンツ（文章・画像・デザイン等）の著作権は、当サイト運営者に帰属します。無断転載・複製を禁じます。引用する場合は、出典元として当サイトへのリンクを明記してください。</p>

  <h2>お問い合わせ</h2>
  <p>プライバシーポリシーに関するお問い合わせは、<a href="/contact/">お問い合わせページ</a>よりお願いいたします。</p>

  <p style="margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--nao-border); font-size: 14px; color: var(--nao-text-light);">
    運営者: 南米おやじのAI実践ラボ<br>
    URL: https://nambei-oyaji.com
  </p>
</div>
<!-- /wp:html -->"""


def get_sitemap_html():
    """サイトマップページ HTML"""
    return """<!-- wp:html -->
<style>
:root {
  --nao-dark: #1A1A1A;
  --nao-text: #333333;
  --nao-text-light: #666666;
  --nao-green: #2E7D32;
  --nao-bg: #FAFAF5;
  --nao-white: #FFFFFF;
  --nao-border: #E0DED6;
  --nao-radius: 12px;
}
.nao-sitemap { font-family: 'Noto Sans JP', -apple-system, BlinkMacSystemFont, sans-serif; color: var(--nao-text); line-height: 1.8; max-width: 760px; margin: 0 auto; padding: 40px 20px; }
.nao-sitemap h1 { font-size: 28px; font-weight: 900; color: var(--nao-dark); margin-bottom: 40px; text-align: center; }
.nao-sitemap-section { margin-bottom: 32px; }
.nao-sitemap-section h2 { font-size: 18px; font-weight: 800; color: var(--nao-dark); margin-bottom: 16px; padding-left: 12px; border-left: 4px solid var(--nao-green); }
.nao-sitemap-section ul { list-style: none; padding: 0; margin: 0; }
.nao-sitemap-section li { padding: 8px 0; border-bottom: 1px solid var(--nao-border); }
.nao-sitemap-section li:last-child { border-bottom: none; }
.nao-sitemap-section a { color: var(--nao-text); text-decoration: none; font-size: 15px; transition: color 0.2s; }
.nao-sitemap-section a:hover { color: var(--nao-green); }
.nao-sitemap-section .desc { color: var(--nao-text-light); font-size: 13px; margin-left: 8px; }
</style>

<div class="nao-sitemap">
  <h1>サイトマップ</h1>

  <div class="nao-sitemap-section">
    <h2>固定ページ</h2>
    <ul>
      <li><a href="/">トップページ</a><span class="desc">- サイトのホーム</span></li>
      <li><a href="/about/">プロフィール</a><span class="desc">- 運営者について</span></li>
      <li><a href="/contact/">お問い合わせ</a><span class="desc">- ご連絡はこちら</span></li>
      <li><a href="/privacy-policy/">プライバシーポリシー</a><span class="desc">- 個人情報の取り扱い</span></li>
    </ul>
  </div>

  <div class="nao-sitemap-section">
    <h2>カテゴリー</h2>
    <ul>
      <li><a href="/category/ai/">AI活用</a><span class="desc">- AIツール・AI副業の実践記録</span></li>
      <li><a href="/category/paraguay/">パラグアイ生活</a><span class="desc">- パラグアイ在住者のリアルな生活情報</span></li>
      <li><a href="/category/side-business/">副業・稼ぎ方</a><span class="desc">- 海外からの副業・収益化ノウハウ</span></li>
      <li><a href="/category/tools/">ツール比較</a><span class="desc">- AI・副業ツールの正直レビュー</span></li>
      <li><a href="/category/report/">実験レポート</a><span class="desc">- 月次収益・PVの実験報告</span></li>
    </ul>
  </div>
</div>
<!-- /wp:html -->"""


# ============================================
# MAIN
# ============================================

def main():
    logger.info("=" * 60)
    logger.info("南米おやじのAI実践ラボ — サイト一括デプロイ開始")
    logger.info("=" * 60)

    config = load_config()
    base, headers = wp_api(config)

    # 1. デフォルトコンテンツ削除
    logger.info("\n[1/5] デフォルトコンテンツ削除")
    delete_default_content(base, headers)

    # 2. カテゴリ作成
    logger.info("\n[2/5] カテゴリ作成")
    cat_map = create_categories(base, headers)
    logger.info(f"  作成済みカテゴリ: {cat_map}")

    # 3. 固定ページ作成
    logger.info("\n[3/5] 固定ページ作成")

    pages = [
        ("トップページ", "home", get_homepage_html()),
        ("プロフィール", "about", get_about_html()),
        ("お問い合わせ", "contact", get_contact_html()),
        ("プライバシーポリシー", "privacy-policy", get_privacy_html()),
        ("サイトマップ", "sitemap", get_sitemap_html()),
    ]

    page_ids = {}
    for title, slug, content in pages:
        pid = create_page(base, headers, title, slug, content)
        if pid:
            page_ids[slug] = pid
        time.sleep(0.5)  # API rate limit対策

    # 4. フロントページ設定
    logger.info("\n[4/5] フロントページ設定")
    if "home" in page_ids:
        set_front_page(base, headers, page_ids["home"])

    # 5. サマリー
    logger.info("\n[5/5] デプロイ完了サマリー")
    logger.info("=" * 60)
    logger.info(f"  カテゴリ: {len(cat_map)}件作成")
    logger.info(f"  固定ページ: {len(page_ids)}件作成")
    for slug, pid in page_ids.items():
        logger.info(f"    - {slug}: https://nambei-oyaji.com/{slug}/ (ID:{pid})")
    logger.info(f"\n  フロントページ: https://nambei-oyaji.com/")
    logger.info("=" * 60)
    logger.info("WordPress管理画面で表示を確認してください。")
    logger.info("  管理画面: https://nambei-oyaji.com/wp-admin/")


if __name__ == "__main__":
    main()
