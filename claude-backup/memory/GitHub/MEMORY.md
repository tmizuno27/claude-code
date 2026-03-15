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
- **定期タスク（22個）**: [scheduled-tasks.md](scheduled-tasks.md) — Healthchecks.io監視（Discord通知）
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

## アフィリエイト（TODO）
- 各サイトの `config/affiliate-links.json` にプレースホルダー残存
- 優先: Wise > NordVPN > ConoHa WING
- ASP登録後に一括置換スクリプト作成予定

## AI自動化ビジネス検討
- 比較表: `planning/ai-business-comparison.md`（16案）
- 状態: リサーチ完了、選定・実装未着手
- 目標: 放置自動化で月22.5〜93万円

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
- 居住地: パラグアイ（PYT, UTC-3通年）
- Googleカレンダー: JST設定（時差12時間）
- X API: [x-api-credentials.md](x-api-credentials.md)

## セーブポイント（Gitタグ）
- savepoint-article-design-v1/v2 (2026-03-09): 記事ページデザイン完成
- savepoint-frontpage-v1 (2026-03-13): トップページ完成 → [front-page-savepoint.md](front-page-savepoint.md)
