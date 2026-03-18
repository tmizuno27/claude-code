---
name: X @prodhq27 マーケティングアカウント
description: Gumroad商品宣伝用の英語Xアカウント。API自動投稿設定済み、Task Scheduler 1日3回（10:00/14:00/19:00 PYT）
type: project
---

Gumroadデジタル商品（Notion + n8n）のマーケティング用Xアカウント（2026-03-17作成）

**Why:** @nambei_oyaji は日本語ブログ用で英語商品の宣伝にミスマッチ。専用英語アカウントで収益最大化。

**How to apply:** 全商品宣伝はこのアカウントから。価値ツイート8割:宣伝2割ルール。

## アカウント情報
- **表示名**: Productivity HQ
- **ユーザー名**: @prodhq27
- **プロフィール画像**: `gumroad-notion/images/x-profile-icon-v2.png`
- **バナー画像**: `gumroad-notion/images/x-banner.png`
- **リンク**: https://tatsuya27.gumroad.com

## API認証
- **認証ファイル**: `gumroad-notion/config/x-credentials.json`（.gitignore対象）
- **プラン**: Pay-Per-Use（$5クレジット購入済み）
- **Developer App**: 2034078280697958400prodhq27
- **権限**: 読み取りと書き込み

## 自動投稿
- **スケジュール**: `gumroad-notion/config/x-schedule.json`
- **スクリプト**: `gumroad-notion/scripts/x_auto_post.py`
- **Task Scheduler**: `XAutoPost-ProdHQ`（毎日10:00, 14:00, 19:00 PYT）
- **ログ**: `logs/x-prodhq27-posts.log`
- **コンテンツ**: 価値ツイート15本 + 商品ツイート10本 = 25本

## 投稿済み（2026-03-17）
- 商品ツイート 1本（Freelance Business OS）
- 価値ツイート 6本（手動5本 + 自動1本）
