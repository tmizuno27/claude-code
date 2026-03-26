# Chrome拡張 審査改善レポート (2026-03-26)

## 状況
- 8本が2026-03-16〜17に提出後、10日経過しても審査待ち
- 公開済み2本: Regex Tester, AI Text Rewriter

## 実施した改善

### 1. プライバシーポリシーURL（最重要）

**問題**: Chrome Web Storeではプライバシーポリシーの**公開URL**が必要。ローカルHTMLファイルのみでは不十分。SEO Inspector以外の7本にはホスティングされたプライバシーポリシーがなかった可能性。

**対応**: `infrastructure/homepage/` にGitHub Pages用のプライバシーポリシーHTMLを7本分作成。

| 拡張 | プライバシーポリシーURL |
|------|----------------------|
| JSON Formatter Pro | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-json-formatter.html` |
| Color Picker | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-color-picker.html` |
| Lorem Ipsum Generator | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-lorem-ipsum-generator.html` |
| Hash & Encode Tool | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-hash-encode-tool.html` |
| Page Speed Checker | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-page-speed-checker.html` |
| Currency Converter | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-currency-converter.html` |
| WHOIS Lookup | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-whois-lookup.html` |
| SEO Inspector | `https://tmizuno27.github.io/claude-code/infrastructure/homepage/privacy-policy-seo-inspector.html`（既存） |

### 2. manifest.json 権限監査

| 拡張 | 権限 | 判定 |
|------|------|------|
| JSON Formatter Pro | activeTab, storage + content_scripts(all_urls) | **要注意**: `<all_urls>`は追加審査対象だがJSON自動検出に必須。正当な使い方 |
| Color Picker | storage | 最小限 OK |
| Lorem Ipsum Generator | なし | 最小限 OK |
| Hash & Encode Tool | contextMenus, storage | 最小限 OK |
| Page Speed Checker | activeTab | 最小限 OK |
| Currency Converter | activeTab, storage, contextMenus | 最小限 OK |
| SEO Inspector | activeTab | 最小限 OK |
| WHOIS Lookup | activeTab, storage | 最小限 OK |

**結論**: 全拡張の権限は適切。不要な権限なし。

### 3. 説明文品質チェック

全8本とも以下を満たしている:
- 機能説明が具体的
- HOW IT WORKS セクションあり
- PRIVACY セクションあり
- ターゲットユーザー記載あり

## ユーザーへの手動アクション（必須）

### Step 1: GitHub Pagesを有効化
リポジトリ `tmizuno27/claude-code` の Settings > Pages で:
- Source: `Deploy from a branch`
- Branch: `main` / `/ (root)` または `main` / `/infrastructure/homepage`

### Step 2: Chrome Developer Dashboardで各拡張のプライバシーポリシーURLを設定
1. https://chrome.google.com/webstore/devconsole にアクセス
2. 各拡張の「Store listing」→「Privacy」タブ
3. 「Privacy policy URL」に上記表のURLを入力
4. 保存

### Step 3: 審査ステータス確認
- Developer Dashboard で各拡張のステータスを確認
- 「Rejected」があれば拒否理由を確認して対応
- 「Pending review」のままなら、プライバシーポリシーURL設定後に再提出

### Step 4: JSON Formatter Pro 追加対応（審査が拒否された場合のみ）
`<all_urls>` content_scripts が拒否された場合:
- `host_permissions` + `optional_host_permissions` パターンに変更
- または content_scripts を削除しpopupのみの動作に変更

## 審査が遅い原因の可能性
1. **プライバシーポリシーURL未設定**（最有力）
2. **大量一括提出**（10本同時は審査キュー待ち）
3. **新規デベロッパーアカウント**（初回審査は厳しい）
4. **JSON Formatter Proの`<all_urls>`**（追加審査対象）
