# Product Builder — カテゴリ別制作ガイド

## 共通ルール
- 既存商品と同等品質・同一フォーマットで生成すること
- コードはスタブ・TODO禁止、動作する完成品を出力
- 英語（グローバル市場向け）
- 出力先: `product-factory/outputs/{YYYY-MM-DD}/{slug}/`

## gumroad-notion（Notionテンプレート）

### 生成ファイル
1. **listing.md** — Gumroad出品テキスト
   - フォーマット参照: `gumroad-notion/listings/01-freelance-business-os.md`
   - 必須セクション: Product Title, Price, Tags, Categories, Description, What's Inside, Who It's For, How To Use, FAQ, Thumbnail Description
2. **template-design.md** — Notionテンプレート設計書
   - DB一覧（名前、プロパティ、リレーション）
   - ビュー一覧（テーブル、カンバン、カレンダー等）
   - ダッシュボード構成
   - サンプルデータ（3-5件）
3. **thumbnail-spec.json** — Pillow生成用パラメータ
   ```json
   {
     "width": 600, "height": 600,
     "background": {"type": "gradient", "colors": ["#1a1a2e", "#16213e"]},
     "title": "商品名",
     "subtitle": "サブタイトル",
     "font_size_title": 36,
     "font_size_subtitle": 18
   }
   ```
4. **x-posts.json** — X投稿テキスト3本
   ```json
   {
     "value_post": "課題提起+解決策（リンクなし）",
     "promo_post": "商品紹介+Gumroadリンク",
     "thread_post": ["ツイート1", "ツイート2", "ツイート3"]
   }
   ```

### 品質基準
- What's Inside: 8-10項目
- DB数: 最低4、ビュー数: 最低15
- FAQ: 3-4件
- ターゲット: 4層以上

## rapidapi（Cloudflare Workers API）

### 生成ファイル
1. **src/index.js** — Worker本体（Pure JS、外部依存なし）
2. **wrangler.toml** — デプロイ設定
3. **openapi.json** — OpenAPI 3.0 スペック
4. **rapidapi-listing.json** — 出品情報（参照: `api-services/01-qr-code-api/rapidapi-listing.json`）
5. **package.json** — メタデータ

### 品質基準
- エンドポイント: 最低2、推奨3-5
- エラーハンドリング: 400/404/500を適切に返す
- レスポンスタイム: 100ms以内（外部API依存を避ける）
- CORS対応

## chrome-ext（Chrome拡張機能）

### 生成ファイル
1. **manifest.json** — Manifest V3
2. **popup.html** + **popup.css** + **popup.js** — ポップアップUI
3. **store/description.txt** — ストア説明文
4. **store/privacy-policy.html** — プライバシーポリシー

### 品質基準
- Manifest V3 必須
- permissions は必要最小限
- UIはクリーン・モダン（既存拡張のCSS参照）
- 外部通信がある場合はprivacy policyに明記

## vscode-ext（VS Code拡張機能）

### 生成ファイル
1. **package.json** — 拡張メタ（publisher: miccho27）
2. **src/extension.ts** — メインロジック
3. **tsconfig.json** — TypeScript設定
4. **README.md** — マーケットプレイス説明

### 品質基準
- activationEvents は適切に（* 禁止）
- contributes.commands は明確な名前
- エラー時はvscode.window.showErrorMessage
