# Fact-Check Report: Draft Articles Batch 2
**Date**: 2026-03-17
**Checker**: Claude Code (Opus 4.6)
**Articles checked**: 0 of 17 (全17記事のファイルが未生成)

---

## ステータス: 全17記事のドラフトファイルが存在しない

`article-management.csv` には下書き（ステータス「下書き」）として17記事が登録されているが、対応するファイル（.md / .html）はいずれもディスク上に存在しない。記事生成が未実行の状態。

### 対象記事一覧（ファイル未生成）

| # | CSV行 | ファイル名 | トピック |
|---|-------|-----------|---------|
| 1 | 30 | article-kaigai-mental-homesick.md | ホームシック対策 |
| 2 | 31 | article-kaigai-ijuu-mochimono.md | 海外移住持ち物リスト |
| 3 | 32 | article-kaigai-nenkin-shakaihoken.md | 年金・社会保険 |
| 4 | 33 | article-kaigai-zaijuu-zeikin.md | 確定申告・税金 |
| 5 | 36 | article-kaigai-programming-fukugyou.md | プログラミング副業 |
| 6 | 37 | article-kaigai-douga-sns.md | 動画編集・SNS運用 |
| 7 | 38 | article-kaigai-online-buppan.md | オンライン物販 |
| 8 | 40 | article-kaigai-nomad-osusume.md | ノマドおすすめ国 |
| 9 | 41 | article-paraguay-chintai.md | パラグアイ賃貸 |
| 10 | 43 | article-paraguay-kigyou.md | パラグアイ起業 |
| 11 | 44 | article-paraguay-koutsuu.md | パラグアイ交通 |
| 12 | 45 | article-paraguay-lifeline.md | 水道・電気・ガス |
| 13 | 46 | article-paraguay-kaimono.md | スーパー・買い物 |
| 14 | 47 | article-paraguay-nihonshoku.md | 日本食レストラン |
| 15 | 48 | article-paraguay-kosodate-hiyo.md | 子育て・教育費 |
| 16 | 49 | article-paraguay-kodomo-naraigoto.md | 子供の習い事 |
| 17 | 50 | article-paraguay-bunka-event.md | 祝日・文化イベント |

---

## 事前ファクトチェック: 記事生成時に使うべき正確なデータ

ファイルは存在しないが、これら17記事が生成される際に含まれる可能性が高い事実情報をWebSearchで事前検証した。以下は記事生成時の参照データとして使用すること。

---

### 1. 年金・社会保険（記事#32）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 国民年金保険料（2025年度） | 月額17,510円 | 日本年金機構 |
| 国民年金保険料（2026年度） | 月額17,920円（+410円） | 公的保険アドバイザー協会 |
| 海外転出時の国民年金 | 任意加入（義務なし）、20~65歳対象 | 日本年金機構 |
| 国民健康保険 | 海外転出届提出で脱退（加入義務消滅） | 厚労省 |
| 日本-パラグアイ社会保障協定 | **締結なし**（2025年時点で対象23ヶ国にパラグアイ含まれず） | 日本年金機構 |
| 海外転出届 | 出国予定日の14日前から手続き可能 | 各市区町村 |

**注意点**: 「パラグアイと社会保障協定がある」と書かないこと。存在しない。

---

### 2. 確定申告・税金（記事#33）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 非居住者の定義 | 日本国内に住所がなく、1年以上居所もない者 | 所得税法 |
| 非居住者の課税範囲 | 国内源泉所得のみ | 国税庁 |
| 非居住者の所得控除 | 雑損控除（国内資産の損失のみ）に限定 | マネーフォワード |
| 住民税の回避 | 1月1日時点で日本に住所がなければ翌年度の住民税なし | マネーフォワード |
| 納税管理人 | 非居住者は国内源泉所得がある場合、納税管理人を選定して確定申告 | 国税庁 |
| 出国時の予定納税 | 前年の予定納税基準額が15万円以上の場合、出国前に手続き必要 | 国税庁 |

**注意点**: 「非居住者は確定申告不要」と一律に書かないこと。国内源泉所得（不動産収入、日本企業からの報酬等）がある場合は申告義務あり。

---

### 3. パラグアイ賃貸（記事#41）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| アスンシオン家賃相場 | $450~$620/月（1BR、中心部） | Wise, Numbeo, ExpatSettle |
| 高級エリア（Villa Morra, Las Lomas） | $600~$1,000+/月 | 各種不動産サイト |
| 不動産価格 | $1,500~$2,000/m2（好立地アパート） | The Wandering Investor |
| 人気エリア | Villa Morra, Las Lomas, Centro | 複数ソース |

**注意点**: 家賃を「月$200~$300」のように極端に安く書かないこと。アスンシオンの家賃は近年上昇傾向。

---

### 4. パラグアイ起業（記事#43）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| SRL（合同会社）最低資本金 | なし（最低資本金要件なし） | Bejarano Consultant |
| SRL設立費用（政府手数料） | PYG 3,000,000~6,000,000（$410~$820）+ 公告費 PYG 1,500,000（$205） | Bejarano Consultant |
| 弁護士・代行込み総費用 | $3,500~$6,650（初年度） | 複数コンサル |
| 設立期間 | 4~6週間 | 複数ソース |
| 取締役要件 | 最低1名がパラグアイ居住者（一時居住でも可） | Multiplier |
| 株主要件 | 最低2名 | 複数ソース |
| 法人税 | 10%（IRE） | PWC |

**注意点**: 「SRL設立は$500で可能」のように安すぎる金額を書かないこと。政府手数料だけでも$600以上かかる。

---

### 5. パラグアイ交通（記事#44）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| バス料金（エアコン付き） | 3,400 Gs（約$0.45） | ParaguayPulse, SimonsParaguay |
| バス料金（エアコンなし） | 2,300 Gs（約$0.30） | 同上 |
| ICカード（Jaha/Mas） | 購入25,000 Gs（1回分3,400 Gs含む） | 同上 |
| バス現金払い | **不可**（ICカード必須） | SimonsParaguay |
| Bolt/Uber市内移動 | $5~$10程度 | ParaguayPulse |
| Bolt vs タクシー | Boltの方が安い（約20%安） | 複数ソース |
| タクシーメーター | メーターがあるが使わないドライバーが多い。事前交渉推奨 | 複数ソース |

**注意点**: 「バスは現金で払える」と書かないこと。ICカード（Jaha or Mas）が必須。

---

### 6. 水道・電気・ガス（記事#45）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 電力会社 | ANDE（国営、垂直統合型） | Wikipedia |
| 電気料金（家庭用） | PYG 401.995/kWh（$0.058/kWh）※2025年3月時点 | GlobalPetrolPrices |
| 世界平均との比較 | 世界平均の32.1%（非常に安い） | GlobalPetrolPrices |
| 水道会社 | ESSAP（国営） | — |
| LPGガス（10kgボンベ） | 小売価格 約90,000 Gs（約$12） | PuntoInformativo |
| LPGガス（13kgボンベ） | 小売価格 約120,000 Gs（約$16） | 同上 |
| 電力源 | 99%水力発電（イタイプー・ヤシレター） | Wikipedia |

**注意点**: 電気代の安さはパラグアイの大きなメリット。ただし停電は夏季に頻発する点も併記すること。

---

### 7. スーパー・買い物（記事#46）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 主要チェーン: Stock | 45店舗以上、最大手 | MoveToParaguay |
| 主要チェーン: Superseis（S6） | 30店舗以上、セルフチェックアウト・QR決済対応 | VivirEnParaguay |
| その他チェーン | Biggie, España（ローカル系） | 複数ソース |
| ローカルカード割引 | Superseis等でローカル銀行カード払いだと大幅割引 | MoveToParaguay |
| 基本食品 | 米・パスタ・食用油は安価 | 複数ソース |

---

### 8. 日本食レストラン（記事#47）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| Restaurante Sukiyaki | 1970年創業、Constitucion 763。農水省「日本食親善大使」認定（2021年） | TripAdvisor |
| Hiroshima Restaurant | 2011年以前から営業、地元で人気 | TripAdvisor |
| 寿司の品質 | パラグアイは内陸国のため魚はチリ・ブラジルからの輸入。品質に限界あり | TripAdvisor |
| 日本人コミュニティ | Nihon Matsuri（日本祭り）がアスンシオンで開催 | TripAdvisor |

**注意点**: 「アスンシオンには日本食レストランが多い」と書かないこと。選択肢は限られる。

---

### 9. 子育て・教育費（記事#48）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| ASA年間授業料 | PK: $5,715、K5-G12: $8,806 | US State Dept 2023-2024 |
| ASA年間登録料 | $700/生徒 | 同上 |
| ASA入学金（一回限り） | K4-G5: $7,750、G6-8: $8,500、G9-12: $9,500 | 同上 |
| SEK Paraguay（IB校） | $6,000~$10,000/年 | ExpatLife.ai |
| バイリンガル私立校 | $200~$500/月 | MoveToParaguay |
| インター校全般 | $3,000~$10,000/年（トップ校は$15,000超も） | ExpatLife.ai |
| 家庭教師 | $9~$20/時間（70,000~150,000 PYG） | ExpatLife.ai |

---

### 10. 子供の習い事（記事#49）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 人気スポーツ | サッカー（最人気）、テニス、バスケ、水泳 | Britannica, TalesMag |
| Centro Paraguayo Japones | 体操、空手等のクラスあり | TalesMag |
| 月謝の具体額 | **検証不能**（公開データなし）。記事に具体額を書く場合は「筆者調べ」と明記すること | — |

**注意点**: 習い事の月謝について公開データがほぼ存在しない。実体験ベースで書き、「一般的に日本の1/3~1/5程度」等の曖昧な表現を避けること。

---

### 11. 祝日・文化イベント（記事#50）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 年間祝日数 | 14日 | TimeAndDate |
| 独立記念日 | 5月14日・15日（2026年は木金→連休） | TimeAndDate |
| 英雄の日 | 3月1日（三国同盟戦争終結記念） | TimeAndDate |
| チャコ休戦記念日 | 6月12日 | TimeAndDate |
| 憲法記念日 | 6月20日（1992年憲法採択） | TimeAndDate |
| アスンシオン建都記念日 | 8月15日（1537年建設） | TimeAndDate |
| カアクペの聖母の日 | 12月8日（最大の宗教行事、巡礼あり） | TimeAndDate |
| FIFA W杯関連 | 政府が最大3日の臨時祝日を宣言可能（2026年W杯出場関連） | AsuncionTimes |

**注意点**: 2026年のパラグアイFIFA W杯出場により臨時祝日が追加される可能性がある。

---

### 12. ホームシック対策（記事#30）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 発症時期 | 渡航後6ヶ月以内が最多、1年を過ぎると大幅減 | JICA調査 |
| ストレス要因 | 仕事面のサポート欠如、生活満足度の低さ | JICA調査 |
| 企業の懸念 | 赴任者の安全・健康・メンタルヘルスを挙げた企業が61%（2021年マーサー調査） | マーサー |

---

### 13. ノマドおすすめ国（記事#40）

| 項目 | 正確なデータ | 出典 |
|------|-------------|------|
| 2026年ランキング上位 | スペイン、マルタ、ポルトガル、ドイツ、ハンガリー | Citizen Remote, ImmigrantInvest |
| Nomad List 1位 | バンコク（スコア4.55/5） | Nomad List |
| スペイン税制優遇 | Beckham Law: 外国所得0%、国内所得24%（最大6年） | Citizen Remote |
| ポルトガルD8ビザ | 月収約€3,680（最低賃金の4倍）が必要 | Citizen Remote |
| 格安都市 | アルバニア（月€800）、バリ（家賃$400~$600） | GlobalTravelWide |
| パラグアイのノマドビザ | **存在しない**（一時居住許可で対応） | — |

**注意点**: パラグアイにはデジタルノマドビザが存在しない。一般の一時居住許可で滞在する形になる点を明記すること。

---

### 14~17. 持ち物リスト / プログラミング副業 / 動画編集SNS / オンライン物販

これら4記事は主に主観的・経験ベースの内容が中心となるため、ファクトチェック対象となる具体的数値は限定的。以下の点のみ注意:

- **持ち物リスト**: 変圧器について「パラグアイは220V/50Hz」と正確に書くこと（日本は100V/50-60Hz）
- **プログラミング副業**: スクール料金を記載する場合は最新価格を確認（DMM WEBCAMP、TechAcademy等は頻繁に改定）
- **動画編集**: クラウドソーシングの手数料率（CrowdWorks 5~20%、ココナラ 22%）は最新を確認
- **オンライン物販**: eBayの販売手数料（カテゴリ別10~15%）、メルカリの手数料（10%）は正確に記載

---

## 全記事共通の注意事項

### 本名・居住地ルール
- 本名（水野達也）は絶対に記載禁止。ペンネーム「南米おやじ」のみ
- 居住地は「アスンシオン」と表記。ランバレとは絶対に書かない

### 為替レート
- 記事生成時の為替レートを使用し、「1ドル≒約XXX円」「1Gs≒約0.0XX円」と明記すること
- 2026年3月時点の目安: 1 USD ≒ 150円、1 PYG ≒ 0.019円

### batch 1からの引き継ぎ注意
- 最低賃金は2,899,048 Gs/月（2025年7月~）を使用
- IVA 5%対象は「基本食品バスケット（canasta familiar）」に限定
- 市民権の滞在要件は「183日（約6ヶ月）」が正しい（「9ヶ月」は誤り）

---

## 次のアクション

1. **記事生成を実行**: 17記事のドラフトファイルが未生成。`article_generator.py` で生成すること
2. **生成後に再ファクトチェック**: ファイル生成後、本レポートの正確なデータと照合して記事内容を検証すること
3. **本レポートを参照データとして使用**: 各記事の生成プロンプトに本レポートのデータを含めることで、初稿から正確な記事を生成できる

---

## Sources
- [日本年金機構 - 海外居住](https://www.nenkin.go.jp/service/scenebetsu/kaigai.html)
- [公的保険アドバイザー協会 - 2026年度年金額](https://siaa.or.jp/column/175)
- [マネーフォワード - 非居住者の確定申告](https://biz.moneyforward.com/tax_return/basic/54429/)
- [Wise - Cost of Living Asuncion](https://wise.com/gb/cost-of-living/paraguay/asuncion)
- [Numbeo - Cost of Living Paraguay](https://www.numbeo.com/cost-of-living/country_result.jsp?country=Paraguay)
- [Bejarano Consultant - Paraguay Company Registration Fees](https://www.bejaranoconsultant.com/paraguay-company-registration/fees-timelines/index.html)
- [Multiplier - Company Registration Paraguay 2026](https://www.usemultiplier.com/paraguay/company-registration)
- [ParaguayPulse - Getting Around Asuncion](https://paraguaypulse.com/en/getting-around-asuncion-paraguay-uber-bolt-buses)
- [SimonsParaguay - City Buses](https://simonsparaguay.com/using-the-city-buses-in-asuncion-paraguay/)
- [GlobalPetrolPrices - Paraguay Electricity](https://www.globalpetrolprices.com/Paraguay/electricity_prices/)
- [GlobalPetrolPrices - Paraguay LPG](https://www.globalpetrolprices.com/Paraguay/lpg_prices/)
- [MoveToParaguay - Cheapest Supermarkets](https://www.movetoparaguay.com/en/blog/cheap-affordable-supermarkets-asuncion-paraguay)
- [VivirEnParaguay - 5 Supermarkets](https://vivirenparaguay.com/en/daily-life/5-supermarkets-in-Paraguay/)
- [TripAdvisor - Japanese Restaurants Asuncion](https://www.tripadvisor.com/Restaurants-g294080-c27-Asuncion.html)
- [US State Dept - ASA Fact Sheet 2023-2024](https://2021-2025.state.gov/the-american-school-of-asuncion-fact-sheet/)
- [ExpatLife.ai - Education in Paraguay 2026](https://www.expatlife.ai/paraguay/education)
- [MoveToParaguay - Best Schools Paraguay](https://www.movetoparaguay.com/en/blog/best-private-international-schools-paraguay)
- [TimeAndDate - Paraguay Holidays 2026](https://www.timeanddate.com/holidays/paraguay/2026)
- [AsuncionTimes - Paraguay National Holidays 2026](https://asunciontimes.com/paraguay-news/national-news/these-are-paraguays-national-and-public-holidays-of-2026/)
- [Citizen Remote - Best Countries Digital Nomads 2026](https://citizenremote.com/blog/the-best-countries-for-digital-nomads-in-2026/)
- [ImmigrantInvest - Digital Nomad Visa Index 2026](https://immigrantinvest.com/reports/digital-nomad-visa-index-2026/)
- [The Wandering Investor - Asuncion Real Estate](https://thewanderinginvestor.com/international-real-estate/paraguay-asuncion-real-estate-market-investment-guide/)
