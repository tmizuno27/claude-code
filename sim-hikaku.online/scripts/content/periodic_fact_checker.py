#!/usr/bin/env python3
"""
定期ファクトチェック＆リライトスクリプト
SIM比較オンライン (sim-hikaku.online) 版。

実行モード:
  --mode check    : チェックのみ（レポート生成）
  --mode fix      : チェック＋自動修正（修正後のMDを上書き）
  --mode rewrite  : 投稿済み記事のリライト提案を生成
  --target drafts : ドラフト記事のみ
  --target published : 投稿済み記事のみ
  --target all    : 全記事（デフォルト）
  --limit N       : 処理する記事数の上限（API コスト管理用）
"""

import argparse
import io
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Windows UTF-8 出力修正
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# プロジェクトルート
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
ARTICLES_DIR = OUTPUTS_DIR / "articles"
REPORTS_DIR = OUTPUTS_DIR / "fact-check-reports"

# ログ設定
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            OUTPUTS_DIR / "periodic-fact-check.log", encoding="utf-8"
        ),
    ],
)
logger = logging.getLogger(__name__)

# --- 依存ライブラリ ---
try:
    import anthropic
except ImportError:
    anthropic = None
    logger.warning("anthropic ライブラリ未インストール。pip install anthropic")

try:
    import requests
except ImportError:
    requests = None

# --- 定数 ---
FACT_CHECK_CATEGORIES = {
    "price": "料金・価格・費用",
    "plan": "プラン内容・データ容量",
    "campaign": "キャンペーン・特典",
    "service": "サービス名・URL・仕様",
    "speed": "通信速度・エリア",
    "procedure": "手続き・MNP・契約",
}

DEEP_FACT_CHECK_PROMPT = """あなたはSIM比較オンライン（sim-hikaku.online）の定期ファクトチェッカーです。
以下のブログ記事を詳細に検証し、古い情報・誤情報・要更新箇所を洗い出してください。

## 検証カテゴリ
1. **料金・価格**: 各格安SIMの月額料金、オプション料金、初期費用が最新か
2. **プラン内容**: データ容量、通話プラン、家族割等の内容が現行プランと一致するか
3. **キャンペーン**: キャンペーン情報が現在も有効か（終了日の確認）
4. **サービス仕様**: サービス名、URL、対応端末、eSIM対応等が正確か
5. **通信速度・エリア**: 速度実測データ、エリアカバー情報が最新か
6. **手続き・MNP**: MNP手順、契約手続き、解約方法が現行制度と一致するか

## 格安SIM検証基準（2026年3月時点）
- LINEMO/ahamo/povo/楽天モバイル/UQモバイル/ワイモバイル/mineo/IIJmio等の最新料金を確認
- MNPワンストップ方式（2023年5月〜）対応状況
- eSIM対応状況の最新化
- 各社キャンペーンの有効期限確認

## 出力形式（JSON）
```json
{
  "verdict": "NEEDS_UPDATE" | "OK",
  "urgency": "critical" | "high" | "medium" | "low",
  "issues": [
    {
      "category": "price|plan|campaign|service|speed|procedure",
      "line_hint": "該当する記述の一部（20文字程度）",
      "current_text": "記事に書かれている内容",
      "correct_text": "正しい最新の内容",
      "source": "根拠となる情報源",
      "severity": "critical|high|medium|low"
    }
  ],
  "rewrite_suggestions": [
    "リライトすべき箇所の提案（文章の改善、SEO最適化等）"
  ]
}
```

critical: 料金の大幅な誤り、終了済みプラン/キャンペーンの掲載
high: 料金の軽微な変更、手続き方法の変更
medium: 速度データの古さ、キャンペーン期間のズレ
low: 表現の改善、SEO最適化の余地"""

AUTO_FIX_PROMPT = """以下のブログ記事の指摘箇所を修正してください。
修正後の記事全文をMarkdownで出力してください。
修正箇所以外は一切変更しないでください。

## 修正指示:
{issues_json}

## 記事本文:
{article_text}"""


def load_secrets():
    """secrets.json を読み込む"""
    secrets_path = CONFIG_DIR / "secrets.json"
    if not secrets_path.exists():
        logger.error(f"secrets.json が見つかりません: {secrets_path}")
        return {}
    with open(secrets_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_claude_api_key():
    """Claude API キーを取得（ローカル → nambei-oyaji.com フォールバック）"""
    secrets = load_secrets()
    key = secrets.get("claude_api", {}).get("api_key", "")
    if key and "YOUR" not in key:
        return key
    # Fallback: shared key from nambei-oyaji.com
    fallback = PROJECT_ROOT.parent / "nambei-oyaji.com" / "config" / "secrets.json"
    if fallback.exists():
        with open(fallback, "r", encoding="utf-8") as f:
            return json.load(f).get("claude_api", {}).get("api_key", "")
    return ""


def collect_draft_articles():
    """ドラフト記事（MD ファイル）を収集"""
    articles = []
    if not ARTICLES_DIR.exists():
        return articles

    for date_dir in sorted(ARTICLES_DIR.iterdir()):
        if not date_dir.is_dir():
            continue
        for md_file in sorted(date_dir.glob("*.md")):
            stat = md_file.stat()
            articles.append({
                "path": md_file,
                "filename": md_file.name,
                "source": "draft",
                "date_dir": date_dir.name,
                "last_modified": datetime.fromtimestamp(stat.st_mtime),
                "size": stat.st_size,
            })
    return articles


def collect_published_articles():
    """WordPress投稿済み記事を収集"""
    articles = []
    if requests is None:
        logger.warning("requests ライブラリ未インストール。投稿済み記事のチェックをスキップ")
        return articles

    secrets = load_secrets()
    wp_config = secrets.get("wordpress", {})
    rest_url = wp_config.get("api_url", "https://sim-hikaku.online/wp-json/wp/v2")
    username = wp_config.get("username", "")
    app_password = wp_config.get("app_password", "")

    if not username:
        logger.warning("WordPress設定が不完全。投稿済み記事のチェックをスキップ")
        return articles

    from base64 import b64encode
    credentials = f"{username}:{app_password}"
    token = b64encode(credentials.encode()).decode()
    headers = {"Authorization": f"Basic {token}"}

    page = 1
    while True:
        try:
            resp = requests.get(
                f"{rest_url}/posts",
                params={"per_page": 20, "page": page, "status": "publish"},
                headers=headers,
                timeout=30,
            )
            if resp.status_code != 200:
                break
            posts = resp.json()
            if not posts:
                break

            for post in posts:
                articles.append({
                    "wp_id": post["id"],
                    "title": post["title"]["rendered"],
                    "content": post["content"]["rendered"],
                    "source": "published",
                    "slug": post["slug"],
                    "last_modified": post["modified"],
                    "url": post["link"],
                })
            page += 1
        except Exception as e:
            logger.error(f"WordPress API エラー: {e}")
            break

    return articles


def fact_check_article(api_key, article_text, filename=""):
    """Claude API で記事をファクトチェック"""
    if anthropic is None:
        return {"verdict": "SKIP", "issues": [], "rewrite_suggestions": []}

    check_text = article_text[:8000] if len(article_text) > 8000 else article_text

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=DEEP_FACT_CHECK_PROMPT,
            messages=[{
                "role": "user",
                "content": f"ファイル名: {filename}\n\n記事本文:\n{check_text}",
            }],
        )
        result_text = response.content[0].text.strip()

        json_match = re.search(r"```json\s*(.*?)\s*```", result_text, re.DOTALL)
        if json_match:
            result_text = json_match.group(1)

        start = result_text.find("{")
        end = result_text.rfind("}") + 1
        if start >= 0 and end > start:
            result_text = result_text[start:end]

        return json.loads(result_text)

    except json.JSONDecodeError as e:
        logger.warning(f"JSON パースエラー ({filename}): {e}")
        return {"verdict": "PARSE_ERROR", "issues": [], "raw": result_text}
    except Exception as e:
        logger.error(f"ファクトチェック API エラー ({filename}): {e}")
        return {"verdict": "API_ERROR", "issues": [], "error": str(e)}


def auto_fix_article(api_key, article_text, issues):
    """指摘箇所を自動修正"""
    if anthropic is None or not issues:
        return None

    issues_json = json.dumps(issues, ensure_ascii=False, indent=2)
    prompt = AUTO_FIX_PROMPT.format(issues_json=issues_json, article_text=article_text)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )
        fixed_text = response.content[0].text.strip()

        if fixed_text.startswith("```"):
            lines = fixed_text.split("\n")
            fixed_text = "\n".join(lines[1:-1]) if lines[-1].strip() == "```" else "\n".join(lines[1:])

        return fixed_text
    except Exception as e:
        logger.error(f"自動修正 API エラー: {e}")
        return None


def generate_report(results, report_path):
    """ファクトチェックレポートを生成"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# 定期ファクトチェックレポート — SIM比較オンライン {now}\n",
        f"## サマリー\n",
        f"- 検査記事数: {len(results)}",
        f"- 要修正: {sum(1 for r in results if r.get('verdict') == 'NEEDS_UPDATE')}",
        f"- 問題なし: {sum(1 for r in results if r.get('verdict') == 'OK')}",
        f"- エラー: {sum(1 for r in results if r.get('verdict') in ('API_ERROR', 'PARSE_ERROR', 'SKIP'))}",
        "",
    ]

    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    needs_update = [r for r in results if r.get("verdict") == "NEEDS_UPDATE"]
    needs_update.sort(key=lambda r: severity_order.get(r.get("urgency", "low"), 4))

    if needs_update:
        lines.append("---\n")
        lines.append("## 要修正記事\n")

        for r in needs_update:
            urgency_label = {"critical": "致命的", "high": "高", "medium": "中", "low": "低"}
            lines.append(f"### {r['filename']} [{urgency_label.get(r.get('urgency', 'low'), '?')}]")
            lines.append(f"- ソース: {r.get('source', '?')}")
            if r.get("auto_fixed"):
                lines.append("- **自動修正済み**")
            lines.append("")

            for issue in r.get("issues", []):
                cat_label = FACT_CHECK_CATEGORIES.get(issue.get("category", ""), issue.get("category", ""))
                sev = issue.get("severity", "medium")
                lines.append(f"  - **[{cat_label}]** ({sev})")
                lines.append(f"    - 現在: {issue.get('current_text', '?')}")
                lines.append(f"    - 正しい: {issue.get('correct_text', '?')}")
                if issue.get("source"):
                    lines.append(f"    - 根拠: {issue.get('source')}")
                lines.append("")

            if r.get("rewrite_suggestions"):
                lines.append("  **リライト提案:**")
                for sug in r["rewrite_suggestions"]:
                    lines.append(f"  - {sug}")
                lines.append("")

    ok_articles = [r for r in results if r.get("verdict") == "OK"]
    if ok_articles:
        lines.append("---\n")
        lines.append("## 問題なし\n")
        for r in ok_articles:
            lines.append(f"- {r['filename']}")
        lines.append("")

    report_text = "\n".join(lines)

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    logger.info(f"レポート生成: {report_path}")
    return report_text


def main():
    parser = argparse.ArgumentParser(description="定期ファクトチェック＆リライト (sim-hikaku.online)")
    parser.add_argument("--mode", choices=["check", "fix", "rewrite"], default="check",
                        help="実行モード (check=チェックのみ, fix=自動修正, rewrite=リライト提案)")
    parser.add_argument("--target", choices=["drafts", "published", "all"], default="all",
                        help="対象 (drafts/published/all)")
    parser.add_argument("--limit", type=int, default=10,
                        help="処理する記事数の上限（APIコスト管理）")
    parser.add_argument("--days", type=int, default=7,
                        help="最終チェックからN日以上経過した記事のみ対象")
    args = parser.parse_args()

    logger.info(f"=== 定期ファクトチェック開始 (sim-hikaku.online, mode={args.mode}, target={args.target}, limit={args.limit}) ===")

    api_key = get_claude_api_key()
    if not api_key:
        logger.error("API キーがないため終了")
        sys.exit(1)

    articles = []
    if args.target in ("drafts", "all"):
        drafts = collect_draft_articles()
        logger.info(f"ドラフト記事: {len(drafts)}件")
        articles.extend(drafts)

    if args.target in ("published", "all"):
        published = collect_published_articles()
        logger.info(f"投稿済み記事: {len(published)}件")
        articles.extend(published)

    if not articles:
        logger.info("対象記事なし。終了")
        return

    articles = articles[:args.limit]
    logger.info(f"チェック対象: {len(articles)}件")

    results = []
    for i, article in enumerate(articles, 1):
        filename = article.get("filename", article.get("slug", "unknown"))
        logger.info(f"[{i}/{len(articles)}] チェック中: {filename}")

        if article["source"] == "draft":
            with open(article["path"], "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = re.sub(r"<[^>]+>", "", article.get("content", ""))

        result = fact_check_article(api_key, text, filename)
        result["filename"] = filename
        result["source"] = article["source"]

        if args.mode == "fix" and result.get("verdict") == "NEEDS_UPDATE" and result.get("issues"):
            if article["source"] == "draft":
                logger.info(f"  -> 自動修正中: {filename}")
                fixed = auto_fix_article(api_key, text, result["issues"])
                if fixed:
                    with open(article["path"], "w", encoding="utf-8") as f:
                        f.write(fixed)
                    result["auto_fixed"] = True
                    logger.info(f"  -> 修正完了: {filename}")
                else:
                    result["auto_fixed"] = False
                    logger.warning(f"  -> 修正失敗: {filename}")

        verdict = result.get("verdict", "?")
        issue_count = len(result.get("issues", []))
        if verdict == "NEEDS_UPDATE":
            logger.warning(f"  結果: {verdict} ({issue_count}件の問題)")
        else:
            logger.info(f"  結果: {verdict}")

        results.append(result)

    date_str = datetime.now().strftime("%Y-%m-%d")
    report_path = REPORTS_DIR / f"fact-check-{date_str}.md"
    generate_report(results, report_path)

    needs_update = sum(1 for r in results if r.get("verdict") == "NEEDS_UPDATE")
    critical = sum(1 for r in results if r.get("urgency") == "critical")
    auto_fixed = sum(1 for r in results if r.get("auto_fixed"))

    logger.info(f"=== 定期ファクトチェック完了 ===")
    logger.info(f"  要修正: {needs_update}件 (致命的: {critical}件)")
    if args.mode == "fix":
        logger.info(f"  自動修正: {auto_fixed}件")
    logger.info(f"  レポート: {report_path}")

    if critical > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
