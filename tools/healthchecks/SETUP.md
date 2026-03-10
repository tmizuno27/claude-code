# Healthchecks.io セットアップ手順

全自動タスクの実行監視を一元管理するための設定手順。

## 所要時間: 約10分

## Step 1: アカウント作成（2分）

1. https://healthchecks.io にアクセス
2. **「Sign Up」** → GitHubアカウントで認証（推奨）
3. プロジェクト名を入力: `南米おやじ 自動タスク監視`

## Step 2: APIキー取得（1分）

1. ログイン後 → 左メニュー **「Settings」**
2. **「API Access」** セクション
3. **「API key (read-write)」** をコピー

## Step 3: secrets.json にキーを追加（1分）

`claude-code/blog/config/secrets.json` に以下を追加:

```json
"healthchecks": {
    "api_key": "ここにコピーしたAPIキーを貼り付け"
}
```

## Step 4: チェック自動作成（1分）

```bash
cd claude-code/tools/healthchecks
python setup_healthchecks.py
```

→ 22個のチェックが自動作成され、`config.json` にping URLが保存される

## Step 5: Discord連携（2分）

1. https://healthchecks.io にログイン
2. 左メニュー **「Integrations」** → **「Discord」** → **「Add Integration」**
3. Webhook URL を入力:
   - `blog/config/settings.json` の `discord.webhook_url` の値をコピー
4. **「Save Integration」**

## Step 6: 全PS1にping追加（1分）

```bash
# まず確認（変更なし）
python integrate_ps1.py --dry-run

# 問題なければ実行
python integrate_ps1.py
```

→ 全PS1ランチャーに開始ping・完了ping（成功/失敗）が自動追加される

## Step 7: 動作確認（2分）

1. https://healthchecks.io のダッシュボードを確認
2. 各チェックが「New」ステータスになっている
3. タスクが次回実行されると「Up」に変わる
4. すぐ確認したい場合:
   ```powershell
   # 手動でpingテスト
   Invoke-WebRequest -Uri "https://hc-ping.com/YOUR-UUID" -Method Post
   ```

## 仕組み

```
[Task Scheduler] → [PS1ランチャー]
                     ├─ /start ping → Healthchecks.io「実行中」
                     ├─ Pythonスクリプト実行
                     └─ 成功 → /ping  → Healthchecks.io「OK」
                        失敗 → /fail  → Healthchecks.io「Down」→ Discord通知
                        未実行（PCスリープ等）→ Grace期間超過 → Discord通知
```

## 無料枠の制限

- 最大20チェック（現在22タスク → GitAutoSync と GoogleSheetsSync を1つに統合するか、$20/月で100チェック）
- 通知チャネル: 無制限
- ログ保持: 100件/チェック
- API: 制限なし

## トラブルシューティング

- **pingが届かない**: PS1内の `Invoke-WebRequest` がファイアウォールでブロックされていないか確認
- **チェックが常にDown**: grace（猶予時間）が短すぎる可能性。setup_healthchecks.py のgrace値を増やす
- **Discord通知が来ない**: Integrations画面でDiscordが「Active」になっているか確認
