# 日次ビジネス総合レポート — 2026年03月16日
*生成日時: 2026年03月16日 15:17 (PYT)*

## エグゼクティブサマリー

## 経営エグゼクティブサマリー

3サイト合計PV21・ユーザー10と収益化以前の段階にあり、記事数62本を抱えるotona-match.comがゼロトラフィックという深刻な乖離が最大の課題である。RapidAPI（20本）・Apify（5件）のアセットは整備されているが、APIの実績データが未取得のため事業全体のROI評価が不能な状態にある。今週中にデータ基盤を整備しつつ、唯一トラフィックが存在するnambei-oyaji.comを成長の起点として戦略を再構築する必要がある。

---

### 箇条書きサマリー

- 💪 **強み**
  nambei-oyaji.comが唯一の生きたトラフィック源（PV21）であり、13記事で10ユーザーを獲得している点はコンテンツ方向性の有効性を示す。RapidAPI×20本・Apify×5件のアセットは収益化・自動化の潜在的な武器となりうる。

- ⚠️ **懸念**
  62記事を投入したotona-match.comのPVゼロは、SEO戦略またはインデックス上の根本的な問題を示唆しており、リソースの無駄遣いが継続中。さらにRapidAPI全20本の実績データが未整備のため、どのAPIが機能しているか把握不能。

- ✅ **今日のアクション**
  ①`rapidapi-stats.json`を即時生成しAPI稼働状況を可視化、②otona-match.comのGoogle Search Consoleでインデック

---

## 1. ブログ3サイト（WordPress）

| サイト | PV | ユーザー | 検索表示 | クリック | 記事数 |
|--------|-----|---------|---------|---------|--------|
| [南米おやじの海外生活ラボ](https://nambei-oyaji.com) | 21 | 10 | 5 | 1 | 13 |
| [大人のマッチングナビ](https://otona-match.com) | 0 | 0 | 0 | 0 | 62 |
| [SIM比較ナビ](https://sim-hikaku.online) | 0 | 0 | 0 | 0 | 2 |

**大人のマッチングナビ ステータス備考:**
- GA4: 未設定

**SIM比較ナビ ステータス備考:**
- GA4: 未設定

---

## 2. RapidAPI（20 APIs）

- **ステータス**: stats未設定（rapidapi-stats.json なし）
- **出品API数**: 20 本
- **利用統計**: `api-services/rapidapi-stats.json` を作成して統計収集を設定してください

---

## 3. Apify Store

- **ステータス**: 取得成功
- **Actor数**: 5 件

| Actor名 | 総実行数 | 最終ステータス | 最終実行日 |
|---------|---------|--------------|----------|
| social-video-downloader | 2 | SUCCEEDED | 2026-03-16 |
| seo-analyzer | 2 | SUCCEEDED | 2026-03-16 |
| company-data-enricher | 2 | SUCCEEDED | 2026-03-16 |
| trends-aggregator | 8 | SUCCEEDED | 2026-03-16 |
| keyword-research | 1 | SUCCEEDED | 2026-03-16 |

---

## 4. pSEO AIツール比較サイト

- **ステータス**: デプロイ未完
- **静的ページ数**: 0 ページ
- **デプロイURL**: 未設定
- **TODO**: Vercel デプロイ + ドメイン取得が必要

---

## 5. Chrome拡張ポートフォリオ事業（NEW）

- **ステータス**: 全10個 Chrome Web Store 審査申請済み（2026-03-16）
- **開発コスト**: $5（デベロッパー登録料のみ）
- **運用コスト**: $0/月
- **戦略**: Rick Blyth方式（量産×放置）、フリーミアム課金予定

| # | 拡張名 | カテゴリ | API使用 |
|---|--------|---------|---------|
| 1 | SEO Inspector | デベロッパー ツール | 自社Workers API |
| 2 | JSON Formatter Pro | デベロッパー ツール | なし（ローカル） |
| 3 | Quick Currency Converter | ツール | exchangerate API |
| 4 | Domain WHOIS Lookup | デベロッパー ツール | WHOIS API |
| 5 | AI Text Rewriter | ツール | OpenAI API（BYOK） |
| 6 | Color Picker & Converter | デベロッパー ツール | なし（ローカル） |
| 7 | Page Speed Checker | デベロッパー ツール | Google PSI API |
| 8 | Hash & Encode Tool | デベロッパー ツール | なし（ローカル） |
| 9 | Lorem Ipsum Generator | デベロッパー ツール | なし（ローカル） |
| 10 | Regex Tester | デベロッパー ツール | なし（ローカル） |

- **審査結果**: 1-3日で順次通知予定
- **次のステップ**: 審査通過後、さらに量産 or フリーミアム課金（Stripe連携）を検討
- **プロジェクトパス**: `claude-code/chrome-extensions/`

---

## 6. n8nテンプレート販売

- **ステータス**: Stripe KYC認証問題により停止中
- **プラットフォーム**: Gumroad（9/10本出品済み）
- **テンプレート数**: 10 本（概算）
- **備考**: Stripe KYC認証が解決次第、販売再開予定

---

## 6. 定期タスク健全性

- **GitHub自動同期**: 正常
- **最終同期**: [2026-03-15 05:06:35]
- **総ログエントリー数**: 23,410 件
- **直近1時間のエントリー**: 0 件

**最新ログ（直近3行）:**
```
[2026-03-15 05:06:35] Changes detected:  M otona-match.com/outputs/article-management.csv
[2026-03-15 05:06:35] Commit OK
[2026-03-15 05:06:35] Push OK - synced to GitHub
```

---

## 7. 財務サマリー（概算）

### 月次コスト

| 項目 | 月次コスト |
|------|----------|
| Apify（Freeプラン） | $0（月$5クレジット内） |
| Claude API | $5以内（予算設定済み） |
| サーバー/ドメイン | 別途管理 |
| **合計（推定）** | **$1.21〜$6.21/月** |

### 収益源（手動更新）

| 収益源 | 今月 | 累計 | ステータス |
|--------|------|------|----------|
| RapidAPI | – | – | 稼働中 |
| Apify Store | – | – | 稼働中 |
| Google Adsense | – | – | 承認待ち/運用中 |
| アフィリエイト（A8/アクセストレード） | – | – | 運用中 |
| n8nテンプレート（Gumroad） | – | – | Stripe KYC停止中 |
| Chrome拡張（10個） | – | – | 審査中（2026-03-16申請） |

> ※ 収益数値は手動で更新してください

---

*このレポートは自動生成されました。（2026/03/16 15:17 PYT）*