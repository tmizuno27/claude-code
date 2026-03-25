# Google Indexing API 送信ログ (2026-03-25)

実行時刻: 2026-03-25 05:05-05:10 PYT

## 結果サマリー

| サイト | 公開記事数 | 成功 | エラー |
|--------|-----------|------|--------|
| nambei-oyaji.com | 73 | 73 | 0 |
| otona-match.com | 70 | 70 | 0 |
| sim-hikaku.online | 72 | 66 | 6 |
| **合計** | **215** | **209** | **6** |

## エラー詳細

sim-hikaku.online の末尾6件で **429 Quota exceeded** (1日あたりの上限200件に到達):

- `5g-taiou-kakuyasu-sim/`
- `ipad-tablet-kakuyasu-sim/`
- `kakuyasu-sim-hikari-set-wari/`
- `sim-povo/`
- `daredemo-sumaho-hyoban/`
- `japan-global-esim-hyoban/`

## 対応

- 上記6件は翌日(2026-03-26)に再送信が必要
- 1日の上限は200件。今回は209件成功+6件失敗=215件送信試行

## 特記事項

- sim-hikaku.online: レポートでは92記事が未インデックス推定。72件中66件を送信済み
- nambei-oyaji.com: 73件全送信完了（レポートでは未インデックス0件だが念のため全送信）
- otona-match.com: 70件全送信完了（同上）

---
*スクリプト: `sites/nambei-oyaji.com/scripts/analytics/gsc_index_request.py`*
