---
name: product-inventory
description: 6プラットフォーム（RapidAPI, Gumroad, Chrome, VSCode, Apify, Etsy）の商品在庫・ステータス横断確認
---

# 全プラットフォーム商品在庫チェック

## 対象プラットフォーム

### 1. RapidAPI（21本）
- `products/api-services/` 配下の全Worker確認
- `memory/rapidapi-business.md` と照合
- 各APIの公開状態・プラン設定を確認

### 2. Gumroad（Notionテンプレート11本 + n8nテンプレート9本）
- `products/gumroad-notion/` の商品一覧確認
- `memory/gumroad-listing-progress.md` と照合
- `products/n8n-templates/` の出品状況確認
- カバー画像・サムネイル・価格設定の有無

### 3. Chrome拡張（10本）
- `products/chrome-extensions/` 配下の全拡張確認
- `memory/chrome-extensions-business.md` と照合
- 公開/審査中/却下のステータス

### 4. VS Code拡張（10本）
- `products/vscode-extensions/` 配下の全拡張確認
- `memory/vscode-extensions-business.md` と照合
- Marketplace公開状態

### 5. Apify Actors（5本）
- `products/api-services/apify-actors/` 確認
- `memory/apify-business.md` と照合

### 6. POD Etsy（準備中）
- `products/pod-etsy/` の準備状況確認
- `memory/pod-etsy-business.md` と照合

## 出力フォーマット

```
## 商品在庫レポート（YYYY-MM-DD）

### サマリー
| プラットフォーム | 公開中 | 審査中 | 未公開 | 合計 |
|-----------------|--------|--------|--------|------|
| RapidAPI | XX | - | XX | 21 |
| Gumroad | XX | - | XX | 20 |
| Chrome拡張 | XX | XX | XX | 10 |
| VS Code拡張 | XX | - | XX | 10 |
| Apify | XX | - | XX | 5 |
| POD Etsy | XX | - | XX | - |
| **合計** | **XX** | **XX** | **XX** | **66+** |

### 要対応アクション
1. ...

### 新商品機会
（市場調査に基づく提案）
```

## ルール
- メモリの情報は参考値。実ファイルを読んで最新状態を確認すること
- 既存商品の重複提案は禁止（`feedback_check_existing_before_listing.md` 参照）
- サムネイル未設定の商品があれば警告（`feedback_gumroad_thumbnails.md` 参照）
