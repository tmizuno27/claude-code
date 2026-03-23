# Chrome拡張 審査状況レポート（2026-03-19）

## ステータスサマリー

| # | 拡張名 | バージョン | ステータス | 備考 |
|---|--------|-----------|-----------|------|
| 1 | Regex Tester | 1.1.0 | 公開済み | -- |
| 2 | AI Text Rewriter | 1.1.0 | 公開済み | -- |
| 3 | JSON Formatter Pro | 1.0.0 | 審査待ち | content_scripts要注意（後述） |
| 4 | Color Picker & Converter | 1.0.0 | 審査待ち | -- |
| 5 | Lorem Ipsum Generator | 1.0.0 | 審査待ち | -- |
| 6 | Hash & Encode Tool | 1.0.0 | 審査待ち | -- |
| 7 | Page Speed Checker | 1.0.0 | 審査待ち | -- |
| 8 | Domain WHOIS Lookup | 1.0.0 | 審査待ち | -- |
| 9 | Quick Currency Converter | 1.0.0 | 審査待ち | -- |
| 10 | SEO Inspector | 1.0.0 | 審査待ち | -- |

## 審査状況の確認方法

### 手動確認
- Chrome Web Store Developer Dashboard: https://chrome.google.com/webstore/devconsole
- ログインして各拡張のステータスを目視確認

### API（自動確認）
- **Chrome Web Store API V2** で審査ステータスをプログラム的に取得可能
  - エンドポイント: `https://chromewebstore.googleapis.com/v2/publishers/{PUBLISHER_ID}/items/{EXTENSION_ID}:fetchStatus`
  - サービスアカウント対応（CI/CD連携可能）
  - V1は2026年10月15日に廃止予定、V2への移行推奨
- 参考: https://developer.chrome.com/docs/webstore/using-api
- 参考: https://developer.chrome.com/blog/cws-api-v2

### 審査期間の目安
- 通常: 数日〜2週間
- 初回提出やsensitive permissionsがある場合はさらに長くなる可能性あり
- 参考: https://developer.chrome.com/docs/webstore/review-process

## manifest.json チェック結果

全10拡張ともManifest V3準拠。個別の所見は以下の通り。

### 問題なし（8本）

| 拡張 | permissions | 所見 |
|------|------------|------|
| Regex Tester | `storage` | 最小権限、問題なし |
| AI Text Rewriter | `activeTab`, `storage`, `contextMenus` | 全て必要な権限、問題なし |
| Color Picker & Converter | `storage` | 最小権限、問題なし |
| Lorem Ipsum Generator | `clipboardWrite` | 用途に合致、問題なし |
| Hash & Encode Tool | `activeTab`, `contextMenus` | 用途に合致、問題なし |
| Page Speed Checker | `activeTab` | 最小権限、問題なし |
| Domain WHOIS Lookup | `activeTab`, `storage` | 問題なし |
| SEO Inspector | `activeTab` | 最小権限、問題なし |

### 要注意（2本）

#### JSON Formatter Pro — `<all_urls>` content_script
```json
"content_scripts": [{
  "matches": ["<all_urls>"],
  "js": ["content.js"],
  "css": ["content.css"],
  "run_at": "document_end"
}]
```
- **リスク**: `<all_urls>` のcontent_scriptは全ページに注入されるため、審査が厳格になる
- **対策案**: JSON検出時のみ動作するなら、`matches`を`["*://*/*"]`に変更し、プライバシーポリシーのURLをストア掲載情報に追加する。または、content_scriptをやめてaction popupからactiveTabで取得する方式に変更
- **却下リスク**: 中程度。理由が明確（JSONの自動フォーマット）なので通る可能性はあるが、プライバシーポリシー未設定だと却下される可能性あり

#### Quick Currency Converter — `contextMenus` + `activeTab`
- 権限自体は問題ないが、`contextMenus` + `activeTab` + `storage` の3権限の組み合わせは普通
- 為替レートの取得先API（外部通信）がある場合、`host_permissions`が未定義だと実行時エラーの可能性あり
- **確認推奨**: background.jsで外部APIを呼んでいるか確認し、必要なら`host_permissions`を追加

## 次のアクション

1. **Developer Dashboard確認**: https://chrome.google.com/webstore/devconsole で8本の審査状態を目視確認
2. **JSON Formatter Pro**: content_scriptの`<all_urls>`が原因で却下された場合、activeTab方式へ変更して再提出
3. **Currency Converter**: 外部API通信がある場合、`host_permissions`を追加
4. **全拡張共通**: プライバシーポリシーのURLがストア掲載情報に設定されているか確認（content_scriptを使う拡張は必須）
5. **API自動化検討**: Chrome Web Store API V2でステータス自動取得スクリプトを作成すれば、毎日自動チェック可能
