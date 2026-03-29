# Product Hunt Launch 準備計画

作成日: 2026-03-29

---

## Launch対象の選定

### 評価基準

| 製品 | PH適性 | 差別化 | Launch準備度 | 推奨度 |
|------|--------|--------|------------|--------|
| keisan-tools | ★★★★☆ | 463ツールの規模感 | 70% | **第1候補** |
| WP Linker | ★★★★★ | WordPress内部リンク自動化はニッチ | 60% | **第2候補** |
| pSEO AIツール比較 | ★★★☆☆ | 5,000ページのpSEO規模 | 50% | 第3候補 |

**推奨: WP Linkerを第1候補とする**

理由:
1. "WordPress + AI + Internal Linking"という明確な問題解決
2. PHで「WordPress tools」カテゴリは反応が良い
3. フリープランあり → 即試用可能（PH評価に直結）
4. Stripe KYCブロック中だが無料プランでのLaunchは可能

---

## WP Linker Product Hunt Launch

### ティーザー文（Twitter/X投稿用）

```
🚀 Something I've been building for WordPress site owners...

Every internal link manually added = time wasted.
I automated the entire process.

WP Linker finds related articles on your WordPress site
and adds internal links automatically — using AI.

Launching on Product Hunt soon. Would you hunt it? 👇
```

```
I manage 3 WordPress blogs with 400+ articles.

Adding internal links manually? I was spending 2 hours/week.

Built a tool to do it automatically → found 741 link opportunities in one run.

Launching on @ProductHunt next week.
Follow @WPLinker to get notified 🔔
```

### Product Hunt ページ説明文（メイン）

```
WP Linker — Automatic Internal Linking for WordPress

Tagline: AI-powered internal links that boost your SEO on autopilot

---

👋 Hey hunters!

I'm Tatsuya, a WordPress blogger managing 3 sites with 400+ articles from Paraguay.

THE PROBLEM
Internal linking is crucial for SEO. But with hundreds of articles, manually finding and adding relevant links is a nightmare. Most bloggers either skip it or spend hours doing it.

THE SOLUTION
WP Linker connects to your WordPress site via REST API, scans all your articles, and uses AI to:
1. Find relevant link opportunities between posts
2. Suggest anchor text that reads naturally
3. Add the links automatically (or show you a preview first)

WHAT MAKES IT DIFFERENT
✅ Works with any WordPress site (no plugin install needed)
✅ Reads your actual content, not just titles
✅ Anchor text is AI-generated to match surrounding context
✅ Dashboard shows all your links with one-click management
✅ Free plan: up to 50 articles

I built this because I needed it. After running it on my own sites, I found 741 internal link opportunities in a single session — links that had been missing for months.

FREE PLAN available — no credit card required.

Would love your feedback! 🙏
```

### First Comment（Maker Comment）

```
Hey PH community! 👋

I'm the solo maker behind WP Linker. A few things I'd love feedback on:

**What's working:**
- The link preview feature (approve before publishing) — users seem to love the control
- Bulk analysis of entire sites at once

**What I'm still figuring out:**
- The right pricing for small bloggers vs. agencies
- Whether to add a WordPress plugin for easier auth

**Free plan details:**
- Up to 50 articles analyzed
- 20 link suggestions per run
- No expiration

Ask me anything! I reply to every comment. 🙌
```

### Gallery（スクリーンショット）の準備リスト

1. ダッシュボードのトップ画面（サイト追加→記事スキャン→リンク候補表示）
2. リンク候補の詳細画面（記事タイトル、アンカーテキスト、コンテキスト表示）
3. 承認フロー（Accept/Reject UIのスクリーンショット）
4. 結果サマリー（"741 links found"の実際の画面）
5. モバイル表示

### 動画（任意・あれば強力）

- 30秒のデモ動画: サイト追加→スキャン→リンク追加の流れ
- ツール: Loom（無料）で録画

---

## keisan-tools Product Hunt Launch（控え）

### ティーザー文

```
I built 463 calculation tools in one year.

Not manually — using AI + code generation + static site templates.

Each tool: tax calculators, unit converters, financial planners...
All free. All Japanese and English.

The site: keisan-tools.vercel.app
Coming to Product Hunt as "Japan's Largest Free Calculator Suite"
```

### Tagline候補

```
Option A: "463 free calculators for everyday Japanese needs — now in English"
Option B: "The calculator for everything — tax, units, finance, health. 463 tools."
Option C: "I built 463 free calculators. Here's the collection."
```

---

## Launch実行チェックリスト（WP Linker）

### Launch 1週間前
- [ ] Product Hunt プロフィール作成・完成（アバター、bio、SNSリンク）
- [ ] Hunter確保（フォロワー多いPHユーザーに依頼、または自己Hunt）
- [ ] ランディングページ最終確認（PH流入用UTMリンク設定）
- [ ] スクリーンショット5枚準備・最適化（1270x952px推奨）
- [ ] 説明文の最終編集
- [ ] X/Twitterでティーザー投稿（2回）

### Launch前日
- [ ] Product Huntへの製品登録（Draft状態で準備）
- [ ] Maker Commentの下書き完成
- [ ] 応援してくれる人リスト作成（知人・フォロワー）
- [ ] Launch告知メール/ツイート準備

### Launch当日（PST 00:01 = JST 17:01）
- [ ] 公開ボタンを押す
- [ ] Maker Commentを即投稿
- [ ] X投稿: "We're live on @ProductHunt!"
- [ ] Reddit、Hacker News、Indie Hackers にも告知
- [ ] 全コメントに返信（最初の3時間が最重要）
- [ ] 進捗モニタリング（1時間ごと）

### Launch翌日
- [ ] お礼ツイート（順位と学びを共有）
- [ ] フィードバックの整理とロードマップ反映
- [ ] Stripe KYCが解決していれば有料プランの案内

---

## 期待値

| 指標 | 現実的な予測 | 良い場合 |
|------|-----------|--------|
| 投票数 | 50-200 | 500+ |
| PH順位 | Top 20 of Day | Top 5 of Day |
| トラフィック | 200-500 UU/day | 1,000+ UU/day |
| 新規登録 | 10-50人 | 100人+ |
| 有料転換 | 0-5人 | 10人+ |

初回Launchの現実: Top 5は難しい。Top 20に入れれば十分。バックリンクとブランディング効果が本当の価値。
