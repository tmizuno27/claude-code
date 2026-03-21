---
name: affiliate-manager-team
description: 4 ASP × 3サイトのアフィリエイト管理チーム（承認確認・リンク挿入・パフォーマンス分析）
team:
  - agent: asp-monitor
    description: 各ASP（A8.net, アクセストレード, もしもアフィリエイト, Value Commerce）の承認状況を確認し、新規承認プログラムを特定する
  - agent: link-inserter
    description: 承認済みプログラムのアフィリエイトリンクを3サイトの該当記事に一括挿入する
  - agent: performance-analyst
    description: ASP別・サイト別・記事別のアフィリエイトパフォーマンスを分析し、最適化提案を行う
---

# アフィリエイト管理チーム

## 概要
4つのASP（A8.net, アクセストレード, もしもアフィリエイト, Value Commerce）× 3サイト（nambei-oyaji.com, otona-match.com, sim-hikaku.online）のアフィリエイト運用を一括管理するチーム。

## 起動トリガー
「アフィリエイト管理」「ASP確認」「アフィリエイトチェック」「リンク挿入」「提携確認」「アフィリエイト最適化」など

## 実行フロー

### Phase 1: ASP承認状況確認（asp-monitor）
1. 各サイトの `config/affiliate-links.json` を読み込み、現在の提携状況を把握
2. メモリファイルを確認:
   - `memory/affiliate-asp-overview.md` — 全体サマリー
   - `memory/accesstrade-affiliate-pending.md` — アクセストレード申請中一覧
   - `memory/moshimo-affiliate-progress.md` — もしもアフィリエイト進捗
3. 新規承認・未提携プログラムを特定
4. 承認状況レポートを生成

### Phase 2: リンク一括挿入（link-inserter）
1. Phase 1で特定された新規承認プログラムについて:
   - 3サイトの `outputs/article-management.csv` から該当記事を特定
   - `config/affiliate-links.json` を更新
   - `scripts/publishing/insert_affiliate_all.py` を実行して一括挿入
2. 3サイトすべてに等しく適用（3サイトパリティルール厳守）
3. 挿入結果をログ出力

### Phase 3: パフォーマンス分析（performance-analyst）
1. ASP別の成果データを集計（可能な範囲で）
2. サイト別・記事別のクリック率・成約率を分析
3. 最適化提案を生成:
   - 高パフォーマンスASPへの集約
   - 低パフォーマンス記事の改善案
   - 未挿入記事の洗い出し
4. メモリファイルを最新状態に更新

## 参照ファイル
- `*/config/affiliate-links.json` — 各サイトのリンク定義
- `*/scripts/publishing/insert_affiliate_all.py` — 一括挿入スクリプト
- `*/outputs/article-management.csv` — 記事管理CSV
- `memory/affiliate-asp-overview.md` — ASP概要

## ルール
- 3サイト必ず並列で処理（1サイトだけの更新は禁止）
- リンク挿入後は必ず `article-management.csv` を更新
- CSV更新後は `create_article_sheet.py` でスプレッドシート同期
