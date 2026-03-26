# ユーザー対応が必要な項目（2026-03-26）

## 1. Google Search Console — サービスアカウント所有権追加（重要度: 高）

Indexing API（URL登録申請）が403エラーで失敗しています。以下の手順でサービスアカウントを「所有者」として追加してください。

### 対象サイト
- `keisan-tools.com`
- `ai-tool-compare-nu.vercel.app`（pSEOサイト）

### 手順
1. [Google Search Console](https://search.google.com/search-console) にログイン
2. 対象プロパティを選択
3. 左メニュー「設定」→「ユーザーと権限」
4. 「ユーザーを追加」をクリック
5. 以下のメールアドレスを入力:

```
claude-indexing@claude-code-indexing.iam.gserviceaccount.com
```

※ 実際のサービスアカウントメールは各サイトの `config/gsc-credentials.json` の `client_email` を確認してください:

```bash
python -c "import json; print(json.load(open('claude-code/sites/nambei-oyaji.com/config/gsc-credentials.json'))['client_email'])"
```

6. 権限を「オーナー」に設定
7. 「追加」をクリック

### 追加後の確認
```bash
# keisan-tools
cd claude-code/saas/keisan-tools/site
python scripts/submit_indexing.py

# pSEO
cd claude-code/saas/pseo-saas
python scripts/submit_indexing.py
```

---

## 2. Google AdSense 申請（keisan-tools.com）

keisan-toolsは460ページ・必要な固定ページ完備で、AdSense申請の準備が整っています。

### 手順
1. [Google AdSense](https://www.google.com/adsense/) にアクセス
2. 「ご利用開始」をクリック
3. サイトURL: `https://keisan-tools.com`
4. アカウント情報を入力
5. AdSenseコードをサイトに貼り付け（指示があれば対応します）
6. 審査完了を待つ（通常1-2週間）

---

## 3. Chrome拡張 審査状況確認

8本が審査待ちです。[Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole) で状況を確認してください。

審査待ち:
- JSON Formatter Pro
- Color Picker
- Lorem Ipsum Generator
- Hash & Encode Tool
- Page Speed Checker
- WHOIS Lookup
- Currency Converter
- SEO Inspector

---

## 4. RapidAPI リスティングSEO改善（任意）

全24 APIの売上$0。`products/api-services/rapidapi-seo-improvements.md` にタイトル・説明・タグの改善案を用意しています。RapidAPI Studio上で手動更新が必要です。

---

## 5. WordPress ドラフト記事の公開確認

今日生成された記事がドラフト状態でWordPressに投稿されています。内容を確認して「公開」してください。

### nambei-oyaji.com
- 編集: https://nambei-oyaji.com/wp-admin/post.php?post=3398&action=edit
- 編集: https://nambei-oyaji.com/wp-admin/post.php?post=3399&action=edit
- （追加記事も生成中）

---

## 6. Google Service Account JWT署名エラー修復（重要度: 最高）

SEO PDCA・GA4分析・Indexing APIが全て `Invalid JWT Signature` エラーで停止しています。

### 影響範囲
- 3サイトのGSCデータ取得
- GA4レポート生成
- Indexing API（URL登録申請）
- Google Sheets同期

### サービスアカウント情報
```
メール: sheets-reader@sheets-sync-489022.iam.gserviceaccount.com
プロジェクト: sheets-sync-489022
```

### 修復手順
1. [Google Cloud Console](https://console.cloud.google.com/) にログイン
2. プロジェクト `sheets-sync-489022` を選択
3. 左メニュー「IAMと管理」→「サービスアカウント」
4. `sheets-reader@sheets-sync-489022.iam.gserviceaccount.com` をクリック
5. 「鍵」タブ → 既存の鍵を削除 → 「鍵を追加」→「新しい鍵を作成」→ JSON
6. ダウンロードしたJSONファイルを以下のパスに配置:

```
claude-code/sites/nambei-oyaji.com/config/gsc-credentials.json
claude-code/sites/otona-match.com/config/gsc-credentials.json
claude-code/sites/sim-hikaku.online/config/gsc-credentials.json
claude-code/infrastructure/tools/sheets-sync/service-account.json
```

7. 「Claudeに認証情報を更新した」と伝えてください。動作確認を実行します。

---

*自動生成: 2026-03-26 05:05 PYT*
