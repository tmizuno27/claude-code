#!/usr/bin/env python3
"""
PS1ファイルに Healthchecks.io ping を自動統合するスクリプト

setup_healthchecks.py で生成した config.json を読み込み、
各PS1ランチャーに開始ping（/start）と完了ping（成功/失敗）を追加する。

【使い方】
  python integrate_ps1.py           # 全PS1に追加
  python integrate_ps1.py --dry-run # 変更内容の確認のみ（書き込みなし）
"""

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
PS1_DIR = Path(r"C:\Users\tmizu\scripts")

# 共通モジュールの内容（各PS1の先頭付近にdot-sourceで読み込む）
COMMON_MODULE = r'''# --- Healthchecks.io ping 関数 ---
$global:HC_PING_URL = "{ping_url}"

function Send-HealthcheckStart {{
    if ($global:HC_PING_URL) {{
        try {{ Invoke-WebRequest -Uri "$($global:HC_PING_URL)/start" -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null }} catch {{}}
    }}
}}

function Send-HealthcheckSuccess {{
    if ($global:HC_PING_URL) {{
        try {{ Invoke-WebRequest -Uri $global:HC_PING_URL -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null }} catch {{}}
    }}
}}

function Send-HealthcheckFail {{
    if ($global:HC_PING_URL) {{
        try {{ Invoke-WebRequest -Uri "$($global:HC_PING_URL)/fail" -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null }} catch {{}}
    }}
}}
'''

# HC_PING マーカー（二重追加防止用）
HC_MARKER = "# --- Healthchecks.io ping"


def load_config():
    if not CONFIG_FILE.exists():
        print(f"ERROR: {CONFIG_FILE} が見つかりません")
        print("先に setup_healthchecks.py を実行してください")
        sys.exit(1)
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def integrate_simple_ps1(content, ping_url, task_name):
    """シンプルなPS1（try/catch 1つ）にpingを追加"""

    # HC関数ブロックを先頭に追加
    hc_block = COMMON_MODULE.format(ping_url=ping_url)

    # 既にマーカーがあれば更新、なければ追加
    if HC_MARKER in content:
        # 既存のHCブロックを置換
        pattern = r'# --- Healthchecks\.io ping.*?(?=\n[^#\n$\s{]|\n\n[^#])'
        content = re.sub(pattern, hc_block.strip(), content, flags=re.DOTALL)
        return content

    lines = content.split("\n")
    result = []
    hc_inserted = False
    start_inserted = False
    has_exit_code_tracking = False

    for i, line in enumerate(lines):
        # HC関数ブロックをスクリプト先頭（コメント後）に挿入
        if not hc_inserted and not line.startswith("#") and line.strip() != "":
            # param() があればその後に
            if line.strip().startswith("param("):
                result.append(line)
                # param ブロックの終わりまで進める
                continue
            result.append(hc_block)
            hc_inserted = True

        # 開始ログの直後に Send-HealthcheckStart を挿入
        if not start_inserted and ("開始" in line or "START" in line or "starting" in line) and "Write-Log" in line or "Add-Content" in line:
            result.append(line)
            result.append("Send-HealthcheckStart")
            start_inserted = True
            continue

        # exit code の追跡
        if "$LASTEXITCODE" in line or "$exitCode" in line:
            has_exit_code_tracking = True

        result.append(line)

    # Send-HealthcheckStart がまだ挿入されてなければ、HC関数の直後に
    if not start_inserted:
        for i, line in enumerate(result):
            if "Send-HealthcheckFail" in line:  # HC関数定義内のは除外
                continue
            if "HC_PING_URL" in line and "global:" in line:
                result.insert(i + 1, "\nSend-HealthcheckStart")
                break

    # 最後に成功/失敗判定を追加
    result.append("")
    result.append("# --- Healthchecks.io 完了通知 ---")
    result.append("if ($LASTEXITCODE -eq 0 -or -not $LASTEXITCODE) {")
    result.append("    Send-HealthcheckSuccess")
    result.append("} else {")
    result.append("    Send-HealthcheckFail")
    result.append("}")

    return "\n".join(result)


def integrate_auto_sync(content, ping_url):
    """auto-sync.ps1 専用の統合（構造が特殊）"""
    hc_block = COMMON_MODULE.format(ping_url=ping_url)

    if HC_MARKER in content:
        return content  # 既に統合済み

    lines = content.split("\n")
    result = []

    # 先頭コメントの後にHC関数を挿入
    inserted = False
    for i, line in enumerate(lines):
        if not inserted and not line.startswith("#") and line.strip() != "":
            result.append(hc_block)
            result.append("Send-HealthcheckStart")
            result.append("")
            inserted = True
        result.append(line)

    # 末尾に成功ping追加（auto-syncは変更なしでもexit 0で正常）
    result.append("")
    result.append("# --- Healthchecks.io 完了通知 ---")
    result.append("Send-HealthcheckSuccess")

    return "\n".join(result)


def integrate_blog_auto_publish(content, ping_url):
    """blog-auto-publish.ps1 専用（複数ステップ、スキップ分岐あり）"""
    hc_block = COMMON_MODULE.format(ping_url=ping_url)

    if HC_MARKER in content:
        return content

    # 先頭コメント後にHC関数挿入
    lines = content.split("\n")
    result = []
    inserted_func = False

    for line in lines:
        if not inserted_func and not line.startswith("#") and line.strip() != "":
            result.append(hc_block)
            inserted_func = True
        result.append(line)

    # 「開始」ログの後に Start ping
    final = "\n".join(result)
    final = final.replace(
        'Write-Log "========== ブログ自動公開チェック開始 =========="',
        'Write-Log "========== ブログ自動公開チェック開始 ==========="\nSend-HealthcheckStart'
    )

    # スキップ時も成功ping（「実行しない」のは正常動作）
    final = final.replace(
        '    exit 0\n}',
        '    Send-HealthcheckSuccess\n    exit 0\n}',
        2  # 曜日スキップと祝日スキップの2箇所
    )

    # 末尾に完了ping
    final += "\n\n# --- Healthchecks.io 完了通知 ---\n"
    final += "Send-HealthcheckSuccess\n"

    return final


def integrate_x_auto_post(content, ping_url_morning, ping_url_noon, ping_url_evening):
    """x-auto-post.ps1 専用（-Slot パラメータで3つのチェックに分岐）"""
    if HC_MARKER in content:
        return content

    # Slot別のping URLマッピング
    hc_block = f'''# --- Healthchecks.io ping 関数 ---
$hcUrls = @{{
    "morning" = "{ping_url_morning}"
    "noon"    = "{ping_url_noon}"
    "evening" = "{ping_url_evening}"
}}
$global:HC_PING_URL = $hcUrls[$Slot]

function Send-HealthcheckStart {{
    if ($global:HC_PING_URL) {{
        try {{ Invoke-WebRequest -Uri "$($global:HC_PING_URL)/start" -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null }} catch {{}}
    }}
}}

function Send-HealthcheckSuccess {{
    if ($global:HC_PING_URL) {{
        try {{ Invoke-WebRequest -Uri $global:HC_PING_URL -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null }} catch {{}}
    }}
}}

function Send-HealthcheckFail {{
    if ($global:HC_PING_URL) {{
        try {{ Invoke-WebRequest -Uri "$($global:HC_PING_URL)/fail" -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null }} catch {{}}
    }}
}}
'''

    lines = content.split("\n")
    result = []
    inserted = False

    for line in lines:
        result.append(line)
        # param() ブロックの閉じ括弧の後に挿入
        if not inserted and line.strip() == ")":
            # paramブロックのValidateSetの後
            if any("ValidateSet" in l for l in lines[:lines.index(line)]):
                result.append("")
                result.append(hc_block)
                inserted = True

    final = "\n".join(result)

    # START ping
    final = final.replace(
        'Write-Log "========== X Auto-Post START',
        'Send-HealthcheckStart\nWrite-Log "========== X Auto-Post START'
    )

    # 末尾に完了ping
    final += "\n\n# --- Healthchecks.io 完了通知 ---\n"
    final += "if ($exitCode -eq 0 -or -not $exitCode) {\n"
    final += "    Send-HealthcheckSuccess\n"
    final += "} else {\n"
    final += "    Send-HealthcheckFail\n"
    final += "}\n"

    return final


def integrate_blog_support(content, check_configs):
    """blog-support-tasks.ps1 専用（-Task パラメータで分岐）"""
    if HC_MARKER in content:
        return content

    # Task別のping URLマッピング
    url_entries = []
    for task_param, ping_url in check_configs.items():
        url_entries.append(f'    "{task_param}" = "{ping_url}"')

    hc_block = '# --- Healthchecks.io ping 関数 ---\n'
    hc_block += '$hcUrls = @{\n'
    hc_block += '\n'.join(url_entries)
    hc_block += '\n}\n'
    hc_block += '$global:HC_PING_URL = $hcUrls[$Task]\n\n'
    hc_block += '''function Send-HealthcheckStart {
    if ($global:HC_PING_URL) {
        try { Invoke-WebRequest -Uri "$($global:HC_PING_URL)/start" -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null } catch {}
    }
}

function Send-HealthcheckSuccess {
    if ($global:HC_PING_URL) {
        try { Invoke-WebRequest -Uri $global:HC_PING_URL -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null } catch {}
    }
}

function Send-HealthcheckFail {
    if ($global:HC_PING_URL) {
        try { Invoke-WebRequest -Uri "$($global:HC_PING_URL)/fail" -Method Post -TimeoutSec 5 -UseBasicParsing | Out-Null } catch {}
    }
}
'''

    lines = content.split("\n")
    result = []
    inserted = False

    for line in lines:
        result.append(line)
        if not inserted and line.strip() == ")":
            if any("ValidateSet" in l for l in lines[:lines.index(line)]):
                result.append("")
                result.append(hc_block)
                inserted = True

    final = "\n".join(result)

    # 開始直後に Start ping
    final = final.replace(
        'Write-Log "========== $taskLabel 開',
        'Send-HealthcheckStart\nWrite-Log "========== $taskLabel 開'
    )

    # 末尾の完了ログの後に成功/失敗ping
    final += "\n\n# --- Healthchecks.io 完了通知 ---\n"
    final += "if ($exitCode -eq 0 -or -not $exitCode) {\n"
    final += "    Send-HealthcheckSuccess\n"
    final += "} else {\n"
    final += "    Send-HealthcheckFail\n"
    final += "}\n"

    return final


def process_all(config, dry_run=False):
    """全PS1ファイルを処理"""
    checks = config.get("checks", {})
    processed = 0
    errors = 0

    for task_name, check_info in checks.items():
        ps1_info = check_info.get("ps1")
        ping_url = check_info.get("ping_url", "")

        if not ps1_info or not ping_url:
            continue

        # パラメータ付きPS1（x-auto-post.ps1:morning 等）は特別処理
        if ":" in str(ps1_info):
            continue  # 後で一括処理

        ps1_path = PS1_DIR / ps1_info
        if not ps1_path.exists():
            print(f"  [SKIP] {ps1_info} が見つかりません")
            continue

        content = ps1_path.read_text(encoding="utf-8")

        if HC_MARKER in content:
            print(f"  [SKIP] {ps1_info} (統合済み)")
            continue

        # ファイル別の処理
        if ps1_info == "auto-sync.ps1":
            new_content = integrate_auto_sync(content, ping_url)
        elif ps1_info == "blog-auto-publish.ps1":
            new_content = integrate_blog_auto_publish(content, ping_url)
        else:
            new_content = integrate_simple_ps1(content, ping_url, task_name)

        if dry_run:
            print(f"  [DRY] {ps1_info} → ping追加予定")
        else:
            ps1_path.write_text(new_content, encoding="utf-8")
            print(f"  [OK] {ps1_info} → ping追加完了")
        processed += 1

    # --- x-auto-post.ps1（3スロット分岐）---
    x_morning = checks.get("XAutoPost-Morning", {}).get("ping_url", "")
    x_noon = checks.get("XAutoPost-Noon", {}).get("ping_url", "")
    x_evening = checks.get("XAutoPost-Evening", {}).get("ping_url", "")

    if x_morning and x_noon and x_evening:
        ps1_path = PS1_DIR / "x-auto-post.ps1"
        if ps1_path.exists():
            content = ps1_path.read_text(encoding="utf-8")
            if HC_MARKER not in content:
                new_content = integrate_x_auto_post(content, x_morning, x_noon, x_evening)
                if dry_run:
                    print(f"  [DRY] x-auto-post.ps1 → 3スロット分岐ping追加予定")
                else:
                    ps1_path.write_text(new_content, encoding="utf-8")
                    print(f"  [OK] x-auto-post.ps1 → 3スロット分岐ping追加完了")
                processed += 1

    # --- blog-support-tasks.ps1（マルチタスク分岐）---
    support_checks = {}
    for task_name, check_info in checks.items():
        ps1_info = check_info.get("ps1", "")
        if isinstance(ps1_info, str) and ps1_info.startswith("blog-support-tasks.ps1:"):
            param = ps1_info.split(":")[1]
            support_checks[param] = check_info.get("ping_url", "")

    if support_checks:
        ps1_path = PS1_DIR / "blog-support-tasks.ps1"
        if ps1_path.exists():
            content = ps1_path.read_text(encoding="utf-8")
            if HC_MARKER not in content:
                new_content = integrate_blog_support(content, support_checks)
                if dry_run:
                    print(f"  [DRY] blog-support-tasks.ps1 → マルチタスク分岐ping追加予定")
                else:
                    ps1_path.write_text(new_content, encoding="utf-8")
                    print(f"  [OK] blog-support-tasks.ps1 → マルチタスク分岐ping追加完了")
                processed += 1

    print(f"\n処理完了: {processed}ファイル更新")


def main():
    parser = argparse.ArgumentParser(description="PS1に Healthchecks.io ping を統合")
    parser.add_argument("--dry-run", action="store_true", help="変更内容の確認のみ")
    args = parser.parse_args()

    print("=== PS1 Healthchecks.io 統合 ===\n")

    config = load_config()
    print(f"チェック数: {config['total_checks']}\n")

    process_all(config, dry_run=args.dry_run)

    if args.dry_run:
        print("\n--dry-run モードです。実際の変更は行われていません。")
        print("変更を適用するには --dry-run なしで再実行してください。")


if __name__ == "__main__":
    main()
