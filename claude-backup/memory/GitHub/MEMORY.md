# Memory - GitHub ワークスペース

## リポジトリ構成
- `c:\Users\tmizu\マイドライブ\GitHub\claude-code` → https://github.com/tmizuno27/data.git (branch: main)

## GitHub自動同期 (data リポジトリ)
- **メインスクリプト**: `C:\Users\tmizu\scripts\auto-sync.ps1` (Unicodeコードポイントでパス構築)
- **VBSランチャー**: `C:\Users\tmizu\scripts\auto-sync-hidden.vbs`
- **タスク名**: `GitAutoSync-Data` (Windows Task Scheduler)
- **頻度**: 1分おき / バッテリー駆動時も動作
- **動作**: settings.jsonバックアップ → 変更検知 → git add -A → commit → push origin main
- **ログ**: `claude-code/auto-sync.log`
- 詳細: [auto-sync-setup.md](auto-sync-setup.md)

## Claude Code データのGitHubバックアップ
- **バックアップ先**: `claude-code/claude-backup/` （auto-syncで自動push）
- **メモリ（ジャンクション）**: 各プロジェクトの memory/ の実体が `claude-backup/memory/` 内に置かれ、Claude Codeが直接読み書き → 自動でGitHubへ
  - `GitHub/` ← `c--Users-tmizu--------GitHub/memory`
  - `cloude-code-business/` ← `c--Users-tmizu--------cloude-code-business/memory`
  - `cloude-code-jidou-business/` ← `c--Users-tmizu--------cloude-code-jidou-business/memory`
  - `cloude-code-upwork-fiverr/` ← `c--Users-tmizu--------cloude-code-upwork-fiverr/memory`
- **設定ファイル（コピー）**: auto-sync.ps1が1分おきに `settings.json`, `.credentials.json` を `claude-backup/settings/` へコピー
- **PC復旧時**: ジャンクションを再作成すれば復元完了（PowerShellの `New-Item -ItemType Junction` を使用）

## パス関連の注意
- Google Drive: `C:\Users\tmizu\マイドライブ\` (G: ドライブ)
- **重要**: Task Scheduler経由でPowerShellを実行する場合、日本語パスはファイルに直書きせず `[char]0x30DE` 等のUnicodeコードポイントで構築する必要がある（UTF-8 BOMでも文字化けする）

## Google Sheets → CSV → GitHub 自動連携
- **スクリプト**: `claude-code/sheets-sync/fetch_sheets.py`
- **設定**: `claude-code/sheets-sync/config.json` (同期するスプレッドシートを登録)
- **認証**: サービスアカウント (`claude-code/sheets-sync/credentials/service-account.json`) ※.gitignoreで除外
- **出力先**: `claude-code/sheets-sync/output/` (CSV + metadata.json)
- **Task Scheduler**: `GoogleSheetsSync` (5分おき)
- **セットアップ状態**: 要初回セットアップ（Google Cloud サービスアカウント）
- **手順書**: `claude-code/sheets-sync/SETUP.md`
- **フロー**: Sheets更新 → 5分おきにCSV取得 → auto-sync.ps1が1分おきにGitHubへpush

## 職務経歴書
- **氏名**: 水野 達也
- **詳細**: [resume.md](resume.md)
- **経歴サマリー**:
  1. 瀬谷インターナショナルフットボール（2014-2015）個人事業主・サッカークラブ設立
  2. トゥエンティーフォーセブン（2015-2019）パーソナルジム店舗責任者
  3. 三洋環境（2020-2021）リユース貿易・拠点責任者
  4. D-ai（2021-2023）個別指導塾・教室長
  5. Sutherland Global（2023-2025）Amazon QA + Team Manager
  6. フリーランス（2025-現在）オンラインセールス

## Slack連携
- **接続済みワークスペース**: ポジウィルキャリア支援ラボ（ただし契約終了済み）
- **ユーザーID**: U09SMM7DQ3Z
- **ポジウィルとの契約**: 終了済み（2025年頃）

## WordPress REST API連携（nambei-oyaji.com）
- **認証情報**: `claude-code/nambei-oyaji/config/wp-credentials.json`（.gitignoreで除外済み）
- **ユーザー名**: メールアドレス（slugではない）
- **権限**: 管理者（記事投稿・ページ編集・メディアアップロード可能）
- **トップページID**: 47（固定ページ、カスタムHTML）
- **再利用ブロック**: ref 932-961（CSS定義等）
- **トップページ構造**: Hero → Value Props → Stats → Two Pillars → Topics(8タイル) → About → Experiment Log → CTA
- **ローカルバックアップ**: `C:\Users\tmizu\wp-home-raw.html`

## ブログ「南米おやじの海外生活ラボ」（nambei-oyaji.com）
- **旧名**: 南米おやじのAI実践ラボ → **2026-03-03に方向転換完了**
- **新戦略**: パラグアイ移住・海外生活が主軸。AIは前面に出さず「便利ツール」として触れるのみ
- **コンテンツ柱**: pillar_1_paraguay_life（メイン）+ pillar_2_overseas_work（サブ）
- **記事数**: 全23記事（集客9, 収益6, キラー6, 実験2）
- **詳細**: [blog-seo-rules.md](blog-seo-rules.md)
- **必須**: 記事作成時は毎回WebSearchで最新SEOトレンド（直近2-3年）をリサーチしてから執筆
- **参考**: ウェブ職TV（なかじ）のSEO手法をベースに、最新Googleアルゴリズムに対応
- **E-E-A-T重視**: パラグアイ在住の実体験（一次情報）を必ず含める
- **プロジェクトパス**: `claude-code/nambei-oyaji/`
- **注意**: AIを記事の主題にしない。「AI副業」「ChatGPT」「Claude」等のKWは使わない
- **記事管理スプレッドシート**: `1rWFxYNCxyeIoW0QKXx4RsPbYfeJLp7j0bwKw8a6x6n8`
  - URL: https://docs.google.com/spreadsheets/d/1rWFxYNCxyeIoW0QKXx4RsPbYfeJLp7j0bwKw8a6x6n8
  - タブ: 「記事一覧」（タイプ別色分け・フィルター付き）+ 「サマリー」（自動集計）
  - 更新スクリプト: `claude-code/nambei-oyaji/scripts/create_article_sheet.py`
  - CSV: `claude-code/nambei-oyaji/outputs/article-management.csv`
  - **記事作成時の運用フロー**: (1) 記事MD作成 → (2) CSVに行追加 → (3) スクリプト実行でシート＋サマリー自動更新
  - サマリーはCSVデータから毎回自動集計（ハードコードではない）

## パラグアイ移住の理由・家族情報（ブログ記事で活用）
- **物価が安い**: 生活費を大幅に抑えられる（日本の1/3〜1/2）
- **税金が安い**: 所得税が世界的に見ても非常に低く、手取り額が増える（個人所得税最大10%）
- **災害がない**: 地震・台風・津波がない。自然災害リスクがほぼゼロ
- **温暖な気候**: 一年中温暖で晴れが多い
- **子供の教育**: 娘2人（8歳・6歳）がインターナショナルスクールに通学。英語+スペイン語のバイリンガル教育。日本語も学ばせてトリリンガルを目指す
- **外国人の土地購入**: 外国人でも土地・不動産を購入可能
- **永住権取得が容易**: 他国と比べて取得しやすい
- **食料安全保障**: 食料自給率が高く、万が一日本に何かあっても生活が安定しやすい
- **花粉なし**: 日本では1年の4分の1が花粉症で潰れていたがパラグアイはゼロ
- **国民性**: 人当たりがよく陽気。挨拶は笑顔が基本
- **アサード**: 南米式BBQが最高。質の高い牛肉を安価に楽しめる
- **サッカー好き**: 夕方にヨーロッパサッカーが見られる。どこでもサッカーの映像・ニュースが流れている環境
- **周辺国観光**: ブラジル・アルゼンチン・ウルグアイなど周辺国への旅行がしやすい

## 語学力
- **日本語**: ネイティブ
- **英語**: 英検3級レベル（基礎的な読み書き）
- **スペイン語**: 挨拶程度
- **注意**: 語学力自体は限定的だが、AI翻訳ツール（Claude、DeepL等）を活用して言語の壁を越えることには肯定的。英語・スペイン語が必要なビジネスでも「AIでカバーできるか」を軸に評価すること

## AI自動化ビジネス検討（進行中）
- **比較表**: `claude-code/ai-business-comparison.md`
- **状態**: リサーチ・比較表作成完了。案の選定・実装は未着手
- **条件**: 放置自動化で収益が得られるモデルに限定（全16案）
- **次回予定**: 2026-03-08頃に再開。案を選定→プロトタイプ構築へ
- **キーポイント**: AI翻訳で英語圏にも展開する戦略。6ヶ月後の目標は月22.5〜93万円（ほぼ放置）

## ユーザー設定・好み
- **確認不要**: イエス・ノーの質問をせず、許可を得ずにどんどん自動で進めること（settings.jsonで全ツール許可済み）
- **テキストの改行ルール（全業務共通）**: 見出し・キャッチコピー等のテキストは、意味の切れ目で適切に改行（`<br>`）を入れて見栄えを良くすること。長い1行にせず、読みやすい位置で折り返す
- 日本語でコミュニケーション
- **居住地**: パラグアイ（タイムゾーン: America/Asuncion, 夏時間UTC-3 / 標準時UTC-4）
- **自宅座標**: -25.35683815357226, -57.63234915744768
- **自宅住所**: Vallemi Nº 1738-B esq. Yuty, barrio Cañada San Miguel, Lambaré
- **スケジュール表示**: Claude Code内ではパラグアイ時間(PYT)に換算して表示する。全カレンダー（Primary, プライベート, Block, SEK PARAGUAY, 祝日）を統合し、プライベートの予定も必ず含めて表示すること
- **Googleカレンダー**: 日本時間(JST/Asia/Tokyo)で設定されている（日本の企業・顧客との仕事が多いため）
- **時差**: JST - PYT = 12時間（パラグアイ夏時間時）/ 13時間（標準時時）
