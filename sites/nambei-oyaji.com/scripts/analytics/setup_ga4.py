#!/usr/bin/env python3
"""
GA4 + Search Console API セットアップスクリプト

既存のサービスアカウント (sheets-sync-489022) を再利用し、
GA4 Data API と Search Console API を有効化 + 設定する。

使い方:
  python setup_ga4.py                # 対話的セットアップ
  python setup_ga4.py --property-id 123456789   # プロパティID指定
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
SETTINGS_PATH = CONFIG_DIR / "settings.json"
SA_SOURCE = CONFIG_DIR / "gsc-credentials.json"
GA4_CRED_PATH = CONFIG_DIR / "ga4-credentials.json"
GSC_CRED_PATH = CONFIG_DIR / "gsc-credentials.json"

SERVICE_ACCOUNT_EMAIL = "sheets-reader@sheets-sync-489022.iam.gserviceaccount.com"
PROJECT_ID = "sheets-sync-489022"


def check_gcloud():
    """gcloud CLI がインストールされているか確認"""
    try:
        result = subprocess.run(["gcloud", "version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def enable_apis():
    """必要な API を有効化"""
    apis = [
        "analyticsdata.googleapis.com",       # GA4 Data API
        "analyticsadmin.googleapis.com",       # GA4 Admin API
        "searchconsole.googleapis.com",        # Search Console API
        "webmasters.googleapis.com",           # Search Console API (legacy)
    ]

    print(f"\n📦 プロジェクト {PROJECT_ID} で API を有効化中...")

    for api in apis:
        print(f"  → {api} ...", end=" ")
        try:
            result = subprocess.run(
                ["gcloud", "services", "enable", api, f"--project={PROJECT_ID}"],
                capture_output=True, text=True, timeout=60,
            )
            if result.returncode == 0:
                print("✅")
            else:
                print(f"⚠️ {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {e}")


def copy_credentials():
    """サービスアカウントの認証ファイルをコピー"""
    if not SA_SOURCE.exists():
        print(f"❌ サービスアカウントファイルが見つかりません: {SA_SOURCE}")
        return False

    for dest in [GA4_CRED_PATH, GSC_CRED_PATH]:
        shutil.copy2(SA_SOURCE, dest)
        print(f"✅ 認証ファイルをコピー: {dest.name}")

    return True


def update_settings(property_id):
    """settings.json の property_id を更新"""
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)

    settings["google_analytics"]["property_id"] = property_id
    settings["google_analytics"]["credentials_file"] = "config/ga4-credentials.json"
    settings["search_console"]["credentials_file"] = "config/gsc-credentials.json"

    with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

    print(f"✅ settings.json 更新完了 (property_id: {property_id})")


def find_ga4_property():
    """GA4 プロパティ ID を自動検出"""
    try:
        from google.analytics.admin_v1beta import AnalyticsAdminServiceClient
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(GA4_CRED_PATH)

        client = AnalyticsAdminServiceClient()
        accounts = list(client.list_accounts())

        if not accounts:
            return None

        for account in accounts:
            properties = list(client.list_properties(
                filter=f"parent:{account.name}"
            ))
            for prop in properties:
                print(f"  発見: {prop.display_name} (ID: {prop.name.split('/')[-1]})")
                return prop.name.split("/")[-1]

        return None
    except Exception as e:
        print(f"  自動検出失敗: {e}")
        return None


def get_property_id_from_measurement_id():
    """measurement_id (G-XXXX) から GA4 の property_id を取得する方法を案内"""
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)

    mid = settings.get("google_analytics", {}).get("measurement_id", "")
    if mid:
        print(f"\n📊 Measurement ID: {mid}")
        print("   GA4管理画面 → 管理 → プロパティの詳細 から property_id を確認できます")
        print("   URL例: https://analytics.google.com/analytics/web/#/a{ACCOUNT}p{PROPERTY}/")
        print("   ↑ pの後の数字が property_id です")
    return mid


def verify_setup():
    """セットアップ確認"""
    print("\n🔍 セットアップ確認中...")

    # 認証ファイル
    for path, name in [(GA4_CRED_PATH, "GA4"), (GSC_CRED_PATH, "Search Console")]:
        if path.exists():
            print(f"  ✅ {name} 認証ファイル: {path}")
        else:
            print(f"  ❌ {name} 認証ファイル未作成")

    # settings.json
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)

    pid = settings.get("google_analytics", {}).get("property_id", "")
    if pid and "YOUR" not in pid:
        print(f"  ✅ GA4 Property ID: {pid}")
    else:
        print(f"  ❌ GA4 Property ID 未設定")

    # GA4 API テスト
    try:
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(GA4_CRED_PATH)
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        client = BetaAnalyticsDataClient()
        print("  ✅ GA4 Data API クライアント初期化成功")
    except ImportError:
        print("  ⚠️ google-analytics-data 未インストール")
        print("     → pip install google-analytics-data")
    except Exception as e:
        print(f"  ❌ GA4 API エラー: {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="GA4 + Search Console セットアップ")
    parser.add_argument("--property-id", help="GA4 プロパティ ID")
    parser.add_argument("--verify", action="store_true", help="セットアップ確認のみ")
    args = parser.parse_args()

    print("=" * 50)
    print("🔧 GA4 + Search Console API セットアップ")
    print("=" * 50)

    if args.verify:
        verify_setup()
        return

    # Step 1: 認証ファイルコピー
    print("\n--- Step 1: 認証ファイル ---")
    if not copy_credentials():
        sys.exit(1)

    # Step 2: gcloud で API 有効化
    print("\n--- Step 2: API 有効化 ---")
    has_gcloud = check_gcloud()
    if has_gcloud:
        enable_apis()
    else:
        print("⚠️ gcloud CLI 未インストール。手動で API を有効化してください:")
        print(f"   https://console.cloud.google.com/apis/library?project={PROJECT_ID}")
        print("   → 'Google Analytics Data API' を有効化")
        print("   → 'Search Console API' を有効化")

    # Step 3: Property ID 設定
    print("\n--- Step 3: GA4 Property ID ---")
    property_id = args.property_id

    if not property_id:
        # 自動検出を試行
        print("  GA4 プロパティを自動検出中...")
        property_id = find_ga4_property()

    if not property_id:
        get_property_id_from_measurement_id()
        property_id = input("\n  GA4 Property ID を入力してください: ").strip()

    if property_id:
        update_settings(property_id)
    else:
        print("  ⚠️ Property ID 未設定。後で settings.json を手動更新してください")

    # Step 4: GA4 管理画面でサービスアカウントに権限付与
    print(f"\n--- Step 4: GA4 権限設定 ---")
    print(f"  GA4管理画面で以下のメールに「閲覧者」権限を付与してください:")
    print(f"  📧 {SERVICE_ACCOUNT_EMAIL}")
    print(f"  手順: GA4 → 管理 → アカウントのアクセス管理 → + → {SERVICE_ACCOUNT_EMAIL}")

    # Step 5: Search Console にもサービスアカウントを追加
    print(f"\n--- Step 5: Search Console 権限設定 ---")
    print(f"  Search Console で以下のメールを「制限付きユーザー」として追加:")
    print(f"  📧 {SERVICE_ACCOUNT_EMAIL}")
    print(f"  手順: Search Console → 設定 → ユーザーと権限 → ユーザーを追加")

    # Step 6: Python ライブラリインストール
    print("\n--- Step 6: ライブラリインストール ---")
    libs = [
        "google-analytics-data",
        "google-analytics-admin",
        "google-api-python-client",
        "google-auth",
    ]
    for lib in libs:
        print(f"  → {lib} ...", end=" ")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", lib, "-q"],
            capture_output=True, text=True,
        )
        print("✅" if result.returncode == 0 else f"❌ {result.stderr[:100]}")

    # 確認
    verify_setup()

    print("\n" + "=" * 50)
    print("📋 残りの手動作業:")
    print(f"  1. GA4管理画面で {SERVICE_ACCOUNT_EMAIL} に「閲覧者」権限を付与")
    print(f"  2. Search Console で同メールを「制限付きユーザー」に追加")
    if not property_id:
        print("  3. settings.json の property_id を GA4 プロパティ ID に更新")
    print("=" * 50)


if __name__ == "__main__":
    main()
