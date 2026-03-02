# セットアップガイド

このガイドに従って、AI副業自動化ビジネスの初期設定を行います。
所要時間: 約2〜3時間（一度だけ）

---

## 1. WordPress環境構築

### 1-1. ConoHa WING契約
1. https://www.conoha.jp/wing/ にアクセス
2. 「WINGパック」を選択（3年契約が最安: 月額約1,452円）
3. 独自ドメインを取得（例: `ai-fukugyou.com`, `ai-jidouka.jp` など）
4. WordPress簡単セットアップを選択

### 1-2. WordPress初期設定
1. 管理画面（`https://あなたのドメイン/wp-admin`）にログイン
2. 「設定」→「一般」でサイト名を設定
3. 「設定」→「パーマリンク」→「投稿名」を選択

### 1-3. Rank Math SEOプラグイン
1. 「プラグイン」→「新規追加」→「Rank Math」を検索→インストール→有効化
2. セットアップウィザードに従って設定
3. 「Rank Math」→「一般設定」→「REST API」を有効化

### 1-4. WordPressアプリケーションパスワード
1. 「ユーザー」→ あなたのプロフィール
2. 下部の「アプリケーションパスワード」セクション
3. 名前に「JidouBiz」と入力→「新しいアプリケーションパスワードを追加」
4. 生成されたパスワードを `config/settings.json` の `wordpress.app_password` にコピー

---

## 2. Google Analytics 4 設定

### 2-1. GA4プロパティ作成
1. https://analytics.google.com/ にアクセス
2. 「管理」→「プロパティを作成」
3. あなたのドメインを登録
4. プロパティIDをメモ（例: `123456789`）

### 2-2. トラッキングコード設置
1. 「データストリーム」→「ウェブ」→ URLを入力
2. 測定IDをコピー（例: `G-XXXXXXXXXX`）
3. WordPressに「Site Kit by Google」プラグインをインストールして連携
   または Rank Math の「分析」機能で測定IDを設定

### 2-3. API認証設定（自動レポート用）
1. https://console.cloud.google.com/ にアクセス
2. プロジェクトを作成
3. 「APIとサービス」→「認証情報」→「サービスアカウント」を作成
4. JSONキーをダウンロード→ `config/ga4-credentials.json` として保存
5. Google Analyticsの管理画面でサービスアカウントに「閲覧者」権限を付与

---

## 3. Google Search Console 設定

1. https://search.google.com/search-console/ にアクセス
2. 「プロパティを追加」→ URLプレフィックス → あなたのドメインを入力
3. DNS認証またはHTML認証で所有権を確認
4. サイトマップを送信: `https://あなたのドメイン/sitemap_index.xml`

---

## 4. アフィリエイトASP登録

### A8.net（最大手）
1. https://www.a8.net/ で無料会員登録
2. サイト情報にWordPressサイトを登録
3. 以下のプログラムに提携申請:
   - ConoHa WING（サーバー）
   - TechAcademy（プログラミングスクール）
   - ランサーズ / クラウドワークス
   - ココナラ

### もしもアフィリエイト
1. https://af.moshimo.com/ で無料会員登録
2. 以下のプログラムに提携申請:
   - Udemy
   - Amazon（Kindle本紹介用）

### 注意
- 提携申請には10記事程度の公開が必要な場合があります
- 最初は記事作成に集中し、10記事公開後にまとめて申請しましょう

---

## 5. Gumroad設定（デジタル商品販売）

1. https://gumroad.com/ でアカウント作成
2. 「Settings」→「API」でAPIキーを取得
3. `config/settings.json` の `gumroad.api_key` に設定

---

## 6. Python環境設定

### 6-1. Pythonインストール確認
```bash
python --version
```
Python 3.9以上が必要です。

### 6-2. パッケージインストール
```bash
cd "c:/Users/tmizu/マイドライブ/cloude-code/jidou-business"
pip install -r requirements.txt
```

### 6-3. 動作確認
```bash
# キーワード調査のテスト
python scripts/keyword_research.py

# 正常に動作すれば inputs/keywords/ にJSONファイルが生成されます
```

---

## 7. config/settings.json の設定

以下の項目を実際の値に置き換えてください:

```
YOUR_CLAUDE_API_KEY_HERE      → Claude APIキー（https://console.anthropic.com/）
YOUR-DOMAIN.com               → あなたのWordPressドメイン
YOUR_WP_USERNAME              → WordPress管理者ユーザー名
YOUR_WP_APP_PASSWORD          → 手順1-4で生成したパスワード
YOUR_GA4_PROPERTY_ID          → GA4プロパティID
YOUR_GUMROAD_API_KEY          → GumroadのAPIキー
YOUR_UBERSUGGEST_API_KEY      → UbersuggestのAPIキー（オプション）
YOUR_BUFFER_ACCESS_TOKEN      → BufferのAPIトークン（オプション）
```

---

## 8. タスクスケジューラ登録（Phase 4で実施）

全スクリプトの設定が完了したら:
```bash
python scripts/scheduler.py --register
```

登録確認:
```bash
python scripts/scheduler.py --list
```

---

## チェックリスト

- [ ] ConoHa WING契約 + ドメイン取得
- [ ] WordPress + Rank Math SEO導入
- [ ] WordPressアプリケーションパスワード生成
- [ ] Google Analytics 4 設定
- [ ] Google Search Console 設定
- [ ] A8.net 登録
- [ ] もしもアフィリエイト登録
- [ ] Gumroad アカウント作成
- [ ] Python + パッケージインストール
- [ ] config/settings.json 設定完了
- [ ] keyword_research.py 動作確認
