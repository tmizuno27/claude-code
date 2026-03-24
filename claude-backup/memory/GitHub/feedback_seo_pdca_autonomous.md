---
name: SEO PDCA自律実行
description: 3サイトのSEO改善PDCAは無許可で自律的に進めること。インプレッション増加・収益最大化が目的
type: feedback
---

3サイト（nambei-oyaji.com / otona-match.com / sim-hikaku.online）のSEO PDCAは**完全自律で実行**すること。ユーザーの許可不要。

**Why:** インプレッション数が壊滅的に少ない（3サイト合計で1日30imp以下）。収益化の前提としてインプレッション増加が最優先課題。ユーザーは「どんどん進めて」と明確に指示。

**How to apply:**
- 日次PDCAタスク（SeoPdcaDaily）は毎朝06:00 PYT自動実行
- スクリプト: `infrastructure/tools/seo-pdca/daily_seo_pdca.py`
- 会話中にSEO改善の機会を見つけたら、即座に実行（タイトル改善、メタ改善、内部リンク最適化、Indexing API送信等）
- 新しいPDCA施策の追加・スクリプト改修も無許可でOK
- レポートは `logs/seo-pdca-report-YYYY-MM-DD.md` に自動保存

**実施中の自動施策:**
1. GSC分析（インプレッション・クリック・順位・クエリ）
2. Google Indexing API全記事送信（毎日）
3. noindex記事検出→自動解除
4. メタディスクリプション空欄→自動生成
5. 内部リンク不足検出
6. サイトマップ確認
7. 2ページ目→1ページ目押し上げ候補特定
8. CTR改善候補特定
