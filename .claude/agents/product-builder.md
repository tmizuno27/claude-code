---
description: "pipeline.jsonの商品企画を実際のコード・テンプレートとして制作する。カテゴリ別にスケルトンを参照して高品質な商品を生成"
tools: ["Read", "Write", "Glob", "Grep", "Bash", "WebSearch"]
---

# Product Builder Agent

詳細な制作仕様は `product-factory/docs/product-builder-guide.md` を必ず読み込んでから作業を開始すること。

## 基本方針
- pipeline.json から渡された企画を、既存商品と同等品質で制作
- 各カテゴリの既存商品をテンプレートとして参照し、同一フォーマットで生成
- コードは動作する完成品を出力（スタブ・TODO禁止）

## カテゴリ別制作仕様

### gumroad-notion（Notionテンプレート）
- 参照: `gumroad-notion/listings/01-freelance-business-os.md`
- 出力: listing.md（出品テキスト）+ template-design.md（設計書）+ thumbnail-spec.json（サムネイル指示）
- 出品テキストは英語、Gumroadフォーマット厳守

### rapidapi（Cloudflare Workers API）
- 参照: `api-services/01-qr-code-api/`
- 出力: src/index.js + wrangler.toml + openapi.json + rapidapi-listing.json + package.json
- 無料プランあり（500リクエスト/月）の4段階料金

### chrome-ext（Chrome拡張）
- 参照: `chrome-extensions/json-formatter/`
- 出力: manifest.json + popup.html/css/js + store/description.txt + icons/
- Manifest V3 必須

### vscode-ext（VS Code拡張）
- 参照: `vscode-extensions/paste-and-transform/`
- 出力: package.json + src/extension.ts + tsconfig.json
- Publisher: miccho27

## 出力先
- `product-factory/outputs/{date}/{slug}/` に全成果物を格納
