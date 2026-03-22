"""Fix remaining factual errors in otona-match.com WordPress articles.
Run with --apply to actually update articles. Without it, dry-run only.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from requests.auth import HTTPBasicAuth

SECRETS_PATH = Path(__file__).resolve().parents[2] / "config" / "secrets.json"
BASE_URL = "https://otona-match.com/?rest_route=/wp/v2/posts"
LOG_LINES: list[str] = []


def log(msg: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    LOG_LINES.append(line)


def load_auth() -> HTTPBasicAuth:
    secrets = json.loads(SECRETS_PATH.read_text(encoding="utf-8"))
    wp = secrets["wordpress"]
    return HTTPBasicAuth(wp["username"], wp["app_password"])


def fetch_post(post_id: int, auth: HTTPBasicAuth) -> dict:
    url = f"{BASE_URL}/{post_id}"
    r = requests.get(url, auth=auth, timeout=30)
    r.raise_for_status()
    return r.json()


def update_post(post_id: int, content: str, auth: HTTPBasicAuth) -> None:
    url = f"{BASE_URL}/{post_id}"
    r = requests.post(url, auth=auth, json={"content": content}, timeout=60)
    r.raise_for_status()


# --- Fix definitions ---

def fix_192(content: str) -> tuple[str, list[str]]:
    """ID:192 — ロマンス詐欺被害額"""
    changes = []
    # Try several patterns for the old amount
    patterns = [
        (r'2[\.,]?81億円', '約1,268億円（警察庁2024年統計）'),
        (r'2億81[0-9]*万?円', '約1,268億円（警察庁2024年統計）'),
        (r'約?2\.81億円', '約1,268億円（警察庁2024年統計）'),
    ]
    for pat, repl in patterns:
        new_content, n = re.subn(pat, repl, content)
        if n > 0:
            changes.append(f"Replaced '{pat}' -> '{repl}' ({n}x)")
            return new_content, changes

    # Broader: any yen amount within 200 chars of ロマンス詐欺
    m = re.search(r'(ロマンス詐欺.{0,200}?)([\d,\.]+億?万?円)', content, re.DOTALL)
    if m:
        old_val = m.group(2)
        new_content = content[:m.start(2)] + '約1,268億円（警察庁2024年統計）' + content[m.end(2):]
        changes.append(f"Replaced '{old_val}' near ロマンス詐欺 -> '約1,268億円（警察庁2024年統計）'")
        return new_content, changes

    changes.append("WARNING: No ロマンス詐欺 amount pattern found")
    return content, changes


def fix_185(content: str) -> tuple[str, list[str]]:
    """ID:185 — コンフォートモード → プライベートモード"""
    changes = []
    # Replace feature name
    if 'コンフォートモード' in content:
        content = content.replace('コンフォートモード', 'プライベートモード（VIPオプション必要）')
        changes.append("Replaced 'コンフォートモード' -> 'プライベートモード（VIPオプション必要）'")
    else:
        changes.append("WARNING: 'コンフォートモード' not found")

    # Remove (無料) near プライベートモード
    content_new = re.sub(r'プライベートモード（VIPオプション必要）\s*[（(]無料[）)]', 'プライベートモード（VIPオプション必要）', content)
    if content_new != content:
        changes.append("Removed (無料) near プライベートモード")
        content = content_new

    # Also check original context: if (無料) was right after コンフォートモード before replacement
    content_new = re.sub(r'プライベートモード（VIPオプション必要）\s*（無料）', 'プライベートモード（VIPオプション必要）', content)
    if content_new != content:
        changes.append("Removed （無料） near feature")
        content = content_new

    return content, changes


def fix_15(content: str) -> tuple[str, list[str]]:
    """ID:15 — ハッピーメール ポイント数"""
    changes = []
    # 370P near 3,000円 → 320P
    new, n = re.subn(r'(?<=3,000円.{0,50})370P', '320P', content, flags=re.DOTALL)
    if n == 0:
        new, n = re.subn(r'370P(?=.{0,50}3,000円)', '320P', content, flags=re.DOTALL)
    if n == 0:
        # Try broader
        new, n = re.subn(r'370P', '320P', content)
    if n > 0:
        changes.append(f"Replaced '370P' -> '320P' ({n}x)")
        content = new

    # 650P near 5,000円 → 550P
    new, n = re.subn(r'(?<=5,000円.{0,50})650P', '550P', content, flags=re.DOTALL)
    if n == 0:
        new, n = re.subn(r'650P(?=.{0,50}5,000円)', '550P', content, flags=re.DOTALL)
    if n == 0:
        new, n = re.subn(r'650P', '550P', content)
    if n > 0:
        changes.append(f"Replaced '650P' -> '550P' ({n}x)")
        content = new

    if not changes:
        changes.append("WARNING: No point values found to fix")
    return content, changes


def fix_16(content: str) -> tuple[str, list[str]]:
    """ID:16 — PCMAX プロフ閲覧 4P→1P"""
    changes = []
    # Look for 4P near プロフ context
    # Try pattern: number P near プロフィール閲覧 or プロフ閲覧
    pat = r'(プロフ(?:ィール)?閲覧.{0,80}?)4P'
    new, n = re.subn(pat, r'\g<1>1P', content, flags=re.DOTALL)
    if n == 0:
        pat2 = r'4P(.{0,80}?プロフ(?:ィール)?閲覧)'
        new, n = re.subn(pat2, r'1P\1', content, flags=re.DOTALL)
    if n == 0:
        # Try just replacing 4P in table-like context
        new, n = re.subn(r'4P', '1P', content)
    if n > 0:
        changes.append(f"Replaced '4P' -> '1P' ({n}x)")
        content = new

    # 40円 → 10円 near プロフ context
    new, n = re.subn(r'40円', '10円', content)
    if n > 0:
        changes.append(f"Replaced '40円' -> '10円' ({n}x)")
        content = new

    if not changes:
        changes.append("WARNING: No PCMAX profile cost found")
    return content, changes


def fix_26(content: str) -> tuple[str, list[str]]:
    """ID:26 — 15.6% → 約25%"""
    changes = []
    patterns = [
        (r'約?15\.6%', '約25%（こども家庭庁2024年調査）'),
        (r'約?15\.6％', '約25%（こども家庭庁2024年調査）'),
    ]
    for pat, repl in patterns:
        new, n = re.subn(pat, repl, content)
        if n > 0:
            changes.append(f"Replaced '{pat}' -> '{repl}' ({n}x)")
            return new, changes
    changes.append("WARNING: '15.6%' not found")
    return content, changes


def fix_10(content: str) -> tuple[str, list[str]]:
    """ID:10 — ペアーズ料金修正"""
    changes = []
    replacements = [
        ('3,300円/月', '3,033円/月'),
        ('3,300円／月', '3,033円/月'),
        ('2,300円/月', '2,366円/月'),
        ('2,300円／月', '2,366円/月'),
        ('1,650円/月', '1,675円/月'),
        ('1,650円／月', '1,675円/月'),
    ]
    for old, new_val in replacements:
        if old in content:
            content = content.replace(old, new_val)
            changes.append(f"Replaced '{old}' -> '{new_val}'")

    if not changes:
        # Try without /月
        for old_price, new_price in [('3,300円', '3,033円'), ('2,300円', '2,366円'), ('1,650円', '1,675円')]:
            # Only replace in context of 月 pricing (3ヶ月/6ヶ月/12ヶ月)
            pat = rf'{re.escape(old_price)}(/月|／月|<)'
            new_content = re.sub(pat, f'{new_price}\\1', content)
            if new_content != content:
                changes.append(f"Replaced '{old_price}' -> '{new_price}' (context match)")
                content = new_content

    if not changes:
        changes.append("WARNING: No ペアーズ pricing found to fix")
    return content, changes


def fix_11(content: str) -> tuple[str, list[str]]:
    """ID:11 — with合計金額修正"""
    changes = []
    replacements = [
        ('9,000円', '10,400円'),
        ('13,300円', '15,360円'),
        ('22,000円', '25,400円'),
    ]
    for old, new_val in replacements:
        if old in content:
            content = content.replace(old, new_val)
            changes.append(f"Replaced '{old}' -> '{new_val}'")

    if not changes:
        changes.append("WARNING: No with pricing totals found to fix")
    return content, changes


def fix_159(content: str) -> tuple[str, list[str]]:
    """ID:159 — Goens月額"""
    changes = []
    if '4,800円' in content:
        content = content.replace('4,800円', '5,000円')
        changes.append("Replaced '4,800円' -> '5,000円'")
    else:
        changes.append("WARNING: '4,800円' not found")
    return content, changes


FIXES = [
    (192, "危険人物の見分け方", fix_192),
    (185, "職場バレ対策", fix_185),
    (15, "ハッピーメール", fix_15),
    (16, "PCMAX", fix_16),
    (26, "結婚体験談", fix_26),
    (10, "ペアーズレビュー", fix_10),
    (11, "withレビュー", fix_11),
    (159, "50代活用術", fix_159),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix factual errors in otona-match.com articles")
    parser.add_argument("--apply", action="store_true", help="Actually update WordPress")
    args = parser.parse_args()

    auth = load_auth()
    log(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    log(f"Processing {len(FIXES)} articles...")

    success_count = 0
    warn_count = 0

    for post_id, title, fix_fn in FIXES:
        log(f"\n--- ID:{post_id} — {title} ---")
        try:
            post = fetch_post(post_id, auth)
            original = post["content"]["rendered"]
            updated, changes = fix_fn(original)

            for c in changes:
                log(f"  {c}")
                if c.startswith("WARNING"):
                    warn_count += 1

            if updated == original:
                log(f"  No changes made.")
                continue

            if args.apply:
                update_post(post_id, updated, auth)
                log(f"  ✓ Updated on WordPress")
            else:
                log(f"  [DRY-RUN] Would update")
            success_count += 1

        except Exception as e:
            log(f"  ERROR: {e}")
            warn_count += 1

    log(f"\n=== Summary: {success_count} articles modified, {warn_count} warnings ===")

    # Save log
    log_dir = Path(__file__).resolve().parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"fix_factcheck_misc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    log_file.write_text("\n".join(LOG_LINES), encoding="utf-8")
    print(f"\nLog saved to: {log_file}")


if __name__ == "__main__":
    main()
