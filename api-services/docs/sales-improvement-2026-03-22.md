# RapidAPI 販促改善レポート（2026-03-22）

## 現状分析

| 指標 | 値 |
|------|-----|
| 総API数 | 24本（全出品済み） |
| 月間売上 | $9.99（IP Geolocation 1件のみ） |
| サブスクライバー | 1名 |
| API呼び出し数 | 0回（全24本） |
| 稼働状態 | 20/20 OK（#21-24はヘルスチェック未対応） |

## 問題の本質

1. **RapidAPI内の検索露出がゼロに近い** -- 新規出品はランキング最下位、サブスク0/レビュー0で圏外
2. **外部流入導線がない** -- ブログ/Dev.to/SNSからのリンクなし、RapidAPI内検索のみに依存
3. **競合が圧倒的に多い** -- 汎用ユーティリティ系は数百の競合あり

## 本日実施した改善

### 1. 上位5 API の README.md 大幅強化

| API | 改善前 | 改善後 | 追加した要素 |
|-----|--------|--------|-------------|
| #06 IP Geolocation | 159行 | 193行 | 競合比較表、FAQ 5問、Getting Started |
| #14 SEO Analyzer | 167行 | 203行 | 競合比較表、FAQ 5問、Getting Started |
| #11 AI Text | 59行 | 175行 | 全5エンドポイント完全ドキュメント、競合比較表、FAQ 4問、Node.js/Fetch例、Getting Started |
| #01 QR Code | 145行 | 176行 | 競合比較表、FAQ 5問、Getting Started |
| #13 Crypto Data | 58行 | 185行 | 全8エンドポイント完全ドキュメント、競合比較表、FAQ 4問、3言語コード例、Getting Started |

**共通追加要素:**
- 「Getting Started in 30 Seconds」セクション（即時コンバージョン誘導）
- 「How It Compares」競合比較表（ipinfo.io/$99 vs 当API/$5.99 等の価格差を明示）
- FAQ（よくある質問への事前回答で離脱防止）
- キーワード追加（"alternative" 系キーワード強化）

### 2. Dev.to記事ドラフト作成（外部流入創出）

| 記事 | ファイル | ターゲットKW |
|------|---------|-------------|
| IP Geolocation紹介 | `marketing/dev-to-articles/01-ip-geolocation-article.md` | "free ip geolocation api", "ipinfo alternative" |
| SEO Analyzer紹介 | `marketing/dev-to-articles/02-seo-analyzer-article.md` | "free seo api", "ahrefs alternative api" |

記事は実用的なコード例（Express.jsミドルウェア、CI/CDパイプライン等）を含み、Dev.toの開発者コミュニティに刺さる構成。

### 3. 発見したバグ

- **API #09 Hash Encoding `/hash` 404問題**: ヘルスチェックがGETで `/hash` を叩いているが、`/hash` はPOSTのみ受付。バグはAPIではなくヘルスチェックスクリプト側。修正推奨。

## 残りの高優先アクション

### 即実行（今日-明日）

| アクション | 効果 | 所要時間 |
|-----------|------|---------|
| Dev.to記事2本を投稿 | 外部流入の創出、被リンク獲得 | 30分 |
| RapidAPI Studio でタイトル更新（5本） | 検索CTR向上 | 15分 |
| ヘルスチェック #09 バグ修正 | 誤アラート解消 | 10分 |
| ヘルスチェック対象を #21-24 に拡張 | 監視カバレッジ100% | 15分 |

### RapidAPI Studio で更新すべきタイトル案

```
#06: IP Geolocation & VPN Detection API - Free 500/mo
#14: SEO Score & Site Audit API - 19 Checks, Free Alternative to Ahrefs
#11: AI Text Generator API - Llama 3.1 Powered, No Per-Token Billing
#01: QR Code Generator API - PNG/SVG/Base64, Custom Colors, Free
#13: Crypto Market Data API - 10,000+ Coins, Real-Time, Free Tier
```

### 中期施策（今週中）

| アクション | 効果 |
|-----------|------|
| @prodhq27 X投稿にAPI紹介を追加（週2-3回） | SNS流入 |
| Hashnode/Medium にも記事クロスポスト | 流入チャネル多角化 |
| 自プロジェクト（wp-linker等）で自APIを使いレビュー投稿 | ランキング改善 |
| stats収集をRapidAPI Provider APIに切り替え | 実データでPDCA |

### 長期施策（月内）

| アクション | 効果 |
|-----------|------|
| 残り19 APIにも同様のREADME強化を展開 | 全体の底上げ |
| 無料枠を競合より大幅に多く設定（例: 1000/mo） | 差別化 |
| Product Hunt への掲出（IP Geolocation） | 大量露出 |

## 収益予測

| シナリオ | 月間売上 | 前提 |
|---------|---------|------|
| 現状維持 | $9.99 | IP Geolocation 1件 |
| Dev.to記事効果 | $20-$50 | 2-5件の新規サブスク |
| タイトル最適化+SNS | $50-$100 | 5-10件の新規サブスク |
| 全施策実行（3ヶ月後） | $100-$300 | 10-30件のサブスク |

## 変更ファイル一覧

```
api-services/01-qr-code-api/README.md          (強化)
api-services/06-ip-geolocation-api/README.md    (強化)
api-services/11-ai-text-api/README.md           (全面書き換え)
api-services/13-crypto-data-api/README.md       (全面書き換え)
api-services/14-seo-analyzer-api/README.md      (強化)
api-services/marketing/dev-to-articles/01-ip-geolocation-article.md (新規)
api-services/marketing/dev-to-articles/02-seo-analyzer-article.md   (新規)
api-services/docs/sales-improvement-2026-03-22.md (本レポート)
```
