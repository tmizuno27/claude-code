# Google Sheets 自動同期 セットアップ手順

## 1. Google Cloud プロジェクト作成

1. https://console.cloud.google.com/ にアクセス
2. 上部の「プロジェクトを選択」→「新しいプロジェクト」をクリック
3. プロジェクト名: `sheets-sync` (任意) → 「作成」

## 2. Google Sheets API を有効化

1. 左メニュー「APIとサービス」→「ライブラリ」
2. 「Google Sheets API」を検索 → クリック → 「有効にする」

## 3. サービスアカウント作成

1. 左メニュー「APIとサービス」→「認証情報」
2. 上部「+ 認証情報を作成」→「サービスアカウント」
3. サービスアカウント名: `sheets-reader` (任意) → 「作成して続行」
4. ロール: 「閲覧者」で十分 → 「続行」→「完了」

## 4. 認証キー(JSON)をダウンロード

1. 作成したサービスアカウントをクリック
2. 「キー」タブ → 「鍵を追加」→「新しい鍵を作成」
3. JSON形式 → 「作成」→ ファイルがダウンロードされる
4. ダウンロードしたファイルを以下に配置:
   ```
   data/sheets-sync/credentials/service-account.json
   ```

## 5. スプレッドシートを共有

1. ダウンロードしたJSONファイルを開き、`client_email` の値をコピー
   - 例: `sheets-reader@sheets-sync-xxxxx.iam.gserviceaccount.com`
2. 同期したいGoogleスプレッドシートを開く
3. 右上「共有」→ コピーしたメールアドレスを追加（閲覧者でOK）

## 6. config.json にスプレッドシートを登録

スプレッドシートのURLからIDを取得:
```
https://docs.google.com/spreadsheets/d/【ここがID】/edit
```

`config.json` を編集:
```json
{
  "sheets": [
    {
      "name": "売上管理",
      "spreadsheet_id": "1ABC...xyz",
      "ranges": ["シート1", "シート2"]
    }
  ],
  "output_dir": "output",
  "credentials_file": "credentials/service-account.json"
}
```

## 7. テスト実行

```bash
python "c:/Users/tmizu/マイドライブ/GitHub/data/sheets-sync/fetch_sheets.py"
```

成功すると `output/` フォルダにCSVが生成されます。

## 8. 自動実行

Task Scheduler `GoogleSheetsSync` が5分おきに実行します（セットアップ済み）。
取得したCSVは `auto-sync.ps1` により自動でGitHubにpushされます。

## トラブルシューティング

- **403 Forbidden**: スプレッドシートがサービスアカウントに共有されていない
- **404 Not Found**: spreadsheet_id が間違っている
- **credentials not found**: JSONファイルのパスを確認
- **ログ確認**: `sheets-sync/sheets-sync.log`
