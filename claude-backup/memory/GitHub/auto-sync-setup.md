# GitHub自動同期 セットアップ詳細

## 概要
`data` リポジトリ内のファイル変更を1分おきに自動でGitHubへ反映する仕組み。

## 構成（2026-03-03修正済み）

### 実行チェーン
```
Task Scheduler (GitAutoSync-Data)
  → wscript.exe auto-sync-hidden.vbs   ← ウィンドウ非表示化
    → powershell.exe scripts/auto-sync.ps1  ← ASCIIパスのスクリプト
      → git add -A → commit → push
```

### ファイル一覧
1. **`C:\Users\tmizu\scripts\auto-sync.ps1`** (メインスクリプト)
   - 日本語パスを**Unicodeコードポイント**で構築（`[char]0x30DE` 等）
   - ファイル自体にはASCII文字のみ → エンコーディング問題を回避
   - 変更がなければ `exit 0`（ログ出力なし）
   - 変更があれば `git add -A` → `commit` → `push`
   - ログは `data/auto-sync.log` に記録

2. **`C:\Users\tmizu\scripts\auto-sync-hidden.vbs`** (VBSランチャー)
   - PowerShellをウィンドウ非表示で起動
   - 日本語パスを含まない構成

3. **`C:\Users\tmizu\マイドライブ\GitHub\data\auto-sync.ps1`** (旧スクリプト・使用停止)
   - UTF-8 BOM付き保存が必要だったがTask Scheduler経由で文字化け問題があった

### Task Scheduler設定
- **タスク名**: `GitAutoSync-Data`
- **アクション**: `wscript.exe "C:\Users\tmizu\scripts\auto-sync-hidden.vbs"`
- **トリガー**: 1分おき
- **設定改善点** (2026-03-03):
  - `AllowStartIfOnBatteries: True` (バッテリー駆動でも実行)
  - `DontStopIfGoingOnBatteries: True` (バッテリー切替時も継続)
  - `StartWhenAvailable: True` (実行逃し時にリカバリ)

## 日本語パス問題の解決策
**問題**: Task Scheduler → VBS → PowerShell の経路で、ファイルパスに日本語（マイドライブ）が含まれるとエンコーディングが壊れる
**解決**: スクリプト内で `[char]0x30DE + [char]0x30A4 + ...` のようにUnicodeコードポイントからパスを動的に構築

## トラブルシューティング
- **スクリプトが動かない**: `powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\tmizu\scripts\auto-sync.ps1"` で直接テスト
- **タスク状態確認**: `powershell -Command "Get-ScheduledTask -TaskName 'GitAutoSync-Data' | Get-ScheduledTaskInfo"`
- **ログ確認**: `tail data/auto-sync.log`

## 停止・削除方法
- PowerShellで: `Set-ScheduledTask -TaskName 'GitAutoSync-Data' -Settings (New-ScheduledTaskSettingsSet -Disable)`
- 削除: `Unregister-ScheduledTask -TaskName 'GitAutoSync-Data' -Confirm:$false`
