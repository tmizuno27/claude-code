---
name: ダッシュボード優先アクション機能
description: 「優先アクション」「優先タスク」と言えば、ダッシュボードの収益最大化アクション管理を指す
type: project
---

「優先アクション」「優先タスク」= ダッシュボードの「今日の優先アクション」セクションのこと。

## 仕組み
- 毎朝5時のレポート生成時（`daily_business_report.py`）にClaude APIが全事業データを分析
- 「収益インパクト÷労力」が高い順に優先アクションを自動生成（件数制限なし、重要なもののみ厳選）
- P1=今日必ず / P2=今日できれば / P3=今週中
- 各アクションに「理由」「労力」「収益ポテンシャル」を表示

## アクション完了の操作
- ユーザーが「○○やったよ」と言えば、Claudeが `dashboard_updater.py done <id>` で完了マーク
- ダッシュボードHTML上で✅+打ち消し線+完了時刻表示
- Gistにも自動反映

## 関連ファイル
- `nambei-oyaji.com/outputs/reports/action-status.json` — 完了状態管理
- `nambei-oyaji.com/scripts/analytics/dashboard_updater.py` — HTML更新+Gistアップロード（1時間ごと自動実行）
- `nambei-oyaji.com/scripts/analytics/daily_business_report.py` — `generate_priority_actions()` で毎朝自動生成
- `nambei-oyaji.com/outputs/reports/daily-business-dashboard.html` — ダッシュボード本体

## ダッシュボード自動更新
- Task Scheduler `DashboardUpdate` — 毎時実行（タイムスタンプ更新+アクション状態反映+Gistアップ）
- Task Scheduler `DailyBusinessReport` — 毎朝5時（全データ収集+優先アクション再生成+Discord通知）
- Gist ID: `16a8680cadf8aed0c207777f7468963b`
- 閲覧URL: htmlpreview.github.io 経由

**Why:** 月間売上$0→Phase1 ¥50,000/月を目指すため、毎日データドリブンで最も収益効率の高いアクションに集中する
**How to apply:** ユーザーが「優先アクション」「優先タスク」と言ったら、action-status.jsonの確認・完了操作・新規生成のいずれかを行う
