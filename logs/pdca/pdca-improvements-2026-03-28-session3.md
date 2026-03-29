# PDCA改善実行レポート — 2026-03-28 Session 3

## 実行概要
全事業横断のPDCA監査を実施し、発見された問題を即座に修正・改善。

## 完了した改善（8件）

### 1. はてなブログPDCA集計バグ修正
- **問題**: hatena-log.jsonがdict形式なのにlist前提のコードで投稿数0と誤表示
- **修正**: dict/list両形式に対応するパース処理に変更
- **影響**: PDCAレポートのはてなブログ統計が正確に

### 2. Gumroad API統計取得実装
- **問題**: 商品数が「1（ディレクトリ数）」と誤カウント、売上データ取得不可
- **修正**: Gumroad API v2から直接商品数・売上データを取得するように変更
- **結果**: 35商品、売上$0.00を正確に反映

### 3. VS Code Marketplace API修正
- **問題**: filterType=4（GUID用）でPublisher名を検索→HTTP 400エラー
- **修正**: filterType=10（Publisher名）+ filterType=8（プラットフォーム）に変更
- **結果**: 13本の拡張統計を正常取得

### 4. sim-hikaku.online Indexing API送信
- **結果**: 57件送信済み、残23件は翌日自動送信
- **影響**: 95記事の未インデックス問題の解消に向けた第一歩

### 5. Indexing API統合バッチにkeisan-tools+pSEO追加
- **修正**: 3サイトのみ→5サイト（+keisan-tools 460ページ、+pSEO 5,056ページ）
- **優先度**: sim-hikaku > keisan-tools > nambei-oyaji > otona-match > pSEO

### 6. GSC認証エラーのグレースフルフォールバック（2スクリプト）
- **問題**: GSC認証失敗でブログセクション全体がスキップ
- **修正**: daily_all_business_pdca.py + daily_seo_pdca.py 両方で認証失敗時もローカルデータでレポート継続

### 7. PDCAスクリプト構文検証
- 全改善後のスクリプトが構文エラーなしを確認

### 8. Gumroad APIトークン動作確認
- secrets.jsonのトークンでAPI呼び出し成功を実証

## 要手動対応

### GSC認証（3サイト分）
`gsc-credentials.json`のサービスアカウント:
```
sheets-reader@sheets-sync-489022.iam.gserviceaccount.com
```
を Google Search Console > 設定 > ユーザーと権限 に追加（3サイト分）:
- nambei-oyaji.com
- otona-match.com
- sim-hikaku.online

### Indexing APIクォータ
日次200件制限は全サイト共通。現在のpending:
- sim-hikaku.online: 23件
- keisan-tools.com: 460件
- pSEO: 未計測（推定5,056件）
→ 優先度順に約25日で全件送信完了予定

## 追加完了した改善（セッション後半）

### 9. 3サイトCTR改善 — WordPressタイトル直接更新（5記事）
| サイト | 記事 | 旧CTR | インプレ | アクション |
|--------|------|-------|---------|-----------|
| sim-hikaku.online | kakuyasu-sim-ryokin-hikaku-ichiran | 0% | 92 | タイトル更新済 |
| sim-hikaku.online | sub-kaisen-kakuyasu-sim-osusume | 0% | 18 | タイトル更新済 |
| otona-match.com | matching-app-ranking-2026 | 0% | 15 | タイトル更新済 |
| otona-match.com | marrish-review | 0% | 17 | タイトル更新済 |
| nambei-oyaji.com | data-entry-automation | 0% | 8 | タイトル更新済 |

### 10. X投稿 @prodhq27 スクリプト新規作成
- 根本原因: Task Schedulerが参照するスクリプトが存在しなかった
- 15本のツイートキューでローテーション投稿するスクリプト作成済み
- 要手動: APIキーをx-credentials.jsonに設定

### 11. Dev.to API統計取得修正
- 認証なしAPI→認証付きAPIに変更（Views 0→175の正確な値取得）
- 8記事のSEO改善案をファイルに保存

### 12. Dev.to記事SEO改善案
- Views 0の根本原因: ニッチタグ・否定形タイトル
- 成功パターン分析: IP Geolocation(52) > Trending(52) > Screenshot(37)
- 11本のドラフト記事を改善後に公開推奨

## 要手動対応（3件）

1. **GSC認証**: `sheets-reader@sheets-sync-489022.iam.gserviceaccount.com`を3サイトのSearch Consoleに追加
2. **@prodhq27 APIキー**: `gumroad-notion/config/x-credentials.json`にX APIキーを設定
3. **Dev.toドラフト公開**: 重複タイトルを整理後、ユニークな記事を公開
