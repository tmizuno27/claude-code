# RapidAPI セラーガイド（API販売の技術リサーチ）

調査日: 2026-03-15

---

## 1. プロバイダーアカウント作成

1. [rapidapi.com](https://rapidapi.com) にサインアップ（GitHub/Google/メール）
2. 右上メニュー → **My APIs** または [rapidapi.com/provider](https://rapidapi.com/provider) でプロバイダーダッシュボードへ
3. **Add API Project** をクリック → 名前・説明・カテゴリ・チームを入力
4. Hub Listing ページにリダイレクト → ロゴ・詳細説明・利用規約等を設定

特別な審査やKYCは**アカウント作成時点では不要**。APIを公開（Public）にするだけでマーケットプレイスに掲載される。

---

## 2. API掲載の自動化（プログラマティック操作）

### REST Platform API（rapidapi.com ユーザー向け）
- **可能な操作**: API作成（OASドキュメントアップロード）、API更新、エンドポイント追加、削除
- **エンドポイント**: `https://platform.rapidapi.com/` 配下
- **認証**: `x-rapidapi-key` + `x-rapidapi-identity-key`（チームコンテキスト用）
- **API作成**: OAS (OpenAPI Specification) ドキュメントをアップロードする方式
- **ドキュメント**: [Managing APIs via the REST Platform API](https://docs.rapidapi.com/docs/creating-updating-apis)

### GraphQL Platform API（Enterprise Hub限定）
- `createApi` / `updateApi` / `updateGraphQLSchema` ミューテーション
- GitHub Actions との連携例あり
- **注意: Enterprise Hub 専用。rapidapi.com の無料ユーザーは利用不可**

### 自動化の結論
| 操作 | REST Platform API | Web UI | 備考 |
|------|:-:|:-:|------|
| API作成 | ○ | ○ | OASファイルが必要 |
| エンドポイント追加/更新 | ○ | ○ | |
| 料金プラン設定 | △ | ○ | REST APIでの対応は限定的 |
| API公開/非公開 | ○ | ○ | |
| モニタリング | ○ | ○ | |

**実用的なワークフロー**: CI/CD（GitHub Actions等）でOASファイルをpush → REST Platform APIでAPI定義を自動更新。料金プラン初期設定はWeb UIで行い、以降はコードで管理。

---

## 3. Stripe Connect について

**重要: RapidAPIは現在Stripe Connectを使っていない。**

- RapidAPIの支払い処理は独自システム + **PayPal**
- Stripe Connect のKYC（本人確認）は無関係
- プロバイダー側でStripeアカウントは不要

---

## 4. 料金プラン設定（Freemium + 有料）

### プランタイプ（3種類）

| タイプ | 説明 |
|--------|------|
| **Monthly Subscription** | 月額固定 + APIコール上限。デフォルト |
| **Pay Per Use** | 従量課金のみ。月額なし |
| **Tiers** | 使用量に応じて単価が自動変動（ボリュームディスカウント） |

### Freemiumモデルの設定
- **BASICプラン**: 月額$0、リクエスト上限あり（例: 100回/月）
- **PROプラン**: 月額$9.99〜、上限1,000回/月
- **ULTRAプラン**: 月額$49.99〜、上限10,000回/月
- **MEGAプラン**: 月額$99.99〜、無制限またはカスタム

### 制限事項
- 無料プランの上限: **1,000リクエスト/時間、500Kリクエスト/月**（システム上限）
- オーバーエイジ料金: 超過分の1リクエストあたりの単価を設定可能
- レートリミット: 秒/分/時間単位で設定可能

### 推奨プラン構成（売れ筋パターン）
```
Basic (Free):  100 req/月, $0
Pro:           1,000 req/月, $9.99/月, 超過 $0.01/req
Ultra:         10,000 req/月, $29.99/月, 超過 $0.005/req
Mega:          50,000 req/月, $99.99/月, 超過 $0.003/req
```

---

## 5. 支払い（Payout）の仕組み

### 手数料
| 項目 | 料率 |
|------|------|
| **RapidAPIマーケットプレイス手数料** | **25%**（固定） |
| PayPal手数料 | 約2%（上限$20） |
| **プロバイダー手取り** | **約73〜75%** |

**計算例**: $100の売上 → RapidAPI $25 → PayPal $1.50 → 手取り **$73.50**

### 支払いスケジュール
- **Net-60方式**: ある月の売上は、翌々月の第1週に支払い
- 例: 7月分 → 9月第1週にPayPalへ送金
- **最低支払い額**: 明記なし（少額でも支払われる模様）

### 支払い方法
- **PayPalのみ**（ACH・銀行振込は非対応）
- USD建てで送金

---

## 6. パラグアイからの受け取り

### PayPalのパラグアイ対応状況

| 項目 | 状況 |
|------|------|
| PayPalアカウント作成 | **可能** |
| 国際送金の受取 | **可能**（制限あり） |
| ローカル銀行への出金 | **不可**（パラグアイの銀行はPayPal非対応） |
| 国際銀行口座への出金 | **可能** |

### 実用的な受け取り方法

1. **Wise（旧TransferWise）経由**
   - PayPal → Wise USD口座 → パラグアイの銀行口座（PYG）
   - 手数料が最も安い

2. **米国法人のPayPalアカウント**
   - doola等でUS LLCを設立 → 米国PayPalアカウント開設
   - 制限なく受け取り可能

3. **Payoneer経由**
   - PayPal → Payoneer → ローカル銀行
   - 為替手数料がやや高い

### 注意点
- パラグアイの「新決済法」により、今後PayPalが正式進出する可能性あり
- 現時点では国際銀行口座（Wise等）を中継するのが最も確実

---

## 7. APIホスティング（バックエンド）

### 推奨インフラ比較

| プラットフォーム | コールドスタート | 無料枠 | 月額目安 | 向いているケース |
|-----------------|:-:|:-:|:-:|------|
| **Cloudflare Workers** | ~0ms（V8 isolate） | 100K req/日 | $5〜 | 軽量API、低レイテンシ |
| **AWS Lambda** | 100-500ms | 1M req/月 | $0〜 | 複雑な処理、AWSエコシステム |
| **Railway** | 常時起動 | $5クレジット/月 | $5〜 | Docker、DB付きAPI |
| **Vercel Functions** | 50-250ms | 100K req/月 | $20〜 | Next.js連携 |
| **Fly.io** | 常時起動 | 3 shared VMs | $0〜 | グローバル分散 |
| **Render** | 常時起動 | 750h/月 | $0〜 | シンプルなWeb API |

### RapidAPIとの接続
- RapidAPI Hub Listing で **Base URL** を設定するだけ
- 例: `https://my-api.workers.dev` や `https://xxx.execute-api.us-east-1.amazonaws.com`
- RapidAPIがプロキシとして動作し、認証・レートリミット・課金を処理

### 推奨構成（コスト最小化）
```
[ユーザー] → [RapidAPI Proxy] → [Cloudflare Workers] → [外部データソース/DB]
```
- Cloudflare Workers: 無料枠10万リクエスト/日で十分
- KV Storage: キャッシュ用（無料枠あり）
- D1 Database: SQLiteベースの軽量DB（無料枠あり）

---

## 8. 自動化可能な全体ワークフロー

```
1. APIコード開発（Python/JS）
   ↓
2. Cloudflare Workers にデプロイ（wrangler deploy）
   ↓
3. OpenAPI Spec (OAS) を自動生成
   ↓
4. REST Platform API で RapidAPI に登録/更新
   ↓
5. Web UI で料金プラン初期設定（初回のみ手動）
   ↓
6. API公開 → マーケットプレイスに掲載
   ↓
7. 売上発生 → RapidAPI が課金処理
   ↓
8. Net-60 で PayPal に USD 送金
   ↓
9. PayPal → Wise → パラグアイ銀行口座
```

### CI/CD自動化（GitHub Actions例）
```yaml
name: Deploy API
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Cloudflare Workers
        run: npx wrangler deploy
      - name: Update RapidAPI listing
        run: |
          curl -X PUT "https://platform.rapidapi.com/api/..." \
            -H "x-rapidapi-key: ${{ secrets.RAPIDAPI_KEY }}" \
            -F "file=@openapi.json"
```

---

## 9. まとめ・判定

| 項目 | 自動化可能性 | 備考 |
|------|:-:|------|
| アカウント作成 | 手動（1回） | サインアップのみ |
| API掲載 | **○ 自動化可** | REST Platform API |
| エンドポイント更新 | **○ 自動化可** | OASアップロード |
| 料金プラン設定 | △ 初回手動 | 以降は変更不要 |
| デプロイ | **○ 自動化可** | CI/CD |
| 課金・集金 | **○ 完全自動** | RapidAPIが処理 |
| PayPal受取 | **○ 自動** | 月次自動送金 |
| パラグアイ受取 | △ | Wise等の中継が必要 |

### 結論
RapidAPIでのAPI販売は**ほぼ完全に自動化可能**。手動が必要なのはアカウント作成と初回料金プラン設定のみ。API開発・デプロイ・掲載更新はCI/CDで自動化でき、課金・集金・送金もプラットフォームが処理する。パラグアイからの受け取りはPayPal + Wise経由で対応可能。

RapidAPIの25%手数料は高めだが、集客・課金・認証・レートリミットを全て代行してくれるため、自前でStripe + API Gateway を構築する手間を考えると妥当。

---

## Sources

- [API Listing Overview - RapidAPI Docs](https://docs.rapidapi.com/docs/api-listing-overview)
- [Adding APIs - Getting Started](https://docs.rapidapi.com/docs/add-api-getting-started)
- [Managing APIs via REST Platform API](https://docs.rapidapi.com/docs/creating-updating-apis)
- [Monetizing Your API](https://docs.rapidapi.com/docs/monetizing-your-api-on-rapidapicom)
- [Subscription Plans & Pricing](https://docs.rapidapi.com/v2.0/docs/api-pricing)
- [Payouts and Finance](https://docs.rapidapi.com/docs/payouts-and-finance)
- [API Provider Payout Schedule](https://support.rapidapi.com/hc/en-us/articles/17777288883988-API-Provider-Payout-Schedule)
- [How are payouts calculated?](https://support.rapidapi.com/hc/en-us/articles/19308532866068-How-are-payouts-calculated)
- [What payment methods are available for payouts?](https://rapidapi.zendesk.com/hc/en-us/articles/11432098898580-What-payment-methods-are-available-for-payouts)
- [REST APIs (GQL PAPI)](https://docs.rapidapi.com/docs/papi-gql-examples-rest-apis)
- [Creating and Updating an API Using GitHub Actions](https://docs.rapidapi.com/docs/example-creating-and-updating-an-api-using-github-actions-gql-platform-api)
- [Hub Listing - Monetize Tab](https://docs.rapidapi.com/docs/hub-listing-monetize-tab)
- [PayPal Paraguay - doola guide](https://www.doola.com/paypal-guide/how-to-open-a-paypal-account-in-paraguay/)
- [Does PayPal Work In Paraguay? - OneSafe](https://www.onesafe.io/blog/does-paypal-work-in-paraguay)
- [Paraguay's New Payment Law - Asuncion Times](https://asunciontimes.com/paraguay-news/economy/paraguays-new-payment-law-opens-door-to-paypal-and-other-payment-providers/)
- [Hosting an API publicly with RapidAPI - Medium](https://medium.com/bewgle/hosting-an-api-publicly-with-rapidapi-2-29709bf4b0ab)
