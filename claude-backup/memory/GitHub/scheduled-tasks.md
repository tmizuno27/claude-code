---
name: 全自動定期タスク一覧
description: Task Schedulerで登録済みの全自動タスク（3サイト共通+インフラ+X+監視）
type: reference
---

# 全自動定期タスク一覧（Task Scheduler）

最終更新: 2026-03-15

## インフラ系（常時稼働）

| タスク名 | 頻度 | 時刻(PYT) | JST相当 | 内容 |
|---------|------|----------|---------|------|
| GitAutoSync-Data | 1分おき | 常時 | 常時 | git add→commit→push |
| GoogleSheetsSync | 5分おき | 常時 | 常時 | Sheets→CSV取得 |

## nambei-oyaji.com 分析系（日次）

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| BlogUpdatePV | 毎日 | 05:00 | GA4→記事別PV→CSV→Sheets |
| BlogDailyAnalytics | 毎日 | 07:00 | GA4+SC+WP日次レポート+Discord |
| BlogSheetSync | 毎日 | 19:00 | 記事管理スプレッドシート更新 |
| NotionSync | 毎日 | 18:30 | CSV→Notion DB+WPステータス同期 |

## nambei-oyaji.com コンテンツ系（週次）

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| BlogAutoPublish | 月木 | 18:00 | 記事自動生成→WP投稿 |
| BlogWeeklyReport | 日曜 | 19:00 | 週次Analyticsレポート |
| BlogKeywordResearch | 日曜 | 20:00 | KW調査→キューに追加 |
| BlogContentCalendar | 土曜 | 20:00 | コンテンツカレンダー更新 |
| BlogInternalLinker | 木曜 | 20:00 | 内部リンク最適化 |
| BlogFactCheck | 水曜 | 10:00 | ファクトチェック |

## nambei-oyaji.com メンテナンス系

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| BlogUptimeMonitor | 30分おき | 常時 | サイト死活監視→Discord通知 |
| BlogBrokenLinks | 日曜 | 21:00 | リンク切れチェック |
| BlogNewKeywords | 月曜 | 20:30 | GSC新規KW検出 |
| BlogRewriteDetector | 月曜 | 21:30 | リライト候補抽出 |
| BlogWpBackup | 土曜 | 22:00 | WP全記事HTML保存(4世代) |

## otona-match.com 記事生成

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| OtonaMatch_Article_Mon | 月曜 | 09:00 | キラー記事自動生成 |
| OtonaMatch_Article_Wed | 水曜 | 09:00 | 比較/収益記事自動生成 |
| OtonaMatch_Article_Fri | 金曜 | 09:00 | 集客記事自動生成 |

## otona-match.com 分析系（日次）— NEW

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| OtonaUpdatePV | 毎日 | 05:10 | GA4→記事別PV→CSV→Sheets |
| OtonaDailyAnalytics | 毎日 | 07:10 | GA4+SC+WP日次レポート+Discord |
| OtonaSheetSync | 毎日 | 19:10 | 記事管理スプレッドシート更新 |

## otona-match.com コンテンツ系（週次）— NEW

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| OtonaContentCalendar | 土曜 | 20:10 | コンテンツカレンダー更新 |
| OtonaKeywordResearch | 日曜 | 20:10 | KW調査→キューに追加 |
| OtonaInternalLinker | 木曜 | 20:10 | 内部リンク最適化 |
| OtonaFactCheck | 水曜 | 10:10 | ファクトチェック |

## otona-match.com メンテナンス系 — NEW

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| OtonaUptimeMonitor | 30分おき | 常時 | サイト死活監視→Discord通知 |
| OtonaBrokenLinks | 日曜 | 21:10 | リンク切れチェック |
| OtonaNewKeywords | 月曜 | 20:40 | GSC新規KW検出 |
| OtonaRewriteDetector | 月曜 | 21:40 | リライト候補抽出 |
| OtonaWpBackup | 土曜 | 22:10 | WP全記事HTML保存(4世代) |

## sim-hikaku.online 予約投稿

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| SimHikakuPublisher | 毎日 | 18:00 | pending記事のWP予約投稿 |

## sim-hikaku.online 分析系（日次）— NEW

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| SimUpdatePV | 毎日 | 05:20 | GA4→記事別PV→CSV→Sheets |
| SimDailyAnalytics | 毎日 | 07:20 | GA4+SC+WP日次レポート+Discord |
| SimSheetSync | 毎日 | 19:20 | 記事管理スプレッドシート更新 |

## sim-hikaku.online コンテンツ系（週次）— NEW

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| SimContentCalendar | 土曜 | 20:20 | コンテンツカレンダー更新 |
| SimKeywordResearch | 日曜 | 20:20 | KW調査→キューに追加 |
| SimInternalLinker | 木曜 | 20:20 | 内部リンク最適化 |
| SimFactCheck | 水曜 | 10:20 | ファクトチェック |

## sim-hikaku.online メンテナンス系 — NEW

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| SimUptimeMonitor | 30分おき | 常時(15分オフセット) | サイト死活監視→Discord通知 |
| SimBrokenLinks | 日曜 | 21:20 | リンク切れチェック |
| SimNewKeywords | 月曜 | 20:50 | GSC新規KW検出 |
| SimRewriteDetector | 月曜 | 21:50 | リライト候補抽出 |
| SimWpBackup | 土曜 | 22:20 | WP全記事HTML保存(4世代) |

## はてなブログ（nambei-oyaji.hatenablog.com）

| タスク名 | 頻度 | 時刻(PYT) | JST相当 | 内容 |
|---------|------|----------|---------|------|
| HatenaPipeline | 月水金 | 07:00 | 19:00 | WP記事→ダイジェスト変換→はてな投稿(2記事) |

## X (Twitter) 系

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| XAutoPost-Morning | 毎日 | 18:30 | X朝投稿（JST 07:00） |
| XAutoPost-Noon | 毎日 | 23:30 | X昼投稿（JST 12:00） |
| XAutoPost-Evening | 毎日 | 08:00 | X夜投稿（JST 20:30） |
| XAnalyticsDaily | 毎日 | 10:00 | Xアカウント指標レポート |

## 監視系

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| TaskHealthCheck | 毎日 | 09:00 | 全タスク稼働状況チェック→Discord |
| TaskDashboardReport | 毎日 | 05:00 | ダッシュボードHTML生成→Discord |
| ApiHealthCheck | 毎日 | 06:00 | 全10 API死活監視→エラー時Discord |

## 統合レポート系

| タスク名 | 頻度 | 時刻(PYT) | 内容 |
|---------|------|----------|------|
| AllBusinessWeeklyKPI | 日曜 | 19:30 | 全事業統合KPIレポート→Discord |

## ファイル配置

全ランチャー: `C:\Users\tmizu\scripts\`
- PS1（ロジック）+ VBS（非表示起動ラッパー）のペア構成
- 登録スクリプト: `register-all-tasks.ps1`, `register-x-tasks.ps1`, `register-otona-tasks.ps1`, `register-multisite-tasks.ps1`
- 3サイト共通タスクは時刻を10分ずつオフセット（nambei=:00, otona=:10, sim=:20）

## 合計タスク数: 52タスク
- nambei-oyaji.com: 17タスク（既存）
- otona-match.com: 15タスク（記事生成3+分析3+コンテンツ4+メンテナンス5）
- sim-hikaku.online: 13タスク（予約投稿1+分析3+コンテンツ4+メンテナンス5）
- X: 4タスク
- インフラ: 2タスク
- 監視: 3タスク
- 統合: 1タスク
