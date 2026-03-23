# RapidAPI 売上$0 原因分析レポート（2026-03-23）

## エグゼクティブサマリー

**結論: 売上$0は当然の結果。24本出品しただけで放置しており、集客施策がゼロ。RapidAPIは「出品すれば売れる」場所ではない。**

24本のAPI全てが購読者0・呼び出し0。問題はAPIの品質ではなく、**発見されていない**こと。RapidAPIには数万のAPIが存在し、出品しただけでは検索結果の海に埋没する。

---

## 根本原因（厳しい現実）

### 1. RapidAPIの集客構造を誤解している
- RapidAPIはAmazonではない。SEOによる自然流入は極めて少ない
- RapidAPIの「Popularity」スコアはリクエスト数とユーザー数で決まる → **0の状態では検索順位も最底辺**
- 新規APIは意図的に外部から流入を作らない限り、永遠に0のまま

### 2. 外部プロモーションが完全にゼロ
- Dev.toに3本draft投稿済みだが**公開していない**
- ブログ記事（チュートリアル・使い方ガイド）が存在しない
- StackOverflow、Reddit、X、HackerNews等での言及がゼロ
- GitHub READMEからのリンクなし

### 3. 差別化要因が弱い
24本全てが「Free ○○ API」という同じフォーマット。競合との違いが不明瞭。

---

## API別 問題点一覧

### 共通問題（全24本に該当）

| 問題 | 深刻度 | 詳細 |
|------|--------|------|
| Popularityスコア最低 | CRITICAL | 呼び出し0→検索順位最下位→発見されない→永遠に0の悪循環 |
| チュートリアルなし | HIGH | RapidAPI公式も「チュートリアル追加で購読率UP」と明言 |
| 外部被リンクゼロ | HIGH | Google検索からの流入も、RapidAPI内での信頼スコアもゼロ |
| レビュー・評価ゼロ | HIGH | 社会的証明がないため信頼されない |
| API Playgroundのサンプルが不明 | MEDIUM | 「Try it」で即座に動くデモが最重要だが確認不可 |

### 個別API問題点

| # | API名 | カテゴリ | 固有の問題 |
|---|--------|----------|-----------|
| 01 | QR Code Generator | Tools | 競合多数（goqr.me等）。差別化：速度だけでは弱い |
| 02 | Email Validation | Data | pricing構造が空（plans:[]）→ 有料プラン未設定の可能性 |
| 03 | Link Preview | Tools | pricing構造が空。Free100/moは少なすぎ |
| 04 | Screenshot | Tools | 競合（urlbox等）と比較してCaptureのクオリティが不明 |
| 05 | Text Analysis | Text Analysis | カテゴリ妥当だが競合（MonkeyLearn等）が強い |
| 06 | IP Geolocation | Tools | pricing構造が空。カテゴリが「Tools」は不適切→「Location」が正しい |
| 07 | URL Shortener | Tools | Free100/moは少ない。Bitly代替を謳うなら機能差明示が必要 |
| 08 | JSON Formatter | Tools | pricing構造が空。そもそもAPI化する意味が薄い（ローカルで十分） |
| 09 | Hash & Encoding | Tools | 需要が極めてニッチ。ローカルライブラリで代替可能 |
| 10 | Currency Exchange | Finance | 競合（exchangerate-api等）が圧倒的。ECBデータだけでは弱い |
| 11 | AI Text | Text | GPT/Claude APIと直接競合。Llama 3.1は差別化にならない |
| 12 | Social Video Download | Video_Images | **法的リスク大**。YouTube/TikTok ToS違反の可能性 |
| 13 | Crypto Data | Finance | CoinGecko/CoinMarketCap APIが無料で使える |
| 14 | SEO Analyzer | Tools | 競合多数だが需要はある。チュートリアルで差別化可能 |
| 15 | Weather | Weather | OpenWeatherMapが圧倒的。勝てる要素がない |
| 16 | WHOIS Domain | Tools | まあまあニッチで需要あり。改善余地あり |
| 17 | News Aggregator | News_Media | RSS scraping。データの鮮度と網羅性が競合に劣る |
| 18 | AI Translate | Translation | DeepL/Google Translate APIと直接競合。M2M100は品質で劣る |
| 19 | Trends | Social | ユニーク性はある（複数ソース集約）。最も差別化しやすい |
| 20 | Company Data | Business | Clearbit/Hunter等が強い。Wikidataベースでは精度不足 |
| 21 | WP Internal Link | Tools | ニッチだが需要あり。WordPress開発者向けに刺さる可能性 |
| 22 | PDF Generator | Tools | 競合多数だがFree tierがあれば需要はある |
| 23 | Placeholder Image | Tools | Lorem Picsum等が既に無料。差別化困難 |
| 24 | Markdown Converter | Tools | 需要極小。ローカルライブラリで十分 |

---

## 改善策（優先度順）

### P0: 即座にやるべきこと（今日〜3日以内）

#### 1. Dev.to記事3本を即座に公開する
既にdraftがある。公開するだけ。各記事にRapidAPIリンクを含める。

#### 2. 「勝てるAPI」5本に集中する
24本全てを均等に推すのは非効率。以下の5本に集中投資：

| 優先 | API | 理由 |
|------|-----|------|
| ★1 | 19-Trends API | 複数ソース集約はユニーク。競合が少ない |
| ★2 | 14-SEO Analyzer | 開発者需要が高い。チュートリアル映えする |
| ★3 | 21-WP Internal Link | ニッチだがWordPress市場は巨大 |
| ★4 | 16-WHOIS Domain | 需要安定。競合が古い |
| ★5 | 01-QR Code Generator | 需要が大きい。チュートリアルが書きやすい |

#### 3. 自分で各APIを10回ずつ呼ぶ（Popularityスコアのブートストラップ）
RapidAPIの「Try it」からテスト実行するだけでリクエストカウントが増える。全24本×10回=240回。Popularityが1→2になるだけでも検索順位が変わる。

### P1: 今週中にやるべきこと

#### 4. 優先5本のチュートリアル記事を書く
各APIについて「How to [use case] with [API name] — Free API Tutorial」形式で：
- Dev.toに投稿（5本）
- nambei-oyaji.comの英語記事として投稿（SEO効果）
- GitHub READMEにサンプルコード＋RapidAPIリンク追加

#### 5. pricing構造が空のAPI（02, 03, 06, 08）を修正
plans:[] のAPIはフリープランすら正しく設定されていない可能性がある。RapidAPI Studioで確認・修正。

#### 6. カテゴリの修正
- 06-IP Geolocation: `Tools` → `Location` or `Data`
- 14-SEO Analyzer: `Tools` → `SEO` or `Website`（もしあれば）
- カテゴリが適切だとカテゴリ別ブラウジングで発見される確率が上がる

### P2: 来週中にやるべきこと

#### 7. 各APIのlong_descriptionに「Alternative To」セクションを強化
既に一部あるが、全24本に競合API名を明記する。RapidAPI内検索で「[競合名] alternative」で引っかかるようにする。

#### 8. Reddit/HackerNews/X での自然な言及
- r/webdev, r/programming, r/SaaS で「こんなFree API見つけた」的な投稿
- ただしRedditは新アカウントでの宣伝が削除されやすい（メモリに記録済み）→ 既存アカウントで自然な文脈で

#### 9. GitHubリポジトリにサンプルプロジェクトを作る
`awesome-free-apis` 的なリポジトリ or 各APIのサンプルコード集。GitHub→RapidAPIへの導線。

### P3: 中期（損切り判断含む）

#### 10. 3ヶ月後に効果測定し、伸びないAPIは非公開にする
24本を維持する意味はない。メンテコストを考えると、購読者が付いた5〜8本に絞り、残りは廃止すべき。

#### 11. 需要が疑わしいAPIの損切り候補
以下は市場に既にFreeの強力な代替があり、差別化が極めて困難：
- 08-JSON Formatter（ローカルツールで十分）
- 09-Hash Encoding（同上）
- 15-Weather（OpenWeatherMapが圧倒的）
- 23-Placeholder Image（Lorem Picsum等）
- 24-Markdown Converter（ローカルライブラリで十分）

---

## Listing改善案（優先5本）

### 19-Trends API（最優先）

**現在のタイトル**: Free Trends API - Google, Reddit, HN, GitHub, Product Hunt Aggregator

**改善案**:
```
タイトル: Multi-Source Trends API - Google, Reddit, GitHub, HN, Product Hunt in One Call
説明: All-in-one trending topics API. Get real-time trends from 5+ sources (Google Trends, Reddit, Hacker News, GitHub, Product Hunt) with a single API call. No scraping needed. 500 req/mo free.
追加タグ: trending-now, social-listening, content-discovery, viral-topics, market-research
```

### 14-SEO Analyzer API

**現在のタイトル**: Free SEO Analyzer API - Meta Tags, Headings, Score, Structured Data Audit

**改善案**:
```
タイトル: SEO Audit API - On-Page Score, Meta Tags, Schema, Lighthouse Alternative
説明: Instant SEO audit for any URL. Get on-page SEO score, meta tag analysis, heading structure, structured data validation, and actionable recommendations. Lighthouse alternative with API access. 100 req/mo free.
追加タグ: seo-score, technical-seo, website-audit, google-ranking, site-analyzer
```

### 21-WP Internal Link API

**現在のタイトル**: Free WordPress SEO API - Internal Link Suggestions, Anchor Text, Scoring

**改善案**:
```
タイトル: WordPress Internal Link API - AI-Powered Link Suggestions for SEO
説明: Boost WordPress SEO with intelligent internal link suggestions. Analyze your content, find link opportunities, get anchor text recommendations with relevance scoring. Perfect for content teams and SEO agencies. 100 req/mo free.
追加タグ: wordpress-plugin, content-strategy, topical-authority, seo-tool, blogging
```

### 16-WHOIS Domain API

**現在のタイトル**: Free WHOIS Domain API - RDAP Lookup, DNS Records, Availability Check

**改善案**:
```
タイトル: WHOIS & DNS API - Domain Lookup, RDAP, Availability Check, SSL Info
説明: Complete domain intelligence API. WHOIS/RDAP lookup, DNS records, domain availability check, SSL certificate info, and nameserver data. Fast RDAP-first approach with WHOIS fallback. 100 req/mo free.
追加タグ: domain-checker, domain-lookup, ssl-certificate, cybersecurity, domain-monitor
```

### 01-QR Code Generator API

**現在のタイトル**: Free QR Code Generator API - PNG, SVG, Base64, Custom Colors | 500/mo free

**改善案**:
```
タイトル: QR Code API - Generate PNG, SVG, Base64 with Custom Colors | Sub-50ms
説明: Ultra-fast QR code generation via Cloudflare edge network (300+ locations). PNG, SVG, and Base64 output. Custom colors, sizes, error correction. No authentication required. Perfect for e-commerce, marketing, and event management. 500 req/mo free.
追加タグ: qr-code-api, qr-generator-api, dynamic-qr, payment-qr, e-commerce-tools
```

---

## 数字で見る厳しい現実

| 指標 | 現状 | 目標（3ヶ月後） |
|------|------|----------------|
| 総購読者 | 0 | 50+（Free含む） |
| 月間リクエスト | 0 | 1,000+ |
| 月間売上 | $0 | $10〜30（最初は少額で十分） |
| Dev.to公開記事 | 0（3本draft） | 10+ |
| 外部被リンク | 0 | 20+ |

**率直に言えば**: RapidAPI事業単体で月$100以上稼ぐのは、現状の24本「出品しただけ」の状態から相当な労力が必要。外部プロモーションに週5時間以上投資する覚悟がなければ、他の事業（ブログ、Gumroad）にリソースを振った方が時間対効果は高い。

---

## 即実行アクションリスト

- [ ] Dev.to draft 3本を今日中に公開
- [ ] RapidAPI「Try it」から全24本×10回テスト実行
- [ ] pricing構造が空の4本（02, 03, 06, 08）をRapidAPI Studioで確認・修正
- [ ] 優先5本のタイトル・説明文を上記改善案で更新
- [ ] 優先5本のカテゴリ・タグを修正
- [ ] 来週までに優先5本のチュートリアル記事をDev.toに投稿

---

*生成日: 2026-03-23 | 忖度なし分析*
