# Google Sheets 自動読み取り セットアップガイド

## 概要
このスクリプトは Google Sheets の「入金管理」シートを自動で読み取り、
ローカルにCSVとして保存します。一度セットアップすれば、以降は自動で動作します。

## セットアップ手順（初回のみ・約5分）

### Step 1: Google Cloud プロジェクト作成
1. https://console.cloud.google.com/ にアクセス
2. 上部の「プロジェクトを選択」→「新しいプロジェクト」をクリック
3. プロジェクト名: `sheets-sync`（任意）
4. 「作成」をクリック

### Step 2: Google Sheets API を有効化
1. 左メニュー「APIとサービス」→「ライブラリ」
2. 「Google Sheets API」を検索 → クリック → 「有効にする」
3. 同様に「Google Drive API」も有効にする

### Step 3: サービスアカウント作成
1. 左メニュー「APIとサービス」→「認証情報」
2. 「認証情報を作成」→「サービスアカウント」
3. サービスアカウント名: `sheets-reader`（任意）
4. 「作成して続行」→「完了」

### Step 4: 鍵ファイルのダウンロード
1. 作成したサービスアカウントをクリック
2. 「鍵」タブ →「鍵を追加」→「新しい鍵を作成」
3. 種類: **JSON** → 「作成」
4. ダウンロードされたJSONファイルを以下に移動:
   ```
   c:\Users\tmizu\マイドライブ\GitHub\data\sheets-sync\credentials\service-account.json
   ```

### Step 5: スプレッドシートを共有
1. Google Sheets で「入金管理」シートを開く
2. 右上の「共有」ボタンをクリック
3. ダウンロードしたJSONファイルを開き、`client_email` の値をコピー
   （例: `sheets-reader@sheets-sync-xxxxx.iam.gserviceaccount.com`）
4. そのメールアドレスを「閲覧者」として追加
5. 「送信」

## 使い方

セットアップ完了後、以下のコマンドで実行:

```bash
python "c:/Users/tmizu/マイドライブ/GitHub/data/sheets-sync/fetch_sheet.py"
```

CSVファイルは `output/` フォルダに保存されます。

## Claude Code での使い方

Claude Code に「入金管理シートを読んで」と言うだけで、
自動的にこのスクリプトを実行してデータを取得・分析します。
