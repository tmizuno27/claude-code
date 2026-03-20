---
name: Product Factory事業
description: AIエージェント×デジタル商品自動量産ビジネス。Felix(OpenClaw)モデルにインスパイア。4エージェント体制でGumroad/RapidAPI/Chrome/VSCode商品を自動生成
type: project
---

## 概要
Claude Codeエージェント4体（product-factory, market-researcher, product-builder, listing-publisher）が
デジタル商品を自動で企画→制作→出品素材生成する仕組み。

**Why:** OpenClawの「Felix」事例（月売上1,200万円・従業員ゼロ）にインスパイア。既存56商品+自動化基盤をフル活用して商品数を10倍に拡大する。

**How to apply:**
- `/product-factory` で1商品自動生成（pipeline.jsonの先頭を処理）
- `/market-researcher` で新企画を5-10件自動追加
- Phase 1: Gumroad Notionテンプレ優先、Phase 2: RapidAPI、Phase 3: 自己改善ループ
- プロジェクトパス: `claude-code/product-factory/`

## 進捗
- **Phase 1完了（2026-03-20）:**
  - エージェント4体定義済み
  - Gumroad Notionテンプレート8商品 → Notion API構築+共有リンク取得+Gumroad出品 全完了
  - RapidAPI 3本（PDF Generator, Placeholder Image, Markdown Converter）→ CF Workersデプロイ+RapidAPI Studio出品 全完了
  - サムネイル38枚生成済み、X投稿16件スケジュール済み
  - pipeline.json: 全11件completed

## 次のステップ（Phase 2 — 2026-03-22日曜お昼から再開予定）
1. `run_pipeline.py` — 毎日9:00 PYTにTask Schedulerで自動実行
2. market-researcher — 毎週月曜に10件の商品企画を自動生成
3. `deploy_rapidapi.py` — wrangler deployラッパー
4. Phase 3: nightly_review.py（23:00 PYT自己改善ループ）、collect_stats.py
