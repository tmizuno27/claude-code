---
name: GitHub Pages無効化済み
description: claude-codeリポジトリのGitHub Pagesを2026-03-27に無効化。自動同期のたびにビルド失敗メールが大量発生していた
type: project
---

GitHub Pages（tmizuno27/claude-code）を2026-03-27に無効化した。

**Why:** 1分おきの自動git pushのたびにPagesビルドがトリガーされ、毎回失敗→GitHub通知メールが大量に届いていた。リポジトリはコード管理用でWebサイトホスティング不要。

**How to apply:** GitHub Pagesを再度有効化しないこと。静的サイトが必要な場合はVercel等を使う。
