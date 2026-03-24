---
name: keisan-tools.com 計算ツールサイト事業
description: keisan-tools.com - 日本語計算・シミュレーターサイト（Next.js 16 SSG、AdSense+アフィリエイト収益化）
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

### 現状（2026-03-24）
- 6計算ツール公開済み（住宅ローン、所得税、手取り、BMI、日数計算、複利）
- 6カテゴリ: money, health, life, business, math, education
- 15静的ページ生成（トップ+6カテゴリ+6計算+α）

### 目標
- 300ページ以上の計算ツール → AdSense申請 → 月5-10万円
- JSON駆動（`data/calculators/`にJSON追加するだけでページ自動生成）
- 構造化データ（FAQ, Breadcrumb）、サイトマップ対応済み

### 収益化
- Google AdSense（30ページ以上で申請）
- アフィリエイト（A8, AccessTrade, Moshimo, Value Commerce）

**Why:** 日本語計算ツールサイトはブルーオーシャン。keisan.casio.jpが独占的だが、UI/UX・SEO・カテゴリ網羅で十分差別化可能。100%自動運用。
**How to apply:** ページ量産→GSC登録→AdSense申請の順で進める。計算ロジックの正確性（特に税率・社会保険料）は最新データで検証必須。
