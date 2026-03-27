# RapidAPI クロスセル・バンドル戦略（2026-03-27）

## 目的

24本のAPIを個別に売るのではなく、**ユースケースベースのバンドル**で提案することで：
1. 客単価を上げる（$5.99 → $14.99-29.99）
2. 1ユーザーあたりの利用API数を増やす（Popularity向上）
3. 競合との差別化（「1 APIで解決」ではなく「ツールキット」として売る）

---

## バンドル提案 — 5パック

### 1. Developer Toolkit Bundle（開発者向け）
**月額 $14.99**（個別合計 $27.94の46%OFF）

| API | 用途 |
|-----|------|
| JSON Formatter | コード検証 |
| Hash & Encoding | セキュリティ・認証 |
| QR Code Generator | テスト用QR |
| Placeholder Image | UI モックアップ |
| Markdown Converter | ドキュメント変換 |

**ターゲット**: 個人開発者、スタートアップエンジニア
**訴求**: 「5つの開発者ユーティリティ、1つのAPI keyで」

---

### 2. SEO & Content Intelligence Bundle（SEO担当者向け）
**月額 $19.99**（個別合計 $31.96の37%OFF）

| API | 用途 |
|-----|------|
| SEO Analyzer | ページ分析 |
| Link Preview | OGメタデータ確認 |
| WHOIS Domain | ドメイン調査 |
| Screenshot | ビジュアル確認 |
| WP Internal Link | 内部リンク最適化 |

**ターゲット**: SEOエージェンシー、コンテンツマーケター
**訴求**: 「Ahrefs + Moz + Screaming Frogの代替。月$19.99で全て」

---

### 3. SaaS Builder Bundle（SaaSプロダクト向け）
**月額 $24.99**（個別合計 $41.94の40%OFF）

| API | 用途 |
|-----|------|
| Email Validation | ユーザー登録バリデーション |
| Screenshot | プレビュー画像生成 |
| QR Code Generator | 決済・共有QR |
| PDF Generator | 請求書・レポート |
| IP Geolocation | ユーザー地域判定 |

**ターゲット**: SaaS開発者、EC運営者
**訴求**: 「SaaS構築に必要な5つのAPIをコスト1/10で」

---

### 4. Data & Intelligence Bundle（データ分析向け）
**月額 $19.99**（個別合計 $35.94の44%OFF）

| API | 用途 |
|-----|------|
| Company Data | 企業情報収集 |
| Email Validation | リード品質チェック |
| WHOIS Domain | ドメイン調査 |
| Currency Exchange | 為替データ |
| Crypto Data | 暗号資産データ |
| Trends | トレンド分析 |

**ターゲット**: データアナリスト、リサーチャー、投資家
**訴求**: 「6つのデータソース、Clearbit+Bloomberg不要」

---

### 5. Content Creator Bundle（コンテンツ制作向け）
**月額 $14.99**（個別合計 $25.95の42%OFF）

| API | 用途 |
|-----|------|
| AI Text | 記事要約・リライト |
| AI Translate | 多言語展開 |
| Text Analysis | 感情分析・キーワード抽出 |
| News Aggregator | トレンド収集 |
| Social Video | 動画メタデータ |

**ターゲット**: ブロガー、YouTuber、マーケター
**訴求**: 「AIコンテンツツールキット。GPT API不要」

---

## クロスセル — API内レスポンスでの相互紹介

### 実装方法

各APIのルートエンドポイント（`/`）のレスポンスに `_related` フィールドを追加：

```json
{
  "name": "SEO Analyzer API",
  "_related": {
    "message": "These APIs work great with SEO Analyzer",
    "apis": [
      {"name": "Screenshot API", "use": "Capture visual snapshots of analyzed pages", "url": "https://rapidapi.com/miccho27-5OJaGGbBiO/api/screenshot-api"},
      {"name": "WHOIS Domain API", "use": "Check domain age & registrar for SEO context", "url": "https://rapidapi.com/miccho27-5OJaGGbBiO/api/whois-domain-api"},
      {"name": "Link Preview API", "use": "Extract OG metadata alongside SEO analysis", "url": "https://rapidapi.com/miccho27-5OJaGGbBiO/api/link-preview-api"}
    ]
  }
}
```

### クロスセルマッピング

| API | 推薦するAPI 3本 |
|-----|----------------|
| SEO Analyzer | Screenshot, WHOIS, Link Preview |
| Email Validation | Company Data, IP Geolocation, Text Analysis |
| QR Code | Screenshot, PDF Generator, Placeholder Image |
| Screenshot | SEO Analyzer, Link Preview, PDF Generator |
| WHOIS Domain | SEO Analyzer, Company Data, IP Geolocation |
| Link Preview | SEO Analyzer, Screenshot, Social Video |
| Text Analysis | AI Text, AI Translate, News Aggregator |
| IP Geolocation | WHOIS, Currency Exchange, Weather |
| URL Shortener | QR Code, Link Preview, Screenshot |
| JSON Formatter | Hash Encoding, Markdown Converter, PDF Generator |
| Hash Encoding | JSON Formatter, Email Validation, IP Geolocation |
| Currency Exchange | Crypto Data, Company Data, IP Geolocation |
| AI Text | AI Translate, Text Analysis, News Aggregator |
| Social Video | Link Preview, Screenshot, Trends |
| Crypto Data | Currency Exchange, Trends, News Aggregator |
| Weather | IP Geolocation, Currency Exchange, Trends |
| News Aggregator | Trends, Social Video, AI Text |
| AI Translate | AI Text, Text Analysis, News Aggregator |
| Trends | News Aggregator, Crypto Data, Social Video |
| Company Data | Email Validation, WHOIS, IP Geolocation |

---

## 実行優先順位

### Phase 1（今週）— 最もインパクトが大きい
1. [x] 上位5本のリスティング最適化（`rapidapi-listing-optimization-2026-03-26.md`完了）
2. [ ] **RapidAPI Studioで上位5本のAPI名・説明文・タグ・プランを手動更新**
3. [ ] Popularity Boosterスクリプトを毎日3回実行（Task Scheduler登録）
4. [ ] 上位5本のクロスセル `_related` フィールドをコードに追加 → デプロイ

### Phase 2（来週）— 残り19本
5. [ ] 残り19本のリスティング最適化をRapidAPI Studioで更新
6. [ ] 残り19本のクロスセル `_related` フィールド追加

### Phase 3（再来週）— 外部プロモーション
7. [ ] Dev.to記事5本公開（上位5本それぞれのチュートリアル）
8. [ ] GitHub READMEにRapidAPIバッジ追加
9. [ ] @prodhq27でAPI活用Tipsツイート（週3回）
10. [ ] RapidAPIのDiscussions / Q&Aに自分で質問＆回答を投稿

### Phase 4（月末）— バンドル販売
11. [ ] バンドル商品ページ作成（RapidAPI上ではバンドル不可なので、LP作成してRapidAPIリンクへ誘導）
12. [ ] バンドルLP → @prodhq27で告知
