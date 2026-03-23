---
name: infrastructure-team
description: 52タスク・ログ監視・バックアップ・API健全性を一括チェックするインフラ監視チーム
team:
  - agent: task-monitor
    description: Task Schedulerの52タスクのログを確認し、失敗・遅延・未実行を検知する
  - agent: api-health-checker
    description: RapidAPI 21本・Apify 5 Actor・WordPress 3サイト・外部APIの稼働状況を確認する
  - agent: backup-verifier
    description: Git自動同期・WPバックアップ・メモリバックアップ・Google Sheets同期の健全性を検証する
---

# インフラ監視チーム

## 概要
52個の自動化タスク、API群、バックアップシステムの健全性を一括監視するチーム。サイレント障害の早期発見が目的。

## 起動トリガー
「インフラチェック」「タスク確認」「ログチェック」「システム健全性」「バックアップ確認」「API稼働確認」「何か壊れてない？」など

## 実行フロー

### Phase 1: タスク稼働確認（task-monitor）
1. `logs/` 配下の全ログファイルを確認:
   - `auto-sync.log` — Git自動同期（1分おき）
   - `sheets-sync.log` — Google Sheets同期（5分おき）
   - `x-auto-post*.log` — X自動投稿（3アカウント）
   - `*-analytics.log` — GA4/SC分析（3サイト）
   - `*-article-gen.log` — 記事生成（3サイト）
   - `healthcheck*.log` — Healthchecks.io監視
2. 各ログの最終実行時刻を確認し、スケジュール通りかチェック
3. エラー・警告メッセージを抽出
4. 未実行・遅延タスクを一覧化

### Phase 2: API健全性確認（api-health-checker）
1. WordPress REST API（3サイト）の疎通確認
2. RapidAPI 21本のエンドポイント稼働確認（`products/api-services/` 参照）
3. Apify 5 Actorのステータス確認
4. 外部API（Claude API, Google APIs, Notion API）の残クォータ確認
5. 障害・レート制限検知時はアラート

### Phase 3: バックアップ検証（backup-verifier）
1. Git自動同期の最終push時刻確認（`git log --oneline -1`）
2. `claude-backup/` のジャンクション健全性確認
3. WordPress HTMLバックアップの4世代ローテーション確認
4. Google SheetsとローカルCSVの同期整合性チェック
5. 問題発見時は修復手順を提示

## 出力フォーマット
```
## インフラ健全性レポート（YYYY-MM-DD HH:MM PYT）

### タスク稼働状況
| カテゴリ | 正常 | 警告 | 障害 |
|----------|------|------|------|
| インフラ | X/2 | X | X |
| ブログ分析 | X/15 | X | X |
| コンテンツ | X/12 | X | X |
| メンテナンス | X/15 | X | X |
| X投稿 | X/4 | X | X |
| 監視 | X/3 | X | X |

### API稼働状況
（詳細）

### バックアップ状況
（詳細）

### 要対応アクション
1. ...
```

## 参照ファイル
- `logs/` — 全ログファイル
- `memory/scheduled-tasks.md` — 52タスク一覧
- `products/api-services/` — RapidAPI Worker群
- `products/api-services/apify-actors/` — Apify Actor群
- `claude-backup/` — バックアップディレクトリ
- `infrastructure/tools/healthchecks/` — Healthchecks.io設定
