# Memory - GitHub ワークスペース

## 【最重要・絶対厳守】ブログ記事の禁止事項
- **本名（水野達也）は絶対にブログ記事・SNS投稿に掲載禁止**。ペンネーム「南米おやじ」のみ使用すること
- **居住地はブログ上では「アスンシオン」と表記する**。ランバレとは絶対に書かない
- 全記事・全コンテンツ・全プラットフォームに適用される永続ルール

## オンラインセールス（現金収入の柱）
- **詳細**: [online-sales.md](online-sales.md)
- フリーランスのオンラインセールスマンとして稼働中（2025年〜）
- Webメディア事業が育つまでの生活費を支える主力収入源

## 運営サイト一覧（3サイト）
- **nambei-oyaji.com**: 南米おやじの海外生活ラボ（主力、51記事）→ [blog-seo-rules.md](blog-seo-rules.md)
- **otona-match.com**: 大人のマッチングナビ（61記事全公開）→ [otona-match-site.md](otona-match-site.md)
- **sim-hikaku.online**: SIM比較オンライン（25記事、成長中）→ [sim-hikaku-site.md](sim-hikaku-site.md)

## ブログデザイン・フォーマット
- **デザイン確定版**: [blog-design-golden-state.md](blog-design-golden-state.md) — Apple風カラー・frosted glass
- **記事フォーマット**: [blog-article-format.md](blog-article-format.md) — ヘッダー/サイドバー/禁止事項
- **視覚的強調**: [blog-visual-emphasis.md](blog-visual-emphasis.md) — 太字+カラーマーカー（黄/ピンク/青）
- **トップページ**: [blog-frontpage-design.md](blog-frontpage-design.md) — PC版完成、モバイル未完

## インフラ・自動化
- **GitHub自動同期**: [auto-sync-setup.md](auto-sync-setup.md) — 1分おき、ログ: `logs/auto-sync.log`
- **定期タスク（52個）**: [scheduled-tasks.md](scheduled-tasks.md) — 3サイト共通化済み（Healthchecks.io監視+Discord通知）
- **タスク共通ルール**: [feedback_blog_tasks_shared.md](feedback_blog_tasks_shared.md) — 自動タスクは全3ブログに等しく適用
- **優先アクション/優先タスク**: [dashboard-priority-actions.md](dashboard-priority-actions.md) — 毎朝Claude APIが収益最大化ベースで自動生成、ダッシュボードで✅管理
- **Sheets同期**: `tools/sheets-sync/` — 5分おき
- **バックアップ**: `claude-backup/` — メモリ（ジャンクション）+ settings.json
- **タスク稼働確認ルール**: [feedback_proactive_task_check.md](feedback_proactive_task_check.md) — 変更時は依存スクリプト全確認、会話冒頭でログ健全性チェック

## WordPress REST API（nambei-oyaji.com）
- 認証: `nambei-oyaji.com/config/secrets.json` + `wp-credentials.json`
- トップページID: 47、再利用ブロック: ref 932-961
- カテゴリ: paraguay, side-business, ijuu-junbi
- Cocoonテーマのul/ol丸数字問題 → インラインCSS挿入で対処
- wp_block作成・編集は403（記事・ページのみ可）
- 画像: `nambei-oyaji.com/images/`、メディアID: `media-mapping.json`
- 旧ダミー記事6本（ID:1065-1070）全て正式公開済み

## 記事管理運用ルール
- 変更時は必ず `outputs/article-management.csv` を同時更新
- CSV更新後、`create_article_sheet.py` でスプレッドシート同期
- nambei-oyaji.com スプレッドシート: `1rWFxYNCxyeIoW0QKXx4RsPbYfeJLp7j0bwKw8a6x6n8`

## nambei-oyaji.com 運用
- 旧名: AI実践ラボ → 2026-03-03方向転換完了。AIは主題にしない
- 柱: pillar_1_paraguay_life（メイン）+ pillar_2_overseas_work（サブ）
- 記事数: 全23記事公開、投稿頻度: 週3回、X投稿: 1日3回
- **プロジェクトパス**: `claude-code/nambei-oyaji.com/`
- ファクトチェック必須、E-E-A-T重視、WebSearch必須

## Notion連携
- DB ID: 31be2be6-f322-81fd-8d66-c0348a3fc2ac
- 同期: `python C:/Users/tmizu/run_notion_init.py`
- notion-client非使用（requestsで直接API呼び出し）

## アフィリエイト（4 ASP × 3サイト）
- **全体概要**: [affiliate-asp-overview.md](affiliate-asp-overview.md) — 4 ASP × 3サイトの提携状況サマリー
- **A8.net**: 3サイトとも提携済み、一括挿入完了（2026-03-16）
- **アクセストレード**: [accesstrade-affiliate-pending.md](accesstrade-affiliate-pending.md) — 3サイト承認済、提携済+申請中多数、一括挿入完了（2026-03-17）
- **もしもアフィリエイト**: [moshimo-affiliate-progress.md](moshimo-affiliate-progress.md) — 3サイト登録済、一括挿入完了（2026-03-17）
- **Value Commerce**: 3サイトメディア登録済（2026-03-17）、プログラム提携未着手

## Apify DaaS事業（稼働中）
- **詳細**: [apify-business.md](apify-business.md)
- 5 Actor公開済み（Social Video Downloader, SEO Analyzer, Company Data Enricher, Trends Aggregator, Keyword Research）
- ユーザー名: miccho27、Creator plan（$7.26/半年）
- **プロジェクトパス**: `claude-code/api-services/apify-actors/`

## RapidAPI API販売事業（稼働中）
- **詳細**: [rapidapi-business.md](rapidapi-business.md)
- 全20 API、Cloudflare Workers デプロイ済み（API 1-10はRapidAPI出品済、11-20は出品待ち）
- 運用コスト$0、完全自動（集客・課金・サポート全てRapidAPI側）
- PayPal payout接続済み、日次ヘルスチェック自動化済み
- **プロジェクトパス**: `claude-code/api-services/`

## Chrome拡張ポートフォリオ事業（2/10本公開済み）
- **詳細**: [chrome-extensions-business.md](chrome-extensions-business.md)
- 公開済み2本: Regex Tester, AI Text Rewriter（2026-03-17確認）
- 審査待ち8本: JSON Formatter Pro, Color Picker, Lorem Ipsum, Hash & Encode, Page Speed, WHOIS Lookup, Currency Converter, SEO Inspector
- **プロジェクトパス**: `claude-code/chrome-extensions/`

## WP Linker Micro SaaS（稼働中）
- **詳細**: [wp-linker-project.md](wp-linker-project.md)
- WordPress内部リンク最適化SaaS、Next.js 15 + Supabase + Vercel
- 本番URL: https://wp-linker.vercel.app
- **プロジェクトパス**: `claude-code/wp-linker/`

## pSEO AIツール比較サイト（構築中）
- **詳細**: [pseo-site.md](pseo-site.md)
- Next.js 16 SSG、291ツール×12カテゴリ、4,003静的ページ生成済み（2026-03-15）
- デプロイ未完（Vercel + ドメイン取得が必要）
- **プロジェクトパス**: `claude-code/pseo-saas/`

## 仮想通貨自動売買（Bybit口座開設待ち）
- **詳細**: [trading-bot.md](trading-bot.md)
- バックテスト＆最適化完了。最優秀: MAクロス+RSI × BTC/USDT (Sharpe 4.91)
- Bybit口座開設待ち（パラグアイ住所証明の準備中）
- **プロジェクトパス**: `claude-code/trading/`

## Gumroad Notionテンプレート販売事業（全11商品 完全セットアップ済み + X自動投稿稼働中）
- **進捗**: [gumroad-listing-progress.md](gumroad-listing-progress.md)
- 全10本+バンドル($49) = 11商品 Cover/Thumbnail/Summary/タグ全て設定済み（2026-03-17）
- アカウント: tatsuya27.gumroad.com（n8nテンプレート9本も同アカウント、こちらも全整備済み）
- **Xマーケティング**: [x-prodhq27-account.md](x-prodhq27-account.md) — @prodhq27、1日3回自動投稿（10:00/14:00/19:00 PYT）
- **Gumroad出品時の注意**: [feedback_gumroad_thumbnails.md](feedback_gumroad_thumbnails.md) — サムネ必須、Pillow自動生成
- **Reddit投稿スケジュール**: [reddit-posting-schedule.md](reddit-posting-schedule.md) — 3/19 r/productivity、3/20 r/sidehustle、当日通知必須
- **プロジェクトパス**: `claude-code/gumroad-notion/`

## POD Printful×Etsy事業 AsuInk（アカウント開設待ち）
- **詳細**: [pod-etsy-business.md](pod-etsy-business.md)
- 50プロンプト・150リスティング・自動化スクリプト3本完成
- Geminiデザイン生成は有料プランが必要（無料枠では画像生成不可）
- 次: Etsy/Printfulアカウント開設 → Gemini有料プランまたは代替画像生成 → デザイン量産
- **プロジェクトパス**: `claude-code/pod-etsy/`

## VS Code拡張ポートフォリオ事業（10/10本公開済み）
- **詳細**: [vscode-extensions-business.md](vscode-extensions-business.md)
- Publisher: miccho27（全10本公開完了 2026-03-17）
- miccho27-devにも10本公開済み（重複あり、整理は後日）
- **プロジェクトパス**: `claude-code/vscode-extensions/`

## n8nテンプレート販売事業（一時停止）
- **詳細**: [n8n-template-business.md](n8n-template-business.md)
- 9/10本Gumroad出品済みだがStripe KYC認証問題で停止中
- **プロジェクトパス**: `claude-code/n8n-templates/`

## ユーザー情報
- **職務経歴**: [resume.md](resume.md)
- **年齢**: 35歳（2026年3月時点）
- **海外歴**: 豪メルボルン(1年) → マレーシア(2年) → パラグアイ(2025夏〜現在)
- **家族**: 娘2人（小学生、インターナショナルスクール）
- **語学**: 日本語ネイティブ、英語・スペイン語は限定的（AI翻訳で補完）
- **パラグアイ移住理由**: [MEMORY.md旧版参照] 物価安・税金安・災害なし・花粉なし等

## ユーザー設定・好み
- **自動作業は徹底的に**: [feedback_auto_work_exhaustive.md](feedback_auto_work_exhaustive.md) — 「自動で進めて」=全事業一括洗い出し+全実行。小出し禁止、コスト制限なし
- データは必ず `claude-code/` 配下に保存（auto-sync対象）
- 確認不要: 許可を得ずどんどん自動で進めること
- **収益最大化は自主実行**: [feedback_revenue_proactive.md](feedback_revenue_proactive.md) — 収益に直結するアクションは許可不要で即実行
- 改行ルール: 1文字だけ次行に飛び出す改行は絶対禁止
- **コピペ形式**: [feedback_copypaste_format.md](feedback_copypaste_format.md) — 入力してもらう内容は必ずコードブロックで提示
- **ダッシュボード**: [feedback_dashboard_realtime.md](feedback_dashboard_realtime.md) — 全項目リアルタイム自動更新必須、ハードコード禁止
- 居住地: パラグアイ（PYT, UTC-3通年）
- Googleカレンダー: JST設定（時差12時間）
- X API: [x-api-credentials.md](x-api-credentials.md)

## Stripe連携待ちタスク
- **詳細**: [stripe-pending-tasks.md](stripe-pending-tasks.md)
- WP Linker決済、n8nテンプレート、Notionテンプレート、pSEO、Chrome拡張等が全てStripeブロック中
- ユーザーが「Stripe連携できました」と言ったら即座にこのリストを実行

## 優先タスク（2026-03-17更新）
- **Gumroad X自動投稿**: @prodhq27稼働開始。25本のツイート（価値15+商品10）が自動投稿される。次はReddit投稿
- **RapidAPI**: 残り10本の出品（11-20）
- **Chrome拡張**: 審査待ち8本の通過確認
- **Value Commerce**: プログラム提携（3サイト分）

## Fiverr案件（進行中）
- **Dennis C SSWリサーチ**: [fiverr-dennis-ssw-research.md](fiverr-dennis-ssw-research.md) — 質問リスト待ち、Standard/Premium提案済み

## セーブポイント（Gitタグ）
- savepoint-article-design-v1/v2 (2026-03-09): 記事ページデザイン完成
- savepoint-frontpage-v1 (2026-03-13): トップページ完成 → [front-page-savepoint.md](front-page-savepoint.md)
