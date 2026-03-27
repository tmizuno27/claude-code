# Memory - GitHub ワークスペース

## 【最重要・絶対厳守】ブログ記事の禁止事項
- **本名（水野達也）は絶対にブログ記事・SNS投稿に掲載禁止**。ペンネーム「南米おやじ」のみ使用すること
- **居住地はブログ上では「アスンシオン」と表記する**。ランバレとは絶対に書かない
- 全記事・全コンテンツ・全プラットフォームに適用される永続ルール

## ユーザーとの関係性
- **詳細**: [user_role_partner.md](user_role_partner.md) — 「世界最強の専属右腕・秘書」として自律的に最大効率で動くこと
- **最上位目標**: [feedback_fully_autonomous_revenue.md](feedback_fully_autonomous_revenue.md) — 完全自動収益の最大化
- **全事業自律PDCA**: [feedback_full_autonomous_pdca.md](feedback_full_autonomous_pdca.md) — 許可不要で試行錯誤→収益最大化
- **聞かずに即実行**: [feedback_execute_dont_ask.md](feedback_execute_dont_ask.md) — 自動実行可能なタスクは確認せず即実行。「やりますか？」禁止

## オンラインセールス（現金収入の柱）
- **詳細**: [online-sales.md](online-sales.md) — フリーランスのオンラインセールスマンとして稼働中（2025年〜）

## 運営サイト一覧（3サイト + はてなブログ）
- **nambei-oyaji.com**: 南米おやじの海外生活ラボ（主力、116記事）→ [blog-seo-rules.md](blog-seo-rules.md)
- **otona-match.com**: 大人のマッチングナビ（132記事）→ [otona-match-site.md](otona-match-site.md)
- **sim-hikaku.online**: SIM比較オンライン（107記事）→ [sim-hikaku-site.md](sim-hikaku-site.md)
- **nambei-oyaji.hatenablog.com**: 南米おやじの海外生活メモ（本家送客用）→ [hatena-blog-business.md](hatena-blog-business.md)
- **3サイト合計: 355記事**（2026-03-27確認、全サイト目標100記事超過達成）

## ブログデザイン・フォーマット
- **デザイン確定版**: [blog-design-golden-state.md](blog-design-golden-state.md) — Apple風カラー・frosted glass
- **記事フォーマット**: [blog-article-format.md](blog-article-format.md)
- **視覚的強調**: [blog-visual-emphasis.md](blog-visual-emphasis.md)
- **トップページ**: [blog-frontpage-design.md](blog-frontpage-design.md) — PC版完成、モバイル未完

## インフラ・自動化
- **GitHub自動同期**: [auto-sync-setup.md](auto-sync-setup.md) — 1分おき
- **定期タスク（52個）**: [scheduled-tasks.md](scheduled-tasks.md) — Healthchecks.io監視+Discord通知
- **優先アクション**: [dashboard-priority-actions.md](dashboard-priority-actions.md) — 毎朝Claude API自動生成、完了状態保持バグ修正済み(2026-03-27)
- **日次PDCAルーティン**: [feedback_daily_pdca_routine.md](feedback_daily_pdca_routine.md)
- **SEO PDCA自動実行**: [feedback_seo_pdca_autonomous.md](feedback_seo_pdca_autonomous.md)
- **タスク共通ルール**: [feedback_blog_tasks_shared.md](feedback_blog_tasks_shared.md)
- **タスク稼働確認**: [feedback_proactive_task_check.md](feedback_proactive_task_check.md)
- **Vercelデプロイ確認**: [feedback_vercel_deploy_check.md](feedback_vercel_deploy_check.md)

## WordPress REST API（nambei-oyaji.com）
- 認証: `nambei-oyaji.com/config/secrets.json` + `wp-credentials.json`
- トップページID: 47、カテゴリ: paraguay, side-business, ijuu-junbi
- Rank MathのSEOタイトル/メタはREST APIから直接更新不可（管理画面で手動合わせ必要）

## 記事管理運用ルール
- 変更時は必ず `outputs/article-management.csv` を同時更新 → `create_article_sheet.py` でスプレッドシート同期

## アフィリエイト（4 ASP × 3サイト）
- **全体概要**: [affiliate-asp-overview.md](affiliate-asp-overview.md)
- A8.net/アクセストレード/もしも: 3サイト提携・一括挿入完了
- Value Commerce: 3サイト登録済、プログラム提携未着手

## RapidAPI API販売事業（24本全出品・収益$0）
- **詳細**: [rapidapi-business.md](rapidapi-business.md)
- 24 API全Active、20本Public（上限20）、4本Private。Cloudflare Workers、運用コスト$0
- **課題**: サブスクライバー0、呼び出し0、収益$0（2026-03-27確認）。マーケティング強化が急務
- rapidapi-stats.logにexit code 2エラーが3/24以降継続中
- **プロジェクトパス**: `claude-code/products/api-services/`

## Apify DaaS事業（稼働中）
- **詳細**: [apify-business.md](apify-business.md) — 5 Actor公開済み、PayPal出金設定済み

## Chrome拡張ポートフォリオ事業（4/10本公開済み）
- **詳細**: [chrome-extensions-business.md](chrome-extensions-business.md)

## WP Linker Micro SaaS / keisan-tools / pSEO
- **WP Linker**: [wp-linker-project.md](wp-linker-project.md) — Stripe KYCブロック中
- **keisan-tools**: [keisan-tools-business.md](keisan-tools-business.md) — 441ツール、AdSense申請済み
- **pSEO**: [pseo-site.md](pseo-site.md) — 5,056ページ、GSCサイトマップ送信完了(2026-03-27)、AdSense未申請

## Gumroad（12商品 + X自動投稿稼働中）
- **進捗**: [gumroad-listing-progress.md](gumroad-listing-progress.md)
- **Xマーケティング**: [x-prodhq27-account.md](x-prodhq27-account.md) — @prodhq27、1日3回自動投稿

## その他事業
- **VS Code拡張**: [vscode-extensions-business.md](vscode-extensions-business.md) — 10本公開完了
- **Product Factory**: [product-factory-business.md](product-factory-business.md) — Phase 1完了
- **POD Etsy**: [pod-etsy-business.md](pod-etsy-business.md) — アカウント開設待ち
- **Stock Assets**: [stock-assets-business.md](stock-assets-business.md) — 出品準備中
- **n8nテンプレート**: [n8n-template-business.md](n8n-template-business.md) — Stripe KYC停止中
- **仮想通貨自動売買**: [trading-bot.md](trading-bot.md) — Bybit口座開設待ち

## ユーザー情報
- **職務経歴**: [resume.md](resume.md) — 35歳、パラグアイ在住
- 居住地: パラグアイ（PYT, UTC-3通年）、Googleカレンダー: JST設定
- X API: [x-api-credentials.md](x-api-credentials.md)

## ユーザー設定・好み
- **忖度禁止**: [feedback_no_sontaku.md](feedback_no_sontaku.md)
- **日本語で回答**: [feedback_respond_in_japanese.md](feedback_respond_in_japanese.md)
- **先送り禁止**: [feedback_no_postpone.md](feedback_no_postpone.md)
- **自動化ファースト**: [feedback_automate_first_always.md](feedback_automate_first_always.md)
- **自動作業は徹底的に**: [feedback_auto_work_exhaustive.md](feedback_auto_work_exhaustive.md)
- **収益最大化は自主実行**: [feedback_revenue_proactive.md](feedback_revenue_proactive.md)
- **コピペ形式**: [feedback_copypaste_format.md](feedback_copypaste_format.md) / [feedback_copypaste_detailed.md](feedback_copypaste_detailed.md)
- **ダッシュボード自動更新**: [feedback_dashboard_realtime.md](feedback_dashboard_realtime.md)
- **エージェント一覧**: [feedback_agent_list_table.md](feedback_agent_list_table.md)

## Stripe連携待ち
- **詳細**: [stripe-pending-tasks.md](stripe-pending-tasks.md) — 「Stripe連携できました」で即実行

## GitHubリポジトリ
- PUBLIC（2026-03-27変更）: https://github.com/tmizuno27/claude-code

## Dev.toアカウント
- **詳細**: [devto-account.md](devto-account.md) — miccho27、効果測定: [devto-followup-todo.md](devto-followup-todo.md)

## PDCA実行記録
- **2026-03-27**: [pdca-2026-03-27.md](pdca-2026-03-27.md) — GA4修正、pSEO GSC送信、ダッシュボードバグ修正3件
