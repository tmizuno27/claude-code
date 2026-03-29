---
name: 週次GA4アナリティクススクリプト作成済み
description: 3サイト週次GA4レポート生成スクリプトをinfrastructure/tools/に作成。Task Scheduler登録推奨
type: reference
---

- **スクリプト**: `infrastructure/tools/weekly_analytics_report.py`
- 3サイト（nambei, otona, sim-hikaku）のGA4データを一括取得
- レポート保存先: 各サイトの`outputs/reports/weekly-analytics-YYYY-MM-DD.md` + 統合JSON `logs/seo/`
- Task Schedulerに週次（日曜）で登録推奨
