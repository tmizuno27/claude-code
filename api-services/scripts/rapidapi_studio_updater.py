#!/usr/bin/env python3
"""RapidAPI Studio 全API リスティング自動更新スクリプト (v2)

全カードを順番にクリックし、Base URLでJSONとマッチングする方式。
Chrome --remote-debugging-port=9222 で起動済みであること。
"""

import json
import os
import sys
import time
import glob
from datetime import datetime
from playwright.sync_api import sync_playwright

STUDIO_URL = "https://rapidapi.com/studio/"
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
WAIT_BETWEEN_APIS = 3

os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def take_screenshot(page, name):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(SCREENSHOT_DIR, f"{ts}_{name}.png")
    try:
        page.screenshot(path=path, full_page=False)
    except:
        pass


def load_listings():
    base = os.path.dirname(os.path.dirname(__file__))
    listings = {}
    for d in sorted(glob.glob(os.path.join(base, "[0-9]*"))):
        jf = os.path.join(d, "rapidapi-listing.json")
        if os.path.exists(jf):
            with open(jf, "r", encoding="utf-8") as f:
                data = json.load(f)
                dirname = os.path.basename(d)
                # "01-qr-code-api" -> "qr-code-api" (番号プレフィックス除去)
                key = "-".join(dirname.split("-")[1:])
                listings[key] = {
                    "data": data,
                    "dir": dirname,
                    "path": jf,
                    "name": data.get("name", ""),
                }
    return listings


def dismiss_cookie_dialog(page):
    """Cookie同意ダイアログを閉じる"""
    try:
        for btn_text in ["Accept All", "Accept all", "Accept", "Reject All", "OK", "Close"]:
            btn = page.get_by_role("button", name=btn_text)
            if btn.is_visible(timeout=1000):
                btn.click()
                time.sleep(1)
                print("  Cookie同意ダイアログを閉じました")
                return
        # ボタンが見つからない場合、OneTrustのAcceptボタンを試す
        ot_btn = page.locator('#onetrust-accept-btn-handler')
        if ot_btn.is_visible(timeout=1000):
            ot_btn.click()
            time.sleep(1)
            print("  Cookie同意ダイアログを閉じました (OneTrust)")
    except:
        pass


def update_api_page(page, listing_data, card_index):
    """現在開いているHub Listing > General ページを更新する"""
    result = {"details": []}
    data = listing_data["data"]

    # Short Description
    short_desc = data.get("description", "")
    if short_desc:
        try:
            label = page.get_by_text("Short Description")
            # ラベルの次のtextareaを探す
            textarea = page.locator('textarea').nth(0)
            if textarea.is_visible(timeout=3000):
                textarea.click()
                time.sleep(0.3)
                textarea.fill("")
                time.sleep(0.2)
                textarea.fill(short_desc)
                time.sleep(0.5)
                # フォーカスを外して保存をトリガー
                page.keyboard.press("Tab")
                time.sleep(1)
                print(f"    [OK] Short Description")
                result["details"].append("short: OK")
            else:
                print(f"    [WARN] Short Description textarea not visible")
                result["details"].append("short: NOT_FOUND")
        except Exception as e:
            print(f"    [WARN] Short Description error: {e}")
            result["details"].append(f"short: ERROR")

    # Long Description
    long_desc = data.get("long_description", "")
    if long_desc:
        try:
            textarea = page.locator('textarea').nth(1)
            if textarea.is_visible(timeout=3000):
                textarea.click()
                time.sleep(0.3)
                textarea.fill("")
                time.sleep(0.2)
                textarea.fill(long_desc)
                time.sleep(0.5)
                page.keyboard.press("Tab")
                time.sleep(1)
                print(f"    [OK] Long Description")
                result["details"].append("long: OK")
            else:
                print(f"    [WARN] Long Description textarea not visible")
                result["details"].append("long: NOT_FOUND")
        except Exception as e:
            print(f"    [WARN] Long Description error: {e}")
            result["details"].append(f"long: ERROR")

    # Visibility - Private -> Public
    try:
        private_text = page.get_by_text("API Project is Private")
        if private_text.is_visible(timeout=2000):
            # チェックボックスをチェック
            checkbox = page.locator('input[type="checkbox"]').first
            if checkbox.is_visible(timeout=2000):
                checkbox.check()
                time.sleep(0.5)
            # トグルスイッチをクリック
            toggle = private_text.locator("..").locator("..").locator('[role="switch"], input[type="checkbox"], [class*="toggle"], [class*="Toggle"]').first
            if toggle.is_visible(timeout=2000):
                toggle.click()
                time.sleep(1)
                print(f"    [OK] Visibility -> Public")
                result["details"].append("visibility: Public")
            else:
                print(f"    [INFO] Toggle not found, trying other approach...")
                # ページ内のすべてのトグル/スイッチを探す
                page.evaluate('''() => {
                    const toggles = document.querySelectorAll('[role="switch"], .toggle, [class*="Toggle"]');
                    toggles.forEach(t => { if(t.offsetParent !== null) t.click(); });
                }''')
                time.sleep(1)
                result["details"].append("visibility: attempted")
        else:
            public_text = page.get_by_text("API Project is Public")
            if public_text.is_visible(timeout=1000):
                print(f"    [OK] Already Public")
                result["details"].append("visibility: already_public")
    except:
        result["details"].append("visibility: skip")

    # Save ボタンがあればクリック
    try:
        for btn_text in ["Save", "save", "Update"]:
            btn = page.get_by_role("button", name=btn_text)
            if btn.is_visible(timeout=1000):
                btn.click()
                time.sleep(2)
                print(f"    [OK] Save clicked")
                result["details"].append("save: OK")
                break
    except:
        pass

    return result


def main():
    print("=" * 60)
    print("RapidAPI Studio 全API リスティング自動更新 (v2)")
    print("=" * 60)

    # リスティング読み込み
    listings = load_listings()
    print(f"\n{len(listings)} 件の listing.json を読み込みました")
    for sub, info in listings.items():
        print(f"  {sub} -> {info['data'].get('name', '?')}")

    with sync_playwright() as p:
        print("\nChrome (port 9222) に接続中...")
        try:
            browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        except Exception as e:
            print(f"\nエラー: Chrome に接続できません。")
            print(f'先に以下でChromeを起動: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir=C:\\Users\\tmizu\\chrome-debug-profile https://rapidapi.com/studio/')
            sys.exit(1)

        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()

        # Studio に遷移
        print("\nRapidAPI Studio を開いています...")
        page.goto(STUDIO_URL, wait_until="domcontentloaded", timeout=30000)
        time.sleep(5)

        # Cookie同意ダイアログを閉じる
        dismiss_cookie_dialog(page)
        time.sleep(2)

        take_screenshot(page, "00_studio_list")

        # 全カードのリンクを収集
        print("\nAPI カードを収集中...")

        # スクロールして全カードを表示
        for _ in range(10):
            page.evaluate("window.scrollBy(0, 500)")
            time.sleep(0.5)
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(2)

        # APIカードを収集（Cookie/Privacy関連を除外）
        card_links = page.evaluate('''() => {
            const links = [];
            const skipTexts = ['privacy', 'cookie', 'consent', 'manage', 'preference'];

            // 方法1: Studio内のAPIプロジェクトリンク
            document.querySelectorAll('a[href*="/studio/"]').forEach(a => {
                const href = a.getAttribute('href') || '';
                const text = a.textContent.trim();
                // /studio/ 直下ではなく、/studio/xxx/ のようなAPI個別ページへのリンク
                if (href && text && text.length > 2 && text.length < 100
                    && !skipTexts.some(s => text.toLowerCase().includes(s))
                    && !links.some(l => l.href === href)
                    && href !== '/studio/' && href !== '/studio') {
                    links.push({ href: href, text: text });
                }
            });

            // 方法2: カード要素内のタイトルを探す
            if (links.length === 0) {
                document.querySelectorAll('[class*="ProjectCard"], [class*="project-card"], [class*="ApiCard"], [class*="api-card"]').forEach(card => {
                    const titleEl = card.querySelector('h2, h3, h4, [class*="title"], [class*="name"]');
                    const linkEl = card.querySelector('a');
                    if (titleEl) {
                        const text = titleEl.textContent.trim();
                        const href = linkEl ? linkEl.getAttribute('href') : '';
                        if (text && !skipTexts.some(s => text.toLowerCase().includes(s))) {
                            links.push({ href: href || '', text: text });
                        }
                    }
                });
            }

            // 方法3: ページ上の全てのクリック可能な要素でAPI名を持つもの
            if (links.length === 0) {
                const apiKeywords = ['API', 'Generator', 'Converter', 'Analyzer', 'Aggregator',
                                     'Translator', 'Downloader', 'Validator', 'Formatter',
                                     'Intelligence', 'Enrichment', 'Optimizer', 'Domain'];
                document.querySelectorAll('h2, h3, h4, [class*="title"], [class*="Title"]').forEach(el => {
                    const text = el.textContent.trim();
                    if (text && apiKeywords.some(k => text.includes(k))
                        && !skipTexts.some(s => text.toLowerCase().includes(s))
                        && !links.some(l => l.text === text)) {
                        const parent = el.closest('a');
                        const href = parent ? parent.getAttribute('href') : '';
                        links.push({ href: href || '', text: text });
                    }
                });
            }

            return links;
        }''')

        print(f"  {len(card_links)} 件のカードを検出")
        for cl in card_links:
            print(f"    {cl['text']} -> {cl['href']}")

        if not card_links:
            print("\nカードが見つかりません。スクリーンショットを確認してください。")
            take_screenshot(page, "00_no_cards")
            sys.exit(1)

        results = []
        total = len(card_links)

        for i, card_info in enumerate(card_links):
            card_text = card_info["text"]
            card_href = card_info["href"]
            print(f"\n{'='*60}")
            print(f"[{i+1}/{total}] {card_text}")
            print(f"{'='*60}")

            result = {
                "name": card_text,
                "status": "unknown",
                "details": [],
            }

            try:
                # カードをクリック（hrefがあればURLで遷移）
                if card_href:
                    full_url = card_href if card_href.startswith("http") else f"https://rapidapi.com{card_href}"
                    page.goto(full_url, wait_until="domcontentloaded", timeout=15000)
                else:
                    page.get_by_text(card_text, exact=True).first.click()
                time.sleep(3)

                # Hub Listing をクリック
                hub_clicked = False
                try:
                    hub = page.get_by_text("Hub Listing").first
                    if hub.is_visible(timeout=3000):
                        hub.click()
                        time.sleep(2)
                        hub_clicked = True
                        print("  Hub Listing クリック")
                except:
                    pass

                if not hub_clicked:
                    # URL で直接遷移
                    current = page.url.rstrip("/")
                    page.goto(current + "/hub-listing", wait_until="domcontentloaded", timeout=10000)
                    time.sleep(2)

                take_screenshot(page, f"{i+1:02d}_hub_listing")

                # Base URL を読み取ってJSONマッチング
                matched_listing = None

                # 方法1: Base URL input から subdomain を取得
                try:
                    base_url_input = page.locator('input[value*="workers.dev"]').first
                    if base_url_input.is_visible(timeout=3000):
                        base_url = base_url_input.input_value()
                        subdomain = base_url.replace("https://", "").split(".")[0]
                        print(f"  Base URL: {base_url} (subdomain: {subdomain})")
                        matched_listing = listings.get(subdomain)
                except:
                    pass

                # 方法2: ページURL から推測
                if not matched_listing:
                    current_url = page.url
                    for key, info in listings.items():
                        if key in current_url.lower():
                            matched_listing = info
                            print(f"  URLマッチ: {key}")
                            break

                # 方法3: カード名で部分マッチ
                if not matched_listing:
                    for key, info in listings.items():
                        api_name = info.get("name", "")
                        # "QR Code Generator API" と "QR Code" のような部分一致
                        if (card_text.lower() in api_name.lower()
                            or api_name.lower() in card_text.lower()
                            or any(w in card_text.lower() for w in key.split("-") if len(w) > 3)):
                            matched_listing = info
                            print(f"  名前マッチ: {card_text} -> {api_name}")
                            break

                if not matched_listing:
                    print(f"  [SKIP] マッチするJSONが見つかりません")
                    result["status"] = "no_match"
                    results.append(result)
                    page.goto(STUDIO_URL, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(3)
                    continue

                print(f"  マッチ: {matched_listing['dir']}")

                # General タブがあればクリック
                try:
                    gen = page.get_by_text("General", exact=True).first
                    if gen.is_visible(timeout=2000):
                        gen.click()
                        time.sleep(2)
                except:
                    pass

                take_screenshot(page, f"{i+1:02d}_general_before")

                # 更新実行
                update_result = update_api_page(page, matched_listing, i)
                result["details"] = update_result["details"]
                result["status"] = "success" if any("OK" in d for d in result["details"]) else "partial"

                take_screenshot(page, f"{i+1:02d}_general_after")

            except Exception as e:
                print(f"  [ERROR] {e}")
                result["status"] = f"error: {str(e)[:80]}"
                take_screenshot(page, f"{i+1:02d}_error")

            results.append(result)

            # Studio一覧に戻る
            page.goto(STUDIO_URL, wait_until="domcontentloaded", timeout=15000)
            time.sleep(WAIT_BETWEEN_APIS)

        browser.close()

    # === 完了レポート ===
    print("\n" + "=" * 60)
    print("完了レポート")
    print("=" * 60)

    success = [r for r in results if r["status"] == "success"]
    partial = [r for r in results if r["status"] == "partial"]
    failed = [r for r in results if r["status"] not in ("success", "partial")]

    print(f"\n成功: {len(success)}/{len(results)}")
    print(f"部分成功: {len(partial)}/{len(results)}")
    print(f"失敗: {len(failed)}/{len(results)}")

    if success:
        print("\n--- 成功 ---")
        for r in success:
            details = ", ".join(r["details"])
            print(f"  [OK] {r['name']} - {details}")

    if partial:
        print("\n--- 部分成功 ---")
        for r in partial:
            details = ", ".join(r["details"])
            print(f"  [PARTIAL] {r['name']} - {details}")

    if failed:
        print("\n--- 失敗 ---")
        for r in failed:
            print(f"  [NG] {r['name']} - {r['status']}")

    print(f"\nスクリーンショット: {SCREENSHOT_DIR}")

    # レポート保存
    report_path = os.path.join(os.path.dirname(__file__), "update_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({"timestamp": datetime.now().isoformat(), "results": results}, f, indent=2, ensure_ascii=False)
    print(f"レポート保存: {report_path}")


if __name__ == "__main__":
    main()
