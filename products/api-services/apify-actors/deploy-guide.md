# Apify Actor デプロイガイド（9 Actor）

## 現状

9個のActorが開発済み。メモリによると6本公開済み、残りデプロイ待ち。

## Actor一覧

| # | Actor | ディレクトリ | 状態 |
|---|-------|-------------|------|
| 1 | Amazon Product Scraper | `amazon-product-scraper/` | 要確認 |
| 2 | Company Data Enricher | `company-data-enricher/` | 要確認 |
| 3 | Email Finder | `email-finder/` | 要確認 |
| 4 | Google Maps Scraper | `google-maps-scraper/` | 要確認 |
| 5 | Keyword Research | `keyword-research/` | 要確認 |
| 6 | SEO Analyzer | `seo-analyzer/` | 要確認 |
| 7 | Social Video Downloader | `social-video-downloader/` | 要確認 |
| 8 | Trends Aggregator | `trends-aggregator/` | 要確認 |
| 9 | Website Tech Detector | `website-tech-detector/` | 要確認 |

## デプロイ手順（各Actor共通）

### 前提
```bash
npm install -g apify-cli
apify login  # APIトークンでログイン
```

### デプロイ
```bash
cd products/api-services/apify-actors/[actor-name]
apify push
```

### 確認
```
https://console.apify.com/actors
```

## 一括デプロイスクリプト

```bash
#!/bin/bash
ACTORS_DIR="C:/Users/tmizu/マイドライブ/GitHub/claude-code/products/api-services/apify-actors"

for actor_dir in "$ACTORS_DIR"/*/; do
    actor_name=$(basename "$actor_dir")
    echo "=== Deploying: $actor_name ==="
    cd "$actor_dir"
    if [ -f "package.json" ] || [ -f "requirements.txt" ]; then
        apify push 2>&1
        echo "  Result: $?"
    else
        echo "  SKIP: No package.json or requirements.txt"
    fi
    echo
done
```

## 各Actorの改善ポイント

### 共通
- README.md に具体的なユースケースと出力例を追加
- INPUT_SCHEMA.json にデフォルト値を設定（初回実行のハードルを下げる）
- SEOキーワードをtitleとdescriptionに含める

### 個別
1. **Amazon Product Scraper** — 「free amazon scraper」「product data extraction」をタイトルに
2. **Company Data Enricher** — 「lead enrichment」「B2B data」をキーワードに
3. **Email Finder** — 「find email from domain」「hunter.io alternative」で差別化
4. **Google Maps Scraper** — 最も需要が高い。「google maps data」「local business scraper」
5. **Keyword Research** — 「free keyword tool」「SEO keyword analysis」
6. **SEO Analyzer** — 「free SEO audit」「website analyzer」
7. **Social Video Downloader** — 「download tiktok」「instagram video」需要大
8. **Trends Aggregator** — 「google trends api」「trend monitoring」
9. **Website Tech Detector** — 「technology stack checker」「wappalyzer alternative」

## 手動アクション

1. `apify login` でトークン認証
2. 上記一括デプロイスクリプトを実行
3. Apifyコンソールで各Actorの公開設定を確認
4. READMEを改善後、再度 `apify push`
