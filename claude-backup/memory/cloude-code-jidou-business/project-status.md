# プロジェクト進捗詳細

## 作成済みファイル（25ファイル）

### 基盤
- `CLAUDE.md` — Claude Code操作ガイド
- `requirements.txt` — Python依存パッケージ

### 設定（config/）
- `settings.json` — API鍵（全てプレースホルダー状態）、WP URL、スケジュール設定
- `affiliate-links.json` — アフィリエイトリンク（AI tools, online schools, crowdsourcing, business tools）
- `content-calendar.json` — シードKW10個、商品スケジュール3商品

### エージェント定義（agents/）
- `seo-research-agent.md` — KW調査
- `article-writer-agent.md` — SEO記事生成（2500-3000字、E-E-A-T重視）
- `product-creator-agent.md` — デジタル商品生成
- `publisher-agent.md` — WordPress投稿
- `sns-scheduler-agent.md` — X投稿生成（週21投稿）
- `analytics-agent.md` — 分析レポート
- `master-prompt.md` — オーナー用コピペコマンド集

### テンプレート（templates/）
- `article-template.md` — SEO記事構成テンプレート
- `ebook-template.md` — 電子書籍テンプレート
- `prompt-collection.md` — プロンプト集テンプレート

### スクリプト（scripts/）
- `keyword_research.py` — Google Suggest APIでKW調査、スコアリング、上位20件出力
- `article_generator.py` — Claude API (anthropic SDK) でSEO記事生成、フロントマター付き
- `wp_publisher.py` — WordPress REST APIでドラフト投稿、Basic認証
- `internal_linker.py` — WP記事間の内部リンク自動挿入
- `pdf_generator.py` — WeasyPrintでMarkdown→PDF変換
- `analytics_reporter.py` — GA4/Gumroad/手動データ集約、Claude APIでレポート生成
- `content_calendar.py` — KWキューから4週間カレンダー自動生成
- `scheduler.py` — Windowsタスクスケジューラ登録（schtasks）

### ドキュメント（docs/）
- `setup-guide.md` — ConoHa WING、WP、GA4、ASP登録の手順書
- `daily-operation.md` — 日次運用マニュアル（1日60分のルーティン）

## 次のアクション（優先順）

1. **差別化戦略の最終決定** — 量産型 vs 質重視型の方針をオーナーと確認
2. **手動セットアップ（オーナー作業）**:
   - ConoHa WING契約 + ドメイン取得
   - WordPress + Rank Math SEO導入
   - GA4 / Search Console設定
   - A8.net / もしもアフィリエイト登録
   - config/settings.json のAPI鍵を実際の値に設定
3. **Pythonパッケージインストール**: `pip install -r requirements.txt`
4. **keyword_research.py の動作テスト**
5. **article_generator.py の動作テスト**（Claude APIキー設定後）
6. **wp_publisher.py の動作テスト**（WordPress設定後）

## 月額コスト見積もり
- Phase 1: 約12,000円/月
- Phase 2以降: 約16,000〜26,000円/月

## 収益目標
| 時期 | 月収目標 |
|------|----------|
| 3ヶ月目 | 44,000円 |
| 6ヶ月目 | 110,000円 |
| 12ヶ月目 | 200,000円 |
