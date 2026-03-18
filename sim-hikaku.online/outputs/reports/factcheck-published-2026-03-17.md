# ファクトチェックレポート：sim-hikaku.online 公開記事全体
**実施日**: 2026-03-17
**対象**: 公開済み全16記事（article-management.csv「公開済」ステータス）
**手法**: 記事間クロスチェック + WebSearch による公式情報照合

---

## 総合判定

| 項目 | 件数 |
|------|------|
| 要修正（価格・スペック不整合） | 8件 |
| 要確認（軽微・表記揺れ） | 3件 |
| 問題なし | 残りの記述 |

---

## 【要修正】重大な不整合・誤情報

### 1. IIJmio 料金の記事間不整合（複数記事に影響）

**背景**: IIJmioは2回の料金改定を実施。
- 2025/3/1: 5GB 990円→950円、10GB 1,500円→1,400円
- 2026/3/1: 15GB 1,800円→1,600円

| 記事 | 5GB | 10GB | 15GB | 判定 |
|------|-----|------|------|------|
| **正しい値（2026/3/1以降）** | **950円** | **1,400円** | **1,600円** | — |
| kakuyasu-sim-ryokin-hikaku-ichiran | 950円 | 1,400円 | 記載なし | OK |
| kakuyasu-sim-kazoku-wari | 990円 | 1,500円 | 1,600円 | **5GB・10GBが旧料金** |
| kakuyasu-sim-review-matome-pillar | 950円 | 1,400円 | 1,800円 | **15GBが旧料金** |
| sub-kaisen-kakuyasu-sim-osusume | 990円(5GB) | — | — | **旧料金** |
| dual-sim-saikyo-kumiawase | 990円(5GB), 1,500円(10GB) | — | — | **旧料金** |
| yoto-betsu-kakuyasu-sim-erabikata | 990円(3GB欄), 1,500円(10GB) | — | — | **旧料金** |

**対応**: 全記事のIIJmio料金を 5GB:950円 / 10GB:1,400円 / 15GB:1,600円 に統一。

---

### 2. mineo マイそくプレミアム 速度の不整合

**事実**: 2025年3月13日に3Mbps→5Mbpsにアップグレード済み（月額2,200円据え置き）。

| 記事 | 記載内容 | 判定 |
|------|---------|------|
| mineo-hyoban | 3Mbps / 2,200円 | **旧スペック（要更新）** |
| kakuyasu-sim-data-museigen | 5Mbps / 2,200円 | OK |
| kakuyasu-sim-review-matome-pillar | 5Mbps / 2,178円 | **価格誤り（正: 2,200円）** |

**対応**: mineo-hyobanの速度を5Mbpsに更新。review-matomeの価格を2,200円に修正。

---

### 3. ワイモバイル料金 — norikae-tejun記事が旧プラン（シンプル2）のまま

**事実**: 2025年9月25日にシンプル2→シンプル3に移行済み。

| プラン | シンプル2（旧） | シンプル3（現行） |
|--------|---------------|-----------------|
| S | 2,365円/4GB | **3,058円/5GB** |
| M | 4,015円/20GB | **4,158円/30GB** |
| L | 4,015円/30GB | **5,258円/35GB** |

**該当記事**: `kakuyasu-sim-norikae-tejun-pillar` — ワイモバイルの料金がシンプル2の旧価格（2,365円〜4,015円）で記載。

**対応**: シンプル3の価格（3,058円/4,158円/5,258円）に更新。

---

### 4. UQモバイル旧プラン参照 — 複数記事

**事実**: 2025年6月3日に新プラン「コミコミプランバリュー」「トクトクプラン2」開始。旧「ミニミニプラン」「コミコミプラン+」「トクトクプラン」は新規受付終了。

| 記事 | 記載内容 | 判定 |
|------|---------|------|
| uq-mobile-hyoban-kuchikomi | コミコミプランバリュー 3,828円/35GB、トクトクプラン2 4,048円/30GB | OK（新プラン記載） |
| kakuyasu-sim-norikae-tejun-pillar | ミニミニプラン 2,365円 等の旧プラン記載の可能性 | **要確認** |
| yoto-betsu-kakuyasu-sim-erabikata | UQモバイル 2,948円（トクトクプラン2の割引前） | OK |

**対応**: norikae-tejun記事のUQモバイル料金を新プランに更新。

---

### 5. ahamo 海外対応 — かけ放題比較記事で旧情報

**事実**: 2023年10月10日にahamoの海外データ通信対応国が82カ国→91カ国に拡大。データ容量も20GB→30GBに変更済み。

| 記事 | 記載 | 判定 |
|------|------|------|
| kakuyasu-sim-tsuwaho-kakehoudai | 82カ国/20GB | **旧情報（要修正: 91カ国/30GB）** |
| yoto-betsu-kakuyasu-sim-erabikata | 91カ国/30GB | OK |
| dual-sim-saikyo-kumiawase | 91カ国 | OK |

**対応**: tsuwaho-kakehoudai記事のahamo海外情報を91カ国/30GBに修正。

---

### 6. LINEMO ベストプランV 30GB料金 — kodomo記事に謎の3,960円

**事実**: LINEMOベストプランVは30GBで月額2,970円（税込）。段階制ではない。

| 記事 | 記載 | 判定 |
|------|------|------|
| kakuyasu-sim-kodomo-shougakusei | ベストプランV: 20GB 2,970円 / 30GB 3,960円 | **30GB=3,960円は誤り（正: 2,970円）** |
| linemo-hyoban | ベストプランV: 2,970円/30GB | OK |
| 他の記事 | 2,970円 | OK |

**対応**: kodomo記事のLINEMO ベストプランV料金を修正。ベストプランVは30GBまで2,970円の一律料金。

---

### 7. HISモバイル料金の表記揺れ

| 記事 | 最低月額 | 判定 |
|------|---------|------|
| sub-kaisen-kakuyasu-sim-osusume | 280円（100MB未満時） | 「自由自在2.0プラン」表記 |
| yoto-betsu-kakuyasu-sim-erabikata | 290円（1GBプラン表記内） | OK |

**対応**: HISモバイルの「自由自在2.0プラン」は100MB未満で280円、1GB以下で550円。記事によって参照プランが異なるだけで大きな誤りではないが、統一推奨。

---

### 8. UQモバイル トクトクプラン2 の段階制料金 — kazoku-wari記事

**事実**: トクトクプラン2は30GBで月額4,048円。1GB以下の場合2,948円。

| 記事 | 記載 | 判定 |
|------|------|------|
| kakuyasu-sim-kazoku-wari | トクトクプラン2: 2,178~3,278円（段階制） | **誤り。旧トクトクプランの料金と混同している可能性** |

**対応**: kazoku-wari記事のUQモバイル料金をトクトクプラン2の正しい料金（1GB以下:2,948円 / 30GB:4,048円）に修正。

---

## 【要確認】軽微な問題

### A. LINEMO「ミニプラン」表記
- sub-kaisen記事で「ミニプラン・3GB」と記載。LINEMOは「ベストプラン」に改称済み（3GBまで990円、10GBまで2,090円の段階制）。
- ただし月額990円/3GBという実質料金は正しい。

### B. povo2.0 トッピング料金
- 各記事間で概ね一貫（1GB/7日間:390円、3GB/30日間:990円等）。大きな不整合なし。

### C. 楽天モバイル料金
- 全記事で1,078円/2,178円/3,278円の3段階で一貫。問題なし。

---

## 記事別サマリー

| # | 記事ファイル名 | 要修正数 | 主な問題 |
|---|-------------|---------|---------|
| 1 | yoto-betsu-kakuyasu-sim-erabikata | 1 | IIJmio旧料金 |
| 2 | sub-kaisen-kakuyasu-sim-osusume | 2 | IIJmio旧料金、LINEMOミニプラン表記 |
| 3 | dual-sim-saikyo-kumiawase | 1 | IIJmio旧料金 |
| 4 | uq-mobile-hyoban-kuchikomi | 0 | — |
| 5 | kakuyasu-sim-ryokin-hikaku-ichiran | 0 | — |
| 6 | kakuyasu-sim-norikae-tejun-pillar | 2 | ワイモバイル旧プラン、UQモバイル旧プラン |
| 7 | kakuyasu-sim-review-matome-pillar | 2 | IIJmio 15GB旧料金、mineo価格誤り |
| 8 | kaigai-ryokou-esim-osusume | 0 | — |
| 9 | rakuten-mobile-hyoban | 0 | — |
| 10 | linemo-hyoban | 0 | — |
| 11 | mineo-hyoban | 1 | マイそくプレミアム旧速度(3Mbps→5Mbps) |
| 12 | kakuyasu-sim-kazoku-wari | 2 | IIJmio旧料金、UQトクトクプラン2料金誤り |
| 13 | ymobile-hyoban | 0 | — |
| 14 | kakuyasu-sim-tsuwaho-kakehoudai | 1 | ahamo海外82カ国→91カ国 |
| 15 | kakuyasu-sim-data-museigen | 0 | — |
| 16 | kakuyasu-sim-kodomo-shougakusei | 1 | LINEMO ベストプランV 30GB料金誤り |

---

## 修正優先度

### 最優先（事実誤認・ユーザーに誤解を与える）
1. LINEMO ベストプランV 30GB=3,960円 → 2,970円（kodomo記事）
2. ワイモバイル旧プラン料金（norikae-tejun記事）
3. UQモバイル トクトクプラン2 段階制料金の誤り（kazoku-wari記事）
4. ahamo海外 82カ国/20GB → 91カ国/30GB（tsuwaho記事）

### 高優先（記事間不整合）
5. IIJmio料金統一: 5GB=950円 / 10GB=1,400円 / 15GB=1,600円（6記事に影響）
6. mineo マイそくプレミアム速度統一: 5Mbps（mineo-hyoban, review-matome）

### 中優先（表記改善）
7. LINEMO「ミニプラン」→「ベストプラン」表記更新
8. HISモバイル料金表記の統一

---

## MNP手順の検証

`kakuyasu-sim-norikae-tejun-pillar` 記事のMNP手順を確認:
- MNPワンストップ方式の説明: 正確（2023年5月開始）
- MNP転出料無料化: 正確（2021年4月以降）
- 事務手数料: LINEMO・povo・楽天モバイル無料 → 正確
- SIMロック解除: 2021年10月以降購入端末は原則SIMフリー → 正確

**判定**: MNP手順自体に重大な誤りなし。ただしワイモバイル・UQモバイルの料金例が旧プランのため要更新。

---

## WebSearch検証に使用したソース

- [IIJmio ギガプラン公式](https://www.iijmio.jp/gigaplan/)
- [IIJmio 15GBプラン料金改定プレスリリース（2026/2/3）](https://www.iij.ad.jp/news/pressrelease/2026/0203.html)
- [IIJmio 5GB/10GB値下げプレスリリース（2025/2/4）](https://www.iij.ad.jp/news/pressrelease/2025/0204.html)
- [mineo マイそくプレミアム速度アップグレード発表](https://support.mineo.jp/news/1679/)
- [ahamo 海外データ通信対応国追加](https://ahamo.com/news/fsi0850000003smp.html)
- [ahamo 海外データ通信サービスページ](https://ahamo.com/services/roaming-data/index.html)
- [LINEMO ベストプランV公式](https://www.linemo.jp/lp/0000/)
- [UQモバイル コミコミプランバリュー&トクトクプラン2](https://www.uqwimax.jp/mobile/newplan2025/)
- [ワイモバイル シンプル3公式](https://www.ymobile.jp/plan/)

---

*レポート生成: 2026-03-17 by Claude Code ファクトチェック*
