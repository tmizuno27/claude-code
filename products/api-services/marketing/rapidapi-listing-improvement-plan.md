# RapidAPI リスティング改善計画

**作成日**: 2026-03-25
**目標**: 売上$0 → 初課金獲得（3ヶ月以内）

## 現状分析

- 24本全てRapidAPI出品済み、購読者0、APIコール0
- Dev.to記事8本公開済み（集客チャネルとして機能開始）
- 運用コスト$0（Cloudflare Workers無料枠）

## 問題点

1. **発見性が低い**: RapidAPI内検索で上位表示されていない
2. **説明が不十分**: 各APIのdescriptionが短く、ユースケースが不明確
3. **外部流入がない**: Dev.to以外の集客チャネルがない
4. **差別化が弱い**: 「なぜこのAPIを使うべきか」が伝わっていない

## 改善施策

### A. RapidAPIリスティング最適化（各API共通）

各APIのRapidAPIページで以下を改善:

| 項目 | 現状 | 改善後 |
|------|------|--------|
| Long Description | 1-2行 | 300-500文字、ユースケース3つ以上 |
| API Endpoints | 説明なし | 各エンドポイントにサンプルレスポンス付き |
| Tags/Categories | 最小限 | 関連タグ5つ以上 |
| Pricing Description | デフォルト | 競合比較を明記（「○○の1/10の価格」） |

### B. 各APIの改善ポイント（優先度順）

#### Tier 1（需要が高い、即効性あり）

**01. QR Code API**
- 改善: 「Shopify/WooCommerceの決済QR」「イベントチケットQR」等のユースケース追加
- キーワード: "free qr code api", "qr code generator api no auth"
- 競合優位: Google Charts API QR廃止後の代替

**02. Email Validation API**
- 改善: バウンス率改善の数値事例を追加（「バウンス率を30%→2%に」）
- キーワード: "email validation api free", "disposable email detection api"
- 競合優位: ZeroBounce(100/mo) vs ここ(500/mo)

**04. Screenshot API**
- 改善: OGP画像自動生成、ビジュアルリグレッションテストのユースケース
- キーワード: "website screenshot api free", "webpage capture api"
- 競合優位: Screenshotlayer($10/mo) vs 無料

**06. IP Geolocation API**
- 改善: VPN検出をフロントに出す（差別化要因）
- キーワード: "ip geolocation api free vpn detection"
- 競合優位: ipinfo.io VPN検出$99/mo vs 無料

**10. Currency Exchange API**
- 改善: リアルタイムレート+ヒストリカルデータの両方を強調
- キーワード: "currency exchange rate api free", "forex api"
- 競合優位: exchangerate-api.com(250/mo) vs 500/mo

#### Tier 2（ニッチだが固定需要あり）

**05. Text Analysis API** — NLP/感情分析需要は安定
**09. Hash Encoding API** — セキュリティ開発者向け
**11. AI Text API** — ChatGPT代替APIとして訴求
**14. SEO Analyzer API** — SEOツール開発者向け
**16. WHOIS Domain API** — ドメイン調査ツール需要

#### Tier 3（差別化困難、長期施策）

残りのAPI — 基本説明の充実のみ

### C. 外部集客チャネル拡大

| チャネル | アクション | 期待効果 |
|---------|-----------|---------|
| Dev.to | 記事8本公開済み → 月2本ペースで追加 | 月500-1000 PV → 50-100クリック |
| GitHub README | 各APIリポジトリにRapidAPIリンク追加 | SEO + 直接流入 |
| Stack Overflow | 関連質問に回答+API紹介（スパムNG） | 高CVR流入 |
| Product Hunt | 24 API集合体として1回ランチ | バースト流入 |
| Hacker News | Show HN投稿（1回のみ） | バースト流入 |
| Reddit r/webdev | 月1回、価値提供型投稿 | 中程度の流入 |

### D. 技術的改善

1. **各APIにデモページ追加**: Workers上に簡易HTMLデモを設置
2. **OpenAPI spec整備**: RapidAPIの自動ドキュメント生成を改善
3. **レスポンス速度の計測・公開**: 「平均23ms」等の具体数値で訴求

## 実行スケジュール

| 週 | アクション |
|----|-----------|
| W1 (3/25-31) | Tier1の5 APIのdescription改善、Dev.to記事2本追加（完了） |
| W2 (4/1-7) | Tier2の5 APIのdescription改善、GitHub README整備 |
| W3 (4/8-14) | デモページ作成（Tier1 5本）、Product Hunt準備 |
| W4 (4/15-21) | Product Huntランチ、Show HN投稿 |

## KPI

- 1ヶ月後: 購読者10名、APIコール100回
- 2ヶ月後: 購読者30名、初課金発生
- 3ヶ月後: 月間収益$10-50
