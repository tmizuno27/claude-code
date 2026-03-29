---
name: Indexing API日次送信状況
description: 5サイトのGoogle Indexing API送信進捗。日次クォータ200件/日の管理
type: project
---

## 送信状況（2026-03-29時点）

| サイト | 総ページ | 送信済み | 残り | 状態 |
|--------|---------|---------|------|------|
| sim-hikaku.online | 80 | 80 | 0 | ✅ 完了 |
| keisan-tools.com | 460 | 178 | 282 | 明日1回で完了 |
| otona-match.com | 104 | 0 | 104 | 3/30朝最優先 |
| nambei-oyaji.com | 未確認 | - | - | 要確認 |
| pseo-saas | 5,053 | 40 | 5,013 | 全件まで約25日 |

## 日次クォータ: 200件/日（全サイト合計）

## 送信優先順位
1. otona-match（PV急落回復のため最優先）
2. keisan-tools（残り少ない）
3. pseo-saas（大量だが地道に）

## スクリプト
- sim-hikaku: `sites/sim-hikaku.online/scripts/analytics/submit_indexing.py`（完了）
- keisan-tools: `saas/keisan-tools/site/scripts/submit_indexing.py`
- otona-match: `sites/otona-match.com/scripts/analytics/submit_pending_indexing.py`
- pseo-saas: `saas/pseo-saas/scripts/submit_indexing.py`

## Task Scheduler登録推奨
keisan-tools + pseo-saas は毎日自動実行が望ましい

**Why:** インデックス登録はSEO流入の前提条件。特にotona-matchはPV回復に直結
**How to apply:** 毎朝otona-match→keisan-tools→pseo-saasの順で送信。クォータ200件/日を超えないよう管理
