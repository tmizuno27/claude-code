# GSC Rank Tracker Pro

Google Search Console データを無期限保存・可視化するSEOモニタリングSaaS。

## 概要

| 項目 | 内容 |
|------|------|
| フレームワーク | Next.js 15 (App Router) |
| データベース | Supabase (PostgreSQL) |
| 認証 | Supabase Auth + Google OAuth |
| ホスティング | Vercel |
| バックグラウンド処理 | Cloudflare Workers Cron（Week 2実装予定） |
| メールアラート | Resend（Week 3実装予定） |
| 決済 | Stripe（Week 4実装予定） |

## 開発ロードマップ

- **Week 1（現在）**: インフラ・認証・ランディングページ ✅
- **Week 2**: Cloudflare Workers日次データ取得 + グラフUI
- **Week 3**: 順位急落アラート + CTR改善フラグ
- **Week 4**: Stripe決済 + Product Hunt Launch

## セットアップ

### 1. 依存パッケージをインストール

```bash
npm install
```

### 2. 環境変数を設定

```bash
cp .env.local.example .env.local
# .env.local を編集して各値を設定
```

必要な環境変数:
- `NEXT_PUBLIC_SUPABASE_URL` — SupabaseプロジェクトURL
- `NEXT_PUBLIC_SUPABASE_ANON_KEY` — Supabase Anon Key
- `SUPABASE_SERVICE_ROLE_KEY` — Supabase Service Role Key（サーバーサイド専用）
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` — Google Cloud Console で取得

### 3. Supabaseセットアップ

1. [Supabase](https://supabase.com) でプロジェクトを作成
2. SQL Editor で `supabase/migrations/001_initial_schema.sql` を実行
3. Authentication > Providers > Google を有効化してOAuth認証情報を設定

### 4. 開発サーバーを起動

```bash
npm run dev
```

http://localhost:3000 でアクセス可能

## ディレクトリ構成

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/          # ログインページ
│   │   └── signup/         # サインアップページ
│   ├── (dashboard)/
│   │   └── dashboard/      # ダッシュボード
│   │       └── sites/      # サイト管理
│   ├── api/
│   │   └── auth/
│   │       ├── callback/   # OAuth コールバック
│   │       └── signout/    # ログアウト
│   ├── layout.tsx
│   └── page.tsx            # ランディングページ
├── lib/
│   └── supabase/
│       ├── client.ts       # ブラウザ用Supabaseクライアント
│       ├── server.ts       # サーバー用Supabaseクライアント
│       └── middleware.ts   # 認証ミドルウェア
├── middleware.ts            # Next.jsミドルウェア
└── types/
    └── database.ts         # Supabaseの型定義
supabase/
└── migrations/
    └── 001_initial_schema.sql  # DBスキーマ
```

## 料金プラン

| プラン | 価格 | サイト数 | データ保存 |
|--------|------|---------|-----------|
| Free | $0 | 1サイト | 3ヶ月 |
| Starter | $9/月 | 3サイト | 無期限 |
| Pro | $19/月 | 10サイト | 無期限 + Slack |
| Agency | $49/月 | 無制限 | 無期限 + レポート |

## 運用コスト（月次）

初期100ユーザーまで**$0**:
- Vercel Hobby: 無料
- Supabase Free: 無料（25GB、50万行以内）
- Cloudflare Workers: 無料（10万req/日）
- Resend: 無料（100通/日）
