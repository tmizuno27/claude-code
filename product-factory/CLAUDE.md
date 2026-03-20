# Product Factory — AIエージェント×デジタル商品自動量産

## 概要
Claude Codeエージェントがデジタル商品を自動で企画→制作→出品→マーケティングする仕組み。
OpenClawの「Felix」モデル（月売上1,200万円・従業員ゼロ）にインスパイア。

## エージェント構成（4体）
| エージェント | 役割 | スラッシュコマンド |
|-------------|------|------------------|
| product-factory | 司令官。パイプライン管理・実行統括 | `/product-factory` |
| market-researcher | 市場調査・商品企画生成 | `/market-researcher` |
| product-builder | 商品本体の制作 | `/product-builder` |
| listing-publisher | 出品素材・マーケティング生成 | `/listing-publisher` |

## 対応カテゴリ（4種）
1. **gumroad-notion**: Notionテンプレート（$9-19）— Phase 1で最優先
2. **rapidapi**: Cloudflare Workers API（フリーミアム）— Phase 2
3. **chrome-ext**: Chrome拡張（フリーミアム）— Phase 3
4. **vscode-ext**: VS Code拡張（無料）— Phase 3

## 使い方

### 商品を1つ自動生成する
```
/product-factory
```
pipeline.json の先頭キューを自動制作。

### 市場調査して新企画を追加する
```
/market-researcher
```
WebSearchで需要調査→pipeline.jsonに5-10件追加。

### 制作済み商品の出品素材を生成
```
/listing-publisher
```

## ファイル構成
```
product-factory/
├── CLAUDE.md              ← このファイル
├── docs/                  ← 設計書・制作ガイド
├── inputs/pipeline.json   ← 商品キュー
├── outputs/               ← 生成物（日付別）
├── reports/               ← レビューレポート
├── scripts/               ← 自動化スクリプト（Phase 2以降）
├── config/                ← 設定
└── templates/             ← カテゴリ別スケルトン
```

## 運用ルール
- 全出力は英語（グローバル市場向け）
- 既存商品と重複しないこと
- 本名は絶対に使用しない
- 生成物は必ず `outputs/{date}/{slug}/` に格納
