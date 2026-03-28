"""
Fiverr Gig自動出品スクリプト
Playwright でブラウザ操作し、Gig 3〜5を自動出品する。

使い方:
  python fiverr_auto_publish.py                  # Gig 3〜5を全部出品
  python fiverr_auto_publish.py --gig 3          # Gig 3のみ
  python fiverr_auto_publish.py --gig 4 --gig 5  # Gig 4と5
  python fiverr_auto_publish.py --dry-run         # Publishボタンを押さない確認モード
  python fiverr_auto_publish.py --login-only      # ログインだけして終了（セッション保存用）
"""

import argparse
import os
import sys
import time
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ---------------------------------------------------------------------------
# 定数
# ---------------------------------------------------------------------------
FIVERR_URL = "https://www.fiverr.com"
SESSION_DIR = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "fiverr_session"
SCREENSHOT_DIR = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "fiverr_screenshots"
BASE_DIR = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\research\freelance")

# 画像は日本語パスにあるためtempにコピーして使う
IMAGE_TEMP_DIR = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "fiverr_images"

# ---------------------------------------------------------------------------
# Gig定義データ
# ---------------------------------------------------------------------------
GIGS = {
    3: {
        "title": "I will build AI automation workflows using n8n zapier or python scripts",
        "category_path": ["Programming & Tech", "AI Development"],
        "subcategory": "AI Agents",
        "search_tags": [
            "ai automation",
            "n8n automation",
            "zapier expert",
            "python automation",
            "business automation",
        ],
        "description": (
            "🤖 AI Automation Expert | Save 10+ Hours/Week\n\n"
            "I build custom automation workflows that eliminate repetitive tasks.\n\n"
            "What I automate:\n"
            "✅ Lead generation & CRM updates\n"
            "✅ Social media scheduling & content repurposing\n"
            "✅ Email parsing & auto-responses\n"
            "✅ Data scraping & report generation\n"
            "✅ Inventory monitoring & alerts\n"
            "✅ SEO monitoring & competitor tracking\n"
            "✅ Invoice processing & bookkeeping prep\n\n"
            "Tools I work with:\n"
            "- n8n, Zapier, Make (Integromat)\n"
            "- Python scripts (custom automation)\n"
            "- Claude AI / OpenAI API integration\n"
            "- Google Sheets, Airtable, Notion\n"
            "- WordPress, Shopify, WooCommerce\n\n"
            "What you get:\n"
            "📋 Workflow documentation\n"
            "🎥 Loom video walkthrough\n"
            "🔧 30-day support after delivery\n\n"
            "I run 50+ automated tasks for my own businesses — I practice what I preach."
        ),
        "packages": {
            "basic": {
                "name": "Simple Automation",
                "description": "1 workflow (up to 3 steps)",
                "delivery_days": 3,
                "revisions": 1,
                "price": 80,
            },
            "standard": {
                "name": "Multi-Step Workflow",
                "description": "1 workflow (up to 10 steps + conditional logic)",
                "delivery_days": 5,
                "revisions": 2,
                "price": 200,
            },
            "premium": {
                "name": "Full System Setup",
                "description": "3-5 workflows + monitoring dashboard",
                "delivery_days": 10,
                "revisions": 3,
                "price": 500,
            },
        },
        "faqs": [
            {
                "question": "What tools do you use for automation?",
                "answer": "I primarily use n8n, Zapier, Make (Integromat), and custom Python scripts depending on your needs and budget.",
            },
            {
                "question": "Do I need to provide API keys?",
                "answer": "Yes, for services you want automated I'll need access credentials. I'll guide you through the setup securely.",
            },
            {
                "question": "Can you maintain the workflows after delivery?",
                "answer": "All packages include 30-day support. For ongoing maintenance, we can discuss a monthly retainer.",
            },
        ],
        "images": [
            BASE_DIR / "fiverr-gig3-automation.png",
            BASE_DIR / "fiverr-gig3-automation-2.png",
            BASE_DIR / "fiverr-gig3-automation-3.png",
        ],
    },
    4: {
        "title": "I will write SEO optimized japanese blog posts and articles",
        "category_path": ["Writing & Translation", "Articles & Blog Posts"],
        "subcategory": "Blog Posts",
        "search_tags": [
            "japanese seo",
            "japanese blog writing",
            "japanese content writer",
            "japan seo article",
            "japanese copywriter",
        ],
        "description": (
            "🇯🇵 Native Japanese SEO Writer | 300+ Articles Published\n\n"
            "I write search-engine-optimized Japanese articles that actually rank.\n\n"
            "What I write:\n"
            "✅ Blog posts & articles (any niche)\n"
            "✅ Product reviews & comparison articles\n"
            "✅ How-to guides & tutorials\n"
            "✅ Landing page copy\n"
            "✅ Meta titles & descriptions\n\n"
            "My SEO approach:\n"
            "- Keyword research using Japanese tools (Ubersuggest JP, Ahrefs, Google JP)\n"
            "- Search intent analysis for Japanese audience\n"
            "- E-E-A-T optimized structure\n"
            "- Internal linking strategy\n"
            "- Proper heading hierarchy (H1-H4)\n\n"
            "Track record:\n"
            "- 350+ articles published across 3 WordPress sites\n"
            "- Multiple #1 rankings on Google Japan\n"
            "- Experience in travel, tech, finance, and lifestyle niches\n\n"
            "Delivery: WordPress-ready HTML or Google Docs with images placement notes."
        ),
        "packages": {
            "basic": {
                "name": "Short Article",
                "description": "1000-character Japanese article with basic SEO",
                "delivery_days": 3,
                "revisions": 1,
                "price": 40,
            },
            "standard": {
                "name": "Full Article",
                "description": "3000-character Japanese article with full SEO optimization",
                "delivery_days": 5,
                "revisions": 2,
                "price": 80,
            },
            "premium": {
                "name": "Premium + KW Research",
                "description": "5000-character article + keyword research report",
                "delivery_days": 7,
                "revisions": 3,
                "price": 150,
            },
        },
        "faqs": [
            {
                "question": "Can you write in both Japanese and English?",
                "answer": "Yes, I'm a native Japanese speaker fluent in English. I can write bilingual content or translate between languages.",
            },
            {
                "question": "Do you provide keyword research?",
                "answer": "The Premium package includes keyword research. For Basic/Standard, I optimize for keywords you provide.",
            },
            {
                "question": "What format do you deliver?",
                "answer": "WordPress-ready HTML or Google Docs. I can also deliver in Markdown or plain text if preferred.",
            },
        ],
        "images": [
            BASE_DIR / "fiverr-gig4-seo-writing.png",
            BASE_DIR / "fiverr-gig4-seo-writing-2.png",
            BASE_DIR / "fiverr-gig4-seo-writing-3.png",
        ],
    },
    5: {
        "title": "I will scrape and collect data from japanese websites and databases",
        "category_path": ["Programming & Tech", "Data"],
        "subcategory": "Data Mining & Scraping",
        "search_tags": [
            "japanese web scraping",
            "japan data collection",
            "scrape japanese website",
            "japan data extraction",
            "japanese database",
        ],
        "description": (
            "🇯🇵 Japanese Web Scraping Expert | Data You Can't Get Elsewhere\n\n"
            "Need data from Japanese websites? I extract structured data from sources "
            "most scrapers can't handle.\n\n"
            "What I scrape:\n"
            "✅ E-commerce data (Rakuten, Amazon JP, Yahoo Shopping)\n"
            "✅ Company directories & business databases\n"
            "✅ Government & regulatory databases\n"
            "✅ Real estate listings (Suumo, Homes.co.jp)\n"
            "✅ Job listings (Indeed JP, Rikunabi)\n"
            "✅ Review sites & social media (Tabelog, Twitter JP)\n"
            "✅ Any Japanese website with structured data\n\n"
            "Deliverables:\n"
            "📊 Clean CSV/Excel/JSON file\n"
            "📋 Data dictionary explaining each field\n"
            "🔄 Optional: recurring scraping setup (weekly/monthly)\n\n"
            "Tech stack: Python (Scrapy, Selenium, Playwright), Apify, custom APIs\n\n"
            "Why me:\n"
            "- Native Japanese speaker — I understand the site structures\n"
            "- 6 Apify Actors published, 24 RapidAPIs built\n"
            "- Ethical scraping practices (respects robots.txt)"
        ),
        "packages": {
            "basic": {
                "name": "Small Scrape",
                "description": "1 website, up to 500 rows of data",
                "delivery_days": 3,
                "revisions": 1,
                "price": 50,
            },
            "standard": {
                "name": "Medium Dataset",
                "description": "1-2 websites, up to 2000 rows of data",
                "delivery_days": 5,
                "revisions": 2,
                "price": 100,
            },
            "premium": {
                "name": "Large Scale + Setup",
                "description": "3+ websites, up to 10000 rows + recurring scraping setup",
                "delivery_days": 7,
                "revisions": 3,
                "price": 250,
            },
        },
        "faqs": [
            {
                "question": "Is web scraping legal?",
                "answer": "I follow ethical scraping practices — respecting robots.txt, rate limits, and terms of service. I won't scrape personal/private data.",
            },
            {
                "question": "What format do you deliver data in?",
                "answer": "Clean CSV, Excel, or JSON — whichever you prefer. I include a data dictionary explaining each field.",
            },
            {
                "question": "Can you set up recurring scraping?",
                "answer": "Yes! The Premium package includes recurring scraping setup (weekly or monthly) using Apify or custom scripts.",
            },
        ],
        "images": [
            BASE_DIR / "fiverr-gig5-scraping.png",
            BASE_DIR / "fiverr-gig5-scraping-2.png",
            BASE_DIR / "fiverr-gig5-scraping-3.png",
        ],
    },
}


# ---------------------------------------------------------------------------
# ユーティリティ
# ---------------------------------------------------------------------------
def log(msg: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")


def screenshot(page, name: str) -> Path:
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"{ts}_{name}.png"
    page.screenshot(path=str(path), full_page=True)
    log(f"  screenshot → {path}")
    return path


def copy_images_to_temp(gig_data: dict) -> list[str]:
    """日本語パスの画像をtempにコピーし、コピー先パスのリストを返す。"""
    IMAGE_TEMP_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    for src in gig_data["images"]:
        if not src.exists():
            log(f"  WARNING: 画像が見つからない → {src}")
            continue
        dst = IMAGE_TEMP_DIR / src.name
        shutil.copy2(src, dst)
        copied.append(str(dst))
    return copied


def wait_between_gigs(seconds: int = 30) -> None:
    """Fiverr連続作成制限回避のためウェイト"""
    log(f"  Fiverr制限回避: {seconds}秒待機...")
    time.sleep(seconds)


def safe_click(page, selector: str, timeout: int = 10000) -> bool:
    """要素をクリック。見つからなければFalse。"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        page.click(selector)
        return True
    except PlaywrightTimeout:
        log(f"  WARNING: 要素が見つからない → {selector}")
        return False


def safe_fill(page, selector: str, text: str, timeout: int = 10000) -> bool:
    """テキスト入力。見つからなければFalse。"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        page.fill(selector, text)
        return True
    except PlaywrightTimeout:
        log(f"  WARNING: 入力フィールドが見つからない → {selector}")
        return False


def safe_type(page, selector: str, text: str, timeout: int = 10000, delay: int = 50) -> bool:
    """キーボード入力（fillが効かないフィールド用）。"""
    try:
        page.wait_for_selector(selector, timeout=timeout)
        page.click(selector)
        page.keyboard.type(text, delay=delay)
        return True
    except PlaywrightTimeout:
        log(f"  WARNING: 入力フィールドが見つからない → {selector}")
        return False


# ---------------------------------------------------------------------------
# ログイン
# ---------------------------------------------------------------------------
def login(page) -> bool:
    """Fiverrにログイン。セッション保存済みなら自動、なければ手動待機。"""
    page.goto(f"{FIVERR_URL}/", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # ログイン済みかチェック
    try:
        page.wait_for_selector('[class*="user-avatar"], [data-testid="header-user-avatar"], a[href*="/users/"]', timeout=5000)
        log("ログイン済み（セッション有効）")
        return True
    except PlaywrightTimeout:
        pass

    # 未ログイン → ログインページへ
    log("未ログイン → 手動ログインしてください")
    page.goto(f"{FIVERR_URL}/login", wait_until="domcontentloaded", timeout=30000)
    print("\n" + "=" * 60)
    print("ブラウザでFiverrにログインしてください。")
    print("ログイン完了後、ダッシュボードが表示されるまで待ちます。")
    print("2FA/CAPTCHA がある場合も手動で完了してください。")
    print("=" * 60 + "\n")

    # ダッシュボードに遷移するまで最大5分待つ
    try:
        page.wait_for_selector(
            '[class*="user-avatar"], [data-testid="header-user-avatar"], a[href*="/users/"]',
            timeout=300000,
        )
        log("ログイン成功！")
        time.sleep(2)
        return True
    except PlaywrightTimeout:
        log("ERROR: ログインタイムアウト（5分）")
        return False


# ---------------------------------------------------------------------------
# Gig作成メインフロー
# ---------------------------------------------------------------------------
def create_gig(page, gig_num: int, gig_data: dict, dry_run: bool = False) -> bool:
    """1つのGigを作成する。成功でTrue。"""
    log(f"=== Gig {gig_num} 作成開始: {gig_data['title'][:50]}... ===")

    # Gig作成ページへ
    page.goto(f"{FIVERR_URL}/seller_dashboard", wait_until="domcontentloaded", timeout=30000)
    time.sleep(3)

    # 「Create a New Gig」ボタンを探してクリック
    # Fiverrは頻繁にUIを変更するので複数セレクタを試す
    create_selectors = [
        'a[href*="/manage_gigs/new"]',
        'a:has-text("Create a New Gig")',
        'button:has-text("Create a New Gig")',
        '.create-new-gig',
        '[data-testid="create-gig"]',
    ]

    gig_page_opened = False
    for sel in create_selectors:
        try:
            page.wait_for_selector(sel, timeout=5000)
            page.click(sel)
            gig_page_opened = True
            break
        except PlaywrightTimeout:
            continue

    if not gig_page_opened:
        # 直接URLでアクセスを試みる
        log("  Create Gigボタンが見つからない → 直接URLでアクセス")
        page.goto(f"{FIVERR_URL}/manage_gigs/new", wait_until="domcontentloaded", timeout=30000)

    time.sleep(3)
    screenshot(page, f"gig{gig_num}_01_create_page")

    # ====== STEP 1: Overview ======
    log(f"  [Gig {gig_num}] Step 1: Overview")
    success = _fill_overview(page, gig_num, gig_data)
    if not success:
        log(f"  ERROR: Overview入力失敗")
        screenshot(page, f"gig{gig_num}_error_overview")
        return False
    screenshot(page, f"gig{gig_num}_02_overview_done")

    # Save & Continue
    if not _click_save_continue(page):
        log(f"  ERROR: Save & Continue失敗 (Overview)")
        screenshot(page, f"gig{gig_num}_error_save_overview")
        return False
    time.sleep(3)

    # ====== STEP 2: Pricing ======
    log(f"  [Gig {gig_num}] Step 2: Pricing")
    success = _fill_pricing(page, gig_num, gig_data)
    if not success:
        log(f"  ERROR: Pricing入力失敗")
        screenshot(page, f"gig{gig_num}_error_pricing")
        return False
    screenshot(page, f"gig{gig_num}_03_pricing_done")

    if not _click_save_continue(page):
        log(f"  ERROR: Save & Continue失敗 (Pricing)")
        screenshot(page, f"gig{gig_num}_error_save_pricing")
        return False
    time.sleep(3)

    # ====== STEP 3: Description & FAQ ======
    log(f"  [Gig {gig_num}] Step 3: Description & FAQ")
    success = _fill_description(page, gig_num, gig_data)
    if not success:
        log(f"  ERROR: Description入力失敗")
        screenshot(page, f"gig{gig_num}_error_description")
        return False
    screenshot(page, f"gig{gig_num}_04_description_done")

    if not _click_save_continue(page):
        log(f"  ERROR: Save & Continue失敗 (Description)")
        screenshot(page, f"gig{gig_num}_error_save_description")
        return False
    time.sleep(3)

    # ====== STEP 4: Requirements ======
    log(f"  [Gig {gig_num}] Step 4: Requirements (スキップ)")
    screenshot(page, f"gig{gig_num}_05_requirements")
    # Requirements は任意なのでそのまま Save & Continue
    if not _click_save_continue(page):
        log(f"  ERROR: Save & Continue失敗 (Requirements)")
        screenshot(page, f"gig{gig_num}_error_save_requirements")
        return False
    time.sleep(3)

    # ====== STEP 5: Gallery ======
    log(f"  [Gig {gig_num}] Step 5: Gallery")
    success = _fill_gallery(page, gig_num, gig_data)
    if not success:
        log(f"  WARNING: Gallery画像アップロードに問題あり（続行）")
    screenshot(page, f"gig{gig_num}_06_gallery_done")

    if not _click_save_continue(page):
        log(f"  ERROR: Save & Continue失敗 (Gallery)")
        screenshot(page, f"gig{gig_num}_error_save_gallery")
        return False
    time.sleep(3)

    # ====== STEP 6: Publish ======
    log(f"  [Gig {gig_num}] Step 6: Publish")
    screenshot(page, f"gig{gig_num}_07_pre_publish")

    if dry_run:
        log(f"  DRY RUN: Publishボタンは押しません")
        screenshot(page, f"gig{gig_num}_08_dry_run_done")
        return True

    # Publishボタン
    publish_selectors = [
        'button:has-text("Publish Gig")',
        'button:has-text("Publish")',
        '[data-testid="publish-gig"]',
        'button.btn-publish',
    ]
    published = False
    for sel in publish_selectors:
        try:
            page.wait_for_selector(sel, timeout=5000)
            page.click(sel)
            published = True
            break
        except PlaywrightTimeout:
            continue

    if not published:
        log(f"  ERROR: Publishボタンが見つからない")
        screenshot(page, f"gig{gig_num}_error_publish")
        return False

    time.sleep(5)
    screenshot(page, f"gig{gig_num}_08_published")
    log(f"  Gig {gig_num} 出品完了!")
    return True


# ---------------------------------------------------------------------------
# 各ステップの入力関数
# ---------------------------------------------------------------------------
def _fill_overview(page, gig_num: int, gig_data: dict) -> bool:
    """Overview: タイトル、カテゴリ、タグ"""
    time.sleep(2)

    # タイトル入力
    title_selectors = [
        '#title',
        'textarea[name="title"]',
        'input[name="title"]',
        '[data-testid="gig-title"]',
        'textarea[placeholder*="will"]',
        '.gig-title textarea',
        '.gig-title input',
    ]
    title_filled = False
    for sel in title_selectors:
        try:
            page.wait_for_selector(sel, timeout=3000)
            page.fill(sel, "")
            page.fill(sel, gig_data["title"])
            title_filled = True
            log(f"    タイトル入力完了")
            break
        except (PlaywrightTimeout, Exception):
            continue

    if not title_filled:
        # フォールバック: 最初のtextareaに入力
        try:
            textareas = page.query_selector_all("textarea")
            if textareas:
                textareas[0].fill(gig_data["title"])
                title_filled = True
                log(f"    タイトル入力完了（フォールバック）")
        except Exception:
            pass

    if not title_filled:
        log(f"    ERROR: タイトルフィールドが見つからない")
        return False

    time.sleep(1)

    # カテゴリ選択（ドロップダウン）
    # FiverrのUIは動的なのでテキストベースで選択を試みる
    _select_category(page, gig_data)
    time.sleep(1)

    # タグ入力
    _fill_tags(page, gig_data["search_tags"])
    time.sleep(1)

    return True


def _select_category(page, gig_data: dict) -> None:
    """カテゴリ・サブカテゴリを選択"""
    log(f"    カテゴリ選択: {' > '.join(gig_data['category_path'])}")

    # カテゴリドロップダウンを探す
    category_selectors = [
        'select[name="categoryId"]',
        '#categoryId',
        '[data-testid="category-select"]',
        '.category-select select',
    ]
    for sel in category_selectors:
        try:
            page.wait_for_selector(sel, timeout=3000)
            # ドロップダウンのオプションからテキストで選択
            options = page.query_selector_all(f"{sel} option")
            for opt in options:
                if gig_data["category_path"][0].lower() in (opt.inner_text() or "").lower():
                    page.select_option(sel, value=opt.get_attribute("value"))
                    log(f"    カテゴリ選択完了: {opt.inner_text()}")
                    break
            break
        except (PlaywrightTimeout, Exception):
            continue

    time.sleep(2)

    # サブカテゴリ
    sub_selectors = [
        'select[name="subCategoryId"]',
        '#subCategoryId',
        '[data-testid="subcategory-select"]',
        '.subcategory-select select',
    ]
    for sel in sub_selectors:
        try:
            page.wait_for_selector(sel, timeout=3000)
            options = page.query_selector_all(f"{sel} option")
            for opt in options:
                text = (opt.inner_text() or "").lower()
                if gig_data["category_path"][-1].lower() in text:
                    page.select_option(sel, value=opt.get_attribute("value"))
                    log(f"    サブカテゴリ選択完了: {opt.inner_text()}")
                    break
            break
        except (PlaywrightTimeout, Exception):
            continue

    time.sleep(1)

    # ネストされたサブカテゴリ（Service Type等）
    nested_selectors = [
        'select[name="nestedSubCategoryId"]',
        '#nestedSubCategoryId',
        'select[name="serviceTypeId"]',
    ]
    for sel in nested_selectors:
        try:
            page.wait_for_selector(sel, timeout=3000)
            options = page.query_selector_all(f"{sel} option")
            for opt in options:
                text = (opt.inner_text() or "").lower()
                if gig_data["subcategory"].lower() in text:
                    page.select_option(sel, value=opt.get_attribute("value"))
                    log(f"    サービスタイプ選択完了: {opt.inner_text()}")
                    break
            break
        except (PlaywrightTimeout, Exception):
            continue


def _fill_tags(page, tags: list[str]) -> None:
    """検索タグを入力"""
    log(f"    タグ入力: {len(tags)}個")

    tag_selectors = [
        'input[name="tags"]',
        'input[placeholder*="tag"]',
        'input[placeholder*="Tag"]',
        '.search-tags input',
        '[data-testid="tag-input"]',
        '.tags-input input',
    ]

    for sel in tag_selectors:
        try:
            page.wait_for_selector(sel, timeout=3000)
            for tag in tags:
                page.fill(sel, tag)
                time.sleep(0.3)
                page.keyboard.press("Enter")
                time.sleep(0.5)
            log(f"    タグ入力完了")
            return
        except (PlaywrightTimeout, Exception):
            continue

    log(f"    WARNING: タグ入力フィールドが見つからない")


def _fill_pricing(page, gig_num: int, gig_data: dict) -> bool:
    """Pricing: 3パッケージの価格・納期・リビジョン"""
    time.sleep(2)

    # パッケージテーブルが表示されるか確認
    # 「3 packages」トグルを有効化する場合
    toggle_selectors = [
        'input[type="checkbox"][name*="package"]',
        '.packages-toggle',
        'label:has-text("3 packages")',
        '[data-testid="packages-toggle"]',
    ]
    for sel in toggle_selectors:
        try:
            el = page.wait_for_selector(sel, timeout=3000)
            if el.is_visible():
                page.click(sel)
                log(f"    3パッケージモード有効化")
                time.sleep(2)
            break
        except (PlaywrightTimeout, Exception):
            continue

    packages = gig_data["packages"]

    for tier, tier_name in [("basic", "Basic"), ("standard", "Standard"), ("premium", "Premium")]:
        pkg = packages[tier]
        log(f"    {tier_name}: ${pkg['price']}, {pkg['delivery_days']}日, rev:{pkg['revisions']}")

        # パッケージ名
        name_selectors = [
            f'input[name*="{tier}"][name*="name"]',
            f'input[name*="{tier}"][name*="title"]',
            f'.{tier} input[name*="name"]',
            f'[data-testid="{tier}-name"]',
        ]
        for sel in name_selectors:
            if safe_fill(page, sel, pkg["name"], timeout=2000):
                break

        # 説明
        desc_selectors = [
            f'textarea[name*="{tier}"][name*="description"]',
            f'.{tier} textarea',
            f'[data-testid="{tier}-description"]',
        ]
        for sel in desc_selectors:
            if safe_fill(page, sel, pkg["description"], timeout=2000):
                break

        # 納期（ドロップダウン）
        delivery_selectors = [
            f'select[name*="{tier}"][name*="delivery"]',
            f'.{tier} select[name*="delivery"]',
            f'[data-testid="{tier}-delivery"]',
        ]
        for sel in delivery_selectors:
            try:
                page.wait_for_selector(sel, timeout=2000)
                page.select_option(sel, value=str(pkg["delivery_days"]))
                break
            except (PlaywrightTimeout, Exception):
                continue

        # リビジョン（ドロップダウン）
        rev_selectors = [
            f'select[name*="{tier}"][name*="revision"]',
            f'.{tier} select[name*="revision"]',
            f'[data-testid="{tier}-revisions"]',
        ]
        for sel in rev_selectors:
            try:
                page.wait_for_selector(sel, timeout=2000)
                page.select_option(sel, value=str(pkg["revisions"]))
                break
            except (PlaywrightTimeout, Exception):
                continue

        # 価格
        price_selectors = [
            f'input[name*="{tier}"][name*="price"]',
            f'.{tier} input[name*="price"]',
            f'[data-testid="{tier}-price"]',
        ]
        for sel in price_selectors:
            if safe_fill(page, sel, str(pkg["price"]), timeout=2000):
                break

    return True


def _fill_description(page, gig_num: int, gig_data: dict) -> bool:
    """Description & FAQ"""
    time.sleep(2)

    # Description入力
    desc_selectors = [
        '.gig-description textarea',
        'textarea[name="description"]',
        '#description',
        '[data-testid="gig-description"]',
        '.description-editor textarea',
        'div[contenteditable="true"]',
    ]
    desc_filled = False
    for sel in desc_selectors:
        try:
            page.wait_for_selector(sel, timeout=3000)
            el = page.query_selector(sel)
            if el.get_attribute("contenteditable") == "true":
                el.click()
                page.keyboard.type(gig_data["description"], delay=5)
            else:
                page.fill(sel, gig_data["description"])
            desc_filled = True
            log(f"    Description入力完了")
            break
        except (PlaywrightTimeout, Exception):
            continue

    if not desc_filled:
        # フォールバック
        try:
            textareas = page.query_selector_all("textarea")
            for ta in textareas:
                if ta.is_visible():
                    ta.fill(gig_data["description"])
                    desc_filled = True
                    log(f"    Description入力完了（フォールバック）")
                    break
        except Exception:
            pass

    if not desc_filled:
        log(f"    ERROR: Descriptionフィールドが見つからない")
        return False

    time.sleep(1)

    # FAQ入力
    for i, faq in enumerate(gig_data.get("faqs", [])):
        log(f"    FAQ {i + 1}: {faq['question'][:40]}...")

        # 「Add FAQ」ボタン
        add_faq_selectors = [
            'button:has-text("Add FAQ")',
            'a:has-text("Add FAQ")',
            '.add-faq',
            '[data-testid="add-faq"]',
            'button:has-text("Add")',
        ]
        for sel in add_faq_selectors:
            if safe_click(page, sel, timeout=3000):
                time.sleep(1)
                break

        # Question
        q_selectors = [
            f'input[name*="faq"][name*="question"]:nth-of-type({i + 1})',
            'input[name*="question"]:last-of-type',
            '.faq-question input:last-of-type',
            'input[placeholder*="question"]',
            'input[placeholder*="Question"]',
        ]
        for sel in q_selectors:
            if safe_fill(page, sel, faq["question"], timeout=2000):
                break

        # Answer
        a_selectors = [
            f'textarea[name*="faq"][name*="answer"]:nth-of-type({i + 1})',
            'textarea[name*="answer"]:last-of-type',
            '.faq-answer textarea:last-of-type',
            'textarea[placeholder*="answer"]',
            'textarea[placeholder*="Answer"]',
        ]
        for sel in a_selectors:
            if safe_fill(page, sel, faq["answer"], timeout=2000):
                break

        time.sleep(0.5)

    return True


def _fill_gallery(page, gig_num: int, gig_data: dict) -> bool:
    """Gallery: 画像アップロード"""
    time.sleep(2)

    # 画像をtempにコピー（日本語パス回避）
    image_paths = copy_images_to_temp(gig_data)
    if not image_paths:
        log(f"    WARNING: アップロードする画像がない")
        return False

    log(f"    画像 {len(image_paths)}枚をアップロード")

    # file input を探す
    file_input_selectors = [
        'input[type="file"][accept*="image"]',
        'input[type="file"]',
        '.upload-area input[type="file"]',
        '[data-testid="gallery-upload"] input[type="file"]',
    ]

    for img_path in image_paths:
        uploaded = False
        for sel in file_input_selectors:
            try:
                inputs = page.query_selector_all(sel)
                for inp in inputs:
                    if inp.is_visible() or True:  # hidden file inputs are normal
                        inp.set_input_files(img_path)
                        uploaded = True
                        log(f"    アップロード: {Path(img_path).name}")
                        time.sleep(3)  # アップロード待ち
                        break
                if uploaded:
                    break
            except Exception as e:
                log(f"    WARNING: アップロード失敗 ({sel}): {e}")
                continue

        if not uploaded:
            log(f"    WARNING: {Path(img_path).name} のアップロードに失敗")

    return True


def _click_save_continue(page) -> bool:
    """Save & Continue ボタンをクリック"""
    selectors = [
        'button:has-text("Save & Continue")',
        'button:has-text("Save")',
        'button[type="submit"]',
        '.save-continue',
        '[data-testid="save-continue"]',
        'button:has-text("Continue")',
    ]
    for sel in selectors:
        try:
            page.wait_for_selector(sel, timeout=5000)
            page.click(sel)
            log(f"    Save & Continue クリック")
            time.sleep(2)
            return True
        except PlaywrightTimeout:
            continue

    log(f"    WARNING: Save & Continueボタンが見つからない")
    return False


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Fiverr Gig自動出品スクリプト")
    parser.add_argument("--gig", type=int, action="append", help="出品するGig番号 (3〜5)。複数指定可")
    parser.add_argument("--dry-run", action="store_true", help="Publishボタンを押さない確認モード")
    parser.add_argument("--login-only", action="store_true", help="ログインだけして終了（セッション保存用）")
    parser.add_argument("--headless", action="store_true", help="ヘッドレスモード（デバッグ用、非推奨）")
    args = parser.parse_args()

    # 対象Gig決定
    target_gigs = args.gig if args.gig else [3, 4, 5]
    for g in target_gigs:
        if g not in GIGS:
            print(f"ERROR: Gig {g} は定義されていません（有効: {list(GIGS.keys())}）")
            sys.exit(1)

    log(f"対象Gig: {target_gigs}")
    log(f"dry-run: {args.dry_run}")
    log(f"セッション保存先: {SESSION_DIR}")
    log(f"スクリーンショット保存先: {SCREENSHOT_DIR}")

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=args.headless,
            viewport={"width": 1280, "height": 900},
            locale="en-US",
            args=[
                "--disable-blink-features=AutomationControlled",
            ],
        )
        page = browser.pages[0] if browser.pages else browser.new_page()

        # ログイン
        if not login(page):
            log("ログイン失敗。終了します。")
            browser.close()
            sys.exit(1)

        if args.login_only:
            log("ログイン完了。セッション保存済み。終了します。")
            browser.close()
            return

        # Gig作成
        results = {}
        for i, gig_num in enumerate(target_gigs):
            if i > 0:
                wait_between_gigs(30)

            try:
                success = create_gig(page, gig_num, GIGS[gig_num], dry_run=args.dry_run)
                results[gig_num] = "OK" if success else "FAILED"
            except Exception as e:
                log(f"ERROR: Gig {gig_num} で例外発生: {e}")
                screenshot(page, f"gig{gig_num}_exception")
                results[gig_num] = f"ERROR: {e}"

        browser.close()

    # 結果サマリ
    print("\n" + "=" * 60)
    print("結果サマリ")
    print("=" * 60)
    for gig_num, result in results.items():
        status = "✓" if result == "OK" else "✗"
        print(f"  Gig {gig_num}: [{status}] {result}")
    print(f"\nスクリーンショット: {SCREENSHOT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
