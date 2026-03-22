"""
ファクトチェック修正スクリプト (2026-03-22)
- デフォルト: ドライラン（変更内容を表示のみ）
- --apply フラグで実際に更新を実行
"""

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import requests

# ── 設定 ──────────────────────────────────────────────
SECRETS_PATH = Path(__file__).resolve().parents[2] / "config" / "secrets.json"
BASE_URL = "https://otona-match.com/?rest_route=/wp/v2/posts/{id}"
LOG_DIR = Path(__file__).resolve().parents[2] / "logs"


def load_credentials():
    with open(SECRETS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    wp = data["wordpress"]
    return (wp["username"], wp["app_password"].replace(" ", ""))


def fetch_post(session, post_id):
    url = BASE_URL.format(id=post_id)
    resp = session.get(url, params={"context": "edit"})
    resp.raise_for_status()
    return resp.json()


def update_post(session, post_id, content):
    url = BASE_URL.format(id=post_id)
    resp = session.post(url, json={"content": content})
    resp.raise_for_status()
    return resp.json()


# ── 修正定義 ──────────────────────────────────────────

def apply_fixes(post_id, content):
    """Return (new_content, list_of_change_descriptions)."""
    changes = []
    original = content

    # === GROUP 1: ゼクシィ縁結びサービス終了 ===
    if post_id == 532:
        notice = (
            '<div class="wp-block-cocoon-blocks-info-box info-box block-box has-background" '
            'style="background-color:#fff3cd;border:2px solid #ffc107;padding:20px;margin-bottom:30px;border-radius:8px;">'
            '<p style="font-weight:bold;font-size:18px;margin-bottom:10px;">⚠️ 重要なお知らせ</p>'
            '<p>ゼクシィ縁結びは<strong>2026年3月31日をもってサービスを終了</strong>しました。'
            '代替アプリとして<a href="/matching-app-ranking-2026/">マッチングアプリおすすめランキング</a>'
            'をご参照ください。</p></div>'
        )
        if notice not in content:
            content = notice + content
            changes.append("[GROUP1] ゼクシィ縁結び サービス終了告知を記事冒頭に追加")

    if post_id == 9:
        # Add service end note after each mention of ゼクシィ縁結び (but not if already annotated)
        pattern = r'(ゼクシィ縁結び)(?!\s*[\(（]※)'
        replacement = r'\1(※2026年3月末サービス終了)'
        new = re.sub(pattern, replacement, content)
        if new != content:
            count = len(re.findall(pattern, content))
            content = new
            changes.append(f"[GROUP1] ゼクシィ縁結びにサービス終了注記を{count}箇所追加")

    # === GROUP 2: Pairs料金 3,700円→4,100円 ===
    pairs_price_ids = {9, 10, 17, 18, 19, 133, 143, 150, 155, 163, 187, 193, 699, 14, 27, 151}
    if post_id in pairs_price_ids:
        # Context-aware replacement: only replace 3,700円 near Pairs/ペアーズ
        # Strategy: split into chunks around "3,700円", check surrounding context
        def pairs_price_replacer(m):
            start = max(0, m.start() - 200)
            context_before = content[start:m.start()].lower()
            end = min(len(content), m.end() + 200)
            context_after = content[m.end():end].lower()
            ctx = context_before + context_after
            # Check for Pairs context, exclude tapple context
            has_pairs = any(kw in ctx for kw in ["pairs", "ペアーズ"])
            has_tapple = any(kw in ctx for kw in ["tapple", "タップル"])
            # If tapple is closer than pairs, skip
            if has_tapple and not has_pairs:
                return m.group(0)
            if has_pairs:
                return "4,100円"
            # Ambiguous - skip to be safe
            return m.group(0)

        new = re.sub(r'3,700円', pairs_price_replacer, content)
        if new != content:
            diff_count = content.count("3,700円") - new.count("3,700円")
            changes.append(f"[GROUP2] Pairs料金 3,700円→4,100円 に{diff_count}箇所修正")
            content = new

    # === GROUP 3: 結婚相談所料金修正 ===
    if post_id in (136, 154):
        # エン婚活エージェント 入会金 33,000円→10,780円
        def replace_near(text, old, new_val, context_kw, label):
            nonlocal changes
            pattern = re.escape(old)
            def repl(m):
                start = max(0, m.start() - 300)
                ctx = text[start:m.end() + 100]
                if any(kw in ctx for kw in context_kw):
                    return new_val
                return m.group(0)
            result = re.sub(pattern, repl, text)
            if result != text:
                changes.append(label)
            return result

        content = replace_near(content, "33,000円", "10,780円（登録料）",
                               ["エン婚活"], f"[GROUP3] ID:{post_id} エン婚活エージェント 入会金33,000円→10,780円（登録料）")

    if post_id == 136:
        def replace_near_136(text, old, new_val, context_kw, label):
            nonlocal changes
            pattern = re.escape(old)
            def repl(m):
                start = max(0, m.start() - 300)
                ctx = text[start:m.end() + 100]
                if any(kw in ctx for kw in context_kw):
                    return new_val
                return m.group(0)
            result = re.sub(pattern, repl, text)
            if result != text:
                changes.append(label)
            return result

        content = replace_near_136(content, "220,000円", "55,000円",
                                   ["パートナーエージェント"], "[GROUP3] ID:136 パートナーエージェント 成婚料220,000円→55,000円")

    if post_id == 154:
        def replace_near_154(text, old, new_val, context_kw, label):
            nonlocal changes
            pattern = re.escape(old)
            def repl(m):
                start = max(0, m.start() - 300)
                ctx = text[start:m.end() + 100]
                if any(kw in ctx for kw in context_kw):
                    return new_val
                return m.group(0)
            result = re.sub(pattern, repl, text)
            if result != text:
                changes.append(label)
            return result

        content = replace_near_154(content, "220,000円", "55,000円",
                                   ["パートナーエージェント"], "[GROUP3] ID:154 パートナーエージェント 成婚料220,000円→55,000円")
        content = replace_near_154(content, "18,700円", "11,000円",
                                   ["パートナーエージェント"], "[GROUP3] ID:154 パートナーエージェント 月会費18,700円→11,000円")
        content = replace_near_154(content, "137,500円", "85,250円",
                                   ["パートナーエージェント"], "[GROUP3] ID:154 パートナーエージェント 初期費用137,500円→85,250円")
        content = replace_near_154(content, "15,400円", "15,950円",
                                   ["ツヴァイ"], "[GROUP3] ID:154 ツヴァイ 月会費15,400円→15,950円")

    if post_id == 144:
        def replace_near_144(text, old, new_val, context_kw, label):
            nonlocal changes
            pattern = re.escape(old)
            def repl(m):
                start = max(0, m.start() - 300)
                ctx = text[start:m.end() + 100]
                if any(kw in ctx for kw in context_kw):
                    return new_val
                return m.group(0)
            result = re.sub(pattern, repl, text)
            if result != text:
                changes.append(label)
            return result

        content = replace_near_144(content, "29,800円", "66,000円",
                                   ["naco-do", "ナコード", "naco"], "[GROUP3] ID:144 naco-do 入会金29,800円→66,000円")
        content = replace_near_144(content, "14,200円", "16,800円",
                                   ["naco-do", "ナコード", "naco"], "[GROUP3] ID:144 naco-do 月会費14,200円→16,800円")

    # === GROUP 4: 会員数の桁修正 ===
    if post_id == 14:
        member_fixes = [
            ("250万人", "2,500万人", ["Pairs", "ペアーズ"]),
            ("100万人", "800万人", ["with", "ウィズ"]),
            ("100万人", "900万人", ["Omiai", "オミアイ"]),
            ("40万人", "200万人", ["marrish", "マリッシュ"]),
            ("350万人", "3,500万人", ["ハッピーメール"]),
            ("200万人", "2,000万人", ["PCMAX"]),
            ("100万人", "1,100万人", ["ワクワクメール"]),
        ]
        for old_val, new_val, ctx_kw in member_fixes:
            pattern = re.escape(old_val)
            def make_repl(ov, nv, kws):
                def repl(m):
                    start = max(0, m.start() - 200)
                    ctx = content_ref[start:m.end() + 100]
                    if any(kw in ctx for kw in kws):
                        return nv
                    return m.group(0)
                return repl
            content_ref = content
            new_content = re.sub(pattern, make_repl(old_val, new_val, ctx_kw), content)
            if new_content != content:
                changes.append(f"[GROUP4] ID:14 {ctx_kw[0]}会員数 {old_val}→{new_val}")
                content = new_content

    if post_id == 142:
        member_fixes_142 = [
            ("130万人", "1,100万人", ["ワクワクメール"]),
            ("135万人", "3,500万人", ["ハッピーメール"]),
            ("200万人", "2,000万人", ["PCMAX"]),
        ]
        for old_val, new_val, ctx_kw in member_fixes_142:
            pattern = re.escape(old_val)
            def make_repl_142(ov, nv, kws):
                def repl(m):
                    start = max(0, m.start() - 200)
                    ctx = content_ref_142[start:m.end() + 100]
                    if any(kw in ctx for kw in kws):
                        return nv
                    return m.group(0)
                return repl
            content_ref_142 = content
            new_content = re.sub(pattern, make_repl_142(old_val, new_val, ctx_kw), content)
            if new_content != content:
                changes.append(f"[GROUP4] ID:142 {ctx_kw[0]}会員数 {old_val}→{new_val}")
                content = new_content

    if post_id == 135:
        old_val, new_val = "200万人", "2,300万人"
        pattern = re.escape(old_val)
        def repl_135(m):
            start = max(0, m.start() - 200)
            ctx = content[start:m.end() + 100]
            if any(kw in ctx for kw in ["タップル", "tapple"]):
                return new_val
            return m.group(0)
        new_content = re.sub(pattern, repl_135, content)
        if new_content != content:
            changes.append(f"[GROUP4] ID:135 タップル会員数 200万人→2,300万人")
            content = new_content

    # === GROUP 5: ポイントレート修正 ===
    if post_id == 15:
        for old_p, new_p in [("370P", "320P"), ("650P", "550P")]:
            if old_p in content:
                content = content.replace(old_p, new_p)
                changes.append(f"[GROUP5] ID:15 ハッピーメール ポイント {old_p}→{new_p}")

    if post_id == 16:
        # プロフ閲覧 4P→1P (context-aware)
        pattern = r'4P'
        def repl_16(m):
            start = max(0, m.start() - 150)
            ctx = content[start:m.end() + 100]
            if "プロフ" in ctx:
                return "1P"
            return m.group(0)
        new_content = re.sub(pattern, repl_16, content)
        if new_content != content:
            changes.append("[GROUP5] ID:16 PCMAX プロフ閲覧 4P→1P")
            content = new_content

    # === GROUP 6: その他 ===
    if post_id == 192:
        old_val = "2.81億円"
        new_val = "約1,268億円（警察庁2024年統計）"
        if old_val in content:
            content = content.replace(old_val, new_val)
            changes.append(f"[GROUP6] ID:192 ロマンス詐欺被害額 {old_val}→{new_val}")

    if post_id == 185:
        old_val = "コンフォートモード"
        new_val = "プライベートモード（VIPオプション必要）"
        if old_val in content:
            content = content.replace(old_val, new_val)
            changes.append(f"[GROUP6] ID:185 with {old_val}→{new_val}")

    return content, changes


# ── メイン ────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="ファクトチェック修正 2026-03-22")
    parser.add_argument("--apply", action="store_true", help="実際にWordPressを更新する")
    args = parser.parse_args()

    all_ids = sorted(set([
        532, 9, 10, 17, 18, 19, 133, 143, 150, 155, 163, 187, 193, 699,
        14, 27, 151, 136, 154, 144, 142, 135, 15, 16, 192, 185
    ]))

    creds = load_credentials()
    session = requests.Session()
    session.auth = creds

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / "factcheck_fix_2026_03_22.log"
    log_lines = []

    mode = "APPLY" if args.apply else "DRY RUN"
    header = f"=== ファクトチェック修正 ({mode}) — {datetime.now().isoformat()} ==="
    print(header)
    log_lines.append(header)

    total_changes = 0
    errors = []

    for pid in all_ids:
        print(f"\n--- ID:{pid} ---")
        try:
            post = fetch_post(session, pid)
        except requests.HTTPError as e:
            msg = f"  ❌ 取得失敗: {e}"
            print(msg)
            log_lines.append(msg)
            errors.append((pid, str(e)))
            continue

        title = post.get("title", {}).get("raw", post.get("title", {}).get("rendered", ""))
        content_raw = post.get("content", {}).get("raw", "")
        print(f"  タイトル: {title}")
        print(f"  文字数: {len(content_raw)}")

        new_content, change_list = apply_fixes(pid, content_raw)

        if not change_list:
            msg = "  変更なし"
            print(msg)
            log_lines.append(f"ID:{pid} ({title}) — 変更なし")
            continue

        for c in change_list:
            print(f"  ✏️  {c}")
            log_lines.append(f"ID:{pid} ({title}) — {c}")
        total_changes += len(change_list)

        if args.apply:
            try:
                update_post(session, pid, new_content)
                msg = f"  ✅ 更新完了"
                print(msg)
                log_lines.append(f"ID:{pid} — 更新完了")
            except requests.HTTPError as e:
                msg = f"  ❌ 更新失敗: {e}"
                print(msg)
                log_lines.append(f"ID:{pid} — 更新失敗: {e}")
                errors.append((pid, str(e)))
        else:
            print("  (ドライラン — 更新スキップ)")

    # サマリ
    summary = f"\n=== 完了: {total_changes}件の変更, {len(errors)}件のエラー ==="
    print(summary)
    log_lines.append(summary)

    if errors:
        print("エラー一覧:")
        for pid, err in errors:
            print(f"  ID:{pid} — {err}")

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    print(f"\nログ保存先: {log_path}")


if __name__ == "__main__":
    main()
