# Dev.to 効果測定レポート 2026-03-25

## 記事一覧（全6本公開済み）

### 既存3本（3/24公開）
| # | タイトル | Views | Reactions | RapidAPI導線 |
|---|---------|-------|-----------|-------------|
| 01 | 20+ Free APIs Every Developer Needs in 2026 | 0 | 0 | 72リンク（全API網羅） |
| 02 | Free IP Geolocation API with VPN Detection | 12 | 0 | 7リンク |
| 03 | Build Automated SEO Audits with a Free API | 4 | 0 | 7リンク |

### 新規3本（3/25公開 — 本日手動公開）
| # | タイトル | URL | RapidAPI導線 |
|---|---------|-----|-------------|
| 04 | Automate WordPress Internal Linking for SEO | https://dev.to/miccho27/automate-wordpress-internal-linking-for-seo-free-api-for-developers-20ad | WP Internal Link API |
| 05 | Free WHOIS & DNS Lookup API | https://dev.to/miccho27/free-whois-dns-lookup-api-build-domain-tools-without-scraping-5h9d | WHOIS Domain API |
| 06 | How to Build a Trending Topics Dashboard | https://dev.to/miccho27/how-to-build-a-trending-topics-dashboard-with-one-api-call-google-reddit-hn-github-product-1a7c | Trends API |

## 効果測定サマリー
- **総Views**: 16（公開24時間以内）
- **総Reactions**: 0
- **RapidAPI導線**: 全6記事にRapidAPIリンクあり、正常動作確認済み

## 問題点と修正
- Task Schedulerによる自動公開が失敗していた
  - **原因**: フロントマター内の`published: false`がAPI経由の公開指示を上書きしていた
  - **修正**: body_markdown内のフロントマターを`published: true`に書き換えてAPI送信 → 公開成功

## 自動公開スクリプトの修正必要
- `devto_publish_drafts.py` はpayloadで`published: True`を送るだけだが、フロントマター内の`published: false`が優先される
- body_markdownのフロントマター書き換えロジックを追加する必要あり

## 次のアクション
- [ ] devto_publish_drafts.pyを修正（フロントマター書き換え対応）
- [ ] 1週間後に効果測定（views/reactions推移）
- [ ] 反応が良い記事のパターンを分析して次回記事に反映
