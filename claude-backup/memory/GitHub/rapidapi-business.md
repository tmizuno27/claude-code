---
name: RapidAPI API販売事業
description: Cloudflare Workers上の21個のAPIをRapidAPIマーケットプレイスで販売する完全自動化ビジネス（全出品済み）
type: project
---

## RapidAPI API-as-a-Service事業

- **ステータス**: 全21 API デプロイ済み・Rapid Studio登録完了（2026-03-20確認）
- **決定経緯**: Gumroad Stripe KYC問題でn8nテンプレート事業が停止 → 5並行リサーチで完全自動モデルを再調査 → RapidAPI選定
- **プロジェクトパス**: `claude-code/products/api-services/`

### インフラ
- **ホスティング**: Cloudflare Workers（無料枠: 100K req/day）
- **アカウント**: Account ID e8428af2b09ec5b43623b6329fbac91c, subdomain t-mizuno27.workers.dev
- **販売**: RapidAPI Hub（25%手数料、PayPal payout接続済み）
- **運用コスト**: $0

### 24 APIs（全デプロイ・全出品済み）
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
22. PDF Generator API ★（2026-03-20追加）
23. Placeholder Image API ★（2026-03-20追加）
24. Markdown Converter API ★（2026-03-20追加）

### プライシング
- API 1-21: BASIC: $0/100req, PRO: $9.99/10K, ULTRA: $24.99/50K, MEGA: $49.99/500K
- API 22-24: BASIC: $0/100-500req, PRO: $5.99, ULTRA: $14.99, MEGA: $49.99
- **pricing設定完了（2026-03-24）**: 02 Email Validation, 03 Link Preview, 06 IP Geolocation, 08 JSON Formatterの4本
- **12-Social Video API**: 非公開化（2026-03-24）— 著作権リスク回避
- **収益目標**: $30-50/mo（現実的修正、2026-03-24）

### リスティング最適化（2026-03-27）
- Top 5 APIのShort Description/Category/Tags/Long Descriptionをユーザーが手動更新済み
- コピペガイド作成済み: `products/api-services/docs/rapidapi-copypaste-guide.txt`

**Why:** KYC不要、PayPal受取、マーケットプレイスが集客・課金・サポート全処理、運用コスト$0
**How to apply:** n8nテンプレート事業と並行。売上モニタリングのみ必要
