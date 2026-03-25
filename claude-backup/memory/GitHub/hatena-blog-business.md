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
- **Task Scheduler**: `HatenaPipeline` — 月・水・金 7:00 PYT（日本時間19:00）、2記事ずつ投稿。収益記事を優先
- **ログ**: `logs/hatena-pipeline.log`（RotatingFileHandler、1MB×3世代）
- **投稿記録**: `published/hatena-log.json`
- **変換済み記事**: `outputs/hatena/`
- **Healthchecks.io**: `691cd9ed-9f36-43ae-a4cc-812b8d4e687d`

## 品質対策（2026-03-24監査で追加）

- XMLエスケープ: CDATA方式でMarkdown記法の破損を防止
- UTMリンク: 後処理で `?utm_source=hatena&utm_medium=blog&utm_campaign=digest` を保証
- リトライ: Claude API・AtomPub API共に3回exponential backoff
- 投稿間隔: 30秒（スパム検知回避）
- タイトル生成: article_id % len(prefixes) で冪等化

## 開設日・初期投稿

- 2026-03-24 開設、12記事公開済み（#1〜#5, #9, #12, #14, #16, #17, #22, #25）
- グループ参加済み: 海外移住綜合 + 海外生活系3グループ
- Aboutページ設定済み
