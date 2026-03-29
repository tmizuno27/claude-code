# Memory - GitHub ワークスペース

## 【最重要・絶対厳守】ブログ記事の禁止事項
- **本名（水野達也）は絶対にブログ記事・SNS投稿に掲載禁止**。ペンネーム「南米おやじ」のみ使用すること
- **居住地はブログ上では「アスンシオン」と表記する**。ランバレとは絶対に書かない
- 全記事・全コンテンツ・全プラットフォームに適用される永続ルール

## ユーザー情報
- **職務経歴**: [resume.md](resume.md) — 35歳、パラグアイ在住
- 居住地: パラグアイ（PYT, UTC-3通年）、Googleカレンダー: JST設定
- X API: [x-api-credentials.md](x-api-credentials.md)

## ユーザーとの関係性
- **詳細**: [user_role_partner.md](user_role_partner.md) — 「世界最強の専属右腕・秘書」として自律的に最大効率で動くこと
- **最上位目標**: [feedback_fully_autonomous_revenue.md](feedback_fully_autonomous_revenue.md) — 完全自動収益の最大化
- **全事業自律PDCA**: [feedback_full_autonomous_pdca.md](feedback_full_autonomous_pdca.md) — 許可不要で試行錯誤→収益最大化
- **聞かずに即実行**: [feedback_execute_dont_ask.md](feedback_execute_dont_ask.md) — 自動実行可能なタスクは確認せず即実行。「やりますか？」禁止

## ユーザー設定・好み（feedback）
- **忖度禁止**: [feedback_no_sontaku.md](feedback_no_sontaku.md)
- **日本語で回答**: [feedback_respond_in_japanese.md](feedback_respond_in_japanese.md)
- **先送り禁止**: [feedback_no_postpone.md](feedback_no_postpone.md)
- **自動化ファースト**: [feedback_automate_first_always.md](feedback_automate_first_always.md) — 手動より自動化を常に優先
- **自動作業は徹底的に**: [feedback_auto_work_exhaustive.md](feedback_auto_work_exhaustive.md)
- **収益最大化は自主実行**: [feedback_revenue_proactive.md](feedback_revenue_proactive.md)
- **コピペ形式**: [feedback_copypaste_format.md](feedback_copypaste_format.md) / [feedback_copypaste_detailed.md](feedback_copypaste_detailed.md)
- **初心者向け手順**: [feedback_beginner_instructions.md](feedback_beginner_instructions.md) — 常に初心者前提で丁寧に説明
- **ダッシュボード自動更新**: [feedback_dashboard_realtime.md](feedback_dashboard_realtime.md)
- **エージェント一覧**: [feedback_agent_list_table.md](feedback_agent_list_table.md)
- **出品前に既存確認**: [feedback_check_existing_before_listing.md](feedback_check_existing_before_listing.md)
- **出品手順は全項目漏れなく**: [feedback_gumroad_listing_complete.md](feedback_gumroad_listing_complete.md) — コンテンツ先に完成→全入力欄を一括提示
- **素材の後回し禁止**: [feedback_never_postpone_assets.md](feedback_never_postpone_assets.md) — 画像・PDF等は手順提示前に全て用意
- **Gumroadサムネ必須**: [feedback_gumroad_thumbnails.md](feedback_gumroad_thumbnails.md) — Python/Pillowで自動生成
- **Reddit投稿は無効**: [feedback_reddit_posting.md](feedback_reddit_posting.md) — モデレーターに削除されるため提案禁止
- **日次レポート鮮度チェック**: [feedback_daily_report_verify.md](feedback_daily_report_verify.md)
- **Vercelデプロイ確認**: [feedback_vercel_deploy_check.md](feedback_vercel_deploy_check.md)
- **タスク稼働確認**: [feedback_proactive_task_check.md](feedback_proactive_task_check.md)

## オンラインセールス（現金収入の柱）
- **詳細**: [online-sales.md](online-sales.md) — フリーランスのオンラインセールスマンとして稼働中（2025年〜）
- **Fiverr案件**: [fiverr-dennis-ssw-research.md](fiverr-dennis-ssw-research.md) — Dennis C SSW市場リサーチ、質問リスト待ち

## 運営サイト一覧（3サイト + はてなブログ）
- **nambei-oyaji.com**: 南米おやじの海外生活ラボ（主力、116記事）→ [blog-seo-rules.md](blog-seo-rules.md)
- **otona-match.com**: 大人のマッチングナビ（132記事）→ [otona-match-site.md](otona-match-site.md)
- **sim-hikaku.online**: SIM比較オンライン（107記事）→ [sim-hikaku-site.md](sim-hikaku-site.md)
- **nambei-oyaji.hatenablog.com**: 南米おやじの海外生活メモ（本家送客用）→ [hatena-blog-business.md](hatena-blog-business.md)
- **3サイト合計: 400記事**（2026-03-28 CSV同期確認: nambei136+otona161+sim113）

## ブログデザイン・フォーマット
- **デザイン確定版**: [blog-design-golden-state.md](blog-design-golden-state.md) — Apple風カラー・frosted glass
- **記事フォーマット**: [blog-article-format.md](blog-article-format.md)
- **視覚的強調**: [blog-visual-emphasis.md](blog-visual-emphasis.md)
- **トップページ**: [blog-frontpage-design.md](blog-frontpage-design.md) — PC版完成、モバイル未完
- **トップページ復元点**: [front-page-savepoint.md](front-page-savepoint.md) — コミットa90ce7f8で復元可能

## WordPress REST API（nambei-oyaji.com）
- 認証: `nambei-oyaji.com/config/secrets.json` + `wp-credentials.json`
- トップページID: 47、カテゴリ: paraguay, side-business, ijuu-junbi
- Rank MathのSEOタイトル/メタはREST APIから直接更新不可（管理画面で手動合わせ必要）

## 記事管理運用ルール
- 変更時は必ず `outputs/article-management.csv` を同時更新 → `create_article_sheet.py` でスプレッドシート同期

## アフィリエイト（4 ASP × 3サイト）
- **全体概要**: [affiliate-asp-overview.md](affiliate-asp-overview.md)
- **アクセストレード**: [accesstrade-affiliate-pending.md](accesstrade-affiliate-pending.md) — 3サイト承認済、提携詳細あり
- **もしも**: [moshimo-affiliate-progress.md](moshimo-affiliate-progress.md) — 3サイト登録済、一括挿入完了
- A8.net: 3サイト提携・一括挿入完了
- Value Commerce: 3サイト登録済、プログラム提携未着手

## フォルダ構成ルール
- **整理規約**: [folder-structure-rules.md](folder-structure-rules.md) — ログ一元管理、ファイル配置ルール（2026-03-28整理済み）

## インフラ・自動化
- **GitHub自動同期**: [auto-sync-setup.md](auto-sync-setup.md) — 1分おき
- **GitHub Pages無効化**: [github-pages-disabled.md](github-pages-disabled.md) — 2026-03-27無効化（ビルド失敗メール対策）
- **定期タスク（52個）**: [scheduled-tasks.md](scheduled-tasks.md) — Healthchecks.io監視+Discord通知
- **優先アクション**: [dashboard-priority-actions.md](dashboard-priority-actions.md) — 毎朝Claude API自動生成
- **日次PDCAルーティン**: [feedback_daily_pdca_routine.md](feedback_daily_pdca_routine.md)
- **SEO PDCA自動実行**: [feedback_seo_pdca_autonomous.md](feedback_seo_pdca_autonomous.md)
- **タスク共通ルール**: [feedback_blog_tasks_shared.md](feedback_blog_tasks_shared.md)

## デジタルプロダクト事業
- **RapidAPI（24本・収益$0）**: [rapidapi-business.md](rapidapi-business.md) — 上位5本クロスセル実装済、Dev.to記事3本準備済
- **Apify（9 Actor全デプロイ完了）**: [apify-business.md](apify-business.md) — バグ修正・構造修正済
- **Apify公開作業中断**: [apify-actor-pending.md](apify-actor-pending.md) — Actor jmtLVhG6qPqjc0b34
- **Chrome拡張（2/11本公開、PP公開済）**: [chrome-extensions-business.md](chrome-extensions-business.md)
- **VS Code拡張（10本SEO改善版パブリッシュ済）**: [vscode-extensions-business.md](vscode-extensions-business.md)
- **Gumroad（35商品・トークン保存済）**: [gumroad-listing-progress.md](gumroad-listing-progress.md) / [gumroad-notion-business.md](gumroad-notion-business.md)
- **Xマーケティング**: [x-prodhq27-account.md](x-prodhq27-account.md) — @prodhq27、1日3回自動投稿

## SaaS・Webサービス
- **WP Linker**: [wp-linker-project.md](wp-linker-project.md) — Free$0プラン新設、大幅改善デプロイ済み。Stripe KYCブロック中
- **keisan-tools**: [keisan-tools-business.md](keisan-tools-business.md) — 463ツール（+15追加）、SEO大幅改善+PP公開デプロイ済み
- **pSEO**: [pseo-site.md](pseo-site.md) — 5,056ページ、GSCサイトマップ送信完了

## その他事業
- **Product Factory**: [product-factory-business.md](product-factory-business.md) — Phase 1完了
- **POD Etsy**: [pod-etsy-business.md](pod-etsy-business.md) — アカウント開設待ち
- **Stock Assets**: [stock-assets-business.md](stock-assets-business.md) — 出品準備中
- **n8nテンプレート**: [n8n-template-business.md](n8n-template-business.md) — Stripe KYC停止中
- **仮想通貨自動売買**: [trading-bot.md](trading-bot.md) — Bybit口座開設待ち

## 外部アカウント
- **Dev.to**: [devto-account.md](devto-account.md) — miccho27、効果測定: [devto-followup-todo.md](devto-followup-todo.md)
- **GitHubリポジトリ**: PUBLIC — https://github.com/tmizuno27/claude-code

## 自動化スクリプト（Playwright）
- **RapidAPI自動更新**: `products/api-services/marketing/rapidapi_auto_update.py` — サイト復旧後に `--dry-run` → 本番実行
- **Fiverr自動出品**: `research/freelance/fiverr_auto_publish.py` — Gig作成制限解除後に実行（セッション保存済み）

## 待機中タスク
- **Stripe連携待ち**: [stripe-pending-tasks.md](stripe-pending-tasks.md) — 「Stripe連携できました」で即実行
- **Fiverr Gig 3-5**: 作成制限解除待ち→自動スクリプトで出品
- **RapidAPI更新**: provider.rapidapi.comダウン復旧待ち→自動スクリプトで更新
- **Hash & Encode Tool PP**: Chrome Web Store審査完了待ち→URL: `https://homepage-three-ochre.vercel.app/privacy-policy-hash-encode-tool.html`

## PDCA実行記録
- **2026-03-28 午後**: [pdca-2026-03-28-session2.md](pdca-2026-03-28-session2.md) — 22タスク自動+手動対応。全10 VS Code拡張パブリッシュ、Apify 9本デプロイ、city-cost-pseoデプロイ、Gumroad 2商品出品、Fiverr Gig2出品、Playwright自動化スクリプト2本作成
- **2026-03-28 午前**: [pdca-2026-03-28.md](pdca-2026-03-28.md) — 22チーム並列+朝4タスク。Sheets Sync復旧、X投稿v2移行、CTR改善、内部リンク強化
- **2026-03-27**: [pdca-2026-03-27.md](pdca-2026-03-27.md) — GA4修正、pSEO GSC送信、ダッシュボードバグ修正3件、GitHub Pages無効化
