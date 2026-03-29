# Gumroad 35商品 最適化レポート — 2026-03-28

## エグゼクティブサマリー

- 全35商品、売上$0（2026-03-28現在）
- 根本原因: タグなし15件、未公開1件、説明文薄い14件、n8nテンプレートはStripe KYCブロック中
- 優先対応: **タグ追加**（15件）と**説明文強化**（AIブロガーバンドル等4件）で即日対応可能

---

## 問題分類

### 🚨 CRITICAL

| # | 問題 | 件数 | 影響 |
|---|------|------|------|
| 1 | 未公開（Published=False） | 1件 | 購入不可 |
| 2 | タグなし（検索に出ない） | 15件 | Gumroad内検索・SEOゼロ |
| 3 | n8nテンプレート（Stripe KYCブロック） | 9件 | 購入できても送金不可 |

### ⚠️ HIGH

| # | 問題 | 件数 | 影響 |
|---|------|------|------|
| 4 | 説明文500文字未満（信頼性低） | 4件 | CVR直撃 |
| 5 | 高額商品（$49+）なのに説明文薄い | 7件 | 購入障壁 |

---

## 詳細改善リスト

### [CRITICAL-1] 未公開商品 → 即公開

| 商品名 | 現在価格 | 対応 |
|--------|---------|------|
| AI Business Automation Mega Prompt Pack — 50+ Prompts to Run Your Business on Autopilot | $12.00 | Published=Trueに変更 |

**対応コマンド:**
```
PATCH https://api.gumroad.com/v2/products/FE9NHRPwlEMXYpOhogllJA==
published: true
```

---

### [CRITICAL-2] タグなし15商品 → タグ追加

タグはGumroad内検索とSEOに直結。現在タグなしの商品一覧と推奨タグ:

| 商品名 | 推奨タグ |
|--------|---------|
| AI Business Automation Mega Prompt Pack | ai, automation, prompts, chatgpt, productivity |
| ADHD Daily Planner (Notion Template) | notion, template, adhd, productivity, planner |
| Social Media Marketing Mega Prompt Pack | social media, prompts, ai, marketing, instagram |
| AI Side Hustle Starter Kit | ai, side hustle, notion, template, prompts |
| Airbnb Host Management Hub | notion, template, airbnb, host, property |
| Personal Finance Dashboard | notion, template, finance, budget, money |
| Habit Tracker & Goal System | notion, template, habit, goals, productivity |
| Travel Planner & Journal | notion, template, travel, planner, journal |
| Property Investment Tracker | notion, template, property, investment, real estate |
| Wedding Planning Hub | notion, template, wedding, planner, events |
| Startup Launch Checklist | notion, template, startup, launch, checklist |
| Ultimate AI Blogger Bundle (3 Packs) | ai, blog, seo, prompts, bundle |
| Affiliate Content Generator | affiliate, blog, prompts, ai, content |
| WordPress Automation Prompt Kit | wordpress, automation, prompts, ai, blog |
| SEO Article Writer Mega Prompt Pack | seo, blog, prompts, ai, content writing |

---

### [HIGH-1] 説明文500文字未満の商品 → 説明文強化

#### 1. Ultimate AI Blogger Bundle（$49）— 現在485文字

**問題:** $49のバンドル商品なのに説明文が最も薄い。購入ボタンを押す根拠が少なすぎる。

**改善後説明文（案）:**
```
🔥 3つのAIプロンプトパックを1つにバンドル。130+プロンプトで今すぐブログを自動化。

## What's Included

**Pack 1: SEO Article Writer (50 Prompts)**
- キーワード調査から記事構成、本文執筆まで完全自動化
- Google上位表示に特化したSEOプロンプト
- H1~H3見出し生成、メタディスクリプション作成

**Pack 2: Affiliate Content Generator (50 Prompts)**
- 収益化を目的としたアフィリエイト記事テンプレート
- 比較記事・ランキング記事・口コミ記事を瞬時に生成
- クリック率を上げるCTA文章プロンプト付き

**Pack 3: WordPress Automation Kit (30 Prompts + Code Snippets)**
- WordPressの自動化コードスニペット30本
- 投稿スケジュール・カテゴリ管理・内部リンク自動化
- WP REST API活用プロンプト集

## Who Is This For?
- ブログで収益化を目指している方
- AIを活用してコンテンツ制作を効率化したい方
- WordPressの自動化で時間を節約したい方

## Format
PDF / Notion Doc（全プロンプトコピペ対応）

通常価格 $57 → バンドル価格 $49（66% OFF）
```

#### 2. Affiliate Content Generator（$19）— 現在517文字

**問題:** タイトルだけ見て何が入っているか不明。プロンプトの具体例がない。

**改善ポイント:**
- 50プロンプトの内訳を箇条書きで示す
- 実際のプロンプト例を1~2個掲載する
- 対象読者（アフィリエイトブロガー）を明示する

#### 3. WordPress Automation Prompt Kit（$29）— 現在612文字

**問題:** $29と中価格帯なのにコードスニペットの具体的内容が不明。

**改善ポイント:**
- 30プロンプトの具体的なカテゴリ（投稿自動化/SEO/内部リンク等）を列挙
- 対象: WordPress + AIを組み合わせたい中級ブロガー
- どの問題を解決するか明示（「毎週10時間のコンテンツ作業を2時間に」など）

#### 4. SEO Article Writer Mega Prompt Pack（$19）— 現在768文字

**問題:** 競合が多いカテゴリ。差別化ポイントが不明確。

**改善ポイント:**
- 「Google上位表示を目指したプロンプト」という具体的ベネフィット
- 50プロンプトのカテゴリ別内訳（KW調査/タイトル/本文/FAQ/まとめ等）
- 使用ツール明示（ChatGPT・Claude・Gemini対応）

---

### [HIGH-2] 高額商品の説明文強化（$49~$99）

n8nテンプレートはStripe KYCブロック中だが、KYC解除後に即販売開始できるよう事前に説明文を強化しておく。

| 商品名 | 価格 | 現在文字数 | 最低目標 |
|--------|------|-----------|---------|
| AI Blog Content Pipeline for n8n | $49 | 872c | 1500c |
| Shopify Order Automation for n8n | $59 | 768c | 1500c |
| PDF & Invoice Data Extraction for n8n | $79 | 886c | 1500c |
| Email Classification & Auto-Routing for n8n | $49 | 768c | 1500c |
| CRM Pipeline Automation for n8n | $69 | 810c | 1500c |
| Social Media Content Factory for n8n | $49 | 825c | 1500c |
| AI Customer Support Agent for n8n | $99 | 863c | 2000c |
| QuickBooks & Stripe Invoice Automation for n8n | $69 | 892c | 1500c |

**強化テンプレート（n8n商品共通）:**
```
## What This Workflow Does
[具体的なワークフロー説明 — 3~5ステップで図示]

## The Problem It Solves
Before: [手動でやると何時間かかるか]
After: [このワークフローを使うと何分で完了するか]

## Requirements
- n8n (Cloud or Self-hosted v1.0+)
- [必要な外部サービス]
- [必要なAPIキー]

## What's Included
- n8nワークフローJSONファイル
- セットアップガイド（PDF）
- 動画チュートリアル（任意）

## Setup Time
[セットアップ所要時間の目安]

## Support
購入後30日間のメールサポート付き
```

---

### [MEDIUM] 無料商品（リードマグネット）の活用強化

| 商品名 | 現状 | 改善案 |
|--------|------|--------|
| Book & Learning Tracker | 無料・説明1634c | 末尾に有料商品（Life OS $19）へのアップセルCTA追加 |
| Job Search Tracker | 無料・説明1757c | 末尾にFreelance Business OS($19)へのCTA追加 |
| Student Study Hub | 無料・説明1597c | 末尾にDigital Products OS($15)へのCTA追加 |

無料商品は「見込み客獲得→有料商品へ誘導」のファネル入口として機能させる。現状はその誘導が不足している。

---

## 優先対応順序（即日実行可能）

### Step 1（5分）: 未公開商品の公開
- AI Business Automation Mega Prompt Pack を Published=True に変更

### Step 2（30分）: 15商品へのタグ追加
- Gumroad管理画面で各商品にタグを5つ設定
- タグは上記推奨タグを使用

### Step 3（2時間）: 説明文強化（4商品）
- Ultimate AI Blogger Bundle — 説明文を上記案に差し替え
- Affiliate Content Generator — 内容詳細を追記
- WordPress Automation Prompt Kit — コードスニペット内容を追記
- SEO Article Writer — 差別化ポイントを追記

### Step 4（Stripe KYC解除後）: n8n商品9本の説明文強化
- 各商品に共通テンプレートを適用
- 動画デモ or スクリーンショットをプレビューに追加

---

## 根本的なトラフィック問題

**重要な指摘:** 説明文・タグを整備しても、Gumroadへの流入がなければ売上は発生しない。現状の$0は「商品品質」より「流入ゼロ」が主因である可能性が高い。

### 必要なトラフィック戦略（別途実施）

1. **ブログからのリンク**: 3サイト（nambei-oyaji.com等）の関連記事からGumroad商品ページへ内部リンク
2. **X（@prodhq27）での告知**: 商品紹介ツイートを週1~2回投稿
3. **Dev.to記事**: 各プロダクトカテゴリのHow-to記事 → Gumroad商品へ誘導
4. **Pinterest**: Notion templateはPinterestで高拡散（無料集客）
5. **Product Hunt**: バンドル商品のローンチに有効

---

## 競合比較（市場相場）

| カテゴリ | 相場価格帯 | 現在価格 | 評価 |
|---------|-----------|---------|------|
| Notionテンプレート（単品） | $5~$29 | $9~$19 | 適正 |
| Notionバンドル | $29~$99 | $49 | 適正 |
| AIプロンプトパック（50本） | $9~$39 | $12~$19 | 適正（やや安め） |
| n8nワークフロー（単品） | $29~$149 | $49~$99 | 適正 |

**価格は問題なし。** 説明文・タグ・流入が課題。

---

## 生成日時
2026-03-28 | by Claude Code
