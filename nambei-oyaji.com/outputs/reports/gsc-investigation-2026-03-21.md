# Google Search Console 表示0件 調査レポート

**調査日**: 2026-03-21
**対象サイト**: https://nambei-oyaji.com

---

## 調査結果サマリー

| 項目 | 状態 | 詳細 |
|------|------|------|
| robots.txt | 正常 | Disallowは/wp-admin/のみ。noindex指示なし |
| sitemap_index.xml | 正常 | Rank Math生成。post/page/categoryの3つ |
| post-sitemap.xml | 正常 | 50件のURL登録済み |
| sitemap.xml | 404 | robots.txtの指定は sitemap_index.xml なので問題なし |
| メタタグ（noindex） | 検出なし | 個別記事にnoindex/nofollowメタタグなし |
| canonical URL | 正常 | 自己参照canonical設定済み |
| WordPress記事 | 正常 | 最新5件全てpublishステータス |
| REST API | 正常 | 正常に応答 |
| SEOプラグイン | Rank Math | 正常稼働 |
| ローカル設定 | 問題なし | settings.jsonに異常なし |

## 結論: サイト側に技術的なブロック要因は見つからない

robots.txt、サイトマップ、メタタグ、canonical全て正常。サイト側でインデックスをブロックする設定は確認されなかった。

---

## 考えられる原因と対処法

### 原因1: WordPress「検索エンジンがサイトをインデックスしないようにする」設定（最有力）

WordPress管理画面 > 設定 > 表示設定 に「検索エンジンがサイトをインデックスしないようにする」チェックボックスがある。これがONだと、HTMLヘッダーに `<meta name='robots' content='noindex, nofollow'>` が出力される。

ただし今回の調査では個別記事にnoindexメタタグは検出されなかったため、この設定はOFFの可能性が高い。

**確認方法**: WP管理画面 > 設定 > 表示設定 > 「検索エンジンがサイトをインデックスしないようにする」がOFFであることを確認

### 原因2: GSCプロパティ設定の問題（有力）

- GSCにサイトが正しく登録されているか
- プロパティタイプ（URLプレフィックス vs ドメイン）が正しいか
- 所有権の確認が完了しているか

**確認方法**:
1. https://search.google.com/search-console にアクセス
2. `https://nambei-oyaji.com` プロパティが存在し、所有権確認済みか確認
3. 「カバレッジ」または「ページ」レポートでインデックス状況を確認

### 原因3: サイトが新しくGoogleがまだクロールしていない

サイトの記事が最近大量公開されたばかりの場合、Googleのクロール・インデックスに数日〜数週間かかる。

**対処法**:
1. GSC > URL検査 > トップページURLを入力 > 「インデックス登録をリクエスト」
2. GSC > サイトマップ > `https://nambei-oyaji.com/sitemap_index.xml` を送信
3. 主要記事10件程度を個別にURL検査でインデックス登録リクエスト

### 原因4: Rank Mathのnoindex設定

Rank Mathはカテゴリ・タグ・投稿タイプ単位でnoindexを設定できる。

**確認方法**: WP管理画面 > Rank Math > タイトルと説明 > 投稿タイプ > 「投稿」のRobots Metaが「index」になっているか確認

---

## 推奨アクション（優先順）

1. **GSCでサイトマップを送信**（即実行）
   - GSC > サイトマップ > `https://nambei-oyaji.com/sitemap_index.xml` を送信

2. **GSCのURL検査でトップページとmain記事5件のインデックスをリクエスト**（即実行）

3. **WP管理画面で以下を確認**（即実行）
   - 設定 > 表示設定 > 「検索エンジンがサイトをインデックスしないようにする」がOFF
   - Rank Math > タイトルと説明 > 投稿 > Robots Meta = index

4. **1週間後にGSCを再確認**
   - インデックス数が増えていなければ、個別記事のHTTPヘッダー（X-Robots-Tag）をcurlで確認

---

## URLスラッグの問題点（副次的）

サイトマップの多くのURLが日本語URLエンコードになっている（例: `%e3%83%91%e3%83%a9%e3%82%b0%e3%82%a2%e3%82%a4...`）。SEO上はローマ字スラッグが推奨される。一部の記事（`kaigai-soukin-tesuuryou-hikaku`）はローマ字スラッグを使用しており、混在している。

**推奨**: 今後の新規記事はローマ字スラッグを使用。既存記事のスラッグ変更はリダイレクト設定が必要なため慎重に。
