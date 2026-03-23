# VS Code Extensions 事業

## 概要

VS Code Marketplace向け拡張機能10本を開発・公開するポートフォリオ事業。
Chrome拡張と同様、Rick Blyth方式（量産×放置）で運用コスト$0を目指す。

## Publisher情報

- **Publisher ID**: miccho27
- **Marketplace**: https://marketplace.visualstudio.com/publishers/miccho27

## 拡張機能一覧

| # | 名前 | ステータス | 概要 |
|---|------|-----------|------|
| 1 | Paste & Transform | **完成** | クリップボード変換（camelCase, Base64, JSON等） |
| 2 | Console Cleaner | **完成** | console.log/debugger一括検出・削除・コメントアウト |
| 3 | ENV Lens | **完成** | .envファイル比較・分析・.env.example生成 |
| 4 | Commit Crafter | scaffold | Git commit メッセージテンプレート＆生成 |
| 5 | File Sticky Notes | scaffold | ファイルに付箋メモを貼る |
| 6 | Markdown Table Pro | scaffold | Markdownテーブルのフォーマット・ソート・CSV変換 |
| 7 | API Response Viewer | scaffold | APIレスポンスをツリービューで可視化 |
| 8 | i18n Helper | scaffold | 多言語キーの補完・未翻訳検出 |
| 9 | Smart Folding | scaffold | カスタムリージョン折りたたみ |
| 10 | Doc Snapshot | scaffold | ドキュメントのスナップショット差分 |

## 公開フロー

1. Gitタグ `ext-name-v1.0.0` をpush
2. GitHub Actionsが自動で `vsce package` → `vsce publish`
3. Marketplace に自動公開

## 収益戦略

- **無料公開**: 全拡張は無料（インストール数最大化）
- **GitHub Sponsors**: プロフィールリンクから誘導
- **プレミアム版（将来）**: 一部拡張でライセンスキー販売
