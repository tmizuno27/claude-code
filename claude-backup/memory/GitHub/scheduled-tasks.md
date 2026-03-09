# 全自動定期タスク一覧（Task Scheduler）

最終更新: 2026-03-09

## インフラ系（常時稼働）

| タスク名 | 頻度 | 時刻(PYT) | JST相当 | 内容 |
|---------|------|----------|---------|------|
| GitAutoSync-Data | 1分おき | 常時 | 常時 | git add→commit→push |
| GoogleSheetsSync | 5分おき | 常時 | 常時 | Sheets→CSV取得 |

## ブログ・分析系（日次）

| タスク名 | 頻度 | 時刻(PYT) | JST相当 | 内容 |
|---------|------|----------|---------|------|
| BlogUpdatePV | 毎日 | 05:00 | 18:00 | GA4→記事別PV→CSV→Sheets |
| BlogDailyAnalytics | 毎日 | 07:00 | 20:00 | GA4+SC+WP日次レポート+Discord |
| BlogSheetSync | 毎日 | 19:00 | 08:00翌日 | 記事管理スプレッドシート更新 |
| NotionSync | 毎日 | 18:30 | 07:30翌日 | CSV→Notion DB+WPステータス同期 |

## ブログ・コンテンツ系（週次）

| タスク名 | 頻度 | 時刻(PYT) | JST相当 | 内容 |
|---------|------|----------|---------|------|
| BlogAutoPublish | 月木 | 18:00 | 06:00翌日 | 記事自動生成→WP投稿 |
| BlogWeeklyReport | 日曜 | 19:00 | 08:00月曜 | 週次Analyticsレポート |
| BlogKeywordResearch | 日曜 | 20:00 | 09:00月曜 | KW調査→キューに追加 |
| BlogContentCalendar | 土曜 | 20:00 | 09:00日曜 | コンテンツカレンダー更新 |
| BlogInternalLinker | 木曜 | 20:00 | 09:00金曜 | 内部リンク最適化 |
| BlogFactCheck | 水曜 | 10:00 | 23:00水曜 | ファクトチェック(fix+check) |

## X (Twitter) 系

| タスク名 | 頻度 | 時刻(PYT) | JST相当 | 内容 |
|---------|------|----------|---------|------|
| XAutoPost-Morning | 毎日 | 18:30 | 07:00翌日 | X朝投稿（Claude API生成） |
| XAutoPost-Noon | 毎日 | 23:30 | 12:00翌日 | X昼投稿 |
| XAutoPost-Evening | 毎日 | 08:00 | 20:30 | X夜投稿 |
| XAnalyticsDaily | 毎日 | 10:00 | 23:00 | Xアカウント指標レポート |

## ファイル配置

全ランチャー: `C:\Users\tmizu\scripts\`
- PS1（ロジック）+ VBS（非表示起動ラッパー）のペア構成
- 登録スクリプト: `register-all-tasks.ps1`, `register-x-tasks.ps1`
