---
name: pSEO AIツール比較サイト
description: Next.js SSGで291 AIツールの比較ページを自動生成するプログラマティックSEOサイト
type: project
---

## pSEO AIツール比較サイト

- **ステータス**: ローカルビルド完了、デプロイ未完（2026-03-15）
- **プロジェクトパス**: `claude-code/pseo-saas/`
- **技術**: Next.js 16 (App Router, SSG, `output: 'export'`)
- **データ**: `data/tools.json` — 291ツール、12カテゴリ
- **生成ページ数**: 4,003ページ（ホーム + 12カテゴリ + 291ツール + 3,697比較）

### カテゴリ（12）
ai-writing(40), ai-image(35), ai-chatbot(20), ai-coding(25), ai-video(25), ai-audio(20), ai-automation(30), ai-seo(22), ai-design(20), ai-productivity(24), ai-translation(15), ai-customer-service(15)

### 主要ファイル
- `site/src/lib/tools.js` — データ読み込み、カテゴリ管理、比較ペア生成
- `site/src/lib/comparison.js` — 決定論的コンテンツ生成（intro/pricing/feature/verdict/FAQ）
- `site/src/app/compare/[slug]/page.js` — 比較ページ（JSON-LD FAQ schema付き）
- `site/src/app/tool/[slug]/page.js` — ツール詳細ページ
- `site/src/app/category/[slug]/page.js` — カテゴリ一覧ページ

### 残タスク
1. sitemap.xml生成スクリプト作成（静的エクスポートではsitemap.js不可）
2. Vercelデプロイ + ドメイン取得
3. アフィリエイトリンク設置
4. Google Search Console登録

**Why:** 英語圏AIツール比較の競合が弱く、300ツールで44K+ページ生成可能。月$8K-15K目標
**How to apply:** コンテンツはテンプレ感排除、独自スコアリング、800語以上のユニーク文章
