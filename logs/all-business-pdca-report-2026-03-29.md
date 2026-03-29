# 全事業 PDCA 日次レポート (2026-03-29)
実行時刻: 2026-03-29 06:30 PYT

# 1. ブログ 3サイト

## 南米おやじ (nambei-oyaji.com)

### CHECK
| 指標 | 今週 | 先週 | 変化 |
|------|-----:|-----:|-----:|
| インプレッション | 431 | 20 | +411 (+2055%) |
| クリック | 9 | 3 | +6 |

- GA4（7日間）: PV=150 / ユーザー=41 / セッション=54

### ACT
- 公開記事数: 85
- 内部リンク不足（2本未満）: 0件

### PLAN
- ✅ 推移観察継続

## マッチングナビ (otona-match.com)

### CHECK
| 指標 | 今週 | 先週 | 変化 |
|------|-----:|-----:|-----:|
| インプレッション | 207 | 44 | +163 (+370%) |
| クリック | 2 | 1 | +1 |

- GA4（7日間）: PV=36 / ユーザー=28 / セッション=29

### ACT
- 公開記事数: 89
- 内部リンク不足（2本未満）: 0件

### PLAN
- ✅ 推移観察継続

## SIM比較 (sim-hikaku.online)

### CHECK
| 指標 | 今週 | 先週 | 変化 |
|------|-----:|-----:|-----:|
| インプレッション | 239 | 31 | +208 (+671%) |
| クリック | 0 | 0 | +0 |

- GA4（7日間）: PV=35 / ユーザー=32 / セッション=32

### ACT
- 公開記事数: 70
- 内部リンク不足（2本未満）: 0件

### PLAN
- 🎯 インプレッションあるがクリック0 → タイトル/メタ改善でCTR向上

# はてなブログ（nambei-oyaji.hatenablog.com）

### CHECK
- 総投稿数: **32**
- 過去7日の投稿: **32件**
- 変換済みダイジェスト: 34件
- パイプラインログ: 未検出

### ACT
- Task Scheduler: `HatenaPipeline`（月水金 07:00 PYT、2記事/回）
- ✅ 直近7日で32件投稿済み

### PLAN
- 本家（nambei-oyaji.com）への送客効果をGA4 UTMパラメータで計測
- はてなコミュニティ（グループ・読者登録）からの流入を分析
- 被リンク効果のGSC確認（参照元ドメインにhatenablog.comがあるか）

# 2. RapidAPI（24 API）

### CHECK
- API数: 24
- 総サブスクライバー: 0
- 総リクエスト: 0
- 総収益: $0.00

### ACT
- ヘルスチェックスクリプト: 存在確認OK（Task Scheduler経由で実行中）

### PLAN
- ⚠️ 全API利用ゼロ → RapidAPIリスティングのSEO改善（タイトル・説明・タグ）が必要
- ⚠️ RapidAPI Provider APIキーの環境変数設定で正確な統計取得を
- 📝 Dev.to/Qiita等での技術記事によるAPI宣伝を継続

# 3. Gumroad（デジタル商品）

### CHECK
- 商品数: **35**（Gumroad API取得）
- 総販売数: **0件**
- 総売上: **$0.00**
- @prodhq27 X投稿（過去7日）: 0件

### ACT
- X自動投稿（@prodhq27）: 毎日3回稼働中
- ⚠️ 販売数ゼロ → 商品ページ・価格・プロモーション戦略の見直しが急務

### PLAN
- Product Hunt / IndieHackers への掲載でトラフィック獲得

# 4. Chrome拡張（10本）

### CHECK
- 拡張数: 12ディレクトリ
- 最終ステータス確認: review-status-2026-03-21.md
- ⚠️ Chrome Developer Dashboard APIは存在しないため自動確認不可

### PLAN
- 審査待ち8本の通過状況を定期的に手動確認
- 公開済み2本のレビュー・DL数をChrome Web Storeで確認

# 5. VS Code拡張（10本）

### CHECK
- 公開数: 13本
- 総インストール数: 0

| 拡張名 | インストール数 |
|--------|----------:|
| M27 ENV Lens | 0 |
| API Response Viewer — Format & Debug REST APIs | 0 |
| Doc Snapshot — Export Code Documentation Instantly | 0 |
| Smart Folding — Intelligent Code Collapse | 0 |
| File Sticky Notes — Add Notes to Any File | 0 |

### PLAN
- ⚠️ 全拡張インストール0 → README改善・スクリーンショット追加・VS Code Marketplaceタグ最適化

# 6. X/Twitter（2アカウント）

### CHECK
- **@nambei_oyaji**（ブログ集客）: 過去7日 1投稿 / エラー0件
- **@prodhq27**（Gumroad販促）: 過去7日 0投稿 / エラー0件

### PLAN
- 投稿がゼロのアカウントがあればTask Scheduler確認
- エンゲージメント率を分析してコンテンツ改善

# 7. Apify Actors（5本）

### CHECK
- 公開Actor数: 9
- ⚠️ Apify API統計の自動取得は未実装

### PLAN
- Apify Store の各Actorページのランキング・利用状況を定期確認
- READMEとサンプルコードの充実で利用促進

# 8. WP Linker SaaS

### CHECK
- URL: https://wp-linker.vercel.app
- 稼働状況: HTTP 200
- ⚠️ Stripe未連携のため決済不可（Stripe待ち）

### PLAN
- Stripe連携完了次第、料金プラン設定→本格ローンチ

# 9. pSEO AIツール比較

### CHECK
- URL: https://ai-tool-compare-nu.vercel.app
- 稼働状況: HTTP 200
- 4,003静的ページ（291ツール×12カテゴリ）

### PLAN
- GSCでインデックス状況確認（4,003ページ中何ページインデックス済みか）
- AdSenseまたはアフィリエイト導線の追加

# 11. Dev.to（技術記事）

### CHECK
- 記事数: 19
- 総閲覧数: 185
- 総リアクション: 1
- 総コメント: 2

| 記事 | 閲覧数 | リアクション |
|------|------:|----------:|
| Build a Trending Topics Dashboard in 10 Minutes -- | 52 | 0 |
| Build an IP Geolocation + VPN Detector in 5 Minute | 52 | 0 |
| Free Screenshot API — Capture Any Webpage as PNG w | 37 | 0 |
| 20+ Free APIs for Developers in 2026 — No Auth, No | 20 | 0 |
| Free WHOIS and DNS Lookup API -- No Scraping, No R | 10 | 0 |

### PLAN
- 閲覧数が伸びている記事があればRapidAPI導線を強化
- 新記事投稿（月2-3本）でRapidAPIへのトラフィック誘導

# 12. n8nテンプレート（一時停止）

### CHECK
- ワークフロー数: 0
- リスティング数: 0
- ステータス: **一時停止**（Stripe KYC認証問題）
- プラットフォーム: Gumroad（tatsuya27.gumroad.com）

### PLAN
- Stripe KYC解決次第、即座に販売再開
- 解決までの間、テンプレートの品質改善・新テンプレート作成を進める

# 13. Stock Assets（出品準備中）

### CHECK
- 生成済み画像: 914枚
- メタデータCSV: 22ファイル
- ステータス: 出品準備中（Adobe Stock/Freepik）

### PLAN
- ✅ 914枚生成済み → Adobe Stockアカウント開設→テスト出品が次のステップ
- 出品後はダウンロード数・収益をAdobe Stock Contributorダッシュボードで追跡

# 14. POD Etsy — AsuInk（準備中）

### CHECK
- リスティング: 0件
- デザインフォルダ: 0件
- ステータス: 準備中（Etsy/Printfulアカウント開設待ち）

### PLAN
- Etsy/Printfulアカウント開設 → デザイン生成（Gemini有料プランまたは代替）→ 出品開始
- 150リスティング完成済みなのでアカウント開設が唯一のブロッカー

# 15. 仮想通貨自動売買（Bybit）

### CHECK
- バックテスト完了: ❌
- 最優秀戦略: MAクロス+RSI × BTC/USDT (Sharpe 4.91)
- ステータス: **口座開設待ち**（パラグアイ住所証明の準備中）

### PLAN
- Bybit口座開設完了次第、小額（$100-200）でライブテスト開始
- パラグアイ住所証明の準備を進める

# 10. インフラ・自動化基盤

### CHECK — ログ最終更新
| ログ | 最終更新 | ステータス |
|------|---------|-----------|
| Git自動同期 | 03/29 06:44 | ✅ 正常 |
| SEO PDCA | 03/29 06:01 | ✅ 正常 |
| X投稿(@nambei) | 03/28 20:22 | ✅ 正常 |
| X投稿(@prodhq27) | 未検出 | ❌ |
| APIヘルスチェック | 03/29 06:00 | ✅ 正常 |
| ダッシュボード更新 | 03/29 06:00 | ✅ 正常 |

### PLAN
- 停止/遅延しているタスクがあれば原因調査→復旧

# 16. keisan-tools.com（計算ツールサイト）

### CHECK
- URL: https://keisan-tools.com
- 稼働状況: HTTP 200
- サイトマップ: ✅ sitemap.xml (460ページ)
- 公開ページ数: 460
- GA4（7日間）: PV=5 / ユーザー=5 / セッション=5

### ACT
- ✅ 460ページ公開中 → AdSense申請可能ライン

### PLAN
- 300ページ目標に向けてページ量産継続
- 30ページ達成後にAdSense申請
- GSCでインデックス状況を定期確認

# 17. Product Factory（AIエージェント×デジタル商品自動量産）

### CHECK
- エージェント数: 0
- 生成済み商品ファイル: 0
- Phase 1完了済み（エージェント4体+テスト商品生成）

### PLAN
- Phase 2（自動量産パイプライン）の進捗確認・実装推進
- 市場リサーチ→商品生成→出品の自動フロー構築

# 18. フリーランス（Fiverr/Upwork）

### CHECK
- Gig定義ファイル数: 14
  - `fiverr-gig-definitions.md`

### PLAN
- Fiverrアカウント開設・Gig公開の進捗確認
- 定義済みGig 3件の公開準備を進める

# 19. せどり（Amazon FBA×電脳せどり）

### CHECK
- リサーチファイル数: 6
- 計画書: ✅ あり
- ステータス: 計画段階

### PLAN
- 事業開始に向けた次のステップ: リサーチ完了→Amazon出品アカウント開設→テスト仕入れ

# 20. eBay輸出

### CHECK
- リサーチファイル数: 1
- ステータス: リサーチ段階

### PLAN
- eBayアカウント開設・出品準備
- 日本→パラグアイの輸出商品リサーチ継続

# 21. AI自動化ビジネス

### CHECK
- 企画書・リサーチファイル数: 2
  - `action-plan-2026-03-28.md`
  - `new-business-ideas-2026.md`
- ステータス: 検討中

### PLAN
- 事業化判断: 市場ニーズ・競合・収益性を評価
- 次のアクション: MVP定義または他事業への注力判断

# 22. ホームページ（ランディングページ）

### CHECK
- HTMLファイル数: 12
  - `privacy-policy-ai-text-rewriter.html`
  - `privacy-policy-color-picker.html`
  - `privacy-policy-currency-converter.html`
  - `privacy-policy-hash-encode-tool.html`
  - `privacy-policy-json-formatter.html`
  - `privacy-policy-lorem-ipsum-generator.html`
  - `privacy-policy-page-speed-checker.html`
  - `privacy-policy-regex-tester.html`
  - `privacy-policy-seo-inspector.html`
  - `privacy-policy-tab-manager.html`

### PLAN
- LPの目的・導線を明確化（全事業へのハブとして活用）
- デザイン・コンテンツの定期見直し

# 23. 財務管理

### CHECK
| ファイル | 最終更新 |
|---------|---------|
| 資産管理.gsheet | 2026-03-02 |
| 入金管理.gsheet | 2026-03-02 |

### PLAN
- 月次で全事業の収支を集計・更新
- 入金管理スプレッドシートの定期チェック
- 事業別ROIの把握 → 注力先の判断材料に

---
*自動生成: 2026-03-29 06:30 PYT*