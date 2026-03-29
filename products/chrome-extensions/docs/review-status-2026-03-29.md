# Chrome拡張 審査・改善ステータス (2026-03-29)

## 現状サマリー

| # | 拡張名 | バージョン | ストアステータス | フリーミアム | PP URL |
|---|--------|-----------|----------------|------------|--------|
| 1 | AI Text Rewriter | 1.2.0 | 公開済み | 実装済み（Gumroad） | 設定済み |
| 2 | Regex Tester | 1.1.0 | 公開済み | 実装済み（Gumroad） | 設定済み |
| 3 | Color Picker & Converter | 1.0.0 | 審査中 | 未実装 | 設定済み |
| 4 | Quick Currency Converter | 1.0.0 | 審査中（再提出済み） | 未実装 | 設定済み |
| 5 | JSON Formatter Pro | 1.0.0 | 審査中 | 未実装 | 設定済み |
| 6 | Lorem Ipsum Generator | 1.0.0 | 審査中 | 未実装 | 設定済み |
| 7 | Page Speed Checker | 1.0.0 | 審査中 | 未実装 | 設定済み |
| 8 | SEO Inspector | 1.0.0 | 審査中 | 未実装 | 設定済み |
| 9 | Hash & Encode Tool | 1.1.0 | 審査中（再提出済み） | 未実装 | 設定済み |
| 10 | WHOIS Lookup | 1.0.0 | 審査中 | 未実装 | 設定済み |
| 11 | Tab Manager & Session Saver | 1.0.0 | 未提出（開発完了） | 実装済み（3セッション制限） | 設定済み |

**プライバシーポリシーURL**: 全11本、`https://homepage-three-ochre.vercel.app/privacy-policy-{ext}.html` で設定済み

---

## 2026-03-29 実施した改善

### 1. ストア説明文のSEO最適化

#### Regex Tester（大幅改善）
- Before: 686文字（機能リスト羅列、弱い）
- After: ~1,500文字（詳細機能説明、ターゲットユーザー明示、カテゴリ追記）
- 追加キーワード: "real-time regular expression testing", "capture groups", "pattern library", "developer tools"

#### Lorem Ipsum Generator（強化）
- Before: 758文字（薄い説明）
- After: ~1,400文字（フォーマット別詳細説明、デザイナー向けユースケース追加）
- 追加キーワード: "placeholder text", "Figma", "Sketch", "Adobe XD", "UI/UX designers"

#### AI Text Rewriter（強化）
- Before: 957文字（BYOKの説明不足）
- After: ~1,600文字（BYOK詳細説明、コスト優位性、ユースケース拡充）
- 追加キーワード: "no subscription", "pay per use", "non-native English", "BYOK"

### 2. Tab Manager ストア素材の整備
- `store/description.txt` 作成（store-assetsから複製）
- `store/short-description.txt` 作成（新規）
  - 内容: "Tab manager & session saver: search tabs, save/restore sessions, remove duplicates, drag to reorder. Free 3 sessions, Pro unlimited."

### 3. 権限監査（再確認）

| 拡張 | 権限 | 評価 |
|------|------|------|
| AI Text Rewriter | activeTab, storage, contextMenus, scripting | 適切（v1.2.0でscripting追加、テキスト選択に必要） |
| Color Picker | storage | 最小限 OK |
| Currency Converter | activeTab, storage, contextMenus | 適切 |
| Hash & Encode Tool | contextMenus, storage | 適切 |
| JSON Formatter Pro | storage + content_scripts(all_urls) | 要注意（JSON自動検出に必要、正当） |
| Lorem Ipsum Generator | なし | 最小限 OK |
| Page Speed Checker | activeTab | 最小限 OK |
| Regex Tester | storage | 最小限 OK |
| SEO Inspector | activeTab | 最小限 OK |
| Tab Manager | tabs, storage | 適切 |
| WHOIS Lookup | activeTab, storage | 適切 |

---

## フリーミアム化の現状と優先アクション

### 実装済み
- **AI Text Rewriter**: 1日10回制限（Free）→ Gumroad Pro版（無制限）
- **Regex Tester**: 保存プリセット上限制限（Free）→ Gumroad Pro版
- **Tab Manager**: 3セッション制限（Free）→ Pro版（未Gumroad出品）

### 未実装（優先度順）

| 拡張 | フリーミアム化アイデア | 実装難易度 |
|------|---------------------|----------|
| SEO Inspector | Free: 基本スコア5項目 / Pro: 20項目フル分析+履歴 | 中 |
| WHOIS Lookup | Free: WHOISのみ / Pro: DNS+SSL+履歴無制限 | 中 |
| JSON Formatter Pro | Free: 基本フォーマット / Pro: 大容量JSON+エクスポート | 低 |
| Page Speed Checker | Free: モバイルのみ / Pro: デスクトップ+比較+履歴 | 低 |
| Currency Converter | Free: 上位20通貨 / Pro: 160+通貨+お気に入り無制限 | 低 |
| Color Picker | Free: 基本変換 / Pro: パレット保存無制限 | 低 |
| Hash & Encode Tool | Free: MD5/SHA-256のみ / Pro: 全アルゴリズム+JWT | 低 |
| Lorem Ipsum Generator | Free: 5パラグラフ上限 / Pro: 無制限+カスタムテキスト | 低 |

**注意**: Stripe KYCブロック中のため、Gumroadリンク方式（既存実装と同様）を使用すること。

---

## Tab Manager CWS提出手順

Tab Managerは開発完了・ストア素材完成済み。CWSに提出するために必要なアクション:

1. **アイコン確認**: `icons/` ディレクトリに16/32/48/128pxのPNGがあるか確認
2. **ZIP作成**: manifest.json, popup.html, popup.css, popup.js, background.js, iconsをZIPに固める
3. **CWSダッシュボード**: https://chrome.google.com/webstore/devconsole
4. **新規アイテム追加** → ZIPアップロード
5. **Store listing入力**:
   - Short description: `store/short-description.txt` の内容
   - Detailed description: `store/description.txt` の内容
   - Screenshots: `store-assets/` の画像を使用（なければ作成必要）
   - Privacy policy URL: `https://homepage-three-ochre.vercel.app/privacy-policy-tab-manager.html`
6. **提出**

---

## Hash & Encode Tool PP設定（審査通過後）

審査通過後、CWSダッシュボードで:
- Privacy policy URL: `https://homepage-three-ochre.vercel.app/privacy-policy-hash-encode-tool.html`
  （または `https://keisan-tools.com/chrome-privacy/` も可）

---

## 審査が遅い場合の対応策

1. **Developer Dashboard確認**: 各拡張のステータスをChrome Developer Dashboardで毎週確認
2. **Rejected拡張への即時対応**: 拒否理由を読んで24時間以内に修正・再提出
3. **JSON Formatter Pro `<all_urls>` 対応**（拒否された場合）:
   - `content_scripts` を削除し、popup内で手動JSONフォーマットのみに変更
   - または `optional_permissions` + ユーザー許可フローに変更
4. **新規デベロッパーアカウントの審査遅延**: 最初の数本は2〜4週間かかることがある。待機継続。
