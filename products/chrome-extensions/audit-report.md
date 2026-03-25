# Chrome拡張 監査レポート（2026-03-25）

## 全10本ステータス一覧

| # | 拡張名 | バージョン | ステータス | 権限 | リスク |
|---|--------|-----------|-----------|------|--------|
| 1 | Regex Tester | 1.1.0 | **公開済み** | storage | なし |
| 2 | AI Text Rewriter | 1.1.0 | **公開済み** | activeTab, storage, contextMenus | なし |
| 3 | JSON Formatter Pro | 1.0.0 | 審査中 | activeTab, storage + content_scripts(`<all_urls>`) | **高** |
| 4 | Color Picker & Converter | 1.0.0 | 審査中 | storage | なし |
| 5 | Lorem Ipsum Generator | 1.0.0 | 審査中 | なし | なし |
| 6 | Hash & Encode Tool | 1.0.0 | 審査中 | activeTab, contextMenus, storage | なし |
| 7 | Page Speed Checker | 1.0.0 | 審査中 | activeTab | なし |
| 8 | Quick Currency Converter | 1.0.0 | 審査中 | activeTab, storage, contextMenus | **中** |
| 9 | SEO Inspector | 1.0.0 | 審査中 | activeTab | なし |
| 10 | Domain WHOIS Lookup | 1.0.0 | 審査中 | activeTab, storage | なし |

## 公開済み2本のストアURL

- **Regex Tester**: Gumroad Pro版 → https://tatsuya27.gumroad.com/l/regex-tester-pro
- **AI Text Rewriter**: Gumroad Pro版 → https://tatsuya27.gumroad.com/l/ai-text-rewriter-pro
- Chrome Web StoreのURLは Developer Dashboard で確認が必要

## 審査通過を妨げる可能性のある問題

### 問題1: JSON Formatter Pro — `<all_urls>` content_script（高リスク）

**現状**: `content_scripts.matches` に `<all_urls>` を使用。全ページにcontent.jsとcontent.cssが注入される。

**なぜ問題か**:
- Chrome Web Storeは `<all_urls>` content_scriptを最も厳しく審査する
- 2024年以降のポリシー強化で、broad host permissionsは追加の正当性説明が必要
- 審査期間が大幅に延長される（数週間〜数ヶ月）

**content.jsの実態**: JSON自動検出のみ。`document.contentType` が `json` か、`<pre>` タグ内のJSON文字列を検出してフォーマットする。外部通信なし、データ収集なし。

**修正案（審査が通らない場合）**:
1. content_scriptを削除し、popup + `activeTab` のみで動作する方式に変更
2. ユーザーがアイコンクリック → activeTabで現在ページのテキストを取得 → JSON検出・フォーマット
3. 自動検出機能は失われるが、審査通過率は大幅に向上

### 問題2: Quick Currency Converter — `host_permissions` 未定義（中リスク）

**現状**: `background.js` が以下の外部APIにfetchしている：
- `https://api.exchangerate-api.com/v4/latest/`
- `https://currency-exchange-api.t-mizuno27.workers.dev/rates?base=`

**なぜ問題か**:
- MV3では外部APIへのfetchに `host_permissions` の宣言が必要
- 未宣言の場合、CORS/ネットワークエラーで実行時に失敗する可能性がある
- 審査で「undeclared host access」として却下される可能性あり

**修正案**: manifest.jsonに以下を追加：
```json
"host_permissions": [
  "https://api.exchangerate-api.com/*",
  "https://currency-exchange-api.t-mizuno27.workers.dev/*"
]
```

### その他（問題なし）

残り6本（Color Picker, Lorem Ipsum, Hash & Encode, Page Speed, SEO Inspector, WHOIS Lookup）は権限・構造ともにクリーン。審査が遅い場合は単純にキュー待ちの可能性が高い。

## ストアリスティング改善案

### 全拡張共通の改善ポイント

1. **タイトル最適化**: Chrome Web Storeの検索はタイトルを最重視。主要キーワードを先頭に配置
2. **説明文1行目**: ストア一覧で表示される最初の1行が最も重要。「何ができるか」を端的に
3. **スクリーンショット**: 既に全拡張にあるが、以下を追加推奨
   - Before/After比較画像
   - 機能ハイライト付きの注釈画像
   - ダークモード対応の拡張はダークモード版も

### 個別改善案

| 拡張 | 現タイトル | 改善案タイトル | スクリーンショット指示 |
|------|-----------|--------------|---------------------|
| JSON Formatter Pro | JSON Formatter Pro | JSON Formatter & Viewer - Syntax Highlight | JSON自動検出のBefore/After、ツリー折りたたみ操作 |
| Color Picker | Color Picker & Converter | Color Picker - HEX RGB HSL Converter & Contrast | カラーピッカーUI、変換結果、コントラストチェック画面 |
| Lorem Ipsum | Lorem Ipsum Generator | Lorem Ipsum Generator - Quick Dummy Text | 生成画面、ワンクリックコピー操作 |
| Hash & Encode | Hash & Encode Tool | Hash Generator & Encoder - MD5 SHA Base64 | 各アルゴリズムの出力画面 |
| Page Speed | Page Speed Checker | Page Speed Test - Core Web Vitals Checker | スコア表示画面、CWV結果画面 |
| Currency Converter | Quick Currency Converter | Currency Converter - 160+ Currencies Real-Time | 変換UI、右クリックメニュー |
| SEO Inspector | SEO Inspector - Instant SEO Analysis | SEO Checker - One-Click SEO Score & Audit | スコア画面、チェックリスト画面 |
| WHOIS Lookup | Domain WHOIS Lookup | WHOIS Lookup - Domain Info DNS & SSL Check | WHOIS結果、DNS表示、SSL情報 |

## 次のアクション（優先順）

1. **Currency Converter**: `host_permissions` を追加 → 再パッケージ → CWSに再アップロード
2. **Developer Dashboard確認**: 8本の審査ステータスを目視確認（却下されていれば理由を確認）
3. **JSON Formatter Pro**: 却下されていた場合、content_scriptを削除してactiveTab方式に変更
4. **全拡張**: タイトル最適化を適用（ストア掲載情報から編集可能、再審査不要）
5. **スクリーンショット追加**: 上記の指示に従って各拡張2-3枚追加
