---
name: はてなブログ事業
description: nambei-oyaji.hatenablog.com — WordPress記事のダイジェスト版を自動投稿、本家への送客チャネル
type: project
---

## はてなブログ「南米おやじの海外生活メモ」

- **URL**: https://nambei-oyaji.hatenablog.com/
- **はてなID**: miccho27
- **ブログID**: nambei-oyaji.hatenablog.com
- **APIキー**: secrets.json の `hatena` セクション
- **編集モード**: Markdown
- **目的**: 本家WordPress（nambei-oyaji.com）への送客チャネル。被リンク獲得+はてなコミュニティからの流入

## 運用ルール

- WordPress記事のコピペは禁止（重複コンテンツペナルティ回避）
- Claude APIで本家記事を1/3以下のダイジェスト（体験メモ調）に変換
- 末尾に本家記事への誘導リンクを必ず挿入
- アフィリエイトリンクは載せない（はてな規約+送客目的のため）

## 自動化パイプライン

- **スクリプト**: `sites/nambei-oyaji.com/scripts/publishing/`
  - `hatena_converter.py` — WP記事→ダイジェスト変換（Claude API使用）
  - `hatena_publisher.py` — AtomPub APIで自動投稿
  - `hatena_pipeline.py` — 統合パイプライン（変換+投稿一括）
- **Task Scheduler**: `HatenaPipeline` — 月・水・金 7:00 PYT（日本時間19:00）、1記事ずつ投稿。収益記事を優先
- **ログ**: `logs/hatena-pipeline.log`
- **投稿記録**: `published/hatena-log.json`
- **変換済み記事**: `outputs/hatena/`

## 開設日・初期投稿

- 2026-03-24 開設、7記事公開済み（#1〜#5, #14, #17 + #4自動変換）
