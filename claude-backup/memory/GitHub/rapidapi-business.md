---
name: RapidAPI API販売事業
description: Cloudflare Workers上の21個のAPIをRapidAPIマーケットプレイスで販売する完全自動化ビジネス（全出品済み）
type: project
---

## RapidAPI API-as-a-Service事業

- **ステータス**: 全21 API デプロイ済み・Rapid Studio登録完了（2026-03-20確認）
- **決定経緯**: Gumroad Stripe KYC問題でn8nテンプレート事業が停止 → 5並行リサーチで完全自動モデルを再調査 → RapidAPI選定
- **プロジェクトパス**: `claude-code/api-services/`

### インフラ
- **ホスティング**: Cloudflare Workers（無料枠: 100K req/day）
- **アカウント**: Account ID e8428af2b09ec5b43623b6329fbac91c, subdomain t-mizuno27.workers.dev
- **販売**: RapidAPI Hub（25%手数料、PayPal payout接続済み）
- **運用コスト**: $0

### 21 APIs（全デプロイ・全出品済み）
1. QR Code Generator API ★RapidAPI出品済
2. Email Validation API ★
3. Link Preview & Website Metadata API ★
4. Website Screenshot API ★
5. Text Analysis & NLP API ★
6. IP Geolocation API ★
7. URL Shortener API（KV使用）★
8. JSON Formatter API ★
9. Hash & Encoding API ★
10. Currency Exchange Rate API ★
11. AI Text Generation API（Workers AI / Llama 3.1）★
12. Social Video Downloader API ★
13. Crypto Data Aggregator API（CoinPaprika）★
14. SEO Analyzer API ★
15. Weather Intelligence API（Open-Meteo）★
16. WHOIS Domain Info API（RDAP）★
17. News Aggregator API（RSS/HN/Dev.to）★
18. AI Translation API（Workers AI / m2m100）★
19. Trends API（Google/Reddit/GitHub）★
20. Company Data Enrichment API（OpenCorporates）★
21. WP Internal Link Optimizer API ★

### プライシング（全API共通）
- BASIC: $0/100req, PRO: $9.99/10K, ULTRA: $24.99/50K, MEGA: $49.99/500K

**Why:** KYC不要、PayPal受取、マーケットプレイスが集客・課金・サポート全処理、運用コスト$0
**How to apply:** n8nテンプレート事業と並行。売上モニタリングのみ必要
