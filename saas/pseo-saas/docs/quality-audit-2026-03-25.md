# pSEO AIツール比較サイト — 品質監査レポート

**監査日**: 2026-03-25
**サイトURL**: ai-tool-compare-nu.vercel.app

## サンプルチェック結果

| ページ | Title | Description | H1 | 構造化データ | 語数 |
|--------|-------|-------------|-----|------------|------|
| chatgpt-vs-claude | OK (67文字) | OK (テンプレ) | OK | 2ブロック | ~2,161 |
| cursor-vs-github-copilot | OK (68文字) | OK (テンプレ) | OK | 2ブロック | ~2,246 |

### 良い点
- Title が「[A] vs [B]: Which is Better in 2026?」で統一（SEO最適化済み）
- 構造化データ（JSON-LD）が2ブロック設置済み
- OGPタグ（og:title, og:description）設置済み
- 語数2,000超で十分なコンテンツ量
- 4,706比較ページ + 329ツール + 12カテゴリの網羅性

### 問題点（要修正）

#### 1. robots.txt と sitemap.xml のドメイン不一致（重要度: HIGH）
- **robots.txt**: `Sitemap: https://aitoolvs.com/sitemap.xml` を参照
- **sitemap.xml**: URL が `https://ai-tool-compare-nu.vercel.app/` を使用
- **実際のドメイン**: `ai-tool-compare-nu.vercel.app`
- **影響**: Googlebotがsitemapを正しく認識できない可能性

**修正方法**: robots.txt と sitemap.xml のドメインを統一する。独自ドメイン `aitoolvs.com` を使うなら sitemap.xml も合わせる。Vercelドメインのままなら robots.txt を修正。

#### 2. canonical URL の不一致リスク（重要度: MEDIUM）
- canonical が `https://ai-tool-compare.vercel.app/compare/chatgpt-vs-claude/` を指している
- 実際のデプロイ先は `ai-tool-compare-nu.vercel.app`
- `aitoolvs.com` がカスタムドメインとして設定済みなら問題なし、未設定なら要修正

#### 3. meta descriptionがテンプレ的（重要度: LOW）
- 全ページ「Detailed comparison of [A] and [B]. Compare features, pricing, ratings, pros & cons...」
- Google側で書き換えられる可能性あり
- 各ページ固有の文言（「ChatGPT excels at...while Claude offers...」等）を入れると改善

#### 4. og:imageが未設定（重要度: MEDIUM）
- SNS共有時にプレビュー画像が表示されない
- Vercel OG Image GenerationまたはCloudflare Workersで動的生成推奨

## GSC サイトマップ登録確認手順

### 前提
- Google Search Console に `ai-tool-compare-nu.vercel.app` が登録済み

### 確認手順

1. **GSCダッシュボードで確認**:
   ```
   https://search.google.com/search-console/sitemaps?resource_id=sc-domain:ai-tool-compare-nu.vercel.app
   ```
   または URL プレフィックスプロパティの場合:
   ```
   https://search.google.com/search-console/sitemaps?resource_id=https://ai-tool-compare-nu.vercel.app/
   ```

2. **サイトマップの送信状態を確認**:
   - 「サイトマップ」→ 送信済みのサイトマップ一覧
   - ステータスが「成功」であること
   - 検出されたURL数が4,706+であること

3. **サイトマップが未送信の場合**:
   - 「新しいサイトマップの追加」に `sitemap.xml` を入力して送信
   - robots.txtのSitemap行のドメインが一致していることを事前確認

4. **GSC API経由で確認**（自動化向け）:
   ```bash
   # GSC APIでサイトマップ一覧取得
   curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     "https://www.googleapis.com/webmasters/v3/sites/https%3A%2F%2Fai-tool-compare-nu.vercel.app%2F/sitemaps"
   ```

### インデックス状況確認
- GSC「カバレッジ」または「ページ」レポートで:
  - インデックス済みページ数
  - 「検出 - インデックス未登録」のページ数
  - エラーがあるページ

## Indexing API による主要ページのインデックス促進

pSEOプロジェクト内にIndexing APIスクリプトは存在しない。以下の手順で対応:

### 方法1: 既存のサイト用スクリプトを流用
nambei-oyaji.com等で使っているIndexing APIスクリプトがあればパスを変えて流用可能。

### 方法2: 新規作成（推奨する優先ページ）
まずインデックスを促進すべき主要ページ（上位100ページ）:
1. トップページ
2. 12カテゴリページ
3. 検索ボリュームが高い比較ページ（chatgpt-vs-claude, midjourney-vs-dall-e, cursor-vs-copilot等）

### Google Indexing API の注意点
- Indexing API は本来 JobPosting / BroadcastEvent 向け
- 一般サイトでは効果が限定的（URL送信→クロール優先度が上がるだけ）
- 代替: GSCの「URL検査」→「インデックス登録をリクエスト」を主要100ページに手動実行
- または `request_indexing.py` スクリプトで自動化（1日200URL制限）

## 次のアクション

1. **今すぐ**: robots.txt / sitemap.xml / canonical のドメイン統一
2. **今週**: GSCでサイトマップ送信状態を確認、主要50ページのインデックスリクエスト
3. **来週**: og:image動的生成の実装、meta descriptionの個別化
