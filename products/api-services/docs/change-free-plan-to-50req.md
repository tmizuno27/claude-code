# RapidAPI 無料プラン 500req → 50req 変更手順

## 結論

- **REST API / Platform APIでのプラン変更は不可能**（pricing関連エンドポイントが存在しない）
- **Provider Studio UI（provider.rapidapi.com）での手動変更が必要**
- provider.rapidapi.comは2026-03-28時点でダウン中（HTTP 530）→ **復旧後に以下を実行**

## 重要な注意点

- プラン変更後、**既存のBASIC無料プラン購読者は旧プラン（500req）のまま残る**（"Deprecated Plan"として表示）
- **新規購読者のみ**が50req制限の新プランを見る
- 既存購読者を新プランに移行させるには、旧プランを完全に削除する必要がある（購読者に影響あり）

## 変更手順（24本 × 同じ操作）

### 1本あたりの手順（約1分）

1. **provider.rapidapi.com** にログイン
2. 左メニューから対象APIを選択
3. **Hub Listing** → **Monetize** タブを開く
4. **BASIC** プランの行を見つける
5. **Requests** の項目（現在「500」と表示）をクリック
6. ダイアログが開く:
   - **Period**: `Monthly` を選択
   - **Quota Limit**: `50` に変更
   - **Limit Type**: `Hard Limit` を選択（50req超えたら429エラーで止める）
7. **Save** をクリック
8. 次のAPIへ移動、繰り返し

### 対象API一覧（24本）

| # | API名 | 現在のBASIC | 変更後 |
|---|--------|------------|--------|
| 01 | QR Code Generator | 500 req/mo | 50 req/mo |
| 02 | Email Validation | 500 req/mo | 50 req/mo |
| 03 | Link Preview & Website Metadata | 500 req/mo | 50 req/mo |
| 04 | Website Screenshot | 500 req/mo | 50 req/mo |
| 05 | Text Analysis & NLP | 500 req/mo | 50 req/mo |
| 06 | IP Geolocation | 500 req/mo | 50 req/mo |
| 07 | URL Shortener | 500 req/mo | 50 req/mo |
| 08 | JSON Formatter | 500 req/mo | 50 req/mo |
| 09 | Hash & Encoding | 500 req/mo | 50 req/mo |
| 10 | Currency Exchange Rate | 500 req/mo | 50 req/mo |
| 11 | AI Text Generation | 500 req/mo | 50 req/mo |
| 13 | Crypto Data Aggregator | 500 req/mo | 50 req/mo |
| 14 | SEO Analyzer | 500 req/mo | 50 req/mo |
| 15 | Weather Intelligence | 500 req/mo | 50 req/mo |
| 16 | WHOIS Domain Info | 500 req/mo | 50 req/mo |
| 17 | News Aggregator | 500 req/mo | 50 req/mo |
| 18 | AI Translation | 500 req/mo | 50 req/mo |
| 19 | Trends | 500 req/mo | 50 req/mo |
| 20 | Company Data Enrichment | 500 req/mo | 50 req/mo |
| 21 | WP Internal Link Optimizer | 500 req/mo | 50 req/mo |
| 22 | PDF Generator | 500 req/mo | 50 req/mo |
| 23 | Placeholder Image | 500 req/mo | 50 req/mo |
| 24 | Markdown Converter | 500 req/mo | 50 req/mo |

※ #12 Social Video は非公開化済みのため対象外

### Hard Limit vs Soft Limit

- **Hard Limit（推奨）**: 50req超過で即座に429エラー。有料プランへの移行を強制
- **Soft Limit**: 超過分にoverage fee（超過料金）を課金。設定が複雑

## 自動化の可能性

### Playwright自動化（provider.rapidapi.com復旧後）

provider.rapidapi.comが復旧したら、Playwrightスクリプトで24本を一括変更できる可能性がある。ただしUI構造の確認が必要。

### 現時点で確認済みのAPI

- **REST Platform API**: `POST/PUT /v1/apis/` — API作成・更新のみ。pricing変更エンドポイントなし
- **GraphQL PAPI**: `BillingPlanVersions` クエリで読み取りは可能だが、更新mutationは未公開
- **結論**: プログラムでのプラン変更は現時点で不可能

## 復旧チェック方法

```bash
curl -s -o /dev/null -w "%{http_code}" https://provider.rapidapi.com
```

200が返ったら復旧。530のままならダウン中。
