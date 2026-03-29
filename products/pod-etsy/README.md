# AsuInk — POD × Etsy 事業ファイル構成

**ストア名**: AsuInk
**ビジネスモデル**: Print-on-Demand × Etsy（在庫ゼロ・完全自動収益）
**目標**: 月$200〜$1,000（6ヶ月後）

---

## ディレクトリ構成

```
products/pod-etsy/
├── README.md                          ← このファイル
│
├── designs/
│   ├── prompts/
│   │   ├── design-prompts-all-50.md  ← 50デザインプロンプト（5ニッチ×10）
│   │   └── seasonal-bonus-50.md      ← 追加50デザイン（季節・高需要ニッチ）
│   ├── images/                        ← 生成済みデザイン画像（要生成）
│   └── printful-ready/                ← Printful用リサイズ済み画像（要生成）
│
├── listings/
│   └── listings-all-150.json         ← 150リスティングのJSONサンプル
│
├── csv-upload/
│   └── etsy-listings-150.csv         ← Etsy一括参照用CSV（150件）✓生成済み
│
├── mockup-specs/
│   └── printful-product-specs.md     ← 商品バリエーション・モックアップ仕様書
│
├── setup/
│   └── launch-checklist.md           ← 開設〜初出品の完全手順書（初心者向け）
│
├── marketing/
│   └── social-media-templates.md     ← Pinterest/X投稿テンプレート
│
└── scripts/
    ├── generate_listings_csv.py       ← 150件CSV生成スクリプト ✓動作確認済み
    ├── generate_designs.py            ← Ideogram/DALL-E API自動生成スクリプト
    └── resize_for_printful.py         ← Printful用画像リサイズスクリプト
```

---

## 商品構成

| ニッチ | デザイン数 | 商品タイプ | リスティング数 |
|--------|-----------|-----------|--------------|
| Japanese Zen Minimalist | 10 | T/マグ/ポスター | 30 |
| South America Vibes | 10 | T/マグ/ポスター | 30 |
| Bilingual JP-ES | 10 | T/マグ/ポスター | 30 |
| Digital Nomad | 10 | T/マグ/ポスター | 30 |
| Quotes & Philosophy | 10 | T/マグ/ポスター | 30 |
| **合計** | **50** | | **150** |

### 追加50デザイン（高需要ニッチ）
| ニッチ | デザイン数 | 出品優先度 |
|--------|-----------|-----------|
| 母の日ギフト | 10 | ★★★ 最優先（5月前） |
| 猫好き×日本禅 | 10 | ★★★ 最優先（常時需要） |
| 父の日ギフト | 10 | ★★ 高優先（6月前） |
| ミニマリスト名言 | 10 | ★★ 高優先（常時需要） |
| 夏・ビーチ | 10 | ★ 普通（夏前） |

---

## 実行手順

### Step 1: CSV確認・再生成
```bash
cd products/pod-etsy/scripts
python generate_listings_csv.py
# → csv-upload/etsy-listings-150.csv が生成される
```

### Step 2: デザイン画像生成（要APIキー）
```bash
# Ideogram APIキー取得: https://ideogram.ai/api
export IDEOGRAM_API_KEY=your_key_here

# ドライラン（確認のみ）
python generate_designs.py --dry-run

# 本番生成（全50デザイン）
python generate_designs.py
```

### Step 3: Printful用リサイズ
```bash
# 要: pip install Pillow
python resize_for_printful.py
# → designs/printful-ready/ にリサイズ済み画像が出力される
```

### Step 4: Etsy × Printful 連携
詳細は `setup/launch-checklist.md` を参照。

---

## ブロッカーと対策

| ブロッカー | 対策 |
|-----------|------|
| Etsyアカウント未開設 | `setup/launch-checklist.md` に手順あり |
| Printfulアカウント未開設 | 同上（無料、5分で開設可能） |
| デザイン画像未生成 | Ideogram無料プランで月25枚生成可 → 有料($8/月)で100枚 |
| 画像生成費用 | Canva無料版でも50デザイン作成可能 |

---

## 収益シミュレーション

| 月の売上件数 | 純利益（T$5.42/マグ$8.50/ポスター$7.00） |
|------------|----------------------------------------|
| 月10件 | ~$55 |
| 月30件 | ~$165 |
| 月100件 | ~$550 |
| 月300件 | ~$1,650 |

初期費用: $30（150件 × $0.20出品料）のみ。
