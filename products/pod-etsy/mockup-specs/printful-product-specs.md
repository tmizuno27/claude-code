# AsuInk Printful 商品バリエーション・モックアップ仕様書

## 推奨商品ラインナップ（Printful）

### 1. Unisex Tシャツ — メイン商品

| 項目 | 詳細 |
|------|------|
| 商品名 | Unisex Staple T-Shirt (Bella+Canvas 3001) |
| 定価 | Printful原価: $12.95 / Etsy出品価: $24.99 |
| 利益率 | ~48% |
| 素材 | 100% combed ringspun cotton |
| サイズ | XS, S, M, L, XL, 2XL, 3XL |
| カラー | White（推奨）, Black, Navy, Heather Grey, Red |
| デザインエリア | 12" × 16"（フロントセンター） |
| 解像度 | 最小300 DPI, 推奨4500 × 5400px |
| ファイル形式 | PNG（透過背景推奨）, PDF |

**モックアップ推奨シーン**:
1. フロント着用（白背景、男性/女性モデル）
2. フラットレイ（折り畳み、清潔感）
3. フロント着用（屋外/ライフスタイル）
4. デザイン拡大クローズアップ

---

### 2. コーヒーマグ — サブ商品

| 項目 | 詳細 |
|------|------|
| 商品名 | White Glossy Mug または Black Glossy Mug |
| 定価 | Printful原価: $7.95 / Etsy出品価: $17.99 |
| 利益率 | ~56% |
| サイズ | 11 fl oz（標準）, 15 fl oz（大） |
| カラー | White, Black |
| デザインエリア | 8.5" × 3.82"（11oz用）|
| 解像度 | 2000 × 900px, 150 DPI以上 |
| ファイル形式 | PNG（透過背景） |

**注意**: マグのデザインは円筒を展開した形（横長）で用意すること。
Tシャツ用縦長デザインをそのまま使用する場合はトリミング・リサイズが必要。

**モックアップ推奨シーン**:
1. コーヒーマグ正面（白背景）
2. 机の上・コーヒーアイテムと一緒
3. 両手で持っているシーン

---

### 3. ポスター / アートプリント

| 項目 | 詳細 |
|------|------|
| 商品名 | Enhanced Matte Paper Poster |
| 定価 | Printful原価: $8〜14（サイズ別）/ Etsy出品価: $19.99 |
| 利益率 | ~40〜60% |
| サイズ展開 | 8×10", 11×14", 16×20", 18×24", 24×36" |
| 素材 | 181 g/m² matte paper |
| 解像度 | 最小150 DPI、推奨300 DPI |
| ファイル形式 | PDF（推奨）, JPG, PNG |

**注意**: ポスターは縦向き（Portrait）が主流。
デザインは縦長比率で作成すること（2:3比率推奨）。

**モックアップ推奨シーン**:
1. 白いフレームに入れた状態（部屋のコーナー）
2. フラットレイ（木目テーブルの上）
3. リビング/寝室インテリアシーン

---

## 無料モックアップ素材リソース

| ツール | 用途 | URL |
|--------|------|-----|
| Printful Mockup Generator | Printful商品直接 | app.printful.com |
| Smartmockups | 高品質モックアップ | smartmockups.com（$9/月） |
| Mockup World | 無料モックアップ | themockupclub.com |
| Canva | 簡単モックアップ作成 | canva.com（無料） |
| Place.it | Tシャツ特化 | placeit.net |

**推奨**: まずPrintfulの内蔵モックアップ生成ツールを使用（無料・高品質）

---

## 商品バリエーション設定（Printful + Etsy連携）

### Tシャツ バリエーション設定
```
Primary Option: Size
Values: XS / S / M / L / XL / 2XL / 3XL

Secondary Option: Color
Values: White / Black / Navy / Heather Grey
(White が売れ筋。最初はWhiteのみでも可)
```

### マグ バリエーション設定
```
Primary Option: Size
Values: 11oz / 15oz

Secondary Option: Color
Values: White / Black
```

### ポスター バリエーション設定
```
Primary Option: Size
Values: 8×10 / 11×14 / 16×20 / 18×24 / 24×36

※ 各サイズで価格を変える（Etsyのバリエーション価格設定）:
8×10: $14.99
11×14: $17.99
16×20: $22.99
18×24: $27.99
24×36: $34.99
```

---

## デザインファイル命名規則

```
products/pod-etsy/designs/images/
├── tshirt/
│   ├── design-1-01-wabisabi-circle_tshirt_4500x5400.png
│   ├── design-1-02-fuji-line-art_tshirt_4500x5400.png
│   └── ...
├── mug/
│   ├── design-1-01-wabisabi-circle_mug_2000x900.png
│   └── ...
└── poster/
    ├── design-1-01-wabisabi-circle_poster_3000x4500.png
    └── ...
```

## サイズ早見表

| 商品 | 幅(px) | 高さ(px) | DPI |
|------|--------|---------|-----|
| Tシャツ（推奨） | 4500 | 5400 | 300 |
| Tシャツ（最小） | 1800 | 2160 | 150 |
| マグ11oz | 2000 | 900 | 150 |
| マグ15oz | 2000 | 1125 | 150 |
| ポスター8×10 | 2400 | 3000 | 300 |
| ポスター11×14 | 3300 | 4200 | 300 |
| ポスター16×20 | 4800 | 6000 | 300 |
| ポスター18×24 | 5400 | 7200 | 300 |
| ポスター24×36 | 7200 | 10800 | 300 |
