---
name: 日次PDCAルーティン
description: 毎日の会話でPDCA改善サイクルを回す。全事業の現状分析→改善実行→検証を日次ルーティンとして組み込む
type: feedback
---

毎日のルーティンとしてPDCAサイクルを回し、全事業をブラッシュアップし続ける。

**Why:** 2026-03-22に初回PDCAを実施し、sim-hikaku重複28本の統合、RapidAPI 24本SEO改善、タスク修復、X投稿V2化など大きな成果が出た。これを一度きりでなく継続的に回すことで収益最大化を加速する。

**How to apply:**
毎日の会話（特に /morning-briefing や「おはよう」等の開始時）で以下を自動実行:

1. **Check（検証）**: 前回のPDCA施策の効果を数値で確認
   - Search Console: CTR変化、インデックス状況
   - RapidAPI: API呼び出し数、新規サブスクライバー
   - Gumroad/X: クリック数、売上
   - タスクログ: エラー・遅延がないか

2. **Act（改善点の特定）**: 数値が動いていない事業を特定し改善案を出す

3. **Plan（計画）**: 当日実行すべき改善アクションを優先順位付け

4. **Do（実行）**: 自動実行可能なものは即実行（並列エージェント活用）

**対象事業（優先順）:**
- 3サイト（SEO・CTR・アフィリエイト導線・重複チェック）
- RapidAPI（リスティング改善・マーケティング）
- Gumroad（X投稿効果・価格テスト）
- Chrome/VS Code拡張（審査状況・ダウンロード数）
- その他デジタル商品（Apify、WP Linker等）

**作成ファイル一覧（参照用）:**
- 3サイトSEO計画: `{site}/docs/seo-optimization-plan.md`
- RapidAPIマーケティング: `api-services/docs/rapidapi-marketing-plan.md`
- RapidAPI更新チェックリスト: `api-services/docs/rapidapi-update-checklist.md`
- X投稿V2: `gumroad-notion/marketing/x-posts-v2.md`
- 重複統合スクリプト: `sim-hikaku.online/scripts/consolidate_duplicates.py`
