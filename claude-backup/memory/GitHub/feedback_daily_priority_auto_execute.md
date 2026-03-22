---
name: 日次優先タスク自動実行ルール
description: 毎日の優先アクションのうちClaude自動実行可能なものは許可不要で即実行する
type: feedback
---

日次レポート生成後、優先アクションのうちClaude側で自動実行できるものは**毎日自動で実行する**。

**Why:** ユーザーは「毎日のルーティンとして自動化」を明確に指示。手動確認は不要。

**How to apply:**
- 毎朝のレポート生成（daily_business_report.py）後に自動実行スクリプトを連鎖実行
- 自動実行対象:
  1. SIMサイト/otona-match/nambei CTR改善（タイトル・メタディスクリプション最適化）
  2. 上位記事強化（リライト・内部リンク挿入）
  3. RapidAPI流入経路分析
  4. X集客投稿
- 手動が必要なもの（外部サイト操作、KYC、アカウント設定等）はスキップしてログに記録
- 実行結果は `logs/daily-auto-actions.log` に記録
- ダッシュボードのaction-status.jsonを完了マークで更新
