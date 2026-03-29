# noindex チェックレポート - 2026-03-28

## 実行概要

3サイト全記事（公開済み）のHTMLを取得し、`<meta name="robots">` タグにnoindex/nofollowが設定されていないかチェック。

## チェック方法

- WordPress REST APIで各サイトの全公開記事を取得
- 各記事URLに直接アクセスしてHTMLを解析
- `<meta name="robots">` および `<meta name="googlebot">` タグのcontent属性を確認
- noindex / nofollow の有無を判定

## 結果サマリー

| サイト | 総記事数 | NOINDEX | NOFOLLOW | 正常 | エラー |
|--------|---------|---------|---------|------|------|
| nambei-oyaji.com | 85 | **0** | 0 | 85 | 0 |
| otona-match.com | 92 | **0** | 0 | 92 | 0 |
| sim-hikaku.online | 70 | **0** | 0 | 70 | 0 |
| **合計** | **247** | **0** | **0** | **247** | **0** |

## 結論

**3サイト合計247記事、noindex/nofollow設定なし。問題なし。**

## 補足：サイト別 robots メタの違い

### nambei-oyaji.com

robots メタに `index, follow` が明示されている：

```
<meta name="robots" content="index, follow, max-snippet:-1, max-video-preview:-1, max-image-preview:large"/>
```

### otona-match.com / sim-hikaku.online

robots メタに `max-image-preview:large` のみ（index/followの明示なし）：

```
<meta name='robots' content='max-image-preview:large' />
```

**これは問題なし。** Googlebotはrobotsメタに `noindex` が指定されていない場合、デフォルトでindexとして扱う。`index, follow` の明示がないだけで、実際にはインデックス可能な状態。

Rank Mathの設定の違いによるもの（nambei-oyajiはRank Mathで明示的にindex/followを設定、他2サイトは省略形）。

## 実行環境

- チェック日時: 2026-03-28
- チェック対象: 公開済み記事のみ（下書き・非公開除く）
- チェック方法: HTML直接取得による robots メタタグ解析
