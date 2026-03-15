# sim-hikaku.online セットアップガイド

**作成日**: 2026-03-14

---

## Step 1: ドメイン取得・追加（ConoHa WING）

ConoHa WINGのWINGパックなら、ディスク容量の範囲内でドメイン無制限追加可能。

### 1-1. ドメイン「sim-hikaku.online」を取得済みか確認

**未取得の場合**: ConoHa WINGコントロールパネルから取得
1. https://manage.conoha.jp/ にログイン
2. 上部「WING」タブをクリック
3. 左メニュー「ドメイン」→「ドメイン取得」
4. `sim-hikaku.online` を検索 → 購入
   - `.online` ドメインは年額1,000-2,000円程度

**取得済みの場合**: 1-2へ進む

### 1-2. サーバーにドメインを追加

1. ConoHaコントロールパネル → 上部「WING」
2. 左メニュー「サーバー管理」→「ドメイン」
3. 右上「+ドメイン」をクリック
4. 「新規ドメインを追加」を選択
5. ドメイン名: `sim-hikaku.online` を入力
6. 無料独自SSL: 「利用する」を選択
7. 「保存」をクリック

> SSL設定は反映まで最大1時間程度かかる場合があります

### 1-3. DNS設定の確認

他社でドメインを取得した場合は、ネームサーバーをConoHaに向ける必要があります:
```
ns-a1.conoha.io
ns-a2.conoha.io
ns-a3.conoha.io
```

---

## Step 2: WordPressインストール

### 2-1. ドメイン切り替え

1. 左メニュー「サイト管理」
2. 「サイト設定」の上部にある現在のドメイン名をクリック
3. 「切り替え」画面で `sim-hikaku.online` を選択

### 2-2. WordPressインストール

1. 「サイト管理」→「サイト設定」→「WordPress」
2. 右上「+WordPress」をクリック
3. 以下を設定:
   - インストール方法: 新規インストール
   - バージョン: 最新
   - URL: wwwなし（`sim-hikaku.online`）
   - サイト名: SIM比較オンライン
   - メールアドレス: （管理用メール）
   - ユーザー名: （管理者ユーザー名）
   - パスワード: （強力なパスワード）
   - データベース: 自動生成
   - テーマ: Cocoon（後でインストールも可）
4. 「保存」をクリック

### 2-3. SSL設定確認

1. 「サイト管理」→「サイトセキュリティ」→「独自SSL」
2. 「無料独自SSL」が「ON」になっていることを確認
3. `https://sim-hikaku.online` でアクセスできることを確認

---

## Step 3: WordPress初期設定

### 3-1. 管理画面にログイン

`https://sim-hikaku.online/wp-admin/` にアクセス

### 3-2. 一般設定

**設定 → 一般**:
- サイトのタイトル: `SIM比較オンライン`
- キャッチフレーズ: `用途別・悩み別で選ぶ格安SIM比較サイト`
- WordPress アドレス: `https://sim-hikaku.online`
- サイトアドレス: `https://sim-hikaku.online`
- タイムゾーン: 東京（UTC+9）

### 3-3. パーマリンク設定

**設定 → パーマリンク**:
- 「投稿名」を選択（`/%postname%/`）
- 保存

### 3-4. テーマ設定（Cocoon）

1. **外観 → テーマ** → Cocoonがなければインストール
   - Cocoon公式: https://wp-cocoon.com/
   - 「Cocoon Child」を有効化（親テーマは直接使わない）
2. **Cocoon設定** → 以下を設定:
   - スキン: なし（カスタムCSSで上書きするため）
   - SEO: メタタグ出力OFF（Rank Mathに任せる）
   - アクセス解析: GA4のトラッキングIDを設定

### 3-5. 必須プラグインのインストール

| プラグイン | 用途 |
|-----------|------|
| Rank Math SEO | SEO管理（メタタグ、構造化データ、サイトマップ） |
| WP Fastest Cache | キャッシュ・高速化 |
| Contact Form 7 | お問い合わせフォーム |
| EWWW Image Optimizer | 画像圧縮 |
| Broken Link Checker | リンク切れ検出 |
| UpdraftPlus | バックアップ |

### 3-6. カテゴリ作成

**投稿 → カテゴリー** で以下を作成:

| カテゴリ名 | スラッグ |
|-----------|---------|
| 用途別おすすめ | yoto-betsu |
| 乗り換えガイド | norikae |
| 料金比較 | ryokin-hikaku |
| キャリアレビュー | review |
| 海外SIM・eSIM | kaigai-sim |

### 3-7. 固定ページ作成

| ページ | スラッグ |
|-------|---------|
| 運営者情報 | about |
| プライバシーポリシー | privacy-policy |
| お問い合わせ | contact |
| 免責事項 | disclaimer |

---

## Step 4: REST API設定（自動投稿用）

nambei-oyaji.comと同じ方式でREST APIを設定。

### 4-1. Application Passwords の生成

1. WordPress管理画面 → ユーザー → プロフィール
2. 「アプリケーションパスワード」セクション
3. 新しいアプリケーションパスワード名: `Claude Code`
4. 「新しいアプリケーションパスワードを追加」
5. 生成されたパスワードをメモ

### 4-2. config/secrets.json を作成

```json
{
  "wordpress": {
    "site_url": "https://sim-hikaku.online",
    "api_url": "https://sim-hikaku.online/wp-json/wp/v2",
    "username": "（ユーザー名）",
    "app_password": "（Application Password）"
  },
  "ga4": {
    "property_id": "（GA4プロパティID）"
  }
}
```

> このファイルは `.gitignore` に含めること

### 4-3. config/wp-credentials.json を作成

```json
{
  "url": "https://sim-hikaku.online",
  "username": "（ユーザー名）",
  "password": "（Application Password）"
}
```

---

## Step 5: GA4 + Search Console 設定

### 5-1. GA4

1. https://analytics.google.com/ にアクセス
2. 「プロパティを作成」
3. プロパティ名: `sim-hikaku.online`
4. データストリーム → ウェブ → URL: `sim-hikaku.online`
5. 測定ID（G-XXXXXXXXXX）をCocoon設定 or Rank Mathに設定

### 5-2. Search Console

1. https://search.google.com/search-console/ にアクセス
2. 「プロパティを追加」→ URLプレフィックス → `https://sim-hikaku.online`
3. 所有権確認（HTMLタグ or DNS）
4. サイトマップ送信: `https://sim-hikaku.online/sitemap_index.xml`

---

## Step 6: デザイン適用

WordPressとプラグインの設置が完了したら、nambei-oyaji.comベースのデザインをSIM比較サイト向けにカスタマイズして適用。

→ 詳細は `docs/design-guide.md` を参照

---

## チェックリスト

- [ ] ドメイン `sim-hikaku.online` 取得
- [ ] ConoHa WINGにドメイン追加
- [ ] SSL設定完了
- [ ] WordPressインストール
- [ ] Cocoon Child テーマ有効化
- [ ] Rank Math SEO インストール・設定
- [ ] パーマリンク設定（投稿名）
- [ ] カテゴリ5つ作成
- [ ] 固定ページ4つ作成（about, privacy-policy, contact, disclaimer）
- [ ] GA4 設定
- [ ] Search Console 設定・サイトマップ送信
- [ ] REST API（Application Password）設定
- [ ] config/secrets.json 作成
- [ ] デザイン（カスタムCSS）適用
