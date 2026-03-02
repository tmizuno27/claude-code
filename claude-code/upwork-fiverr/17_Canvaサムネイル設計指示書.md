# Fiverr Gig サムネイル画像 — Canva設計指示書（詳細版）

---

## 共通仕様

| 項目 | 設定値 |
|------|--------|
| サイズ | 1280 × 769 px（Fiverr推奨） |
| フォーマット | PNG（高品質） or JPG |
| カラースキーム | 紺色 #1a365d / 白 #ffffff / 赤アクセント #c53030 |
| フォント（英語） | Montserrat Bold（タイトル）+ Open Sans（サブテキスト） |
| フォント（日本語要素） | Noto Sans JP |
| 解像度 | 300dpi推奨 |

---

## Gig 1: Market Research（集客用メインGig）

### レイアウト構成

```
┌────────────────────────────────────────────────────┐
│  背景: 東京スカイラインの夜景写真                      │
│  （半透明ダークオーバーレイ: #1a365d, 70%不透明度）     │
│                                                     │
│  ┌─────────────────────────────────────────┐        │
│  │  🇯🇵 アイコン（左上に小さく配置）          │        │
│  │                                          │        │
│  │  JAPANESE                                │        │
│  │  MARKET RESEARCH                         │        │
│  │  ─────────────── （赤い細線）              │        │
│  │  Native Researcher Based in Tokyo        │        │
│  │                                          │        │
│  │  ✓ Industry Analysis                     │        │
│  │  ✓ Competitor Research                   │        │
│  │  ✓ Consumer Insights                     │        │
│  └─────────────────────────────────────────┘        │
│                                                     │
│  ┌──────────┐  右下にサンプルレポートのモックアップ     │
│  │ SAMPLE   │  （斜め15度で配置、影付き）              │
│  │ REPORT   │                                       │
│  │ ページ画像│                                       │
│  └──────────┘                                       │
└────────────────────────────────────────────────────┘
```

### Canva操作手順

1. **Canva.com** → 「デザインを作成」→「カスタムサイズ」→ 1280 × 769 px
2. **背景を設定**:
   - 左メニュー「写真」→ 「Tokyo skyline night」で検索
   - 写真を全体に配置
   - 写真の上に長方形を重ねる（色: #1a365d、透明度: 70%）
3. **テキストを配置**:
   - 「JAPANESE」: Montserrat Bold, 56pt, 白, 左寄せ
   - 「MARKET RESEARCH」: Montserrat Bold, 64pt, 白, 左寄せ
   - 赤い細線: 長方形（幅200px, 高さ3px, 色: #c53030）
   - 「Native Researcher Based in Tokyo」: Open Sans, 22pt, 白, 左寄せ
   - チェックマーク項目: Open Sans, 18pt, 白, 左寄せ（✓は#c53030色）
4. **日本国旗アイコン**:
   - 左メニュー「素材」→「japan flag」で検索
   - 左上に40×30pxで配置
5. **サンプルレポートモックアップ**:
   - 15_サンプルレポートの1ページ目をスクリーンショット
   - 右下に配置、15度回転、ドロップシャドウ追加
   - サイズ: 約200×280px
6. **PNGでダウンロード**

---

## Gig 2: Consumer Insights / Social Listening

### レイアウト構成

```
┌────────────────────────────────────────────────────┐
│  背景: 渋谷スクランブル交差点 or 日本の消費者イメージ   │
│  （半透明ダークオーバーレイ: #1a365d, 75%不透明度）     │
│                                                     │
│  左側テキストエリア（幅60%）                          │
│  ┌─────────────────────────────┐ ┌────────────────┐│
│  │  JAPANESE                    │ │  グラフ/チャート ││
│  │  CONSUMER                    │ │  のモックアップ  ││
│  │  INSIGHTS                    │ │                ││
│  │  ───────────（赤い細線）       │ │  ★★★★☆ 4.1   ││
│  │  Social Listening &          │ │  Sentiment     ││
│  │  Review Analysis             │ │  Analysis      ││
│  │                              │ │                ││
│  │  🇯🇵 Japan-Based Native      │ │  [円グラフ風]   ││
│  │     Researcher               │ │  Pos 68%       ││
│  └─────────────────────────────┘ │  Neg 14%       ││
│                                   └────────────────┘│
└────────────────────────────────────────────────────┘
```

### Canva操作手順

1. **背景**: 「Shibuya crossing」or「Japanese consumers shopping」で検索
2. **テキスト**:
   - 「JAPANESE」: Montserrat Bold, 48pt, 白
   - 「CONSUMER INSIGHTS」: Montserrat Bold, 56pt, 白
   - 赤い細線
   - 「Social Listening & Review Analysis」: Open Sans, 20pt, 白
3. **右側にデータビジュアル**:
   - Canvaの「グラフ」素材を使用
   - 円グラフ: Positive 68% / Neutral 18% / Negative 14%
   - 色: 緑 #48bb78 / グレー #a0aec0 / 赤 #c53030
   - ★★★★☆ の星評価を追加（色: #ecc94b = 金色）
4. **PNGでダウンロード**

---

## Gig 3: Monthly Reports（月額レポート）

### レイアウト構成

```
┌────────────────────────────────────────────────────┐
│  背景: ビジネスグラフ/データダッシュボード風           │
│  （半透明ダークオーバーレイ: #1a365d, 70%不透明度）     │
│                                                     │
│  中央揃えレイアウト                                   │
│                                                     │
│          MONTHLY JAPAN                               │
│          MARKET REPORTS                              │
│          ────────────（赤い細線）                      │
│          Stay Updated on the                         │
│          Japanese Market                             │
│                                                     │
│    ┌──────┐  ┌──────┐  ┌──────┐                     │
│    │ JAN  │  │ FEB  │  │ MAR  │  ← レポート3冊が     │
│    │ 2026 │  │ 2026 │  │ 2026 │    並んでいるイメージ │
│    │      │  │      │  │      │                     │
│    └──────┘  └──────┘  └──────┘                     │
│                                                     │
│    📊 Trends  📈 Data  🇯🇵 Native                    │
└────────────────────────────────────────────────────┘
```

### Canva操作手順

1. **背景**: 「business dashboard」or「data analytics dark」で検索
2. **テキスト**:
   - 「MONTHLY JAPAN」: Montserrat Bold, 52pt, 白, 中央揃え
   - 「MARKET REPORTS」: Montserrat Bold, 60pt, 白, 中央揃え
   - 赤い細線（中央配置）
   - 「Stay Updated on the Japanese Market」: Open Sans, 22pt, 白
3. **レポートモックアップ**:
   - 長方形3つ（白背景、角丸5px）を横に並べる
   - 各長方形の中に「JAN 2026」「FEB 2026」「MAR 2026」
   - テキスト: Montserrat Bold, 14pt, #1a365d
   - 軽い影効果を追加
4. **下部アイコン**:
   - Canvaの素材から📊📈アイコンを検索
   - テキスト付きで3つ横並びに配置
5. **PNGでダウンロード**

---

## デザインチェックリスト（全Gig共通）

```
□ テキストが読みやすい（背景とのコントラスト十分か）
□ スマホの小さい画面でも判読できるか（Fiverrはモバイル閲覧が50%+）
□ 情報を詰め込みすぎていないか（要素は5つ以下に）
□ 色が3色以内に収まっているか（紺・白・赤）
□ プロフェッショナルな印象か（子供っぽくないか）
□ 他のFiverr出品者と差別化できているか
□ 日本関連の要素が含まれているか（国旗、地図、写真等）
□ サンプルレポートの画像が含まれているか（信頼性UP）
□ テキストに誤字脱字がないか（英語ネイティブにチェック推奨）
□ 1280×769pxのサイズで書き出したか
```

---

## 追加: Fiverr プロフィール写真の仕様

| 項目 | 推奨 |
|------|------|
| サイズ | 最低 400×400px（正方形） |
| 背景 | 白 or 無地の明るい色 |
| 服装 | ビジネスカジュアル（清潔感重視） |
| 表情 | 自然な笑顔 |
| 撮影 | スマホのポートレートモードOK |
| 加工 | 明るさ調整のみ。過度なフィルター不可 |
| NG | サングラス、帽子、集合写真、ロゴ、イラスト |

---

## 追加: Fiverr 自己紹介動画の仕様

| 項目 | 推奨 |
|------|------|
| 長さ | 30〜60秒（長くても90秒以内） |
| 解像度 | 720p以上 |
| 言語 | 英語（字幕付き推奨） |
| 背景 | シンプルで清潔（白壁 or 書斎） |
| 照明 | 自然光 or デスクライト（顔が明るく見える） |

### 動画スクリプト（30秒版）

```
Hi, I'm [Your Name], a native Japanese market researcher based in Tokyo.

I help international businesses understand the Japanese market
through in-depth research, competitive analysis, and consumer insights.

With native-level Japanese and real-time access to local data sources,
I provide insights that automated tools simply cannot match.

Whether you're entering the Japanese market or expanding your presence,
I'll deliver a comprehensive, actionable report within 5 business days.

Let's work together. Send me a message to get started.
```

### 動画スクリプト（日本語訳 — 練習用）

```
こんにちは、東京在住の日本市場リサーチャー、[名前]です。

海外企業の皆さまが日本市場を理解できるよう、
詳細なリサーチ、競合分析、消費者インサイトを提供しています。

ネイティブの日本語力とリアルタイムの現地データアクセスにより、
自動化ツールでは得られないインサイトをお届けします。

日本市場への参入や事業拡大をお考えでしたら、
5営業日以内に包括的で実用的なレポートをお届けします。

ぜひメッセージをお送りください。お待ちしております。
```
