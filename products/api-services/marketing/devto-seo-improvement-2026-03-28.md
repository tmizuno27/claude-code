# Dev.to SEO改善案 2026-03-28

## 現状分析

### パフォーマンスデータ（2026-03-26時点）
| 記事ID | タイトル | Views | 問題点 |
|--------|---------|-------|--------|
| 3388759 | 20+ Free APIs for Developers in 2026 -- No Auth... | 10 | タイトルが漠然すぎる |
| 3388761 | Build an IP Geolocation + VPN Detector in 5 Minutes | 22 | 比較的良好 |
| 3388762 | Automate SEO Audits for Free -- Build Your Own Ahrefs Alternative | 4 | "Ahrefs Alternative"は検索需要なし |
| 3397562 | Build a Trending Topics Dashboard in 10 Minutes | 22 | 比較的良好 |
| 3397563 | Stop Adding Internal Links Manually -- This Free API... | 4 | 否定形タイトルはCTR低い |
| 3397564 | Free WHOIS and DNS Lookup API -- No Scraping... | 0 | 検索需要の薄いキーワード |
| 3401777 | Validate Emails for Free -- Catch Disposable & Fake... | 6 | "for Free"の位置が弱い |
| 3401779 | Free Screenshot API -- Capture Any Webpage as PNG... | 37 | 最良パフォーマンス（参考にすべき） |

### 高パフォーマンス記事の共通点（Views 22-37）
- **具体的な時間**: "in 5 Minutes", "in 10 Minutes"
- **具体的な出力**: "PNG", "JSON Response in 50ms"
- **技術的な問題解決**: "without Scraping", "No Puppeteer Setup"
- **数字で始まる/数字を含む**: 読者が価値を即判断できる

### 低パフォーマンス記事の共通点（Views 0-6）
- 否定形: "Stop Adding...", "No Rate Limits"
- 漠然とした比較: "Ahrefs Alternative"（知名度の低い読者には響かない）
- 需要の薄いニッチキーワード: "WHOIS DNS Lookup"

---

## Dev.toアルゴリズム特性（2026年版）

1. **タグが最重要**: `#webdev`, `#javascript`, `#tutorial`, `#beginners` が最大リーチ
2. **公開後48時間が勝負**: この期間のエンゲージメントで露出量が決まる
3. **タイトルのCTR**: "How to", "Build X in N Minutes", "Free X for Y" 形式が高CTR
4. **本文冒頭のhook**: 最初の200文字でスクロールを止める必要あり

---

## 改善案：タイトル・タグ・description

### 記事1: 20+ Free APIs（ID: 3388759）

**現タイトル**: `20+ Free APIs for Developers in 2026 -- No Auth, No Credit Card, Instant Access`

**改善タイトル（3案）**:
```
A: I Built 24 Free APIs You Can Use Today — No Auth, No Credit Card Required
B: 24 Free APIs Every JavaScript Developer Should Know in 2026
C: Build Faster: 24 Production-Ready Free APIs with JavaScript Examples
```
**推奨**: **A案** — "I Built" は個人的な実績感でエンゲージメント高。Dev.toのコミュニティ文化に合う。

**改善タグ**:
```
#webdev, #javascript, #api, #beginners
```
（`#tutorial` → `#beginners` に変更。Viewsが最も多いタグ）

**改善description**:
```
24 free APIs running on Cloudflare Workers — QR codes, screenshot capture, email validation, SEO audits, IP geolocation and more. All endpoints return JSON. No API key required for the free tier.
```

---

### 記事2: IP Geolocation（ID: 3388761）— 維持＋微調整

**現タイトル**: `Build an IP Geolocation + VPN Detector in 5 Minutes -- Free API, No ipinfo.io Needed`

**改善タイトル**:
```
A: How to Build an IP Geolocation App in 5 Minutes (Free API — No ipinfo.io Account Needed)
B: Detect VPN Users and Geolocate IPs for Free — Build It in 5 Minutes with One API Call
```
**推奨**: **B案** — "Detect VPN Users" は実務的なユースケースで需要が高い

**改善タグ**:
```
#javascript, #webdev, #tutorial, #api
```

---

### 記事3: SEO Audits（ID: 3388762）— 大幅改善必要

**現タイトル**: `Automate SEO Audits for Free -- Build Your Own Ahrefs Alternative with One API`

**問題**: "Ahrefs Alternative" は知らない読者に刺さらない。"SEO Audits" は抽象的。

**改善タイトル（3案）**:
```
A: Add SEO Scoring to Your CI/CD Pipeline in 5 Minutes — Free API with 19 Checks
B: How I Built an Automated SEO Checker with 19 Rules Using a Free API
C: Check Any URL's SEO Score with One API Call — Free, JSON, No Ahrefs Needed
```
**推奨**: **A案** — "CI/CD Pipeline" は開発者に刺さるキーワード。具体的数字（19 checks）が信頼感を高める。

**改善タグ**:
```
#devops, #javascript, #seo, #api
```
（`#seo` は開発者文脈では弱い。`#devops` 追加で開発者層にリーチ）

---

### 記事4: Trending Topics（ID: 3397562）— 維持

**現タイトル**: `Build a Trending Topics Dashboard in 10 Minutes -- Google, Reddit, HN and GitHub in One API Call`

→ 良好。タグに `#beginners` 追加のみ推奨。

**改善タグ**:
```
#javascript, #webdev, #tutorial, #beginners
```

---

### 記事5: WordPress Internal Linking（ID: 3397563）— 要改善

**現タイトル**: `Stop Adding Internal Links Manually -- This Free API Automates WordPress SEO Linking`

**問題**: 否定形タイトルはDev.to読者層（主にJSエンジニア）には響かない。WPプラグインの代替として訴求すべき。

**改善タイトル（3案）**:
```
A: Automate WordPress Internal Linking with a Free API — Replace $77/yr Link Whisper Plugin
B: How to Add Smart Internal Links to WordPress Posts Automatically (Free API + Python Script)
C: WordPress SEO Automation: Auto-Suggest Internal Links with a Free REST API
```
**推奨**: **A案** — 具体的な金額比較（$77/yr）は読者の意思決定を加速させる。

**改善タグ**:
```
#wordpress, #python, #api, #tutorial
```

---

### 記事6: WHOIS / DNS（ID: 3397564）— Views 0 → 根本的改善

**現タイトル**: `Free WHOIS and DNS Lookup API -- No Scraping, No Rate Limits, JSON Response in 50ms`

**問題**: "WHOIS" と "DNS Lookup" のDev.to検索需要が低い。ユースケースから訴求すべき。

**改善タイトル（3案）**:
```
A: Check If a Domain Is Available Before Your User Finishes Typing — Free API in 50ms
B: Build a Domain Availability Checker in 10 Minutes — Free WHOIS API with JSON
C: How to Validate Domain Names and Check Expiry Dates with a Free API
```
**推奨**: **A案** — "before your user finishes typing" = リアルタイム検索という具体的なユースケース。UXエンジニアに刺さる。

**改善タグ**:
```
#javascript, #webdev, #tutorial, #api
```

---

### 記事7: Email Validation（ID: 3401777）

**現タイトル**: `Validate Emails for Free -- Catch Disposable & Fake Addresses with One API Call`

**改善タイトル**:
```
A: Stop Fake Signups: Validate Email Addresses for Free with One API Call
B: How to Block Disposable Email Addresses at Signup — Free API, Zero Dependencies
```
**推奨**: **A案** — "Stop Fake Signups" は認証フォームを持つすべての開発者に刺さる。

**改善タグ**:
```
#javascript, #webdev, #tutorial, #beginners
```
（emailタグ削除 → `#beginners` 追加でリーチ拡大）

---

### 記事8: Screenshot API（ID: 3401779）— 最良。微調整のみ

**現タイトル**: `Free Screenshot API -- Capture Any Webpage as PNG with One HTTP Request (No Puppeteer Setup)`

→ Views 37で最高。このフォーマットを他記事の手本にする。

**改善タグ**:
```
#javascript, #webdev, #tutorial, #beginners
```

---

## 未公開ドラフト（`devto/` フォルダ）の改善案

以下5記事はまだ未公開（`published: false`）。公開前に改善すること。

### QR Code Generator（devto/01-qr-code-generator.md）

**現タイトル**: `Generate Custom QR Codes via API — Free, No Auth, SVG & PNG with Branded Colors`

**改善タイトル**:
```
Generate QR Codes with Custom Colors via API — Free, SVG/PNG, No Auth Required
```
→ "Branded Colors" → "Custom Colors" に変更（より検索されるキーワード）

**改善タグ**:
```
#javascript, #webdev, #tutorial, #beginners
```

### Text Analysis NLP（devto/04-text-analysis-nlp.md）

**現タイトル**: `Free Text Analysis API — Sentiment, Keywords, Readability in One Call (No GPT Costs)`

**改善タイトル**:
```
Analyze Text Without OpenAI: Free Sentiment + Keyword Extraction API (No GPT Costs)
```
**改善タグ**:
```
#javascript, #ai, #webdev, #tutorial
```
（`#nlp` → `#ai` はDev.toで高トラフィック）

---

## 即実行アクションプラン

### Priority 1（今すぐ）: Views 0の記事を修正
1. **記事6（WHOIS/DNS）**: タイトルをA案に変更、タグ更新
2. **記事3（SEO Audits）**: タイトルをA案に変更、タグに`#devops`追加

### Priority 2（本日中）: 全記事タグを統一フォーマットに
- 全8記事のタグに `#tutorial` または `#beginners` のいずれかを必ず含める
- `#email`, `#seo`, `#nlp` 等のニッチタグを削除してリーチを広げる

### Priority 3（今週中）: エンゲージメント戦略
- 公開後48時間以内に他の人気Dev.to記事（同タグ）にコメントして自分のプロフィールを露出
- 各記事の本文冒頭（最初の3行）に「TL;DR」セクションを追加
- 記事末尾に「Related APIs」セクションを追加して相互リンク

### Priority 4（今週中）: 未公開5記事の公開
`devto/` フォルダの5記事を上記改善タイトルで公開（合計13記事体制へ）

---

## Dev.to記事タイトルの黄金公式

Dev.toで高Views（50+）を獲得しているパターン分析：

```
パターン1: [動詞] [具体的なもの] in [N] Minutes — [ベネフィット]
例: Build a Trending Dashboard in 10 Minutes — Google, Reddit, HN in One API

パターン2: How to [問題解決] Without [嫌なもの]
例: How to Validate Emails Without a Database — Free API, One HTTP Request

パターン3: [数字] [具体的なもの] Every [対象読者] Should Know
例: 24 Free APIs Every JavaScript Developer Should Know in 2026

パターン4: Stop [面倒なこと]: [解決策] with [手段]
例: Stop Fake Signups: Validate Email Addresses for Free with One API Call
```

---

## Dev.to API更新スクリプト対応（参考）

記事更新はDev.to APIで一括実行可能：
```python
# PUT https://dev.to/api/articles/{id}
payload = {
    "article": {
        "title": "新タイトル",
        "tags": ["javascript", "webdev", "tutorial", "beginners"],
        "description": "新description"
    }
}
```
`devto_publish_drafts.py` を改修してタイトル・タグの一括更新機能を追加することを推奨。

---

*作成: 2026-03-28 | 次回効果測定: 2026-04-04*
