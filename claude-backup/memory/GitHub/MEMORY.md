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

## アフィリエイト
- A8.net: 3サイトとも提携済み、`insert_affiliate_all.py` で全記事に一括挿入完了（2026-03-16）
- **アクセストレード進捗**: [accesstrade-affiliate-pending.md](accesstrade-affiliate-pending.md) — nambei+sim承認済、otona申請中。承認後に一括作業予定

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

## Chrome拡張ポートフォリオ事業（審査中）
- **詳細**: [chrome-extensions-business.md](chrome-extensions-business.md)
- 10個の拡張を開発・Chrome Web Store審査申請済み（2026-03-16）
- Rick Blyth方式（量産×放置）、運用コスト$0
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

## Gumroad Notionテンプレート販売事業（構築済み）
- **詳細**: [gumroad-notion-business.md](gumroad-notion-business.md)
- テンプレート10本+バンドル、設計書・出品テキスト・マーケティング素材完成
- Notion実構築→Gumroad出品が次ステップ
- **プロジェクトパス**: `claude-code/gumroad-notion/`

## POD Printful×Etsy事業 AsuInk（構築済み）
- **詳細**: [pod-etsy-business.md](pod-etsy-business.md)
- 50デザイン×3商品=150リスティング、プロンプト・出品テキスト完成
- Etsy/Printfulアカウント開設→デザイン生成が次ステップ
- **プロジェクトパス**: `claude-code/pod-etsy/`

## VS Code拡張ポートフォリオ事業（構築済み）
- **詳細**: [vscode-extensions-business.md](vscode-extensions-business.md)
- 10本企画、うち3本フルコード完成（Paste & Transform, Console Cleaner, ENV Lens）
- Azure DevOps PAT取得→Marketplace公開が次ステップ
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
- データは必ず `claude-code/` 配下に保存（auto-sync対象）
- 確認不要: 許可を得ずどんどん自動で進めること
- 改行ルール: 1文字だけ次行に飛び出す改行は絶対禁止
- **コピペ形式**: [feedback_copypaste_format.md](feedback_copypaste_format.md) — 入力してもらう内容は必ずコードブロックで提示
- 居住地: パラグアイ（PYT, UTC-3通年）
- Googleカレンダー: JST設定（時差12時間）
- X API: [x-api-credentials.md](x-api-credentials.md)

## Stripe連携待ちタスク
- **詳細**: [stripe-pending-tasks.md](stripe-pending-tasks.md)
- WP Linker決済、n8nテンプレート、Notionテンプレート、pSEO、Chrome拡張等が全てStripeブロック中
- ユーザーが「Stripe連携できました」と言ったら即座にこのリストを実行

## セーブポイント（Gitタグ）
- savepoint-article-design-v1/v2 (2026-03-09): 記事ページデザイン完成
- savepoint-frontpage-v1 (2026-03-13): トップページ完成 → [front-page-savepoint.md](front-page-savepoint.md)
