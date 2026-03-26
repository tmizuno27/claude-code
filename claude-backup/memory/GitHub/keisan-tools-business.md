---
name: keisan-tools.com 計算ツールサイト事業
description: keisan-tools.com - 日本語計算・シミュレーターサイト（Next.js 16 SSG、441計算ツール、AdSense+アフィリエイト収益化）
type: project
---

## keisan-tools.com — 高精度計算シミュレーションサイト

2026-03-24 新規事業として開始。ブルーオーシャン×自動化×高収益化率の3条件で選定。

- **URL**: https://keisan-tools.com
- **ドメイン**: Cloudflare登録（$10.46/年、2027-03-24更新）
- **ホスティング**: Vercel（無料枠、静的エクスポート）
- **DNS**: Cloudflare CNAME → cname.vercel-dns.com（DNS only）
- **技術**: Next.js 16 App Router + SSG (`output: 'export'`)、TypeScript、CSS custom properties（Apple風デザイン）
- **プロジェクトパス**: `claude-code/saas/keisan-tools/site/`
- **GA4**: G-3R1LVHX9VJ
- **AdSense**: ca-pub-7177224921699744（コード設置済み）

### 現状（2026-03-26）
- **441計算ツール**公開済み（457静的ページ生成 = 441ツール + 7カテゴリ + 固定ページ）
- 7カテゴリ: money, health, life, business, math, education, unit
- sitemap.xml + robots.txt 追加済み（2026-03-26）
- Google Indexing API送信スクリプト整備済み（`scripts/submit_indexing.py`）

### 目標
- AdSense申請 → 月5-10万円（441ページで条件クリア済み）
- JSON駆動（`data/calculators/`にJSON追加するだけでページ自動生成）
- 構造化データ（FAQ, Breadcrumb）対応済み

### 収益化
- Google AdSense（コード設置済み、審査通過待ち or 未申請）
- アフィリエイト（A8, AccessTrade, Moshimo, Value Commerce）

**Why:** 日本語計算ツールサイトはブルーオーシャン。keisan.casio.jpが独占的だが、UI/UX・SEO・カテゴリ網羅で十分差別化可能。100%自動運用。
**How to apply:** sitemap/robots追加済み。次はIndexing API全URL送信→AdSense申請→アフィリエイトリンク挿入。
