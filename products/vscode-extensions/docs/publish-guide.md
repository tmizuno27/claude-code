# VS Code Extension 公開手順ガイド

## 1. 事前準備

### Azure DevOps PAT（Personal Access Token）取得

1. https://dev.azure.com にアクセス
2. 右上のユーザーアイコン → **Personal Access Tokens**
3. **New Token** をクリック
4. 設定:
   - Name: `vsce-publish`
   - Organization: **All accessible organizations**
   - Expiration: 1年
   - Scopes: **Custom defined** → **Marketplace** → **Manage** にチェック
5. **Create** → トークンをコピーして安全に保存

### Publisher 作成

1. https://marketplace.visualstudio.com/manage にアクセス
2. **Create publisher** をクリック
3. 設定:
   ```
   Publisher ID: miccho27
   Display Name: miccho27
   ```
4. 作成完了

### vsce インストール＆ログイン

```bash
npm install -g @vscode/vsce
vsce login miccho27
# PATを入力
```

## 2. 手動公開（初回テスト用）

```bash
cd claude-code/vscode-extensions/paste-and-transform
npm install
npm run compile
vsce package
# paste-and-transform-1.0.0.vsix が生成される
vsce publish
```

## 3. GitHub Actions 自動公開

### シークレット設定

リポジトリの Settings → Secrets → Actions に以下を追加:

```
VSCE_PAT=<Azure DevOps PAT>
```

### 公開トリガー

Gitタグをpushすると自動公開される:

```bash
cd claude-code/vscode-extensions/paste-and-transform
git tag paste-and-transform-v1.0.0
git push origin paste-and-transform-v1.0.0
```

### ワークフロー内容

各拡張の `.github/workflows/publish.yml` に定義済み:
1. タグpush検知
2. `npm install` + `npm run compile`
3. `vsce publish`

## 4. バージョンアップ手順

1. `package.json` の `version` を更新
2. `CHANGELOG.md` に変更内容を追記
3. コミット＆新タグをpush

```bash
# 例: paste-and-transform v1.1.0
cd claude-code/vscode-extensions/paste-and-transform
# package.json の version を "1.1.0" に変更
# CHANGELOG.md を更新
git add -A && git commit -m "paste-and-transform v1.1.0"
git tag paste-and-transform-v1.1.0
git push origin main --tags
```

## 5. トラブルシューティング

| 問題 | 解決策 |
|------|--------|
| `vsce publish` が403 | PATのスコープに Marketplace > Manage があるか確認 |
| `publisher not found` | `vsce login miccho27` を再実行 |
| GitHub Actions失敗 | リポジトリSecrets に `VSCE_PAT` が設定されているか確認 |
| vsixが大きすぎる | `.vscodeignore` に `node_modules/`, `src/` を追加 |
