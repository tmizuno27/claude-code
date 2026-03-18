---
name: ダッシュボード優先アクション＋自動同期体制
description: ビジネスダッシュボード（Gist）の優先アクション機能と自動ステータス同期体制
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

## ダッシュボードGist URL（固定・ブックマーク用）
- `https://gist.github.com/tmizuno27/16a8680cadf8aed0c207777f7468963b`
- Gist ID: `16a8680cadf8aed0c207777f7468963b`

## 自動ステータス同期体制（2026-03-17構築）

### スクリプト
- `dashboard_status_sync.py` — 実データからステータス・スコアを自動計算してHTML更新+Gistアップロード
- `dashboard_updater.py` — アクション完了状態反映+ステータス同期呼び出し（毎時実行）
- `daily_business_report.py` — レポート生成時にステータス同期を実行してからGist更新

### 自動更新される項目
- ブログ記事数（3サイト、CSV読み取り）
- GA4接続ステータス（API実アクセスで判定）
- Chrome拡張数、VS Code拡張数
- AccessTrade承認状況
- 定期タスク数
- ビジネス健全性スコア（5カテゴリ×20点、忖度禁止の厳格評価）
- 日付・タイムスタンプ

### トリガー
- 毎時: DashboardUpdate（Task Scheduler）→ dashboard_updater.py
- 毎日: daily_business_report.py 実行時
- 即時: wp_publisher.py 記事投稿後にバックグラウンド同期

### 削除済みセクション（2026-03-17）
- 今週のスケジュール（Weekly Schedule）
- Notion連携
- ドメイン・サーバー管理
- コンテンツパイプライン

### ナビゲーション修正（2026-03-17）
- サイドバーの`scrollTo`→`navScrollTo`にリネーム（window.scrollToとの名前衝突修正）

**Why:** 月間売上$0→Phase1 ¥50,000/月を目指すため、毎日データドリブンで最も収益効率の高いアクションに集中する
**How to apply:** ユーザーが「優先アクション」「優先タスク」と言ったら、action-status.jsonの確認・完了操作・新規生成のいずれかを行う
