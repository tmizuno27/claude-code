# POD デザイン生成・アップロード スクリプト

AsuInk (Printful × Etsy) のデザイン生成パイプライン。

## セットアップ

```bash
cd claude-code/pod-etsy/scripts
pip install -r requirements.txt
```

## 環境変数の設定

```bash
export GEMINI_API_KEY="your-gemini-api-key"
export PRINTFUL_API_KEY="your-printful-api-key"
```

## 実行手順（順番通りに実行）

### Step 1: デザイン生成（Gemini API）

```bash
python generate_designs.py
```

- `../designs/prompts/` の5ファイル（各10プロンプト）から50デザインを生成
- 出力先: `../designs/generated/{niche-name}/`
- 途中で止まっても再実行で続きから再開（生成済みはスキップ）
- 進捗ログ: `../designs/generated/progress.json`

### Step 2: Printful用リサイズ

```bash
python resize_for_printful.py
```

- 生成されたデザインを3つの商品サイズにリサイズ
  - Tシャツ: 4500x5400px (300 DPI)
  - マグカップ11oz: 2700x1050px (150 DPI)
  - ポスター18x24: 5400x7200px (300 DPI)
- 出力先: `../designs/printful-ready/{product-type}/{niche}/`
- アスペクト比を維持し、透明パディングで調整

### Step 3: Printfulアップロード＆商品作成

```bash
python upload_to_printful.py
```

- Printful APIでデザインをアップロード＆商品を自動作成
- Etsy連携済みなら自動でEtsyにリスティングが同期される
- アップロードログ: `../designs/upload-log.json`
- 再実行で未作成分のみ処理（作成済みはスキップ）

## ディレクトリ構成

```
pod-etsy/
├── designs/
│   ├── prompts/           ← プロンプト定義（5ファイル×10プロンプト）
│   ├── generated/         ← Gemini生成画像
│   │   ├── niche-01-japan-zen/
│   │   ├── niche-02-south-america/
│   │   └── ...
│   ├── printful-ready/    ← リサイズ済み画像
│   │   ├── tshirt/
│   │   ├── mug-11oz/
│   │   └── poster-18x24/
│   └── upload-log.json    ← アップロード記録
└── scripts/
    ├── generate_designs.py
    ├── resize_for_printful.py
    ├── upload_to_printful.py
    └── requirements.txt
```
