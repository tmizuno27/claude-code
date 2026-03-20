---
name: pSEO AIツール比較サイト
description: Next.js SSGで291 AIツールの比較ページを自動生成するプログラマティックSEOサイト
type: project
---

## pSEO AIツール比較サイト

- **ステータス**: Vercelデプロイ完了（2026-03-20）、GSC登録済み（sitemap送信済み、インデックス待ち）
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

### 完了タスク（2026-03-20）
- Vercelデプロイ: `ai-tool-compare-nu.vercel.app`
- sitemap.xml生成: `generate-sitemap.js` → 4,200 URL
- GSC登録: `ai-tool-compare-nu.vercel.app` プロパティ追加済み
- Google検証: HTMLタグ + HTMLファイル両方配置

### 残タスク
1. カスタムドメイン取得・設定
2. アフィリエイトリンク設置
3. GSC sitemap「成功」確認（翌日）

**Why:** 英語圏AIツール比較の競合が弱く、300ツールで44K+ページ生成可能。月$8K-15K目標
**How to apply:** コンテンツはテンプレ感排除、独自スコアリング、800語以上のユニーク文章
