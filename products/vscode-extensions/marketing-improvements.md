# VS Code拡張 マーケティング改善計画

## 現状（2026-03-25取得）

| 拡張名 | Publisher | Installs | 状態 |
|--------|-----------|----------|------|
| M27 API Response Viewer | miccho27 | 0 | 要改善 |
| M27 Commit Crafter | miccho27 | 0 | 要改善 |
| M27 Debug Log Cleaner | miccho27-dev | 0 | 要改善 |
| M27 Doc Snapshot | miccho27 | 0 | 要改善 |
| M27 Env File Lens | miccho27-dev | 0 | 要改善 |
| M27 File Sticky Notes | miccho27 | 1 | 要改善 |
| M27 i18n Helper | miccho27 | 0 | 要改善 |
| M27 Markdown Table Pro | miccho27 | 1 | 要改善 |
| M27 Paste & Transform | miccho27-dev | 0 | 要改善 |
| M27 Smart Folding | miccho27 | 0 | 要改善 |

**合計インストール数: 2** — 全拡張がほぼゼロ。根本的な改善が必要。

## 問題分析

### 1. Publisher分散問題（最優先）
- `miccho27` と `miccho27-dev` の2つに分散している
- ブランド認知が分散し、ユーザーが同シリーズと認識できない
- **対策**: `miccho27` に統一。miccho27-devの3本（console-cleaner, env-lens, paste-and-transform）を移行

### 2. 発見性の低さ
- 拡張名に「M27」プレフィックスがあるが、検索で見つかりにくい
- 検索される用語（例: "json viewer", "commit message", "env file"）がdisplayNameに含まれていない場合がある
- **対策**: keywordsフィールドの最適化、description冒頭に検索用語を入れる

### 3. README/説明文の改善が必要
- Marketplaceページの第一印象はREADMEで決まる
- GIF/スクリーンショットが不足している可能性

## 拡張別改善案

### M27 API Response Viewer（優先度: 高）
- **競合**: REST Client, Thunder Client等が強い
- **改善案**:
  - displayName案: "API Response Viewer - JSON/XML Tree Explorer"
  - keywords追加: `json viewer`, `api response`, `rest`, `xml`, `tree view`
  - READMEに操作GIF追加（JSON展開/検索/フィルタリングのデモ）
  - description改善: "Instantly visualize JSON/XML API responses as interactive trees. Search, filter, and copy paths with one click."

### M27 Commit Crafter（優先度: 高）
- **競合**: Conventional Commits, Git Commit Plugin
- **改善案**:
  - displayName案: "Commit Crafter - Smart Commit Message Generator"
  - keywords追加: `git`, `commit message`, `conventional commits`, `gitmoji`, `changelog`
  - READMEにcommitメッセージ生成のGIF
  - description改善: "Auto-generate conventional commit messages from staged changes. Supports gitmoji, scopes, and breaking change detection."

### M27 Debug Log Cleaner（優先度: 中）
- **ニッチだが需要あり**: コードレビュー前のクリーンアップ
- **改善案**:
  - displayName案: "Debug Log Cleaner - Remove console.log & print()"
  - keywords: `console.log`, `debugger`, `print`, `clean`, `remove logs`, `code cleanup`
  - description改善: "One-click removal of console.log, debugger, and print() statements. Comment-out mode available. Supports JS/TS/Python/Java."

### M27 Env File Lens（優先度: 高）
- **需要大**: .envファイル管理は多くの開発者が困っている
- **改善案**:
  - displayName案: "Env File Lens - .env Manager & Secret Scanner"
  - keywords: `dotenv`, `env`, `environment variables`, `secrets`, `.env`, `configuration`
  - description改善: "Browse, compare, and secure .env files. Detect missing keys across environments, find exposed secrets, and auto-generate .env.example."

### M27 Paste & Transform（優先度: 高）
- **実用性高い**: 日常的に使う変換機能
- **改善案**:
  - displayName案: "Paste & Transform - camelCase, snake_case, Base64 & More"
  - keywords: `paste`, `transform`, `camelCase`, `snake_case`, `base64`, `json format`, `url encode`
  - description改善: "Paste with instant text transformations. Convert between camelCase, snake_case, PascalCase, Base64, JSON, URL encoding, and more."

### M27 Markdown Table Pro（優先度: 中）
- **競合**: Markdown All in One内のテーブル機能
- **改善案**:
  - displayName案: "Markdown Table Pro - Format, Sort & Convert Tables"
  - keywords: `markdown`, `table`, `csv`, `sort`, `align`, `format`
  - 特にCSVインポート/エクスポートを強調

### M27 File Sticky Notes（優先度: 中）
- **ユニーク**: 類似拡張が少ない差別化ポイント
- **改善案**:
  - displayName案: "File Sticky Notes - Code Annotations & Bookmarks"
  - keywords: `notes`, `annotations`, `bookmarks`, `comments`, `sticky`, `todo`
  - コードレビュー用途を強調

### M27 Doc Snapshot（優先度: 低）
- **改善案**: "Doc Snapshot - File Version History & Diff" に改名
- ローカルGitなしで使える点を強調

### M27 i18n Helper（優先度: 低）
- **競合が多い**: i18n Ally等の強力な競合あり
- **差別化**: 軽量・シンプルさを訴求

### M27 Smart Folding（優先度: 低）
- **改善案**: "Smart Folding - Fold by Type: Imports, Functions, Classes"
- VS Codeの標準折りたたみとの差を明確に

## 全体アクションプラン

### Phase 1: 即実行（今週中）
1. [ ] 全拡張のkeywords最適化（package.json）
2. [ ] description冒頭を検索用語重視に書き換え
3. [ ] Publisher統一（miccho27-devの3本をmiccho27に移行）

### Phase 2: README強化（来週）
4. [ ] 各拡張のREADMEにGIF/スクリーンショット追加
5. [ ] Features一覧を箇条書きで明確化
6. [ ] "Before/After" セクション追加（特にDebug Log Cleaner, Paste & Transform）

### Phase 3: 集客（再来週以降）
7. [ ] Dev.toに各拡張の紹介記事投稿（5本）
8. [ ] Reddit r/vscode に投稿（ルール遵守、宣伝的にならないよう注意）
9. [ ] X (@prodhq27) で定期的にTips投稿と拡張紹介

### Phase 4: 機能改善
10. [ ] 各拡張のGitHub Issuesで機能リクエストを収集
11. [ ] 最もDL数が伸びた拡張に注力して機能追加

## X API制限メモ
- Free Tierでは投稿API（POST tweets）が利用不可の場合あり
- Basic plan ($100/mo) で月17,000ツイート投稿可能
- 現在のアカウント: @prodhq27（Free Tier想定）
- 拡張の宣伝はまず手動投稿で開始し、効果を見てからAPI利用を検討
