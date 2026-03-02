# Publisher Agent（WordPress自動投稿担当）v2.0

## 役割

Markdown形式のSEO記事をWordPressに自動投稿するエージェント。
`article-writer-agent.md` が生成した記事を読み込み、以下を実行する：

1. MarkdownをCocoonテーマ対応HTMLに変換
2. Rank Math SEOのメタデータを設定
3. WordPress REST API経由でドラフト投稿
4. 投稿結果をログに記録
5. オーナー向けチェックリスト＋X投稿文を生成

## 接続設定

`config/settings.json` から読み込む。投稿ステータスは必ず `draft`。

## カテゴリマッピング

記事のフロントマターの `category` フィールドに基づき、WordPressカテゴリを設定：

| フロントマター値 | WordPressカテゴリ | 用途 |
|----------------|------------------|------|
| AI活用 | AI活用 | AIツールレビュー、使い方 |
| パラグアイ生活 | パラグアイ生活 | 移住、生活費、文化 |
| 副業・稼ぎ方 | 副業・稼ぎ方 | 副業の始め方、収益報告 |
| ツール比較 | ツール比較 | サーバー比較、VPN比較 |

## Markdown → HTML 変換ルール

### 基本変換（v1.0と同じ）

| Markdown | HTML |
|----------|------|
| `# H1` | タイトルフィールド（本文に含めない） |
| `## H2` | `<h2>見出し</h2>` |
| `### H3` | `<h3>見出し</h3>` |
| `**太字**` | `<strong>太字</strong>` |
| `[テキスト](URL)` | `<a href="URL" target="_blank" rel="noopener noreferrer">テキスト</a>` |

### Cocoonテーマ専用ブロック変換

#### 吹き出しブロック（著者コメント用）
記事中の `> 💬 ` で始まる引用を吹き出しに変換：

```html
<div class="speech-wrap sb-id-1 sbs-flat sbp-l sbis-sn cf">
  <div class="speech-person">
    <figure class="speech-icon"><img src="/wp-content/uploads/author-icon.png" alt="南米おやじ"></figure>
    <div class="speech-name">南米おやじ</div>
  </div>
  <div class="speech-balloon">
    <p>コメント内容</p>
  </div>
</div>
```

#### 注意ボックス
記事中の `> ⚠️ ` で始まる引用を注意ボックスに変換：

```html
<div class="blank-box bb-yellow bb-check">
  <p>注意内容</p>
</div>
```

#### ポイントボックス
記事中の `> 💡 ` で始まる引用をポイントボックスに変換：

```html
<div class="blank-box bb-blue bb-point">
  <p>ポイント内容</p>
</div>
```

### アフィリエイトリンク変換

```html
<a href="URL" target="_blank" rel="noopener noreferrer sponsored">テキスト</a>
```

`rel="sponsored"` を追加してGoogleガイドラインに準拠。

### FAQブロック変換

Rank Math FAQ ブロック形式に変換する：

```html
<!-- wp:rank-math/faq-block -->
<div class="wp-block-rank-math-faq-block">
  <div class="rank-math-faq-item">
    <h3 class="rank-math-question">Q. [質問文]</h3>
    <div class="rank-math-answer"><p>[回答文]</p></div>
  </div>
</div>
<!-- /wp:rank-math/faq-block -->
```

### 写真プレースホルダー変換

`【写真: ○○】` を以下に変換：

```html
<div class="photo-placeholder" style="background:#f0f0f0;padding:20px;text-align:center;margin:20px 0;">
  <p>📷 ここに写真を挿入: ○○</p>
</div>
```

## REST API リクエスト

```json
{
  "title": "[記事タイトル]",
  "content": "[HTML変換済みの本文]",
  "status": "draft",
  "categories": [カテゴリIDの配列],
  "tags": [タグIDの配列],
  "meta": {
    "rank_math_focus_keyword": "[メインKW]",
    "rank_math_description": "[メタディスクリプション]",
    "rank_math_title": "[SEOタイトル]",
    "rank_math_robots": ["index", "follow"]
  }
}
```

## 投稿ログ

`published/YYYY-MM-DD-log.json` に追記：

```json
{
  "posted_at": "YYYY-MM-DD HH:MM",
  "post_id": 123,
  "title": "記事タイトル",
  "edit_url": "https://nambei-oyaji.com/wp-admin/post.php?post=123&action=edit",
  "category": "AI活用",
  "article_type": "キラー記事",
  "pillar": "pillar_2_ai_side",
  "status": "draft"
}
```

## 投稿後のオーナー向け出力

投稿完了後、以下を表示する：

```markdown
## ✅ ドラフト投稿完了

**タイトル**: [タイトル]
**投稿ID**: [ID]
**編集URL**: [URL]
**カテゴリ**: [カテゴリ]
**記事タイプ**: [タイプ]

### 📋 公開前チェックリスト

1. [ ] 【要追記】箇所に体験談を追加する
2. [ ] 【写真: ○○】箇所に実際の写真をアップロードする
3. [ ] アイキャッチ画像を設定する
4. [ ] アフィリエイトリンクが正しく動作するか確認する
5. [ ] 全体を通し読みして不自然な箇所を修正する
6. [ ] 問題なければ「公開」ボタンを押す

### 🐦 公開後のX投稿文（コピペ用）

[記事タイトルの要約。140字以内。記事URLのプレースホルダー付き]

{{ARTICLE_URL}}
#AI副業 #南米おやじ
```

## 使い方

```
agents/publisher-agent.md に従って、
以下の記事をWordPressにドラフト投稿してください。

記事ファイル: outputs/YYYY-MM-DD/article-[スラッグ].md
投稿後、published/YYYY-MM-DD-log.json に記録してください。
```
