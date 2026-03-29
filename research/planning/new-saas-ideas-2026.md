# 新規SaaSアイデア（月$100-1,000規模）

作成日: 2026-03-29
技術スタック: Next.js + Supabase + Cloudflare Workers

---

## 評価基準

| 基準 | 重み | 説明 |
|------|------|------|
| 課題の明確さ | 30% | 「誰が・何で困っているか」が明確か |
| 既存競合の弱さ | 25% | ニッチすぎて大手が参入しない領域か |
| 実装工数 | 25% | 1-2ヶ月で MVP できるか |
| マネタイズ可能性 | 20% | 月$100-1,000に到達する道筋が見えるか |

---

## アイデア1: ★★★★★ GSC Rank Tracker Pro（SEO特化ツール）

### 課題
Google Search Console(GSC)は無料で最高のSEOデータを持っているが：
- 過去16ヶ月分しか保存されない
- 記事単位の詳細トレンドが見づらい
- 競合比較ができない
- アラート機能がない（順位が突然落ちても気づかない）

### ソリューション
GSC APIを使って独自DBに蓄積 → 長期トレンド可視化 + アラート + 改善提案

### 主要機能
- GSC データ毎日自動取得・無期限保存
- 記事別の順位推移グラフ（過去2年+）
- 順位急落アラート（メール/Slack通知）
- 「CTR低い = タイトル改善余地あり」の自動フラグ
- 複数サイト管理（最大10サイト）

### 技術実装
```
Next.js 15 (フロント + API routes)
Supabase (GSCデータ保存、認証)
Google OAuth + Search Console API
Cloudflare Workers Cron (毎日データ取得)
Resend (メールアラート)
Stripe (決済)
```

### 価格設定
| プラン | 価格 | 制限 |
|--------|------|------|
| Free | $0 | 1サイト、3ヶ月保存 |
| Starter | $9/月 | 3サイト、無期限保存 |
| Pro | $19/月 | 10サイト + Slackアラート |
| Agency | $49/月 | 無制限サイト + クライアントレポート |

### 収益試算
- Free: 0
- Starter ($9): 20人 = $180
- Pro ($19): 15人 = $285
- Agency ($49): 5人 = $245
- **合計: 月$710**（3ヶ月で達成可能）

### 競合
- Ahrefs, SEMrush: 高すぎる（$100+/月）
- Google Looker Studio: 無料だが設定が複雑すぎる
- **本サービスの差別化: 設定5分、GSCデータだけに特化、安い**

### 初期実装工数（概算）
- Week 1: GSC OAuth + データ取得 + Supabase保存
- Week 2: ダッシュボードUI + グラフ表示
- Week 3: アラート機能 + Stripe連携
- Week 4: 複数サイト対応 + テスト + Launch

**合計: 4週間でMVP**

---

## アイデア2: ★★★★☆ Cloudflare Workers Monitor（エッジAPI監視ツール）

### 課題
Cloudflare Workersで本番APIを運用している開発者は：
- レスポンスタイムのトレンドが見えない
- エラー率が上がっても気づくのが遅れる
- API使用量のコスト予測ができない
- 複数Workerを一画面で管理できない

### ソリューション
Cloudflare APIを使って全WorkerのメトリクスをDB蓄積 → アラート + ダッシュボード

### 主要機能
- 全Workerのリクエスト数・エラー率・P50/P99レスポンスタイム
- 異常検知アラート（エラー率5%超 → 即通知）
- API使用量のコスト予測（無料枠の残量可視化）
- ログのリアルタイム表示（wrangler tail不要）
- Slack/Discord/Email通知

### 技術実装
```
Next.js (ダッシュボード)
Cloudflare Analytics API + GraphQL
Supabase (メトリクス保存・アラートルール)
Cloudflare Durable Objects (リアルタイムログ中継)
```

### 価格設定
| プラン | 価格 | 制限 |
|--------|------|------|
| Free | $0 | 3 Workers、7日保存 |
| Developer | $12/月 | 20 Workers、90日保存 |
| Team | $29/月 | 無制限 Workers、1年保存 |

### 収益試算
- Developer ($12): 25人 = $300
- Team ($29): 10人 = $290
- **合計: 月$590**

### 競合
- Datadog, New Relic: 高すぎ・複雑すぎ
- Cloudflare標準ダッシュボード: 機能不足
- **差別化: Cloudflare専門、シンプル、安い**

### ターゲットユーザー
- RapidAPI出品者（自分と同じ）
- Cloudflare Workers依存のスタートアップ
- フリーランス開発者

### 初期実装工数
- Week 1-2: Cloudflare API連携 + データ取得
- Week 3: ダッシュボードUI
- Week 4: アラート + Stripe
- **合計: 4週間でMVP**

---

## アイデア3: ★★★★☆ Affiliate Link Manager SaaS

### 課題
アフィリエイトブロガーは：
- 複数ASP（A8, もしも, アクセストレードetc）のリンクをバラバラに管理
- 記事内のリンクが古くなっても気づかない（広告主がサービス終了等）
- どのリンクが稼いでいるか記事単位でわからない
- ASP提携申請の管理が煩雑

### ソリューション
全ASPのリンクをDB一元管理 → WordPress記事への一括挿入 + パフォーマンス追跡

### 主要機能
- アフィリエイトリンクのDB管理（ASP・商品・URL・ステータス）
- WordPress記事への一括リンク挿入（REST API経由）
- リンク有効性チェック（毎週自動クロール）
- 記事×リンク別のクリック数トラッキング（UTMベース）
- ASP提携状況管理ダッシュボード

### 技術実装
```
Next.js (フロント)
Supabase (リンクDB、クリックログ)
WordPress REST API連携
Cloudflare Workers (リンクチェッカーCron)
Vercel (ホスティング)
```

### 価格設定
| プラン | 価格 | 制限 |
|--------|------|------|
| Free | $0 | 50リンク、1サイト |
| Blogger | $9/月 | 500リンク、3サイト |
| Pro | $19/月 | 無制限リンク、10サイト |

### 収益試算
- Blogger ($9): 20人 = $180
- Pro ($19): 10人 = $190
- **合計: 月$370**

### 競合
- ThirstyAffiliates, Pretty Links: WordPress Plugin型、SaaS型は少ない
- **差別化: 日本のASP対応、複数サイト横断管理、クラウド型**

### 自社利用価値
自分自身がこのツールを必要としている。3サイト×4 ASP×数百リンクを管理するのに現在はJSONファイル+Pythonスクリプトで対応中。

### 初期実装工数
- Week 1: リンクCRUD + WordPress連携
- Week 2: 一括挿入機能
- Week 3: リンクチェッカー + UI
- Week 4: クリックトラッキング + Stripe
- **合計: 4週間でMVP**

---

## 最優先: アイデア1（GSC Rank Tracker Pro）基本設計

### 選定理由
1. **自分が最も必要としているツール**: 3サイト・400記事のGSCデータを管理
2. **既存のコードベースが流用可能**: pSEOサイトでGSC API統合経験あり
3. **課題が普遍的**: ブロガー・SEO担当者は全員このニーズを持つ
4. **価格帯が広い**: フリーから$49まで幅広く対応

---

## GSC Rank Tracker Pro 基本設計

### システム概要

```
[ユーザー]
    → Next.js フロントエンド (Vercel)
    → Next.js API Routes
    → Supabase (データ・認証)
    ↓
[バックグラウンド]
    → Cloudflare Workers Cron (毎日AM3:00 JST)
    → Google Search Console API
    → Supabase (データ保存)
```

### データベース設計（Supabase）

```sql
-- ユーザー管理
users (
  id uuid PRIMARY KEY,
  email text,
  plan text DEFAULT 'free', -- free/starter/pro/agency
  stripe_customer_id text,
  created_at timestamptz
)

-- サイト管理
sites (
  id uuid PRIMARY KEY,
  user_id uuid REFERENCES users,
  domain text,
  gsc_property_url text, -- GSCプロパティURL
  created_at timestamptz
)

-- キーワード順位データ（メインテーブル）
rankings (
  id uuid PRIMARY KEY,
  site_id uuid REFERENCES sites,
  date date,
  page_url text,
  query text,
  position numeric,
  impressions int,
  clicks int,
  ctr numeric,
  created_at timestamptz
)
-- インデックス: (site_id, date, page_url, query)

-- アラートルール
alert_rules (
  id uuid PRIMARY KEY,
  site_id uuid REFERENCES sites,
  alert_type text, -- position_drop/ctr_low/impressions_spike
  threshold numeric,
  notification_channels jsonb -- {email: true, slack_webhook: "..."}
)

-- アラート履歴
alert_logs (
  id uuid PRIMARY KEY,
  alert_rule_id uuid REFERENCES alert_rules,
  triggered_at timestamptz,
  payload jsonb
)
```

### API設計

```
POST /api/auth/connect-gsc    -- Google OAuth
GET  /api/sites               -- サイト一覧取得
POST /api/sites               -- サイト追加
GET  /api/sites/:id/rankings  -- 順位データ取得（期間・URL・クエリフィルタ）
GET  /api/sites/:id/summary   -- サマリー（上昇/下落キーワード）
POST /api/alerts              -- アラートルール作成
GET  /api/alerts/history      -- アラート履歴
```

### Cloudflare Workers Cron（日次データ取得）

```typescript
// workers/gsc-sync/index.ts
export default {
  async scheduled(event: ScheduledEvent, env: Env) {
    // Supabaseから全アクティブサイトを取得
    const sites = await getActiveSites(env);

    // 各サイトのGSCデータを取得（過去3日分、重複は上書き）
    for (const site of sites) {
      const data = await fetchGSCData(site, env);
      await saveToSupabase(data, env);

      // アラートチェック
      await checkAlerts(site, data, env);
    }
  }
}
```

### フロントエンド主要ページ

```
/dashboard          -- 全サイト概要
/sites/:id          -- サイト詳細（グラフ）
  /rankings         -- キーワード別順位テーブル
  /pages            -- ページ別パフォーマンス
  /alerts           -- アラート設定
/settings           -- プラン変更・Stripe
```

### UI/UX設計

- shadcn/ui + Tailwind CSS
- グラフ: Recharts（軽量）
- テーブル: TanStack Table（ソート・フィルタ）
- 日付ピッカー: react-day-picker

### MVC実装計画（4週間）

**Week 1: インフラ + 認証**
- Next.js 15 プロジェクト初期化
- Supabase セットアップ（スキーマ作成、RLS設定）
- Google OAuth + GSC API連携
- サイト追加フロー

**Week 2: データ取得 + 表示**
- Cloudflare Workers Cron（日次GSCデータ取得）
- 順位データのグラフUI（Recharts）
- キーワード別テーブル

**Week 3: アラート + 差別化機能**
- 順位急落検知アルゴリズム
- メールアラート（Resend）
- 「CTR改善余地」自動フラグ機能

**Week 4: マネタイズ + Launch**
- Stripe Subscription連携
- フリープラン制限実装
- Product Hunt Launch準備
- ランディングページ最終化

### 想定コスト（月次）
| 項目 | 費用 |
|------|------|
| Vercel Pro | $0（Hobby枠で開始） |
| Supabase Free | $0（25GB、50万行以内） |
| Cloudflare Workers | $0（10万req/日無料） |
| Resend | $0（100通/日無料） |
| **合計** | **$0（最初の100ユーザーまで）** |

### 最初のユーザー獲得戦略

1. **自分自身が使う**: 3サイト・400記事のGSCデータをすぐに移行
2. **Dev.to記事**: "I Built a Free GSC Data Archiver" → ツールへ誘導
3. **Product Hunt Launch**: 上記の準備計画を流用
4. **Reddit r/SEO, r/Blogging**: ツール紹介投稿（規約確認要）
5. **Twitter/X**: ビルドログを毎日投稿（#buildinpublic）

---

## 実行優先順位（全3アイデア）

| 順位 | アイデア | 開始時期 | 理由 |
|------|---------|---------|------|
| 1 | GSC Rank Tracker Pro | **今月中** | 自社ニーズ高・既存技術流用・競合弱 |
| 2 | Affiliate Link Manager | 来月以降 | 自社でもすぐ使える・WP Linkerとシナジー |
| 3 | CF Workers Monitor | 3ヶ月後 | RapidAPIのトラフィック増加後に自社でも必要になる |
