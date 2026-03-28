# デジタルプロダクト事業 改善アクションプラン（2026-03-28）

## 実行済みアクション（このセッション）

### 1. RapidAPI（24本・収益$0）
- [x] Dev.to記事公開スクリプト作成（`marketing/devto/publish_to_devto.py`）
  - 13本の記事が準備済み → スクリプトでDev.toにドラフト一括投稿可能
  - `python publish_to_devto.py` で全記事をドラフト投稿
  - `python publish_to_devto.py --publish` で公開投稿
  - Dev.to APIキー設定済み（`dev-to-config.json`）
- [x] SEO改善ガイドは既に詳細に作成済み（`rapidapi-seo-improvements.md`）→ 24本全APIのタイトル・説明文・タグの改善案完備

### 2. Chrome拡張（2/11本公開、8本審査中）
- [x] 審査改善レポート確認（`audit-improvements-2026-03-26.md`）
- **現状**: 2026-03-16提出、12日経過。プライバシーポリシーURL未設定が最大のボトルネック
- **GitHub Pages無効化済み**（2026-03-27）→ プライバシーポリシーURLが使えない状態

### 3. VS Code拡張（10本公開・インストール計3）
- [x] SEOキーワード最適化ガイド作成（`seo-keyword-optimization.md`）
  - 10本全拡張のkeywords・displayName・description改善案
  - 「M27」プレフィックスが検索妨害している問題を特定

### 4. Gumroad（13商品 + 新商品2本準備中）
- [x] Business Automation Prompts（52プロンプト完全版）制作（`06-business-automation-prompts-full.md`）
  - 5カテゴリ・52プロンプト・プロンプトチェイニングガイド・LLM比較表付き
- [x] ADHD Daily Plannerのリスティング確認（既に高品質で準備完了）

### 5. Apify Actor（9本開発済み）
- [x] デプロイガイド作成（`deploy-guide.md`）
  - 一括デプロイスクリプト・各Actorの改善ポイント

---

## ユーザー手動アクション（必須・優先順）

### 【最優先】即日実行（30分以内）

#### A. Dev.to記事をドラフト投稿
```bash
cd "C:/Users/tmizu/マイドライブ/GitHub/claude-code/products/api-services/marketing/devto"
python publish_to_devto.py
```
→ 13本がドラフトとして投稿される。Dev.to管理画面で確認後、1本ずつ公開。

#### B. RapidAPIリスティング更新（上位5本から）
`rapidapi-seo-improvements.md` のコピペガイドに従い、RapidAPI Provider Dashboardで：
1. QR Code API
2. Email Validation API
3. Screenshot API
4. SEO Analyzer API
5. IP Geolocation API
のタイトル・Short Description・タグを更新。

### 【高優先】今週中

#### C. Chrome拡張プライバシーポリシー対応
GitHub Pagesが無効化されているため、別のホスティングが必要：
- **選択肢1**: GitHub Pagesを再有効化（ビルド失敗メール覚悟）
- **選択肢2**: 各HTMLをGistに置いてraw URLを使う
- **選択肢3**: Vercel/Netlifyに静的サイトとしてデプロイ
→ URLを確保したらChrome Developer Dashboardで8本全てに設定

#### D. VS Code拡張のpackage.json更新
`seo-keyword-optimization.md` の推奨に従い、各拡張の：
1. `keywords` を更新
2. `description` を更新
3. `vsce publish patch` で再公開

優先順位: Paste & Transform → Console Cleaner → ENV Lens → Markdown Table Pro

#### E. Gumroad新商品出品
1. **Business Automation Prompts ($12)**: `06-business-automation-prompts-full.md` をZIP化してGumroadに出品
2. **ADHD Daily Planner ($14)**: Notionテンプレート制作 → Gumroadに出品
   - リスティング文は `17-adhd-daily-planner.md` に準備済み

#### F. Apify Actor一括デプロイ
```bash
apify login
cd "C:/Users/tmizu/マイドライブ/GitHub/claude-code/products/api-services/apify-actors/amazon-product-scraper"
apify push
# 各Actorで繰り返し
```

---

## 収益インパクト予測

| アクション | 期待効果 | 時間軸 |
|-----------|---------|--------|
| Dev.to記事13本公開 | RapidAPIへの外部トラフィック誘導、初の購読者獲得 | 1-2週間 |
| RapidAPIリスティング更新 | マーケットプレイス内検索順位UP | 1-4週間 |
| VS Code拡張SEO最適化 | インストール数10-50件 | 2-4週間 |
| Gumroad新商品2本 | 月$20-100の追加収益 | 1-3ヶ月 |
| Chrome拡張8本公開 | フリーミアム収益の基盤 | 審査通過次第 |
| Apify Actor公開 | 月$5-20のActorごと | 1-2ヶ月 |

## 厳しい現実

- **全プロダクト収益$0**: 24 API + 10 VS Code拡張 + 13 Gumroad商品 + 9 Apify Actor = 56商品で$0
- **根本問題はトラフィック不足**: 商品の品質は十分。見つけてもらえていない
- **最も即効性があるのはDev.to記事**: 開発者コミュニティに直接リーチできる唯一のチャネル
- **Chrome拡張のプライバシーポリシー問題が最大のブロッカー**: これが解決しないと8本永久に審査落ち
