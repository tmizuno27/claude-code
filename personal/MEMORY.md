# Memory - GitHub ワークスペース

## リポジトリ構成
- `c:\Users\tmizu\マイドライブ\GitHub\data` → https://github.com/tmizuno27/data.git (branch: main)

## GitHub自動同期 (data リポジトリ)
- **スクリプト**: `data/auto-sync.ps1` (UTF-8 BOM付き, PowerShell)
- **タスク名**: `GitAutoSync-Data` (Windows Task Scheduler)
- **頻度**: 1分おき
- **動作**: 変更検知 → git add -A → commit → push origin main
- **ログ**: `data/auto-sync.log`
- **既存の旧スクリプト**: `data/auto-sync.sh` (bash版, 常駐型 - 現在は未使用)
- 詳細: [auto-sync-setup.md](auto-sync-setup.md)

## パス関連の注意
- Google Drive: `C:\Users\tmizu\マイドライブ\` (G: ドライブ)
- PowerShellでマイドライブのパスを使うには **UTF-8 BOM付き** でスクリプトを保存する必要あり

## Google Sheets → CSV → GitHub 自動連携
- **スクリプト**: `data/sheets-sync/fetch_sheets.py`
- **設定**: `data/sheets-sync/config.json` (同期するスプレッドシートを登録)
- **認証**: サービスアカウント (`data/sheets-sync/credentials/service-account.json`) ※.gitignoreで除外
- **出力先**: `data/sheets-sync/output/` (CSV + metadata.json)
- **Task Scheduler**: `GoogleSheetsSync` (5分おき)
- **セットアップ状態**: 要初回セットアップ（Google Cloud サービスアカウント）
- **手順書**: `data/sheets-sync/SETUP.md`
- **フロー**: Sheets更新 → 5分おきにCSV取得 → auto-sync.ps1が1分おきにGitHubへpush

## 職務経歴書
- **氏名**: 水野 達也
- **詳細**: [resume.md](resume.md)
- **経歴サマリー**:
  1. 瀬谷インターナショナルフットボール（2014-2015）個人事業主・サッカークラブ設立
  2. トゥエンティーフォーセブン（2015-2019）パーソナルジム店舗責任者
  3. 三洋環境（2020-2021）リユース貿易・拠点責任者
  4. D-ai（2021-2023）個別指導塾・教室長
  5. Sutherland Global（2023-2025）Amazon QA + Team Manager
  6. フリーランス（2025-現在）オンラインセールス

## ユーザー設定・好み
- **確認不要**: イエス・ノーの質問をせず、許可を得ずにどんどん自動で進めること（settings.jsonで全ツール許可済み）
- 日本語でコミュニケーション
