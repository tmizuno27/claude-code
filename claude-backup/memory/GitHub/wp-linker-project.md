---
name: WP Linker SaaS Project
description: WP Linker Micro SaaS。2026-03-28大幅改善（Free$0プラン/テスティモニアル/セキュリティ強化/SEO/オンボーディング）Vercelデプロイ済み
type: project
---

## 2026-03-28更新
- Free $0プラン新設（30記事/週1回分析）、Pro $29→$19、Agency $79→$49
- テスティモニアル3件追加、信頼バッジ追加
- セキュリティ: 全APIルート認証追加、SSRF防止、セキュリティヘッダー5種追加
- SEO: sitemap.ts/robots.txt自動生成、構造化データ更新
- オンボーディング: 初回ユーザー3ステップガイド追加
- Vercelデプロイ完了（ビルド45秒、11ページ）

## WP Linker — WordPress Internal Link Optimizer SaaS

**プロジェクトパス**: `claude-code/saas/wp-linker/`
**本番URL**: https://wp-linker.vercel.app
**Supabase**: https://acagbtiscghcybrkcajh.supabase.co

### 技術スタック
- Next.js 15 + Tailwind CSS v4
- Supabase (Auth + PostgreSQL + RLS)
- Vercel deployment
- WordPress REST API

### テスト用WPサイト接続情報
- REST API URL: `https://nambei-oyaji.com/wp-json/wp/v2`
- Username: `t.mizuno27@gmail.com`
- App Password: `WutS MaRq ukGx OcQ8 uhBj Ej0D`

### テスト用SaaSアカウント
- Email: `t.mizuno27+x@gmail.com`

### Stripe
- 未実装（Stripeが機能しないため保留。LemonSqueezy等の代替を検討）

**Why:** internal_linker.pyスクリプトをSaaS化して収益源にする
**How to apply:** WP Linker関連の作業時にこの情報を参照
