"""
RapidAPI Studio 全24本API リスティング自動更新スクリプト
Playwrightでブラウザ自動操作し、各APIの Short/Long Description + Visibility を更新する。
"""

import json
import os
import sys
import time
import glob
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
except ImportError:
    print("=" * 60)
    print("Playwright が未インストールです。以下を実行してください:")
    print()
    print("  pip install playwright")
    print("  playwright install chromium")
    print()
    print("=" * 60)
    sys.exit(1)

# === 設定 ===
BASE_DIR = Path(r"C:\Users\tmizu\マイドライブ\GitHub\claude-code\api-services")
SCREENSHOT_DIR = BASE_DIR / "scripts" / "screenshots"
STUDIO_URL = "https://rapidapi.com/studio/"
WAIT_BETWEEN_APIS = 3  # 秒


def load_all_listings() -> list[dict]:
    """全APIディレクトリから rapidapi-listing.json を読み込む"""
    listings = []
    for d in sorted(BASE_DIR.iterdir()):
        if not d.is_dir() or not d.name[:2].isdigit():
            continue
        json_path = d / "rapidapi-listing.json"
        if not json_path.exists():
            print(f"  [SKIP] {d.name}: rapidapi-listing.json なし")
            continue
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["_dir"] = d.name
        data["_path"] = str(json_path)
        listings.append(data)
    print(f"\n合計 {len(listings)} 件の listing.json を読み込みました\n")
    return listings


def take_screenshot(page, name: str):
    """スクリーンショットを保存"""
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"{ts}_{name}.png"
    page.screenshot(path=str(path), full_page=False)
    return path


def clear_and_type(page, selector: str, text: str, field_name: str = ""):
    """フィールドをクリアして新しいテキストを入力"""
    try:
        el = page.locator(selector).first
        el.click()
        time.sleep(0.3)
        # 全選択 → 削除 → 入力
        page.keyboard.press("Control+a")
        time.sleep(0.1)
        page.keyboard.press("Backspace")
        time.sleep(0.1)
        el.fill(text)
        time.sleep(0.3)
        print(f"    [OK] {field_name} 更新完了")
        return True
    except Exception as e:
        print(f"    [ERROR] {field_name}: {e}")
        return False


def update_single_api(page, listing: dict, index: int, total: int) -> dict:
    """1つのAPIを更新する。結果dictを返す"""
    api_name = listing.get("name", "Unknown")
    dir_name = listing.get("_dir", "")
    result = {"name": api_name, "dir": dir_name, "status": "unknown", "details": []}

    print(f"\n{'='*60}")
    print(f"[{index+1}/{total}] {api_name} ({dir_name})")
    print(f"{'='*60}")

    try:
        # Studio一覧ページにいることを確認
        if "/studio" not in page.url:
            page.goto(STUDIO_URL, wait_until="networkidle", timeout=30000)
            time.sleep(2)

        take_screenshot(page, f"{index+1:02d}_{dir_name}_01_list")

        # APIカードを探してクリック
        # カード内のAPI名テキストでマッチング
        api_card = None
        # 方法1: テキストで探す
        cards = page.locator('[class*="card"], [class*="Card"], [class*="api"], [class*="Api"], [class*="item"], [class*="Item"], a[href*="/studio/"]')
        card_count = cards.count()
        print(f"  カード候補: {card_count} 件")

        # まずリンクテキストで直接探す
        link = page.get_by_text(api_name, exact=False).first
        if link.is_visible(timeout=3000):
            api_card = link
            print(f"  テキストマッチでカード発見: {api_name}")

        if api_card is None:
            # slug で href マッチ
            slug = listing.get("slug", "")
            if slug:
                link2 = page.locator(f'a[href*="{slug}"]').first
                if link2.is_visible(timeout=3000):
                    api_card = link2
                    print(f"  slugマッチでカード発見: {slug}")

        if api_card is None:
            print(f"  [FAIL] カードが見つかりません")
            result["status"] = "card_not_found"
            return result

        api_card.click()
        time.sleep(3)
        take_screenshot(page, f"{index+1:02d}_{dir_name}_02_api_page")

        # 「Hub Listing」をクリック（左サイドバー）
        hub_listing_clicked = False
        for selector in [
            'text="Hub Listing"',
            '[data-testid*="hub-listing"]',
            'a:has-text("Hub Listing")',
            'button:has-text("Hub Listing")',
            'span:has-text("Hub Listing")',
        ]:
            try:
                el = page.locator(selector).first
                if el.is_visible(timeout=2000):
                    el.click()
                    hub_listing_clicked = True
                    print("  Hub Listing クリック")
                    time.sleep(2)
                    break
            except:
                continue

        if not hub_listing_clicked:
            # URLで直接遷移を試みる
            print("  Hub Listing ボタンが見つかりません。URL遷移を試みます...")
            # 現在のURLから推測
            current_url = page.url
            if "/studio/" in current_url:
                # hub-listing パスを付加
                hub_url = current_url.rstrip("/") + "/hub-listing"
                page.goto(hub_url, wait_until="networkidle", timeout=15000)
                time.sleep(2)
                hub_listing_clicked = True

        take_screenshot(page, f"{index+1:02d}_{dir_name}_03_hub_listing")

        # 「General」タブ or 「General Information」をクリック
        for selector in [
            'text="General"',
            'text="General Information"',
            '[data-testid*="general"]',
            'a:has-text("General")',
            'button:has-text("General")',
        ]:
            try:
                el = page.locator(selector).first
                if el.is_visible(timeout=2000):
                    el.click()
                    print("  General タブクリック")
                    time.sleep(2)
                    break
            except:
                continue

        take_screenshot(page, f"{index+1:02d}_{dir_name}_04_general")

        # === Short Description 更新 ===
        short_desc = listing.get("description", "")
        if short_desc:
            updated = False
            for selector in [
                'textarea[name*="short"], textarea[name*="Short"]',
                'textarea[placeholder*="short description" i]',
                'input[name*="short"], input[name*="Short"]',
                'textarea[name*="description"]:not([name*="long"])',
                # General ページの最初のtextarea
                'textarea:nth-of-type(1)',
            ]:
                try:
                    el = page.locator(selector).first
                    if el.is_visible(timeout=1500):
                        el.click()
                        time.sleep(0.2)
                        page.keyboard.press("Control+a")
                        page.keyboard.press("Backspace")
                        el.fill(short_desc)
                        time.sleep(0.3)
                        print(f"    [OK] Short Description 更新完了")
                        result["details"].append("short_desc: OK")
                        updated = True
                        break
                except:
                    continue
            if not updated:
                # ラベルから探す
                try:
                    label = page.get_by_text("Short Description", exact=False).first
                    textarea = label.locator("..").locator("textarea, input").first
                    textarea.click()
                    page.keyboard.press("Control+a")
                    page.keyboard.press("Backspace")
                    textarea.fill(short_desc)
                    print(f"    [OK] Short Description (ラベル経由)")
                    result["details"].append("short_desc: OK")
                    updated = True
                except:
                    pass
            if not updated:
                print(f"    [WARN] Short Description フィールドが見つかりません")
                result["details"].append("short_desc: NOT_FOUND")

        # === Long Description 更新 ===
        long_desc = listing.get("long_description", "")
        if long_desc:
            updated = False
            for selector in [
                'textarea[name*="long"], textarea[name*="Long"]',
                'textarea[placeholder*="long description" i]',
                # General ページの2番目のtextarea
                'textarea:nth-of-type(2)',
            ]:
                try:
                    el = page.locator(selector).first
                    if el.is_visible(timeout=1500):
                        el.click()
                        time.sleep(0.2)
                        page.keyboard.press("Control+a")
                        page.keyboard.press("Backspace")
                        el.fill(long_desc)
                        time.sleep(0.3)
                        print(f"    [OK] Long Description 更新完了")
                        result["details"].append("long_desc: OK")
                        updated = True
                        break
                except:
                    continue
            if not updated:
                try:
                    label = page.get_by_text("Long Description", exact=False).first
                    textarea = label.locator("..").locator("textarea, input").first
                    textarea.click()
                    page.keyboard.press("Control+a")
                    page.keyboard.press("Backspace")
                    textarea.fill(long_desc)
                    print(f"    [OK] Long Description (ラベル経由)")
                    result["details"].append("long_desc: OK")
                    updated = True
                except:
                    pass
            if not updated:
                print(f"    [WARN] Long Description フィールドが見つかりません")
                result["details"].append("long_desc: NOT_FOUND")

        # === Visibility 確認・切替 ===
        try:
            # Private/Public のトグルまたはラジオボタンを探す
            visibility_changed = False
            # トグルスイッチ
            for selector in [
                'text="Private"',
                '[data-testid*="visibility"]',
                '[class*="visibility" i]',
                '[class*="toggle" i]',
            ]:
                try:
                    el = page.locator(selector).first
                    if el.is_visible(timeout=1500):
                        # Privateが表示されている → Publicに切り替え
                        # Public ボタンまたはトグルをクリック
                        public_btn = page.get_by_text("Public", exact=True).first
                        if public_btn.is_visible(timeout=1500):
                            public_btn.click()
                            time.sleep(1)
                            print(f"    [OK] Visibility → Public に切り替え")
                            result["details"].append("visibility: switched_to_public")
                            visibility_changed = True
                        break
                except:
                    continue
            if not visibility_changed:
                # 既に Public の可能性
                try:
                    pub = page.get_by_text("Public", exact=True).first
                    if pub.is_visible(timeout=1000):
                        print(f"    [INFO] Visibility: 既に Public")
                        result["details"].append("visibility: already_public")
                except:
                    print(f"    [WARN] Visibility セクションが見つかりません")
                    result["details"].append("visibility: NOT_FOUND")
        except Exception as e:
            print(f"    [ERROR] Visibility: {e}")
            result["details"].append(f"visibility: ERROR")

        take_screenshot(page, f"{index+1:02d}_{dir_name}_05_after_update")

        # === 保存 ===
        try:
            save_btn = None
            for selector in [
                'button:has-text("Save")',
                'button[type="submit"]',
                '[data-testid*="save"]',
                'button:has-text("Update")',
            ]:
                try:
                    el = page.locator(selector).first
                    if el.is_visible(timeout=1500):
                        save_btn = el
                        break
                except:
                    continue
            if save_btn:
                save_btn.click()
                time.sleep(2)
                print(f"    [OK] 保存完了")
                result["details"].append("save: OK")
            else:
                print(f"    [INFO] Saveボタンなし（自動保存の可能性）")
                result["details"].append("save: auto_save_assumed")
        except Exception as e:
            print(f"    [WARN] 保存: {e}")

        take_screenshot(page, f"{index+1:02d}_{dir_name}_06_saved")

        result["status"] = "success"

        # Studio一覧に戻る
        page.goto(STUDIO_URL, wait_until="networkidle", timeout=30000)
        time.sleep(2)

    except Exception as e:
        print(f"  [ERROR] {api_name}: {e}")
        result["status"] = f"error: {str(e)[:100]}"
        take_screenshot(page, f"{index+1:02d}_{dir_name}_ERROR")
        # Studio一覧に戻る
        try:
            page.goto(STUDIO_URL, wait_until="networkidle", timeout=15000)
            time.sleep(2)
        except:
            pass

    return result


def main():
    print("=" * 60)
    print("RapidAPI Studio 全24本API リスティング自動更新")
    print("=" * 60)

    # listing.json 読み込み
    listings = load_all_listings()
    if not listings:
        print("更新対象の listing.json が見つかりません")
        sys.exit(1)

    results = []

    with sync_playwright() as p:
        # headful モードでブラウザ起動
        browser = p.chromium.launch(
            headless=False,
            slow_mo=200,  # 操作を少し遅くして安定化
        )
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            locale="en-US",
        )
        page = context.new_page()

        # Studio に遷移
        print("\nRapidAPI Studio を開いています...")
        page.goto(STUDIO_URL, wait_until="domcontentloaded", timeout=60000)
        time.sleep(2)
        take_screenshot(page, "00_initial")

        # ログイン待ち（APIカードが表示されるまで自動待機）
        print("\n" + "=" * 60)
        print("ブラウザでRapidAPI Studioにログインしてください。")
        print("API一覧が表示されるまで自動で待機します...")
        print("=" * 60)

        # API一覧のカードが表示されるまで最大5分待機
        try:
            page.wait_for_selector('[class*="ApiCard"], [class*="api-card"], [data-testid*="api"], a[href*="/studio/"]', timeout=300000)
        except Exception:
            pass
        # 追加で10秒待ってページ安定化
        time.sleep(10)

        take_screenshot(page, "00_after_login")
        print("\nAPI一覧を検出。更新を開始します...\n")

        # 全API更新
        total = len(listings)
        for i, listing in enumerate(listings):
            result = update_single_api(page, listing, i, total)
            results.append(result)
            if i < total - 1:
                print(f"\n  次のAPIまで {WAIT_BETWEEN_APIS}秒 待機...")
                time.sleep(WAIT_BETWEEN_APIS)

        browser.close()

    # === 完了レポート ===
    print("\n" + "=" * 60)
    print("完了レポート")
    print("=" * 60)

    success = [r for r in results if r["status"] == "success"]
    failed = [r for r in results if r["status"] != "success"]

    print(f"\n成功: {len(success)}/{len(results)}")
    print(f"失敗: {len(failed)}/{len(results)}")

    if success:
        print("\n--- 成功 ---")
        for r in success:
            details = ", ".join(r["details"]) if r["details"] else "no details"
            print(f"  [OK] {r['name']} ({r['dir']}) - {details}")

    if failed:
        print("\n--- 失敗 ---")
        for r in failed:
            print(f"  [NG] {r['name']} ({r['dir']}) - {r['status']}")

    print(f"\nスクリーンショット: {SCREENSHOT_DIR}")

    # レポートをJSONで保存
    report_path = BASE_DIR / "scripts" / "update_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total": len(results),
            "success": len(success),
            "failed": len(failed),
            "results": results,
        }, f, ensure_ascii=False, indent=2)
    print(f"レポート保存: {report_path}")


if __name__ == "__main__":
    main()
