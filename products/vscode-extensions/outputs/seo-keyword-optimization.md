# VS Code Extension SEO Keyword Optimization Guide

> 10本全公開済み、全拡張インストール数0-1。Marketplace検索で発見されるためのキーワード最適化。

## 現状分析

| 拡張 | DL数 | Install | 課題 |
|------|------|---------|------|
| M27 API Response Viewer | 19 | 0 | 名前が汎用的すぎ |
| M27 Commit Crafter | 19 | 0 | 「commit message」で検索されにくい |
| M27 Console Cleaner | 18 | 0 | ニッチだが需要あり |
| M27 Doc Snapshot | 19 | 0 | 機能が伝わりにくい |
| M27 ENV Lens | 19 | 0 | .envファイル関連は需要あり |
| M27 File Sticky Notes | 19 | 1 | 唯一のインストール |
| M27 i18n Helper | 19 | 0 | i18n市場は競合多数 |
| M27 Markdown Table Pro | 19 | 1 | Markdown需要あり |
| M27 Smart Folding | 19 | 0 | コードフォールディング需要あり |
| Paste & Transform | 19 | 1 | ブランド名なし、発見されやすい |

## 重要な発見

- **「M27」プレフィックスが検索ノイズ**: ユーザーは「api response viewer」で検索する。「M27」は検索に貢献しない
- **Paste & Transform が唯一ブランド名なし→唯一インストール1**: 相関あり
- **全拡張 downloads=19前後**: ボットまたはインデックス巡回のみ

## 改善推奨（package.json の keywords + description）

### 1. M27 API Response Viewer
**現在の検索可能性**: 低
**推奨 keywords**: `["api", "rest", "json", "response", "viewer", "http", "prettify", "format", "debug", "endpoint"]`
**推奨 displayName**: `API Response Viewer — Format & Debug REST APIs`
**推奨 description**: `View, format, and debug REST API responses directly in VS Code. Pretty-print JSON, XML, and HTML responses with syntax highlighting.`

### 2. M27 Commit Crafter
**推奨 keywords**: `["commit", "message", "git", "conventional", "changelog", "commit message", "template", "semantic", "version"]`
**推奨 displayName**: `Commit Crafter — AI-Powered Git Commit Messages`
**推奨 description**: `Generate conventional commit messages with AI. Follows Conventional Commits spec. Supports custom templates, scopes, and breaking change detection.`

### 3. M27 Console Cleaner
**推奨 keywords**: `["console", "log", "debug", "clean", "remove", "console.log", "debugger", "production", "lint"]`
**推奨 displayName**: `Console Cleaner — Remove console.log Before Deploy`
**推奨 description**: `Find and remove all console.log, console.warn, console.error, and debugger statements in one click. Clean your code before production.`

### 4. M27 Doc Snapshot
**推奨 keywords**: `["documentation", "snapshot", "markdown", "export", "readme", "docs", "generate", "code documentation"]`
**推奨 displayName**: `Doc Snapshot — Export Code Documentation Instantly`
**推奨 description**: `Generate documentation snapshots from your codebase. Export functions, classes, and modules to Markdown with one command.`

### 5. M27 ENV Lens
**推奨 keywords**: `["env", "environment", "variables", "dotenv", ".env", "secrets", "config", "hover", "definition"]`
**推奨 displayName**: `ENV Lens — See .env Values Inline`
**推奨 description**: `Hover over environment variable references to see their values. Supports .env, .env.local, .env.production. Warns about missing variables.`

### 6. M27 File Sticky Notes
**推奨 keywords**: `["notes", "annotation", "bookmark", "comment", "todo", "sticky", "file notes", "code notes", "memo"]`
**推奨 displayName**: `File Sticky Notes — Add Notes to Any File`
**推奨 description**: `Attach sticky notes to any file in your project. Notes persist across sessions. Perfect for code reviews, onboarding, and personal reminders.`

### 7. M27 i18n Helper
**推奨 keywords**: `["i18n", "internationalization", "translation", "locale", "localize", "react-intl", "i18next", "multilingual"]`
**推奨 displayName**: `i18n Helper — Internationalization Made Easy`
**推奨 description**: `Manage translations, find missing keys, and extract hardcoded strings. Supports JSON, YAML, and PO formats. Works with i18next, react-intl, vue-i18n.`

### 8. M27 Markdown Table Pro
**推奨 keywords**: `["markdown", "table", "format", "align", "csv", "tsv", "table formatter", "markdown table", "column"]`
**推奨 displayName**: `Markdown Table Pro — Format & Align Tables`
**推奨 description**: `Format, align, and sort Markdown tables with one shortcut. Import from CSV/TSV. Auto-align columns. The fastest way to work with Markdown tables.`

### 9. M27 Smart Folding
**推奨 keywords**: `["folding", "collapse", "fold", "code folding", "region", "minimize", "sections", "outline", "navigation"]`
**推奨 displayName**: `Smart Folding — Intelligent Code Collapse`
**推奨 description**: `Intelligently fold code by functions, classes, imports, or custom patterns. Fold all tests, fold all comments, or create custom folding profiles.`

### 10. Paste & Transform
**推奨 keywords**: `["paste", "transform", "convert", "json", "csv", "case", "format", "clipboard", "camelCase", "snake_case"]`
**推奨 displayName 変更不要**: 現在の名前が最適
**推奨 description**: `Paste and transform clipboard content: JSON ↔ Object, CSV ↔ Table, camelCase ↔ snake_case, and more. 15+ transformations built in.`

## 実行手順

各拡張の `package.json` を更新して `vsce publish` するだけ。

```bash
# 例: Console Cleaner
cd m27-console-cleaner
# package.json の keywords, description を更新
vsce publish patch  # バージョンをパッチアップして公開
```

## 優先順位

1. **Paste & Transform** — 既にインストールあり、最もポテンシャル高い
2. **Console Cleaner** — 明確なユースケース、検索需要あり
3. **ENV Lens** — .env関連は日常的に使う
4. **Markdown Table Pro** — Markdown需要は安定
5. **File Sticky Notes** — ユニークなコンセプト
6. 残り5本

## 追加施策

- **README.md にGIF動画を追加**: Marketplace で最もインストール率を上げる要素
- **VS Code Marketplace のバッジ**: install count, rating, version バッジをREADMEに
- **Marketplace カテゴリ選択**: 各拡張で最適なカテゴリを選択（Formatters, Linters, Other等）
