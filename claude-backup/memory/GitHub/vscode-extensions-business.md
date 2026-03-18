---
name: VS Code拡張ポートフォリオ事業
description: VS Code Marketplace に10本の拡張を公開済み（7/10本）。残り3本はレート制限解除後に公開
type: project
---

VS Code拡張10本をMarketplaceに公開する事業（2026-03-16構築・公開）

**Why:** Chrome拡張と同じ量産×放置戦略の横展開。運用コスト$0。

**How to apply:** `claude-code/vscode-extensions/` 配下。Publisher: miccho27 + miccho27-dev

## Publisher情報
- メインPublisher: `miccho27`（Azure DevOps PAT取得済み）
- サブPublisher: `miccho27-dev`（10本公開済み、将来統合予定）
- メール: t.mizuno27@gmail.com

## 公開状況（2026-03-16）

| # | 名前 | miccho27 | miccho27-dev |
|---|------|----------|-------------|
| 1 | Paste & Transform | 公開済み | 公開済み |
| 2 | Debug Log Cleaner | 公開済み | 公開済み |
| 3 | Env File Lens | 公開済み | 公開済み |
| 4 | Commit Crafter | 公開済み | 公開済み |
| 5 | File Sticky Notes | 公開済み | 公開済み |
| 6 | Markdown Table Pro | 公開済み | 公開済み |
| 7 | API Response Viewer | 公開済み | 公開済み |
| 8 | i18n Helper | **未公開（レート制限）** | 公開済み |
| 9 | Smart Folding | **未公開（レート制限）** | 公開済み |
| 10 | Doc Snapshot | **未公開（レート制限）** | 公開済み |

## 残り3本の公開コマンド
```bash
cd claude-code/vscode-extensions/i18n-helper && npx @vscode/vsce publish --pat "$PAT" --packagePath *.vsix
cd claude-code/vscode-extensions/smart-folding && npx @vscode/vsce publish --pat "$PAT" --packagePath *.vsix
cd claude-code/vscode-extensions/doc-snapshot && npx @vscode/vsce publish --pat "$PAT" --packagePath *.vsix
```

## 収益目標
月$50〜$300（6ヶ月後）— GitHub Sponsors + ライセンスキー
