# ファクトチェック報告書 — Batch 3（ID 140-163）

**対象**: otona-match.com 22記事
**実施日**: 2026-03-17
**ステータス**: WebSearch検証完了

---

## 1. 重大な誤り（要修正）

### 1-1. Pairs（ペアーズ）月額料金が旧価格のまま

| 記事 | 記載値 | 現在の正確な値 | 備考 |
|------|--------|---------------|------|
| matching-app-saiyasune | 1ヶ月 3,700円 | クレカWeb版 3,700円 / Android 4,100円 / iOS 4,300円 | クレカ限定なら正しいが、記事では決済方法の区別なし |
| matching-app-40dai-osusume | 3,700円〜 | 同上 | 同上 |
| matching-app-saiyasune | 3ヶ月 3,100円/月 | クレカWeb版 3,300円/月 | **誤り**（値下がりではなく値上がりしている） |
| matching-app-saiyasune | 6ヶ月 2,100円/月 | クレカWeb版 2,000円/月 | 微差だが要確認 |
| matching-app-saiyasune | 12ヶ月 1,650円/月 | クレカWeb版 1,667円/月 | 微差 |

### 1-2. with（ウィズ）月額料金が旧価格

| 記事 | 記載値 | 現在の正確な値 |
|------|--------|---------------|
| matching-app-saiyasune | 1ヶ月 3,600円 | **4,160円**（大幅値上げ済み） |
| matching-app-saiyasune | 3ヶ月 2,667円/月 | **3,467円/月** |
| matching-app-saiyasune | 6ヶ月 2,350円/月 | **2,560円/月** |
| matching-app-saiyasune | 12ヶ月 1,833円/月 | **2,117円/月** |

> **重要度: 高** — withは全プランで大幅値上げ済み。記事の料金は完全に古い。

### 1-3. ワクワクメール ポイント購入レート

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| wakuwaku-mail-review | 2,000円=210P | 銀行振込: 2,000円=200P+30S（サービスポイント）。210Pとは異なる |
| wakuwaku-mail-review | 3,000円=370P | 未確認（公式サイトで要確認） |
| wakuwaku-mail-review | 5,000円=650P | 未確認（公式サイトで要確認） |
| wakuwaku-mail-review | 10,000円=1,300P | 未確認 |
| wakuwaku-mail-review | 1,000円=100P | 銀行振込: 1,000円=100P+10S → 基本レートは正しい |

> **注意**: 記事のレートは「P＋サービスポイント(S)の合算」を単純にPとして表記している可能性あり。決済方法によってレートが異なるため、決済方法を明記すべき。

### 1-4. エン婚活エージェント 登録料の矛盾

| 記事 | 記載値 | 現在の正確な値 |
|------|--------|---------------|
| online-kekkon-soudan-hikaku | 登録料 33,000円 | **旧価格は10,780円だったが、現在は33,000円に改定済み** → 記事の値は正しい |
| kekkon-soudan-ryoukin-hikaku | 登録料 33,000円 | 正しい |

> 登録料33,000円は2026年現在の正確な値。

### 1-5. エン婚活エージェント 紹介可能会員数の記事間矛盾

| 記事 | 記載値 |
|------|--------|
| online-kekkon-soudan-hikaku | 約18.7万人 |
| kekkon-soudan-ryoukin-hikaku | 約3万人 |

> **検証結果**: エン婚活単体の会員数は約3万人。コネクトシップ含む紹介可能会員数は約18.7万人。**両方正しいが、比較軸が異なる**。同サイト内で統一すべき（「紹介可能会員数」か「自社会員数」か明記が必要）。

### 1-6. naco-do 料金の変動

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| online-kekkon-soudan-hikaku | 入会金 66,000円、月会費 16,800円 | **旧価格の可能性**。現在は入会金29,800円、月会費14,200円に改定されている情報あり |

> **重要度: 高** — naco-doは料金改定を頻繁に行っており、記事の66,000円/16,800円は旧プランの可能性大。最新の公式サイトで再確認必須。

### 1-7. IBJメンバーズ 初期費用の記事間矛盾

| 記事 | 記載値 |
|------|--------|
| kekkon-soudan-ryoukin-hikaku | 初期費用 181,500円 |
| kekkon-soudan-30dai-josei | 入会金 252,450円 |

> **検証結果**: IBJメンバーズは登録料33,000円＋活動サポート費219,450円＝**初期費用合計252,450円**が現在の正確な値。181,500円は旧料金の可能性。kekkon-soudan-ryoukin-hikakuの値が古い。

### 1-8. オーネット 料金の記事間矛盾

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| kekkon-soudan-ryoukin-hikaku | 入会金+初期 122,600円 | 入会金30,000円＋その他費用。合計額は公式非公開で要確認 |
| kekkon-soudan-30dai-josei | 入会金 116,600円 | 上記と異なる |
| kekkon-soudan-ryoukin-hikaku | 月会費 15,950円 | 正しい（オーネットプラン） |
| kekkon-soudan-30dai-josei | 月会費 16,500円 | **誤り**。正しくは15,950円 |

### 1-9. ツヴァイ 料金の記事間矛盾

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| kekkon-soudan-ryoukin-hikaku | 入会金 115,500円 | **旧価格**。現在のご紹介プランは118,800円 |
| kekkon-soudan-30dai-josei | 入会金 118,800円 | 正しい |
| kekkon-soudan-ryoukin-hikaku | 月会費 15,400円 | 要確認（15,400～17,400円の範囲） |
| kekkon-soudan-30dai-josei | 月会費 15,950円 | 要確認 |

---

## 2. youbride（ユーブライド）関連の整合性問題

### 2-1. 会員数

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| youbride-review | 300万人 | **累計300万人以上** → 正しい |
| matching-app-batuichi-saikon | 260万人 | **古い数値**。現在は300万人以上 |

### 2-2. 月額料金

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| youbride-review | 4,300円〜 | 正しい（1ヶ月プラン） |
| matching-app-nentai-betsu | 4,500円〜 | **誤り**。正しくは4,300円 |
| matching-app-40dai-osusume | 2,400円〜(12ヶ月) | 正しい |
| matching-app-sotsukon-saikon | 4,300円〜 | 正しい |

### 2-3. 成婚統計

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| youbride-review | 75%が6ヶ月以内に成婚 | 公式サイトで「成婚退会者の75%が6ヶ月以内」と確認 → **正しい** |
| matching-app-nentai-betsu | 約6割が3か月以内 | **出典不明・誤りの可能性高い** |
| youbride-review | 成婚者約1.9万人 | 累計約18,888名 → おおむね正しい |

### 2-4. 運営会社

| 記事 | 記載値 | 検証結果 |
|------|--------|---------|
| youbride-review | 運営IBJ（東証プライム） | 正しい |

---

## 3. 正確と確認された情報

### ワクワクメール
- メール送信 5P（50円）: **正しい**
- 初回最大1,700円分無料ポイント: **正しい**
- 会員数1,300万人: **正しい**
- PCMAX会員数2,000万人: 未検証（記事記載のまま）
- ハッピーメール会員数3,500万人: 未検証（記事記載のまま）

### マッチングアプリ月額（1ヶ月プラン・クレカWeb版）
- Pairs 3,700円: **正しい**（クレカWeb版限定）
- marrish 3,400円: **正しい**
- アンジュ 3,800円: **正しい**
- Omiai 3,900円: **正しい**（クレカ版。iOS版は4,900円）
- tapple 3,700円: **正しい**（Web版。アプリ版は4,400円）

### エン婚活エージェント
- 月会費 14,300円: **正しい**
- 成婚料 0円: **正しい**
- 年間約18万円: おおむね正しい（登録料33,000円＋月会費14,300円×12＝204,600円。初年度約20万円）

### スマリッジ
- 登録料 6,600円: **正しい**
- 月会費 9,900円: **正しい**
- 成婚料 0円: **正しい**
- 年間約12.5万円: **正しい**（6,600＋9,900×12＝125,400円）
- 会員数 約3万人 / 紹介可能5.5万人: コネクトシップ全体の有効会員数22,347人（2026年1月）との情報あり。5.5万人は要確認

### marrish
- 会員数200万人以上（matching-app-batuichi-saikon）: **古い**。現在は累計400万人超
- 女性無料: **正しい**

### その他
- Pairs会員数2,500万人: **正しい**（公式発表値）
- Tinder有料1,200円〜: 未検証
- tapple会員数2,000万人: 未検証
- with会員数1,000万人: 未検証

---

## 4. 統計データ（出典不明・検証困難）

| 記事 | 記載統計 | 判定 |
|------|---------|------|
| matching-app-douki-fukusu | 「92%が同時進行を実践」 | 出典不明。要出典明記 |
| matching-app-tsukare-taisaku | 「男性89.2%/女性91.6%が疲れ経験」 | 出典不明。要出典明記 |
| matching-app-sotsukon-saikon | 「88人の50代調査で75%が会えた」 | 出典不明。要出典明記 |
| matching-app-sotsukon-saikon | 「約64%が利用して満足」 | 出典不明。要出典明記 |
| matching-app-sotsukon-saikon | youbride 50代推定会員数51万人 | 推定値。公式発表なし |
| kekkon-soudan-30dai-josei | パートナーエージェント成婚率61.4% | **疑わしい**。公式は27.0%。61.4%は別の算出基準の可能性 |
| youbride-review | 料金表（3ヶ月3,600円/月、6ヶ月2,967円/月、12ヶ月2,400円/月） | 正しい |

---

## 5. 修正優先度まとめ

### 最優先（料金が大幅に古い）
1. **matching-app-saiyasune**: with全プラン料金を更新（3,600円→4,160円等）
2. **online-kekkon-soudan-hikaku**: naco-do料金を最新値に更新（66,000円→29,800円等）
3. **kekkon-soudan-ryoukin-hikaku**: IBJメンバーズ初期費用を252,450円に修正
4. **kekkon-soudan-30dai-josei**: オーネット月会費16,500円→15,950円に修正

### 高優先（記事間の不整合）
5. **matching-app-batuichi-saikon**: youbride会員数260万人→300万人に更新
6. **matching-app-batuichi-saikon**: marrish会員数200万人→400万人に更新
7. **matching-app-nentai-betsu**: youbride月額4,500円→4,300円に修正
8. **matching-app-nentai-betsu**: youbride成婚統計「6割が3か月以内」→「75%が6ヶ月以内」に修正
9. **kekkon-soudan-ryoukin-hikaku**: ツヴァイ入会金115,500円→118,800円に修正

### 中優先（表記改善）
10. **全料金記事**: 決済方法（クレカWeb版/iOS/Android）を明記
11. **エン婚活関連2記事**: 会員数の定義を統一（自社/コネクトシップ含む）
12. **wakuwaku-mail-review**: ポイント購入レートの決済方法を明記
13. **kekkon-soudan-30dai-josei**: パートナーエージェント成婚率61.4%の出典確認

### 低優先（出典追加）
14. 統計データ4件に出典URLを追加

---

## 6. 記事別サマリー（全22記事）

| # | スラッグ | 料金記載 | 判定 |
|---|---------|---------|------|
| 1 | matching-app-line-koukan | なし | OK |
| 2 | matching-app-douki-fukusu | なし | 統計出典要追加 |
| 3 | wakuwaku-mail-review | あり | ポイントレート要確認 |
| 4 | matching-app-40dai-osusume | あり | おおむね正確 |
| 5 | online-kekkon-soudan-hikaku | あり | naco-do料金要更新 |
| 6 | youbride-review | あり | 正確 |
| 7 | matching-app-tsukare-taisaku | なし | 統計出典要追加 |
| 8 | deaikei-anzen-tsukaikata | なし | OK |
| 9 | konkatsu-party-vs-app | 少量 | OK |
| 10 | matching-app-batuichi-saikon | あり | youbride/marrish会員数要更新 |
| 11 | matching-app-shinjitsu-uso | なし | OK |
| 12 | matching-app-koppun-taikendan | なし | OK |
| 13 | kekkon-soudan-ryoukin-hikaku | あり | IBJ/ツヴァイ/オーネット要修正 |
| 14 | matching-app-nentai-betsu | あり | youbride料金・統計要修正 |
| 15 | matching-app-tomodachi-kara | 少量 | OK |
| 16 | kekkon-soudan-30dai-josei | あり | 複数料金要修正 |
| 17 | matching-app-jikoshoukai | 少量 | OK |
| 18 | matching-app-sotsukon-saikon | あり | 統計出典不明多数 |
| 19 | kekkon-soudan-mendan-nagare | 少量 | OK |
| 20 | matching-app-video-tsuwwa | なし | OK |
| 21 | matching-app-nenrei-sasyou | なし | OK |
| 22 | matching-app-saiyasune | あり | **with料金全面更新必須** |

---

*検証ソース: WebSearch（2026-03-17実施）。各サービス公式サイト・主要比較メディアの情報を参照。*
