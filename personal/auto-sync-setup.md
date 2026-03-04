# GitHub自動同期 セットアップ詳細

## 概要
`data` リポジトリ内のファイル変更を1分おきに自動でGitHubへ反映する仕組み。

## 構成
1. **PowerShellスクリプト**: `data/auto-sync.ps1`
   - UTF-8 BOM付きで保存（マイドライブのパス対応）
   - 変更がなければ何もしない（ログも出さない）
   - 変更があれば `git add -A` → `commit` → `push`
   - ログは `data/auto-sync.log` に記録

2. **Windows Task Scheduler**: タスク名 `GitAutoSync-Data`
   - 1分おきに実行
   - 登録コマンド:
     ```
     MSYS_NO_PATHCONV=1 schtasks.exe /Create /TN "GitAutoSync-Data" /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File \"C:\Users\tmizu\マイドライブ\GitHub\data\auto-sync.ps1\"" /SC MINUTE /MO 1 /F
     ```
   - Git Bashから登録する場合は `MSYS_NO_PATHCONV=1` が必要（パス変換防止）

## トラブルシューティング
- **PowerShellでマイドライブのパスが見つからない**: スクリプトがUTF-8 BOM付きで保存されているか確認
- **タスクが動かない**: `schtasks.exe /Query /TN "GitAutoSync-Data"` で状態確認
- **ログ確認**: `cat data/auto-sync.log`

## 停止・削除方法
- 一時停止: `MSYS_NO_PATHCONV=1 schtasks.exe /Change /TN "GitAutoSync-Data" /DISABLE`
- 再開: `MSYS_NO_PATHCONV=1 schtasks.exe /Change /TN "GitAutoSync-Data" /ENABLE`
- 削除: `MSYS_NO_PATHCONV=1 schtasks.exe /Delete /TN "GitAutoSync-Data" /F`
