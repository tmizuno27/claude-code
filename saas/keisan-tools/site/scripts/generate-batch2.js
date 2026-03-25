const fs = require('fs');
const path = require('path');

const BASE = path.resolve(__dirname, '..');
const DATA_DIR = path.join(BASE, 'data', 'calculators');

const calcs = [
  {
    slug: "blood-type-child", category: "health", subcategory: "medical",
    title: "子供の血液型予測", description: "両親の血液型から子供の血液型の確率を予測",
    metaTitle: "子供の血液型予測ツール｜両親の血液型から確率を計算",
    metaDescription: "両親の血液型を入力して子供の血液型の確率を計算。ABO式血液型の遺伝パターンを表示。",
    calculatorFunction: "bloodTypeChild",
    inputs: [
      { id: "parent1", label: "親1の血液型", type: "select", options: [{ value: "A", label: "A型" }, { value: "B", label: "B型" }, { value: "O", label: "O型" }, { value: "AB", label: "AB型" }], default: "A" },
      { id: "parent2", label: "親2の血液型", type: "select", options: [{ value: "A", label: "A型" }, { value: "B", label: "B型" }, { value: "O", label: "O型" }, { value: "AB", label: "AB型" }], default: "B" },
    ],
    outputs: [
      { id: "result", label: "子供の血液型確率", format: "text", primary: true },
    ],
    explanation: "<h3>血液型の遺伝</h3><p>ABO式血液型は、A・B・Oの3つの遺伝子の組み合わせで決まります。A型はAA/AO、B型はBB/BO、O型はOO、AB型はABの遺伝子型を持ちます。</p>",
    faq: [{ question: "A型×B型の子供は？", answer: "A型25%、B型25%、O型25%、AB型25%の確率です（両親がAOとBOの場合）。" }],
    related: [], popular: false,
  },
  {
    slug: "percentage-change", category: "math", subcategory: "basic",
    title: "増減率計算", description: "2つの数値の増減率（何%増えた/減った）を計算",
    metaTitle: "増減率計算ツール｜何%増えた・減ったか自動計算",
    metaDescription: "変更前と変更後の数値から増減率（パーセント変化）を計算。売上比較・前年比の計算に便利。",
    calculatorFunction: "percentageChange",
    inputs: [
      { id: "oldValue", label: "変更前の値", type: "number", default: 100, min: -999999999, max: 999999999, step: 0.01 },
      { id: "newValue", label: "変更後の値", type: "number", default: 120, min: -999999999, max: 999999999, step: 0.01 },
    ],
    outputs: [
      { id: "change", label: "増減率", format: "text", primary: true },
      { id: "difference", label: "差分", format: "number" },
    ],
    explanation: "<h3>増減率の計算</h3><p>増減率 = (新しい値 - 元の値) ÷ 元の値 × 100%です。正の値は増加、負の値は減少を表します。</p>",
    faq: [{ question: "前年比とは？", answer: "前年同期と比較した増減率のことです。売上が100万→120万なら前年比+20%（または前年比120%）です。" }],
    related: ["percentage"], popular: false,
  },
  {
    slug: "square-root", category: "math", subcategory: "basic",
    title: "平方根計算", description: "数値の平方根（ルート）を計算",
    metaTitle: "平方根計算ツール｜ルート（√）を自動計算",
    metaDescription: "数値を入力して平方根（ルート）を計算。立方根にも対応した無料ツール。",
    calculatorFunction: "squareRootCalc",
    inputs: [
      { id: "number", label: "数値", type: "number", default: 144, min: 0, max: 999999999, step: 0.01 },
    ],
    outputs: [
      { id: "squareRoot", label: "平方根（√）", format: "text", primary: true },
      { id: "cubeRoot", label: "立方根（∛）", format: "text" },
    ],
    explanation: "<h3>平方根とは</h3><p>ある数aの平方根とは、2乗するとaになる数です。√144 = 12（12² = 144）。</p>",
    faq: [{ question: "√2はいくつ？", answer: "約1.41421356...（ひとよひとよにひとみごろ）です。" }],
    related: ["power-calculator"], popular: false,
  },
  {
    slug: "mortgage-affordability", category: "money", subcategory: "loan",
    title: "住宅ローン借入可能額計算", description: "年収から住宅ローンの借入可能額を計算",
    metaTitle: "住宅ローン借入可能額計算ツール｜年収からいくら借りられるか計算",
    metaDescription: "年収・返済比率・金利から住宅ローンの借入可能額を自動計算。マイホーム購入の予算目安に。",
    calculatorFunction: "mortgageAffordability",
    inputs: [
      { id: "annualIncome", label: "年収", type: "number", unit: "万円", default: 500, min: 100, max: 10000, step: 10 },
      { id: "repaymentRatio", label: "返済比率", type: "number", unit: "%", default: 25, min: 10, max: 40, step: 1 },
      { id: "rate", label: "金利", type: "number", unit: "%", default: 1.5, min: 0.1, max: 10, step: 0.1 },
      { id: "years", label: "返済期間", type: "number", unit: "年", default: 35, min: 5, max: 50, step: 1 },
    ],
    outputs: [
      { id: "maxLoan", label: "借入可能額（概算）", format: "text", primary: true },
      { id: "monthlyPayment", label: "月々の返済額上限", format: "text" },
    ],
    explanation: "<h3>借入可能額の計算</h3><p>年間返済額 = 年収 × 返済比率で月々の返済額上限を求め、そこから逆算して借入可能額を算出します。一般的に返済比率は25〜30%が安全圏とされています。</p>",
    faq: [{ question: "年収の何倍まで借りられる？", answer: "一般的に年収の7〜8倍が上限目安です。ただし返済に無理がない額は年収の5〜6倍です。" }],
    related: ["loan-repayment", "rent-vs-buy"], popular: false,
  },
  {
    slug: "commute-cost-compare", category: "life", subcategory: "car",
    title: "通勤費用比較", description: "車通勤と電車通勤のコストを比較",
    metaTitle: "通勤費用比較ツール｜車vs電車の通勤コストを比較",
    metaDescription: "車通勤と電車通勤の月額・年額コストを比較。駐車場代・ガソリン代・定期代を含む総コスト計算。",
    calculatorFunction: "commuteCostCompare",
    inputs: [
      { id: "trainMonthly", label: "電車定期（月額）", type: "number", unit: "円", default: 15000, min: 0, max: 100000, step: 100 },
      { id: "carDistance", label: "車通勤片道距離", type: "number", unit: "km", default: 20, min: 1, max: 200, step: 1 },
      { id: "fuelEfficiency", label: "燃費", type: "number", unit: "km/L", default: 15, min: 3, max: 40, step: 1 },
      { id: "parkingMonthly", label: "駐車場代（月額）", type: "number", unit: "円", default: 10000, min: 0, max: 100000, step: 1000 },
    ],
    outputs: [
      { id: "trainAnnual", label: "電車通勤（年額）", format: "currency" },
      { id: "carAnnual", label: "車通勤（年額）", format: "currency", primary: true },
      { id: "difference", label: "年間差額", format: "text" },
    ],
    explanation: "<h3>通勤費用の比較</h3><p>車通勤のコスト = ガソリン代 + 駐車場代 + 車の維持費（保険・税金・車検等を月2万円と仮定）。電車通勤のコスト = 定期代です。</p>",
    faq: [{ question: "車通勤の隠れコストは？", answer: "保険料・自動車税・車検・メンテナンス・減価償却で月2〜4万円が別途かかります。" }],
    related: ["commute-cost", "fuel-cost"], popular: false,
  },
  {
    slug: "paint-area", category: "life", subcategory: "unit",
    title: "壁面積・ペンキ量計算", description: "部屋の寸法からペンキの必要量を計算",
    metaTitle: "壁面積・ペンキ量計算ツール｜必要なペンキの量を計算",
    metaDescription: "部屋の寸法から壁面積を計算し、必要なペンキの量を算出。DIYのペンキ塗りに便利。",
    calculatorFunction: "paintArea",
    inputs: [
      { id: "length", label: "部屋の長さ", type: "number", unit: "m", default: 5, min: 1, max: 50, step: 0.1 },
      { id: "width", label: "部屋の幅", type: "number", unit: "m", default: 4, min: 1, max: 50, step: 0.1 },
      { id: "height", label: "天井高", type: "number", unit: "m", default: 2.4, min: 1, max: 10, step: 0.1 },
    ],
    outputs: [
      { id: "wallArea", label: "壁面積（窓除く概算）", format: "text", primary: true },
      { id: "paintLiters", label: "必要なペンキ量", format: "text" },
    ],
    explanation: "<h3>壁面積の計算</h3><p>壁面積 = 周囲長 × 天井高 - 窓・ドア面積（約10%差引）。ペンキは1Lで約8〜10m²塗れます（1回塗り）。2回塗りが推奨されるため、必要量は2倍になります。</p>",
    faq: [{ question: "ペンキは何回塗る？", answer: "通常2回塗りが推奨です。1回目で下地を作り、2回目でムラなく仕上げます。" }],
    related: ["paint-calculator", "concrete-volume"], popular: false,
  },
  {
    slug: "sleep-debt", category: "health", subcategory: "body",
    title: "睡眠負債計算", description: "睡眠時間から睡眠負債（不足時間）を計算",
    metaTitle: "睡眠負債計算ツール｜あなたの睡眠不足を数値化",
    metaDescription: "実際の睡眠時間と理想の睡眠時間から、1週間の睡眠負債（不足時間）を計算。",
    calculatorFunction: "sleepDebt",
    inputs: [
      { id: "actualHours", label: "実際の平均睡眠時間", type: "number", unit: "時間", default: 6, min: 1, max: 14, step: 0.5 },
      { id: "idealHours", label: "理想の睡眠時間", type: "number", unit: "時間", default: 7.5, min: 5, max: 12, step: 0.5 },
    ],
    outputs: [
      { id: "dailyDebt", label: "1日の睡眠負債", format: "text" },
      { id: "weeklyDebt", label: "1週間の睡眠負債", format: "text", primary: true },
      { id: "monthlyDebt", label: "1ヶ月の睡眠負債", format: "text" },
    ],
    explanation: "<h3>睡眠負債とは</h3><p>必要な睡眠時間と実際の睡眠時間の差が「睡眠負債」です。成人の理想睡眠時間は7〜9時間。40時間以上の累積負債は注意力・判断力の著しい低下を招きます。</p>",
    faq: [{ question: "睡眠負債は週末に返せる？", answer: "研究では完全な返済は難しいとされています。普段から適切な睡眠時間を確保することが重要です。" }],
    related: ["sleep-calculator", "sleep-cycle"], popular: false,
  },
  {
    slug: "carbon-offset", category: "life", subcategory: "car",
    title: "CO2排出量計算", description: "移動手段別のCO2排出量を計算",
    metaTitle: "CO2排出量計算ツール｜移動手段別のCO2排出量を比較",
    metaDescription: "車・電車・バス・飛行機の移動距離からCO2排出量を計算。環境負荷の比較に。",
    calculatorFunction: "carbonOffset",
    inputs: [
      { id: "distance", label: "移動距離", type: "number", unit: "km", default: 100, min: 1, max: 50000, step: 1 },
      { id: "transport", label: "移動手段", type: "select", options: [{ value: "car", label: "自家用車" }, { value: "train", label: "電車" }, { value: "bus", label: "バス" }, { value: "plane", label: "飛行機" }], default: "car" },
    ],
    outputs: [
      { id: "co2kg", label: "CO2排出量", format: "text", primary: true },
      { id: "treesNeeded", label: "吸収に必要な木の本数", format: "text" },
    ],
    explanation: "<h3>交通手段別CO2排出量</h3><p>1人1kmあたりのCO2排出量（目安）：自家用車130g、バス57g、電車17g、飛行機246g。電車が最もエコな移動手段です。</p>",
    faq: [{ question: "木1本で吸収できるCO2量は？", answer: "スギの成木1本で年間約14kgのCO2を吸収するとされています。" }],
    related: ["carbon-footprint", "ev-charging-cost"], popular: false,
  },
  {
    slug: "gift-amount", category: "life", subcategory: "shopping",
    title: "ご祝儀金額計算", description: "関係性から適切なご祝儀金額を判定",
    metaTitle: "ご祝儀金額計算ツール｜結婚式のご祝儀相場を判定",
    metaDescription: "新郎新婦との関係性と自分の年代からご祝儀の相場金額を判定。結婚式のご祝儀マナーもチェック。",
    calculatorFunction: "giftAmount",
    inputs: [
      { id: "relation", label: "関係性", type: "select", options: [{ value: "friend", label: "友人" }, { value: "colleague", label: "同僚" }, { value: "boss", label: "上司/先輩" }, { value: "relative", label: "親族" }, { value: "sibling", label: "兄弟姉妹" }], default: "friend" },
      { id: "age", label: "自分の年代", type: "select", options: [{ value: "20s", label: "20代" }, { value: "30s", label: "30代" }, { value: "40s", label: "40代以上" }], default: "30s" },
    ],
    outputs: [
      { id: "amount", label: "推奨ご祝儀額", format: "text", primary: true },
      { id: "note", label: "注意事項", format: "text" },
    ],
    explanation: "<h3>ご祝儀の相場</h3><p>ご祝儀は「割り切れない」奇数が縁起が良いとされ、3万円・5万円が一般的です。2万円は「ペア」で許容、4万円・9万円は避けましょう。</p>",
    faq: [{ question: "夫婦で出席する場合は？", answer: "2人で5〜7万円が相場です。個別に3万円ずつよりまとめて奇数にするのがマナーです。" }],
    related: ["wedding-budget", "split-bill"], popular: false,
  },
  {
    slug: "calorie-deficit", category: "health", subcategory: "calorie",
    title: "ダイエットカロリー計算", description: "目標体重から1日の摂取カロリー目標を計算",
    metaTitle: "ダイエットカロリー計算ツール｜1日何kcalで痩せるか計算",
    metaDescription: "現在の体重・目標体重・期間から1日の目標摂取カロリーを計算。健康的なダイエット計画に。",
    calculatorFunction: "calorieDeficit",
    inputs: [
      { id: "currentWeight", label: "現在の体重", type: "number", unit: "kg", default: 70, min: 30, max: 200, step: 0.1 },
      { id: "targetWeight", label: "目標体重", type: "number", unit: "kg", default: 60, min: 30, max: 200, step: 0.1 },
      { id: "weeks", label: "達成期間", type: "number", unit: "週間", default: 12, min: 1, max: 104, step: 1 },
      { id: "gender", label: "性別", type: "select", options: [{ value: "male", label: "男性" }, { value: "female", label: "女性" }], default: "male" },
    ],
    outputs: [
      { id: "dailyCalorie", label: "1日の目標摂取カロリー", format: "text", primary: true },
      { id: "dailyDeficit", label: "1日のカロリー不足量", format: "text" },
      { id: "weeklyLoss", label: "週あたりの減量", format: "text" },
    ],
    explanation: "<h3>ダイエットのカロリー計算</h3><p>体脂肪1kgは約7,200kcalです。1週間に0.5kg減量するには1日あたり約500kcalの赤字が必要です。極端な制限（基礎代謝以下）は健康に悪影響があるため避けましょう。</p>",
    faq: [{ question: "1ヶ月に何kg減量が安全？", answer: "体重の4%以内（70kgの人なら約2.8kg/月）が健康的なペースです。" }],
    related: ["daily-calorie", "basal-metabolism", "calories-bmr"], popular: false,
  },
  {
    slug: "hourly-to-annual", category: "money", subcategory: "salary",
    title: "時給から年収計算", description: "時給・勤務時間から月収・年収を計算",
    metaTitle: "時給から年収計算ツール｜アルバイトの年収を自動計算",
    metaDescription: "時給と週の勤務時間から月収・年収・手取りの目安を計算。扶養内で働く際の上限チェックにも。",
    calculatorFunction: "hourlyToAnnual",
    inputs: [
      { id: "hourlyRate", label: "時給", type: "number", unit: "円", default: 1200, min: 500, max: 50000, step: 10 },
      { id: "hoursPerWeek", label: "週の勤務時間", type: "number", unit: "時間", default: 30, min: 1, max: 60, step: 1 },
    ],
    outputs: [
      { id: "monthlyIncome", label: "月収", format: "currency" },
      { id: "annualIncome", label: "年収", format: "currency", primary: true },
      { id: "wall103", label: "103万円の壁", format: "text" },
      { id: "wall130", label: "130万円の壁", format: "text" },
    ],
    explanation: "<h3>時給から年収の計算</h3><p>月収 = 時給 × 週時間 × 52/12。年収 = 月収 × 12。103万円を超えると所得税、130万円を超えると社会保険の扶養から外れます。</p>",
    faq: [{ question: "103万円と130万円の壁とは？", answer: "103万円超で所得税が発生、130万円超で社会保険の扶養から外れ、自分で社保加入が必要になります。" }],
    related: ["hourly-wage", "annual-income"], popular: false,
  },
  {
    slug: "laundry-cost", category: "life", subcategory: "shopping",
    title: "洗濯コスト計算", description: "洗濯機の1回あたりの水道代・電気代を計算",
    metaTitle: "洗濯コスト計算ツール｜1回の洗濯代はいくら？",
    metaDescription: "洗濯機の容量・水道代・電気代から1回の洗濯にかかるコストを計算。コインランドリーとの比較も。",
    calculatorFunction: "laundryCost",
    inputs: [
      { id: "waterCost", label: "水道単価", type: "number", unit: "円/L", default: 0.24, min: 0.1, max: 1, step: 0.01 },
      { id: "waterUsage", label: "1回の使用水量", type: "number", unit: "L", default: 90, min: 30, max: 200, step: 10 },
      { id: "electricityCost", label: "電気代単価", type: "number", unit: "円/kWh", default: 30, min: 15, max: 50, step: 1 },
      { id: "electricityUsage", label: "1回の消費電力", type: "number", unit: "Wh", default: 70, min: 20, max: 500, step: 10 },
    ],
    outputs: [
      { id: "waterFee", label: "水道代", format: "text" },
      { id: "electricFee", label: "電気代", format: "text" },
      { id: "totalCost", label: "1回の洗濯コスト", format: "text", primary: true },
      { id: "monthlyCost", label: "月30回の場合", format: "text" },
    ],
    explanation: "<h3>洗濯1回のコスト</h3><p>一般的な縦型洗濯機の1回のコストは約25〜35円（水道代22円+電気代2〜3円+洗剤5〜10円）です。ドラム式は水道代が約半分で節水できます。</p>",
    faq: [{ question: "コインランドリーと比較すると？", answer: "コインランドリーは1回300〜500円。年間200回洗う場合、自宅洗濯で年間約5〜7千円、コインランドリーで約6〜10万円です。" }],
    related: ["electricity-cost", "water-cost"], popular: false,
  },
  {
    slug: "screen-time", category: "life", subcategory: "utility",
    title: "スクリーンタイム計算", description: "1日のスクリーンタイムの年間合計を計算",
    metaTitle: "スクリーンタイム計算ツール｜年間の画面時間を計算",
    metaDescription: "1日のスマホ・PC利用時間から年間の累計時間を計算。時間の使い方を見直すきっかけに。",
    calculatorFunction: "screenTime",
    inputs: [
      { id: "dailyHours", label: "1日のスクリーンタイム", type: "number", unit: "時間", default: 6, min: 0.5, max: 20, step: 0.5 },
    ],
    outputs: [
      { id: "weeklyHours", label: "週間合計", format: "text" },
      { id: "monthlyHours", label: "月間合計", format: "text" },
      { id: "annualHours", label: "年間合計", format: "text", primary: true },
      { id: "annualDays", label: "年間日数換算", format: "text" },
    ],
    explanation: "<h3>スクリーンタイムの影響</h3><p>日本人の平均スクリーンタイムは1日約4〜7時間です。過度な画面使用はブルーライトによる眼精疲労、睡眠の質低下、姿勢悪化のリスクがあります。</p>",
    faq: [{ question: "適切なスクリーンタイムは？", answer: "仕事以外で1日2時間以内が推奨されています。20-20-20ルール（20分ごとに20フィート先を20秒見る）で眼精疲労を軽減できます。" }],
    related: [], popular: false,
  },
  {
    slug: "room-air-volume", category: "life", subcategory: "unit",
    title: "部屋の体積・換気計算", description: "部屋の寸法から体積と必要換気量を計算",
    metaTitle: "部屋の体積・換気計算ツール｜空気の量と換気回数を計算",
    metaDescription: "部屋の広さと天井高から空気の体積を計算し、適切な換気回数を表示。エアコン選びの参考にも。",
    calculatorFunction: "roomAirVolume",
    inputs: [
      { id: "area", label: "部屋の広さ", type: "number", unit: "畳", default: 6, min: 1, max: 100, step: 0.5 },
      { id: "height", label: "天井高", type: "number", unit: "m", default: 2.4, min: 1.5, max: 5, step: 0.1 },
    ],
    outputs: [
      { id: "volumeM3", label: "空気の体積", format: "text", primary: true },
      { id: "sqm", label: "平米換算", format: "text" },
      { id: "ventilationPerHour", label: "推奨換気量", format: "text" },
    ],
    explanation: "<h3>部屋の体積計算</h3><p>1畳 = 約1.62m²（中京間）。体積 = 面積 × 天井高です。建築基準法では住宅の換気は0.5回/時以上が義務付けられています。</p>",
    faq: [{ question: "エアコンの畳数と部屋の関係は？", answer: "エアコンの適用畳数は木造と鉄筋で異なります。6畳用なら鉄筋で8〜9畳まで対応することもあります。" }],
    related: ["air-conditioner-cost"], popular: false,
  },
  {
    slug: "data-transfer-time", category: "life", subcategory: "utility",
    title: "データ転送時間計算", description: "USBやSDカードのデータ転送時間を計算",
    metaTitle: "データ転送時間計算ツール｜USB・SDの転送速度から時間を計算",
    metaDescription: "ファイルサイズとUSB/SDカードの転送速度からデータコピーにかかる時間を計算。",
    calculatorFunction: "dataTransferTime",
    inputs: [
      { id: "fileSize", label: "ファイルサイズ", type: "number", unit: "GB", default: 64, min: 0.01, max: 100000, step: 0.01 },
      { id: "speed", label: "転送速度", type: "select", options: [{ value: "5", label: "USB 2.0（5MB/s目安）" }, { value: "100", label: "USB 3.0（100MB/s目安）" }, { value: "300", label: "USB 3.1（300MB/s目安）" }, { value: "30", label: "SDカード（30MB/s）" }, { value: "90", label: "SDカードUHS-I（90MB/s）" }], default: "100" },
    ],
    outputs: [
      { id: "transferTime", label: "転送時間", format: "text", primary: true },
    ],
    explanation: "<h3>データ転送速度の目安</h3><p>USB 2.0は理論上480Mbps（実効5〜30MB/s）、USB 3.0は5Gbps（実効60〜100MB/s）、USB 3.1は10Gbps（実効200〜400MB/s）です。実際の速度はデバイスやファイルサイズにより大きく変動します。</p>",
    faq: [{ question: "USB 3.0と2.0の見分け方は？", answer: "USB 3.0のコネクタ内部は青色、2.0は黒色です。また3.0のロゴにはSSの表記があります。" }],
    related: ["download-time", "internet-speed", "data-size"], popular: false,
  },
];

let created = 0;
for (const c of calcs) {
  const dir = path.join(DATA_DIR, c.category, c.subcategory);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const fp = path.join(dir, `${c.slug}.json`);
  if (fs.existsSync(fp)) { console.log(`SKIP: ${c.slug}`); continue; }
  fs.writeFileSync(fp, JSON.stringify(c, null, 2) + '\n');
  created++;
  console.log(`CREATED: ${c.slug}`);
}
console.log(`\nCreated: ${created}`);
