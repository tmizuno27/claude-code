# RapidAPI 収益化アクションプラン（2026-03-24）

## 現状の厳しい評価

| 指標 | 値 | 評価 |
|------|-----|------|
| 総API数 | 24本 | 出品は完了 |
| 月間売上 | $0〜$9.99 | 壊滅的 |
| サブスクライバー | 0〜1名 | ほぼゼロ |
| Dev.to 3記事（3/23公開） | リアクション0、コメント0 | 効果なし |
| README改善 | 全24本完了（3/23） | Studio反映が未確認 |

## 根本問題の診断

**Dev.to記事が効果ゼロの理由:**
1. 3本を同じ日に一括投稿 — Dev.toのアルゴリズムは新着順でフィードに流すため、同時投稿は互いのインプレッションを食い合う
2. フォロワー0のアカウントからの投稿 — 初期ブーストがない
3. 投稿時間が不適切な可能性 — Dev.toの主要ユーザーはUS/EU圏、UTC 14:00-18:00が最適
4. タグに `#beginners` がない — Dev.toで最も読まれるタグの一つ

**料金設計の問題:**
- 全24本が「Free 500 req/mo」で統一 — これは**多すぎる**
- 月500回あれば個人開発者のほとんどのユースケースが無料で完結する
- 有料に切り替える動機がない

## 即実行アクション（今日）

### 1. Dev.to記事投稿戦略の修正

**新しい3記事を1日1本ずつ投稿する:**
- 3/25（火）: `03-trends-api-article.md` — Trends API
- 3/26（水）: `04-wp-internal-link-article.md` — WP Internal Link API
- 3/27（木）: `05-whois-domain-article.md` — WHOIS API

**投稿時の最適化:**
- 投稿時間: UTC 14:00〜16:00（US東海岸の朝、EU夕方）
- タグに `#beginners` を必ず含める（Dev.toで最も読まれるタグ）
- カバー画像を設定する（画像付き記事はCTR 2-3倍）
- 投稿後24時間以内にDev.toの他記事にコメントしてプロフィール露出を増やす

### 2. 料金設計の見直し（CRITICAL）

**現在:** 全API統一 Free 500 req/mo
**推奨:** 段階的な無料枠制限

| API群 | 現在のFree | 推奨Free | 理由 |
|--------|-----------|----------|------|
| 高価値（Trends, SEO, WP Link, WHOIS, AI Text） | 500/mo | **100/mo** | 試すには十分だが実運用には足りない |
| 中価値（Screenshot, IP Geo, Email, PDF） | 500/mo | **200/mo** | やや絞る |
| 低価値（QR, JSON, Hash, Placeholder, Markdown） | 500/mo | **500/mo** | そのまま（有料化しても売れない） |

**有料プラン設計（優先5本）:**

```
Basic: $4.99/mo — 5,000 req/mo
Pro:   $9.99/mo — 25,000 req/mo
Ultra: $29.99/mo — 100,000 req/mo
```

### 3. Popularityスコアのブートストラップ

**全24本のAPIを自分で10回ずつ呼ぶ（RapidAPI "Test Endpoint"経由）。**
これだけでリクエスト数が0→240になり、検索順位が最底辺から脱出する可能性がある。

手順:
1. RapidAPI Studioにログイン
2. 各APIの「Test Endpoint」タブを開く
3. 主要エンドポイントを10回ずつ実行
4. 所要時間: 約30分

### 4. RapidAPI Studioでの反映確認

3/21-23で改善したREADME・タイトル・descriptionが**実際にRapidAPI上に反映されているか**確認する。
GitHubのREADMEを更新しただけでは、RapidAPI Studioへのコピペが必要。

`docs/rapidapi-studio-copypaste.md` のテキストが全13本分Studio反映済みか要確認。

## 今週中アクション

### 5. GitHubにサンプルプロジェクトを公開

リポジトリ: `miccho27/free-api-examples`
- 優先5本のAPIのサンプルコード（Python + Node.js）
- 各サンプルからRapidAPIへのリンク
- GitHubのStar/Forkが被リンク効果を生む

### 6. 損切り候補の明確化

**3ヶ月後（6月末）の判断基準:**
- サブスクライバー0のAPIは非公開化
- 維持するのは需要のある5-8本のみ
- 24本全部を推し続けるのは散漫で非効率

## 中期アクション（4月）

### 7. StackOverflow回答でのAPI言及

「how to get trending topics api」「free seo audit api」等の質問に対し、自然な文脈で自APIを紹介。
StackOverflowからの被リンクはRapidAPI内SEOにも寄与。

### 8. Product Huntへの投稿

「24 Free APIs」をProduct Huntに投稿。一度のバイラルで数十〜数百のサブスクライバーを獲得できる可能性。

## 収益目標

| 期間 | 目標 | KPI |
|------|------|-----|
| 4月末 | $50/mo | サブスク10名 |
| 6月末 | $200/mo | サブスク30名 |
| 9月末 | $500/mo | サブスク50名（or 損切り判断） |

**$200/moを6月末までに達成できなければ、RapidAPI事業は維持コスト$0とはいえ時間の無駄。他の事業にリソースを振る判断をすべき。**
