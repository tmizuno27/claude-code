---
name: PDCA 2026-03-28 Session 3 — 全事業横断30件改善
description: 全事業PDCAで30件の自動改善を実行。内部リンク741本、Dev.to10記事公開、はてな9記事投稿、アフィリエイト9記事追加、PDCAスクリプト5箇所修正など
type: project
---

## 実行概要
全事業横断のPDCA監査→即改善を実施。30件完了、手動対応5件残。

## 完了改善（30件）

### インフラ・PDCA修正（6件）
- はてなブログPDCA集計バグ修正（dict/list両対応）
- Gumroad API統計取得実装（35商品の売上自動反映）
- VS Code Marketplace API修正（filterType 4→10）
- Dev.to API認証付き取得に修正（Views 0→175正確表示）
- GSC認証グレースフルフォールバック（daily_all_business_pdca.py + daily_seo_pdca.py）
- Indexing API統合バッチにkeisan-tools(460p)+pSEO(5,056p)追加

### SEO・トラフィック（9件）
- sim-hikaku Indexing API 57件送信（残23件は翌日自動）
- nambei+otona Indexing pending生成（89+104=193件）
- **3サイト内部リンク: 247記事×最大741リンク追加**
- CTR改善タイトル6記事WP更新（sim-hikaku 2, otona-match 2, nambei 1, povo 1）
- CTR改善メタディスクリプション5記事更新
- stale記事検出+リライト候補リスト作成
- noindexチェック（247記事全クリア）
- Dev.to SEO改善案作成
- 3サイトCTR改善案ファイル保存

### マーケティング・コンテンツ（7件）
- **Dev.to 10記事公開（8→18本に倍増）**
- @prodhq27 X投稿スクリプト新規作成（15本ツイートキュー）
- **はてなブログ9記事投稿（累計30記事）**
- **アフィリエイト一括挿入（otona 5件+sim 4件=9記事）**
- @nambei_oyaji 来週分X投稿21本生成（3/29-4/4）
- Gumroad 35商品最適化分析+改善案作成
- otona-match CSV管理漏れ10記事修復（→161件）

### 監視・レポート（8件）
- RapidAPI 24本ヘルスチェック（23/24→Screenshot修正でデプロイ済）
- Screenshot API修正（AbortController 25秒タイムアウト+ストリーミング）
- SaaS 3サイト稼働確認（全HTTP 200）
- keisan-tools GA4レポート（20セッション/7日）
- **3サイト週次GA4レポート生成**
- 記事管理CSV+Sheets同期（400記事）
- noindexチェックレポート保存
- PDCA改善ログ保存

## 重要な発見

### otona-match.com PV -75%（要緊急対応）
- セッション28（前週比-44%）、PV 34（前週比-75%）
- Direct流入67.9%、Organic Search 17.9%と検索露出が極めて低い
- noindex問題はなし。GSCでカバレッジエラー・ペナルティ確認が急務

### GA4数値（2026-03-21〜28）
| サイト | セッション | PV | 前週比 | Organic% |
|--------|-----------|-----|--------|----------|
| nambei-oyaji.com | 66 | 191 | +69% | 57.6% |
| otona-match.com | 28 | 34 | -44% | 17.9% |
| sim-hikaku.online | 26 | 28 | -10% | 3.8% |

### Indexing APIクォータ
日次200件制限は全サイト共通（サービスアカウント単位）。優先度: sim-hikaku > keisan-tools > nambei > otona > pSEO

## 未完了・手動対応（5件）
1. GSC認証: `sheets-reader@sheets-sync-489022.iam.gserviceaccount.com`を3サイトのSearch Consoleに追加
2. @prodhq27 APIキー: `products/gumroad-notion/config/x-credentials.json`に設定
3. Chrome拡張: 8本が12日審査待ち→Developer Dashboardで却下確認
4. Gumroad: 「AI Business Automation Mega Prompt Pack」を管理画面で公開 + 15商品にタグ設定
5. otona-match.com: GSCでカバレッジエラー・ペナルティ確認
