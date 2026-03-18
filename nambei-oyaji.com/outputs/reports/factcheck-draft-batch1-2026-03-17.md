# Fact-Check Report: Draft Articles Batch 1
**Date**: 2026-03-17
**Checker**: Claude Code (Opus 4.6)
**Articles checked**: 6 of 8 (2 files not found)

---

## Files Not Found
- `article-paraguay-ijuu-shippai.md` (記事#6) — ファイルが存在しない
- `article-kaigai-hoken-hikaku.md` (記事#24) — ファイルが存在しない

---

## 1. article-paraguay-zeikin.html (税金安い理由)

### 所得税 8~10%
- **記事の記載**: 個人所得税 8~10%、最低賃金の36倍~120倍で8%、120倍超で10%
- **検証結果**: OK。PWC Tax Summaries・GoParaguayともにIRP 8%/10%の2段階を確認。
- **最低賃金の記載**: 記事は「2025年の最低賃金は月額約2,680,373グアラニー（約5万円前後）」と記載。
- **実際**: 2025年7月1日から**2,899,048 Gs**に引き上げ済み（3.6%増）。記事の数字は2024年の旧最低賃金の可能性が高い。
- **判定**: **要修正** — 最低賃金を2,899,048 Gsに更新すべき。年間所得の閾値も連動して変わる。

### 法人税 10%
- **検証結果**: OK。IRE（旧IRACIS/IRAGRO統合）一律10%。PWC・Chambers確認済み。

### 消費税（IVA）一般10%、食料品5%
- **検証結果**: OK。ただし5%は「食料品全般」ではなく「基本食品バスケット（米・麺・食用油・マテ・牛乳・卵・小麦粉・ヨード塩）」と「不動産賃貸・売買・利息」に限定。記事の「食料品・医薬品5%」はやや広すぎる表現。
- **判定**: **要精緻化** — 「基本食品（canasta familiar）・不動産取引等5%」と限定表現にすべき。

### 配当税 8%
- **記事の記載**: 配当税8%
- **実際**: 居住者8%、**非居住者15%**（IDU）。記事は居住者のみ記載。
- **判定**: **要補足** — 非居住者15%の記載を追加すべき。

### 相続税・贈与税ゼロ
- **検証結果**: OK。PWC・複数ソースで確認。パラグアイに相続税・贈与税は存在しない。

### 属地主義（テリトリアル課税）
- **検証結果**: OK。パラグアイ国内源泉所得のみ課税。海外源泉所得は非課税。

### 住民税なし
- **検証結果**: OK。パラグアイに日本型の住民税は存在しない。

### 税理士費用「月額5~15万グアラニー（約1,000~3,000円）」
- **判定**: **要確認** — 5万Gs=約700円、15万Gs=約2,100円程度（1Gs≈0.014円）。独自検証が困難だが、レンジとしては妥当な範囲。

### 法人税+配当税の実効税率「約17%」
- **計算**: 利益100 × 10% = 税10、残り90 × 8% = 7.2、合計17.2/100 = 17.2%
- **検証結果**: OK。計算は正しい（居住者の場合）。

---

## 2. article-paraguay-visa.html (ビザ種類)

### 法律6984号（2022年）で制度変更
- **検証結果**: OK。Ley N 6984/2022 de Migraciones、移民局公式サイトで確認。

### 「いきなり永住権」が廃止、一時居住2年→永住権
- **検証結果**: OK。一時居住許可（最大2年）→永住権のステップ制に変更。

### 「以前は銀行に約5,000ユーロを預金すれば永住権が取れた」
- **検証結果**: 概ねOK。旧制度では$5,000程度の銀行預金で永住権取得可能だった。Ley 6984で**この預金要件自体が撤廃**された（一時居住にも不要に）。
- **判定**: **要補足** — 現行制度では銀行残高証明は「生活資金の証明」として求められるが、具体的な金額要件は撤廃されている点を明記すべき。

### 市民権「永住権取得後さらに3年」（計5年）
- **記事の記載**: 永住権後3年、年間183日以上の滞在要件あり
- **実際**: 永住権後3年で申請可能。年間183日の滞在要件あり。
- **検証結果**: OK。ただし記事本文に「年間183日以上」と書かれているのに、別の箇所（immigration-failures記事）では「年間9ヶ月以上」と記載されており**矛盾**がある（後述）。

### 観光ビザ免除90日
- **検証結果**: OK。日本国籍はビザ免除で90日滞在可能。

### 一時居住許可の費用目安「合計2,000~4,000ドル」
- **検証結果**: 妥当な範囲。弁護士費用1,000~3,000ドル＋手数料・翻訳費用。

### 投資による直接永住権ルート（記事に記載なし）
- **判定**: **情報追加推奨** — USD 70,000の投資＋5人以上の現地雇用で一時居住を経ずに永住権取得可能なルートがある。読者に有益な情報。

---

## 3. article-paraguay-internet.html (インターネット通信)

### ISP: Tigo, Personal, Copaco
- **検証結果**: OK。ただし**VOX**（第4のISP）も近年存在感を増している。

### 光回線100~300Mbps、月額15万~40万Gs（約3,000~8,000円）
- **実際**: Tigoの光回線はエントリープランが約29,900 Gs（約420円）から存在。都市部の100~150Mbpsプランは$18~$20（約2,800~3,100円）程度。
- **判定**: **要修正** — 下限15万Gs（約2,100円）はやや高め。安価なプランは10万Gs未満から存在する。上限40万Gs（500Mbps級）は妥当。

### モバイル3キャリア: Tigo, Personal, Claro
- **検証結果**: OK。

### モバイル料金: Tigo 15GB 約5万Gs
- **判定**: **要最新確認** — プランは頻繁に変更されるが、月約5万Gs（約700円）で15GB程度は妥当なレンジ。

### 停電「月に2~3回」
- **判定**: 独自検証困難だが、パラグアイの電力事情（夏季の雷雨・停電）は広く知られた事実であり、妥当な記述。

---

## 4. article-paraguay-kyouiku.html (教育インターナショナルスクール)

### ASA（American School of Asuncion）年間学費「約100~150万円」
- **実際**: US State Dept 2023-2024 Fact Sheetでは K5-G12 学費 $8,806/年（約130万円）。入学金は別途$7,750~$9,500。
- **判定**: **やや過大** — 授業料のみなら約130万円。入学金込み初年度は150万円超だが、年間ベースでは100~150万円のレンジは入学金込みの印象を与える。「授業料約$8,800（約130万円）＋入学金別途」と明記すべき。ただし2025-2026の最新学費は未公開のため値上げ可能性あり。

### パラグアイの学年「2月開始」
- **検証結果**: OK。パラグアイの学年は2月に開始。

### 義務教育9年間
- **検証結果**: OK。初等教育（Educacion Escolar Basica）9年間が義務教育。

### インター校の年間学費「50~150万円」
- **判定**: OK。ASA以外のバイリンガル校・インター校のレンジとして妥当。

---

## 5. article-paraguay-gengo.html (言語スペイン語)

### 公用語はスペイン語とグアラニー語
- **検証結果**: OK。

### 「国民の約90%が何らかの形で（グアラニー語を）理解できる」
- **実際**: 2024年EPHC調査では約70%が日常的にグアラニー語を使用。Jopara（混合言語）を含めると約90%。
- **判定**: **要精緻化** — 「約90%」はJopara（スペイン語+グアラニー語の混合）を含む数字。純粋なグアラニー語話者は約30%。「Joparaを含めると約90%」と明記すべき。

### 「日系人約7,000人」
- **実際**: 複数ソースで約7,000~10,000人。
- **判定**: OK。控えめな数字だが許容範囲内。

### 「EF英語能力指数で『非常に低い』カテゴリ」
- **実際**: EF EPI 2025でパラグアイは**43位/スコア531**。これは「Low」ではなく**「Moderate」**カテゴリ（500-549）に分類される可能性がある。
- **判定**: **要修正** — 最新のEF EPIでは「非常に低い（Very Low）」ではない。2025年版の正確なカテゴリ名を確認して修正すべき。

---

## 6. article-paraguay-immigration-failures.html (移住失敗注意点7選)

### 市民権「年間9ヶ月以上の滞在要件あり」
- **実際**: 複数ソースで**年間183日**（約6ヶ月）の滞在要件。
- **判定**: **要修正（重大）** — 「9ヶ月」は誤り。正しくは**183日（約6ヶ月）**。visa記事との矛盾あり。

### 犯罪統計「殺人442件、傷害・暴行7,085件、強盗5,259件、窃盗12,464件」（2023年）
- **実際**: 2023年の殺人率は6.2/10万人（人口692万で約429件）。強盗は上半期だけで約10,000件（一般+加重合計）。
- **判定**: **要確認** — 殺人件数442件は概ね妥当（6.2/10万×692万≒429）だが出典の年度を明記すべき。強盗5,259件は**上半期のみの一般強盗**の可能性があり、通年の加重強盗を含めると大幅に増える。

### 「人口約692万人」
- **判定**: OK。概ね妥当（2023年推定約700万人前後）。

### その他の記述（物価、医療、資金計画）
- **判定**: 定性的な記述が中心で、具体的な数字の誤りは見当たらない。生活費目安「月20~30万円」は妥当。

---

## 全記事共通チェック

### 本名・居住地ルール
- 全6記事とも本名（水野達也）の記載なし: OK
- 全6記事とも居住地は「アスンシオン」と表記: OK
- ペンネーム「南米おやじ」使用: OK

---

## 修正優先度サマリー

| 優先度 | 記事 | 問題 | 内容 |
|--------|------|------|------|
| **高** | immigration-failures | 市民権滞在要件 | 「9ヶ月」→「183日（約6ヶ月）」に修正 |
| **高** | zeikin | 最低賃金 | 2,680,373 Gs → 2,899,048 Gs（2025年7月~） |
| **中** | zeikin | 配当税 | 居住者8%のみ→非居住者15%を追記 |
| **中** | zeikin | IVA 5%対象 | 「食料品・医薬品」→「基本食品バスケット・不動産取引等」 |
| **中** | gengo | EF EPI | 「非常に低い」→最新ランキング（43位/Moderate）に修正 |
| **中** | gengo | グアラニー語90% | Jopara含む旨を明記 |
| **低** | internet | 光回線下限価格 | 15万Gs→10万Gs未満のプランも存在 |
| **低** | visa | 投資ルート | USD 70,000投資による直接永住権ルートを追記推奨 |
| **低** | visa | 預金要件撤廃 | 現行制度では金額要件なしと明記推奨 |
| **低** | kyouiku | ASA学費 | 授業料$8,806と入学金を分けて記載推奨 |

---

## Sources
- [PWC - Paraguay Individual Taxes](https://taxsummaries.pwc.com/paraguay/individual/taxes-on-personal-income)
- [PWC - Paraguay Corporate Taxes](https://taxsummaries.pwc.com/paraguay/corporate/taxes-on-corporate-income)
- [GoParaguay - Tax System Guide 2026](https://goparaguay.co/en/blog/paraguay-tax-system-guide)
- [Paraguay Migraciones - Residencia Temporal](https://migraciones.gov.py/residencia-temporal/)
- [Destination Paraguay - Permanent Residence Guide 2026](https://destination-paraguay.com/en/permanent-residence-in-paraguay-100-free-guide-2026/)
- [Chambers - Corporate Tax 2025 Paraguay](https://practiceguides.chambers.com/practice-guides/corporate-tax-2025/paraguay)
- [Paraguay Pathways - VAT IVA](https://paraguaypathways.com/vat-iva/)
- [Trading Economics - Paraguay Minimum Wage](https://tradingeconomics.com/paraguay/minimum-wages)
- [WageIndicator - Paraguay Minimum Wage July 2025](https://wageindicator.org/salary/minimum-wage/minimum-wages-news/2025/minimum-wage-updated-in-paraguay-from-01-july-2025-july-14-2025)
- [US State Dept - ASA Fact Sheet 2023-2024](https://2021-2025.state.gov/the-american-school-of-asuncion-fact-sheet/)
- [EF EPI 2025 - Paraguay](https://www.ef.com/wwen/epi/regions/latin-america/paraguay/)
- [Wikipedia - Languages of Paraguay](https://en.wikipedia.org/wiki/Languages_of_Paraguay)
- [Statista - Homicide Rate Paraguay 2023](https://www.statista.com/statistics/984892/homicide-rate-paraguay/)
- [Global Citizen Solutions - Paraguay Citizenship](https://www.globalcitizensolutions.com/paraguay-citizenship/)
- [ImmigrantInvest - Paraguay Citizenship 2026](https://immigrantinvest.com/blog/paraguay-citizenship/)
