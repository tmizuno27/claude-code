---
name: 自動タスクの稼働確認を毎回行う
description: ディレクトリ変更・スクリプト修正時は依存タスクの動作確認を必ず行い、会話の最初にタスク健全性を能動的にチェックする
type: feedback
---

自動タスクが正常に動いているか、ユーザーに指摘される前に自分から確認すること。

**Why:** 2026-03-14〜17にX自動投稿が3日間停止していたが、`blog/` → `nambei-oyaji.com/` リネーム時にPowerShellスクリプトのパス更新を漏らしたのが原因。ユーザーが自分で気づいて指摘するまで誰も検知できなかった。

**How to apply:**
1. **ディレクトリ名変更・リネーム時**: 必ず `C:\Users\tmizu\scripts\` 配下の全PS1/VBSファイルで旧パスを grep し、依存スクリプトを全て更新する
2. **会話の冒頭や作業の区切りで**: `logs/` 配下のログファイル（x-auto-post.log, auto-sync.log, dashboard-update.log等）の最終更新日時を確認し、停止しているタスクがないかチェックする
3. **スクリプト修正後**: 必ずdry-runまたはテスト実行で動作確認する
4. **確認すべきログ一覧**: x-auto-post.log, auto-sync.log, x-analytics-daily.log, dashboard-update.log, task-healthcheck.log
