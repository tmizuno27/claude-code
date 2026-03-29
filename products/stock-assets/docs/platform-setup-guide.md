# Stock Asset 出品プラットフォーム セットアップガイド

## プラットフォーム比較

| 項目 | Adobe Stock | Freepik |
|------|------------|---------|
| AI画像 | ✅ 受付（47%がAI生成） | ✅ 受付 |
| ロイヤリティ | 33%（$0.33-0.99/DL） | 変動制 |
| 初回要件 | なし（即アップ可） | 150-200枚一括提出 |
| 最小解像度 | 4MP（2000×2000+） | 2000-10000px |
| ファイル形式 | JPEG/PNG/EPS/AI | JPEG（AI画像） |
| CSV一括アップ | ✅（AIフラグは手動） | ✅ |
| 支払い | PayPal/Skrill | PayPal |

## 推奨戦略

**Phase 1: Adobe Stock**（優先 — 参入障壁低い）
- 初回アップロード制限なし、1枚からでも出品可能
- AI画像の47%がAdobe Stock上に存在 → 市場が成熟
- $0.33-0.99/DL × 大量アップで積み上げ

**Phase 2: Freepik**（150枚溜まったら）
- 初回150-200枚の一括提出が必要（審査あり）
- 量産後に一気に提出

---

## Adobe Stock アカウント開設手順

### Step 1: アカウント作成
1. https://contributor.stock.adobe.com/ にアクセス
2. 「Join now」をクリック
3. Adobe IDを作成（既存IDがあれば「Link my Adobe ID」）
4. **国の選択: Paraguay**（後から変更不可）

### Step 2: メール・電話認証
1. 登録メールに届く確認リンクをクリック
2. 電話番号を入力して SMS認証

### Step 3: プロフィール設定
1. 表示名を設定（例: `AsuInk Designs`）
2. 自己紹介を入力

```
Digital pattern designer specializing in seamless floral and botanical patterns.
High-quality tileable designs for textile, wallpaper, and surface design.
```

### Step 4: 税務情報
1. 左メニュー → Tax Information
2. 以下を選択:
   - US resident: **No**
   - Individual or Business: **Individual**
   - Country of residence: **Paraguay**
3. W-8BEN フォームを提出（非米国居住者用）

### Step 5: 支払い設定
1. PayPalアカウントを接続
2. 最低支払額: $25

### Step 6: 画像アップロード
1. Contributor Portal → Upload
2. JPEG画像をドラッグ＆ドロップ
3. **必ず「Created using generative AI tools」にチェック**
4. **「People and Property are fictional」にチェック**
5. タイトル・キーワードを入力（CSVからコピペ）
6. カテゴリ: Backgrounds/Textures または Abstract
7. Submit

### 重要な注意事項
- プロンプトにアーティスト名・実在人物名を含めない
- 著作権のある作品への言及を避ける
- AI生成のチェックボックスは必ずオンにする（違反 → アカウント停止）

---

## Freepik アカウント開設手順（150枚以上揃ってから）

### Step 1: アカウント作成
1. https://contributor.freepik.com/ にアクセス
2. Google/Facebook/メールでサインアップ
3. 利用規約に同意
4. ユーザー名と国を設定

### Step 2: 初回アップロード（150-200枚）
1. 150-200枚のアセットを一括アップロード
2. 各画像に「AI generated」チェックを入れる
3. 提出ボタンをクリック（149枚以下では押せない）
4. Freepikチームが審査（数日〜数週間）

### Step 3: 承認後
1. 通常のコントリビューターとしてアクセス可能
2. 以降は制限なくアップロード可能

### 技術要件
- JPEG形式
- 2000-10000px（いずれかの辺）
- RGBカラーモード

---

## Shutterstock アカウント開設手順（Phase 3）

### 概要
| 項目 | 詳細 |
|------|------|
| AI画像 | ✅ 受付（2023年〜 AI画像ポリシー適用） |
| ロイヤリティ | 15-40%（累積販売数に応じてスライド制） |
| 初回要件 | なし（1枚から可）、ただし審査あり |
| 最小解像度 | 4MP（1600×2560 以上） |
| ファイル形式 | JPEG（RGB、最大50MB） |
| CSV一括アップ | ✅ Bulk Upload 対応 |
| 支払い | PayPal / Payoneer（最低 $35） |

### Step 1: アカウント作成

1. [submit.shutterstock.com](https://submit.shutterstock.com/) にアクセス
2. 「Join as Contributor」をクリック
3. メールアドレスとパスワードで登録
4. 国: **Paraguay** を選択

### Step 2: 税務情報
1. Dashboard → Tax Info
2. W-8BEN フォームを提出（非米国居住者）
3. パラグアイ在住の場合、源泉徴収税率は適用外

### Step 3: AI画像ポリシーへの同意
1. Dashboard → Terms → AI Content Agreement に同意
2. アップロード時に「AI Generated」フラグを必ずオン

### Step 4: CSV一括アップロード
1. Dashboard → Upload → CSV Upload
2. `output/metadata/shutterstock_metadata.csv` を使用
3. 列: `filename, description, keywords, categories, editorial, mature_content`
4. 画像ファイルと同時にZIPで提出

### 重要な注意事項
- **AI生成必須開示**: 未開示はアカウント停止リスク
- **タイトルに人名・ブランド名禁止**
- **キーワードは関連性のあるものだけ**（水増しは審査落ち原因）
- **初回審査**: 最初の10枚は人間が目視チェック（3-5営業日）

---

## 出品戦略（2026年版）

### Phase 1: Adobe Stock（即開始・914枚）
- **理由**: 参入障壁最低、AI画像受付実績あり
- **目標**: 914枚を3バッチ（300/300/314）に分けて提出
- **CSV**: `output/metadata/adobe_stock_metadata.csv`
- **期間**: 2週間以内に全件提出

### Phase 2: Freepik（150枚準備済み → 即提出可能）
- **理由**: 914枚 > 150枚の閾値をクリア済み
- **CSV**: `output/metadata/freepik_metadata.csv`
- **戦略**: geometric・abstract・botanical など多様なカテゴリで提出
- **期間**: Adobe Stock 提出後に並行開始

### Phase 3: Shutterstock（Phase 1-2 の審査結果次第）
- **理由**: ロイヤリティが高くなる潜在力（Top Contributor で40%）
- **CSV**: `output/metadata/shutterstock_metadata.csv`
- **戦略**: Adobe で通過した画像を優先提出

### Phase 4: 追加画像生成（288新プロンプト）
- ビジネス（66件）・テクノロジー（48件）・ライフスタイル（108件）
- 教育（42件）・サステナビリティ（24件）
- **プロンプトファイル**: `output/metadata/prompts_business.json`
- Recraft/Midjourney/DALL-E で生成後、v2スクリプトでメタデータ生成

### 収益試算
| プラットフォーム | 単価（平均） | 914枚×月50DL | 年間 |
|-----------------|-------------|--------------|------|
| Adobe Stock | $0.50/DL | $457 | $5,484 |
| Freepik | $0.10/DL | $91 | $1,092 |
| Shutterstock | $0.25/DL | $229 | $2,748 |
| **合計** | | **$777/月** | **$9,324** |

※ 月50DLは控えめな試算。人気タグが当たれば数倍も期待できる。

---

## 即実行チェックリスト

- [ ] Adobe Stock アカウント開設（[contributor.stock.adobe.com](https://contributor.stock.adobe.com/)）
- [ ] W-8BEN 提出
- [ ] `adobe_stock_metadata.csv` 準備済み（914行）
- [ ] 画像をJPEG変換（output/upscaled/ の914枚）
- [ ] 最初の50枚をテストアップロード
- [ ] Freepik アカウント開設
- [ ] 150枚一括提出（diverse カテゴリ優先）
- [ ] Shutterstock アカウント開設
- [ ] 新カテゴリ288プロンプトの画像生成（`scripts/generate_business_prompts.py` 実行済み）
