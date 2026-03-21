# Chrome拡張 レビューステータス (2026-03-21)

## 全10本サマリー

| # | 拡張名 | バージョン | ステータス | MV3 | Permissions | リスク |
|---|--------|-----------|-----------|-----|-------------|--------|
| 1 | Regex Tester | 1.1.0 | 公開済み | OK | storage | なし |
| 2 | AI Text Rewriter | 1.1.0 | 公開済み | OK | activeTab, storage, contextMenus | なし |
| 3 | JSON Formatter Pro | 1.0.0 | 審査待ち | OK | activeTab, storage + content_scripts(all_urls) | 中 |
| 4 | Color Picker & Converter | 1.0.0 | 審査待ち | OK | storage | なし |
| 5 | Lorem Ipsum Generator | 1.0.0 | 審査待ち | OK | なし (修正済み) | なし |
| 6 | Hash & Encode Tool | 1.0.0 | 審査待ち | OK | activeTab, contextMenus | なし |
| 7 | Page Speed Checker | 1.0.0 | 審査待ち | OK | activeTab | なし |
| 8 | Quick Currency Converter | 1.0.0 | 審査待ち | OK | activeTab, storage, contextMenus | なし |
| 9 | SEO Inspector | 1.0.0 | 審査待ち | OK | activeTab | なし |
| 10 | Domain WHOIS Lookup | 1.0.0 | 審査待ち | OK | activeTab, storage | なし |

## 最終更新日

| 拡張名 | 最終更新 |
|--------|---------|
| Regex Tester | 2026-03-19 |
| AI Text Rewriter | 2026-03-19 |
| Color Picker | 2026-03-17 |
| Lorem Ipsum Generator | 2026-03-16 |
| Hash & Encode Tool | 2026-03-16 |
| Page Speed Checker | 2026-03-16 |
| JSON Formatter Pro | 2026-03-16 |
| WHOIS Lookup | 2026-03-16 |
| Currency Converter | 2026-03-16 |
| SEO Inspector | 2026-03-16 |

## 審査リスク分析

### 全拡張共通（問題なし）
- 全10本 Manifest V3 準拠
- 全10本 `store/privacy-policy.html` あり
- 全10本 `store/description.txt` + `short-description.txt` あり
- 全10本 スクリーンショット・プロモーション画像あり

### 修正済みの問題

#### Lorem Ipsum Generator - `clipboardWrite` 削除
- **問題**: `permissions` に `clipboardWrite` が設定されていたが、コードは `navigator.clipboard.writeText()` を使用しており不要
- **リスク**: MV3では `clipboardWrite` は非推奨。不要なpermissionは審査で拒否の原因になりうる
- **対応**: `permissions` を空配列 `[]` に修正済み
- **注意**: store/extension.zip の再パッケージが必要

### 要注意項目

#### JSON Formatter Pro - `content_scripts` with `<all_urls>`
- **状況**: JSON自動検出のため `content_scripts` の `matches` に `"<all_urls>"` を使用
- **リスク**: Chrome Web Storeでは `<all_urls>` は追加審査対象。審査が長引く可能性あり
- **正当性**: JSON自動検出は全URLへのアクセスが必要であり、descriptionでも適切に説明済み
- **データ送信**: なし（100%ローカル処理）。privacy-policyでも明記
- **対応**: 現状維持。審査で拒否された場合はオプショナルpermissionsへの変更を検討

## 次のアクション

1. **Lorem Ipsum Generator**: manifest.json修正済み → `store/extension.zip` を再パッケージしてCWSに再アップロード
2. **JSON Formatter Pro**: 審査結果を待つ。拒否された場合は `host_permissions` + `optional_permissions` パターンに変更
3. **全8本**: 審査ステータスをChrome Developer Dashboardで確認
