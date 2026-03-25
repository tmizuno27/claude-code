const fs = require('fs');
const path = require('path');

const BASE = path.resolve(__dirname, '..');
const DATA_DIR = path.join(BASE, 'data', 'calculators');

// All new calculators to create
const newCalculators = [
  // === life/date ===
  {
    slug: "date-add", category: "life", subcategory: "date",
    title: "日付加算計算", description: "指定した日付から○日後・○日前の日付を計算します",
    metaTitle: "日付加算計算ツール｜○日後・○日前の日付を自動計算",
    metaDescription: "指定した日付に日数を足したり引いたりして、○日後・○日前の日付を瞬時に計算。納期計算や予定日の確認に便利な無料ツール。",
    calculatorFunction: "dateAdd",
    inputs: [
      { id: "startDate", label: "基準日", type: "date", default: "2026-01-01" },
      { id: "days", label: "加算日数", type: "number", unit: "日", default: 30, min: -99999, max: 99999, step: 1 },
    ],
    outputs: [
      { id: "resultDate", label: "計算結果の日付", format: "text", primary: true },
      { id: "dayOfWeek", label: "曜日", format: "text" },
    ],
    explanation: "<h3>日付加算の使い方</h3><p>基準日に日数を足す（正の数）か引く（負の数）かで、未来・過去の日付を求められます。納期管理、産休・育休の期間計算、契約満了日の確認など幅広く利用できます。</p>",
    faq: [
      { question: "マイナスを入力するとどうなる？", answer: "基準日から指定日数分だけ過去の日付が計算されます。例えば-30なら30日前の日付です。" },
      { question: "うるう年は考慮される？", answer: "はい。うるう年の2月29日も正しく計算されます。" },
    ],
    related: ["days-between", "countdown", "work-days"], popular: false,
  },

  // === life/shopping ===
  {
    slug: "tax-excluded", category: "life", subcategory: "shopping",
    title: "税抜価格計算", description: "税込価格から税抜価格と消費税額を計算します",
    metaTitle: "税抜価格計算ツール｜税込価格から税抜き価格を自動計算",
    metaDescription: "税込価格を入力するだけで税抜価格と消費税額を自動計算。標準税率10%・軽減税率8%に対応した無料ツール。",
    calculatorFunction: "taxExcluded",
    inputs: [
      { id: "priceIncluded", label: "税込価格", type: "number", unit: "円", default: 1100, min: 0, max: 999999999, step: 1 },
      { id: "taxRate", label: "消費税率", type: "select", options: [{ value: "10", label: "10%（標準税率）" }, { value: "8", label: "8%（軽減税率）" }], default: "10" },
    ],
    outputs: [
      { id: "priceExcluded", label: "税抜価格", format: "currency", primary: true },
      { id: "taxAmount", label: "消費税額", format: "currency" },
    ],
    explanation: "<h3>税抜計算の方法</h3><p>税込価格 ÷ (1 + 税率) = 税抜価格で計算します。10%の場合は税込価格 ÷ 1.1、8%の場合は税込価格 ÷ 1.08です。</p>",
    faq: [
      { question: "1円未満はどう処理される？", answer: "切り捨てで計算しています。実際の店舗では四捨五入の場合もあります。" },
      { question: "軽減税率8%の対象は？", answer: "飲食料品（酒類・外食を除く）と週2回以上発行の新聞（定期購読）が対象です。" },
    ],
    related: ["tax-included", "discount"], popular: false,
  },
  {
    slug: "double-discount", category: "life", subcategory: "shopping",
    title: "二重割引計算", description: "2つの割引が重なった場合の最終価格を計算",
    metaTitle: "二重割引計算ツール｜割引の重ねがけ後の価格を計算",
    metaDescription: "セール割引＋クーポン割引など、2つの割引が重なった場合の最終価格を自動計算。実質何%OFFかもわかる無料ツール。",
    calculatorFunction: "doubleDiscount",
    inputs: [
      { id: "price", label: "元の価格", type: "number", unit: "円", default: 10000, min: 0, max: 999999999, step: 1 },
      { id: "discount1", label: "1つ目の割引率", type: "number", unit: "%", default: 30, min: 0, max: 100, step: 1 },
      { id: "discount2", label: "2つ目の割引率", type: "number", unit: "%", default: 20, min: 0, max: 100, step: 1 },
    ],
    outputs: [
      { id: "finalPrice", label: "最終価格", format: "currency", primary: true },
      { id: "totalDiscount", label: "合計割引額", format: "currency" },
      { id: "effectiveRate", label: "実質割引率", format: "percent" },
    ],
    explanation: "<h3>二重割引の計算方法</h3><p>2つの割引は掛け算で計算します。30%OFF＋20%OFFは50%OFFではなく、元値×0.7×0.8=元値×0.56で44%OFFになります。</p>",
    faq: [
      { question: "割引の順番で結果は変わる？", answer: "いいえ。掛け算なので順番に関係なく最終価格は同じです。" },
      { question: "30%OFF+20%OFFは50%OFFにならないの？", answer: "なりません。30%OFFの後の価格にさらに20%OFFするので、実質44%OFFです。" },
    ],
    related: ["discount", "tax-included"], popular: false,
  },
  {
    slug: "price-per-gram", category: "life", subcategory: "shopping",
    title: "グラム単価計算", description: "商品の価格と重量からグラム単価を比較します",
    metaTitle: "グラム単価計算ツール｜お得な商品を比較",
    metaDescription: "商品の価格と重量を入力してグラム単価を計算。大容量と小容量のどちらがお得かを簡単に比較できる無料ツール。",
    calculatorFunction: "pricePerGram",
    inputs: [
      { id: "price", label: "価格", type: "number", unit: "円", default: 500, min: 0, max: 999999999, step: 1 },
      { id: "weight", label: "重量", type: "number", unit: "g", default: 200, min: 0.1, max: 999999, step: 0.1 },
    ],
    outputs: [
      { id: "pricePerGram", label: "1gあたり単価", format: "currency", primary: true },
      { id: "pricePer100g", label: "100gあたり単価", format: "currency" },
      { id: "pricePerKg", label: "1kgあたり単価", format: "currency" },
    ],
    explanation: "<h3>グラム単価の計算</h3><p>価格÷重量(g)でグラム単価を求めます。スーパーでの食品比較や、化粧品・サプリメントのコスパ比較に便利です。</p>",
    faq: [
      { question: "大容量は必ずお得？", answer: "多くの場合グラム単価は安くなりますが、使い切れず無駄になることもあるため、消費量とのバランスが大事です。" },
    ],
    related: ["per-unit-price", "discount"], popular: false,
  },
  {
    slug: "coupon-value", category: "life", subcategory: "shopping",
    title: "クーポン割引計算", description: "クーポン利用時のお支払い金額を計算",
    metaTitle: "クーポン割引計算ツール｜クーポン使用後の支払額を計算",
    metaDescription: "割引クーポン適用後の支払い金額を自動計算。割引率クーポンと定額クーポンの両方に対応。",
    calculatorFunction: "couponValue",
    inputs: [
      { id: "price", label: "商品価格", type: "number", unit: "円", default: 5000, min: 0, max: 999999999, step: 1 },
      { id: "couponType", label: "クーポン種類", type: "select", options: [{ value: "percent", label: "割引率（%OFF）" }, { value: "fixed", label: "定額値引き（円OFF）" }], default: "percent" },
      { id: "couponValue", label: "クーポン値", type: "number", default: 10, min: 0, max: 999999, step: 1 },
    ],
    outputs: [
      { id: "finalPrice", label: "支払い金額", format: "currency", primary: true },
      { id: "savings", label: "割引額", format: "currency" },
    ],
    explanation: "<h3>クーポン計算</h3><p>割引率クーポンは商品価格×割引率で割引額を計算。定額クーポンはそのまま価格から差し引きます。</p>",
    faq: [
      { question: "最低購入金額がある場合は？", answer: "クーポンの利用条件は各店舗で異なります。このツールでは単純な割引計算を行います。" },
    ],
    related: ["discount", "double-discount"], popular: false,
  },
  {
    slug: "cost-per-use", category: "life", subcategory: "shopping",
    title: "使用回数あたりコスト計算", description: "商品の価格と使用回数から1回あたりのコストを計算",
    metaTitle: "1回あたりコスト計算ツール｜商品のコスパを数値化",
    metaDescription: "商品価格と予想使用回数から1回あたりのコストを計算。高い商品でも長く使えばコスパが良いか判断できる無料ツール。",
    calculatorFunction: "costPerUse",
    inputs: [
      { id: "price", label: "商品価格", type: "number", unit: "円", default: 30000, min: 0, max: 999999999, step: 1 },
      { id: "uses", label: "予想使用回数", type: "number", unit: "回", default: 100, min: 1, max: 999999, step: 1 },
    ],
    outputs: [
      { id: "costPerUse", label: "1回あたりコスト", format: "currency", primary: true },
    ],
    explanation: "<h3>コストパフォーマンスの計算</h3><p>商品価格÷使用回数で1回あたりのコストを算出します。衣類・家電・スポーツ用品など、長く使うものの購入判断に役立ちます。</p>",
    faq: [
      { question: "どんな商品に使える？", answer: "コート、靴、家電、ジム会員権など、何度も使う商品・サービスのコスパ比較に最適です。" },
    ],
    related: ["per-unit-price", "price-per-gram"], popular: false,
  },
  {
    slug: "installment-payment", category: "life", subcategory: "shopping",
    title: "分割払い計算", description: "分割払い時の月々の支払額と手数料を計算",
    metaTitle: "分割払い計算ツール｜月々の支払額と手数料を自動計算",
    metaDescription: "クレジットカードの分割払いの月々の支払額と手数料総額を自動計算。3回〜36回払いに対応。",
    calculatorFunction: "installmentPayment",
    inputs: [
      { id: "totalAmount", label: "購入金額", type: "number", unit: "円", default: 100000, min: 0, max: 999999999, step: 1 },
      { id: "installments", label: "分割回数", type: "select", options: [{ value: "3", label: "3回" }, { value: "6", label: "6回" }, { value: "10", label: "10回" }, { value: "12", label: "12回" }, { value: "24", label: "24回" }, { value: "36", label: "36回" }], default: "12" },
      { id: "annualRate", label: "年利", type: "number", unit: "%", default: 15, min: 0, max: 30, step: 0.1 },
    ],
    outputs: [
      { id: "monthlyPayment", label: "月々の支払額", format: "currency", primary: true },
      { id: "totalFee", label: "手数料総額", format: "currency" },
      { id: "totalPayment", label: "支払い総額", format: "currency" },
    ],
    explanation: "<h3>分割払いの手数料</h3><p>クレジットカードの分割払いは年利12〜15%が一般的です。回数が多いほど月々の負担は減りますが、手数料総額は増えます。2回払いは手数料無料のカードが多いです。</p>",
    faq: [
      { question: "2回払いは手数料がかかる？", answer: "ほとんどのクレジットカードで2回払いは手数料無料です。3回以上から手数料が発生します。" },
      { question: "リボ払いとの違いは？", answer: "分割払いは回数を指定し完済時期が明確です。リボ払いは月々の支払額を固定するため完済時期が不明確で手数料が膨らみやすいです。" },
    ],
    related: ["credit-card-interest", "discount"], popular: false,
  },

  // === life/utility (expand) ===
  {
    slug: "paper-size", category: "life", subcategory: "utility",
    title: "用紙サイズ計算", description: "A判・B判の用紙サイズ（mm）を表示",
    metaTitle: "用紙サイズ一覧・計算ツール｜A判B判のサイズを確認",
    metaDescription: "A0〜A10、B0〜B10の用紙サイズをmm単位で一覧表示。面積や用途も確認できる便利ツール。",
    calculatorFunction: "paperSize",
    inputs: [
      { id: "series", label: "規格", type: "select", options: [{ value: "A", label: "A判（ISO 216）" }, { value: "B", label: "B判（JIS）" }], default: "A" },
      { id: "size", label: "サイズ番号", type: "number", default: 4, min: 0, max: 10, step: 1 },
    ],
    outputs: [
      { id: "width", label: "幅", format: "text", primary: true },
      { id: "height", label: "高さ", format: "text" },
      { id: "area", label: "面積", format: "text" },
    ],
    explanation: "<h3>用紙サイズの規格</h3><p>A判はISO 216国際規格で、A0（841×1189mm）を基準に半分に切るとA1、さらに半分がA2…と続きます。B判は日本独自のJIS規格で、A判より一回り大きいサイズです。</p>",
    faq: [
      { question: "A4のサイズは？", answer: "210mm × 297mmです。" },
      { question: "B5のサイズは？", answer: "182mm × 257mmです。" },
    ],
    related: [], popular: false,
  },
  {
    slug: "shoe-size-convert", category: "life", subcategory: "utility",
    title: "靴サイズ換算", description: "日本・US・UK・EUの靴サイズを相互変換",
    metaTitle: "靴サイズ換算ツール｜日本・US・UK・EUサイズ変換",
    metaDescription: "日本のcmサイズからUS・UK・EUの靴サイズへ簡単変換。メンズ・レディース対応の無料ツール。",
    calculatorFunction: "shoeSizeConvert",
    inputs: [
      { id: "jpSize", label: "日本サイズ", type: "number", unit: "cm", default: 26, min: 15, max: 35, step: 0.5 },
      { id: "gender", label: "性別", type: "select", options: [{ value: "men", label: "メンズ" }, { value: "women", label: "レディース" }], default: "men" },
    ],
    outputs: [
      { id: "us", label: "USサイズ", format: "text", primary: true },
      { id: "uk", label: "UKサイズ", format: "text" },
      { id: "eu", label: "EUサイズ", format: "text" },
    ],
    explanation: "<h3>靴サイズの国際比較</h3><p>日本はcm表記ですが、海外ではUS・UK・EU各国で異なる番号体系を使います。メーカーによって多少の差があるため、目安としてご利用ください。</p>",
    faq: [
      { question: "26cmはUSサイズでいくつ？", answer: "メンズでUS8、レディースでUS9.5が目安です。" },
    ],
    related: ["clothing-size"], popular: false,
  },
  {
    slug: "ring-size", category: "life", subcategory: "utility",
    title: "指輪サイズ計算", description: "指の周囲長から指輪サイズ（号数）を計算",
    metaTitle: "指輪サイズ計算ツール｜指の太さから号数を自動判定",
    metaDescription: "指の周囲長（mm）を入力するだけで指輪の号数を自動計算。日本・US・EUサイズ対応。",
    calculatorFunction: "ringSize",
    inputs: [
      { id: "circumference", label: "指の周囲長", type: "number", unit: "mm", default: 54, min: 38, max: 76, step: 0.5 },
    ],
    outputs: [
      { id: "jpSize", label: "日本サイズ（号）", format: "text", primary: true },
      { id: "usSize", label: "USサイズ", format: "text" },
      { id: "euSize", label: "EUサイズ", format: "text" },
    ],
    explanation: "<h3>指輪サイズの測り方</h3><p>糸や紙テープを指の一番太い部分に巻いて周囲長を測ります。日本の号数は内径と周囲長で決まり、1号=内径13mm(周囲40.8mm)を基準に0.33mmずつ大きくなります。</p>",
    faq: [
      { question: "指輪のサイズはいつ測るのがベスト？", answer: "体温が安定している午後がおすすめです。朝はむくみやすく、入浴後は指が細くなりやすいです。" },
    ],
    related: ["shoe-size-convert"], popular: false,
  },
  {
    slug: "battery-life", category: "life", subcategory: "utility",
    title: "バッテリー持続時間計算", description: "バッテリー容量と消費電力から持続時間を計算",
    metaTitle: "バッテリー持続時間計算ツール｜mAhから稼働時間を計算",
    metaDescription: "バッテリー容量(mAh)と消費電力から持続時間を計算。スマホ・ノートPC・モバイルバッテリーの目安に。",
    calculatorFunction: "batteryLife",
    inputs: [
      { id: "capacity", label: "バッテリー容量", type: "number", unit: "mAh", default: 5000, min: 1, max: 999999, step: 1 },
      { id: "consumption", label: "消費電流", type: "number", unit: "mA", default: 500, min: 1, max: 99999, step: 1 },
    ],
    outputs: [
      { id: "hours", label: "持続時間", format: "text", primary: true },
    ],
    explanation: "<h3>バッテリー持続時間の計算</h3><p>バッテリー容量(mAh) ÷ 消費電流(mA) = 持続時間(h)です。実際は充放電効率（約80〜90%）があるため、計算値より短くなります。</p>",
    faq: [
      { question: "mAhとWhの違いは？", answer: "mAhは電流容量、Whはエネルギー容量です。Wh = mAh × 電圧(V) ÷ 1000で変換できます。" },
    ],
    related: ["electricity-cost"], popular: false,
  },

  // === health/body (expand) ===
  {
    slug: "daily-water-intake", category: "health", subcategory: "body",
    title: "1日の水分摂取量計算", description: "体重から推奨される1日の水分摂取量を計算",
    metaTitle: "1日の水分摂取量計算ツール｜体重から適切な水分量を計算",
    metaDescription: "体重を入力するだけで1日に必要な水分摂取量を計算。運動量別の目安も表示する無料ツール。",
    calculatorFunction: "dailyWaterIntake",
    inputs: [
      { id: "weight", label: "体重", type: "number", unit: "kg", default: 60, min: 20, max: 200, step: 0.1 },
      { id: "activity", label: "運動レベル", type: "select", options: [{ value: "low", label: "ほとんど運動しない" }, { value: "moderate", label: "週2〜3回運動" }, { value: "high", label: "毎日運動" }], default: "low" },
    ],
    outputs: [
      { id: "dailyMl", label: "1日の推奨水分量", format: "text", primary: true },
      { id: "glasses", label: "コップ数（200ml換算）", format: "text" },
    ],
    explanation: "<h3>水分摂取量の目安</h3><p>一般的に体重1kgあたり30〜40mlの水分が必要とされています。運動をする人や暑い環境ではさらに多くの水分が必要です。食事からも約1Lの水分を摂取しているため、飲み物からの摂取量は計算値より少なくて構いません。</p>",
    faq: [
      { question: "お茶やコーヒーもカウントしていい？", answer: "はい。カフェイン入り飲料にも水分はあります。ただし大量のカフェインは利尿作用があるため、水やお茶をメインにするのが理想的です。" },
    ],
    related: ["water-intake", "basal-metabolism"], popular: false,
  },
  {
    slug: "walking-calorie", category: "health", subcategory: "body",
    title: "ウォーキングカロリー計算", description: "歩行時間・速度から消費カロリーを計算",
    metaTitle: "ウォーキングカロリー計算ツール｜歩行の消費カロリー計算",
    metaDescription: "体重と歩行時間からウォーキングの消費カロリーを計算。速度別のMETs値で正確に算出。",
    calculatorFunction: "walkingCalorie",
    inputs: [
      { id: "weight", label: "体重", type: "number", unit: "kg", default: 60, min: 20, max: 200, step: 0.1 },
      { id: "minutes", label: "歩行時間", type: "number", unit: "分", default: 30, min: 1, max: 600, step: 1 },
      { id: "speed", label: "速度", type: "select", options: [{ value: "slow", label: "ゆっくり（3.2km/h）" }, { value: "normal", label: "普通（4.8km/h）" }, { value: "fast", label: "速歩き（6.4km/h）" }], default: "normal" },
    ],
    outputs: [
      { id: "calories", label: "消費カロリー", format: "text", primary: true },
      { id: "distance", label: "歩行距離", format: "text" },
      { id: "steps", label: "推定歩数", format: "text" },
    ],
    explanation: "<h3>ウォーキングの消費カロリー</h3><p>消費カロリー = METs × 体重(kg) × 時間(h) × 1.05で計算します。ゆっくり歩行で2.8METs、通常歩行で3.5METs、速歩きで5.0METsです。</p>",
    faq: [
      { question: "1日何歩歩けばいい？", answer: "厚生労働省は成人で1日8,000〜10,000歩を推奨しています。" },
    ],
    related: ["calorie-burn", "running-pace", "steps-to-distance"], popular: false,
  },
  {
    slug: "muscle-mass", category: "health", subcategory: "body",
    title: "筋肉量推定計算", description: "体重と体脂肪率から除脂肪体重・筋肉量を推定",
    metaTitle: "筋肉量推定計算ツール｜体重と体脂肪率から筋肉量を計算",
    metaDescription: "体重と体脂肪率を入力して除脂肪体重(LBM)と推定筋肉量を計算。筋トレの目標設定に。",
    calculatorFunction: "muscleMass",
    inputs: [
      { id: "weight", label: "体重", type: "number", unit: "kg", default: 65, min: 20, max: 200, step: 0.1 },
      { id: "bodyFat", label: "体脂肪率", type: "number", unit: "%", default: 20, min: 3, max: 60, step: 0.1 },
    ],
    outputs: [
      { id: "leanMass", label: "除脂肪体重", format: "text", primary: true },
      { id: "fatMass", label: "体脂肪量", format: "text" },
      { id: "estimatedMuscle", label: "推定筋肉量", format: "text" },
    ],
    explanation: "<h3>除脂肪体重と筋肉量</h3><p>除脂肪体重(LBM) = 体重 × (1 - 体脂肪率)です。LBMには筋肉のほか骨・内臓・水分が含まれます。筋肉量はLBMの約50%が目安です。</p>",
    faq: [
      { question: "筋肉量の理想値は？", answer: "男性は体重の40%前後、女性は35%前後が標準的です。" },
    ],
    related: ["body-fat", "ideal-weight", "bmi"], popular: false,
  },
  {
    slug: "protein-intake", category: "health", subcategory: "body",
    title: "タンパク質必要量計算", description: "体重と目的に応じた1日のタンパク質推奨摂取量を計算",
    metaTitle: "タンパク質必要量計算ツール｜1日のプロテイン摂取量を計算",
    metaDescription: "体重と運動目的から1日に必要なタンパク質量を計算。筋トレ・ダイエット・健康維持それぞれの推奨量を表示。",
    calculatorFunction: "proteinIntake",
    inputs: [
      { id: "weight", label: "体重", type: "number", unit: "kg", default: 65, min: 20, max: 200, step: 0.1 },
      { id: "goal", label: "目的", type: "select", options: [{ value: "maintain", label: "健康維持" }, { value: "muscle", label: "筋肉増量" }, { value: "diet", label: "ダイエット" }], default: "maintain" },
    ],
    outputs: [
      { id: "dailyProtein", label: "1日の推奨タンパク質量", format: "text", primary: true },
      { id: "perMeal", label: "1食あたり（3食の場合）", format: "text" },
    ],
    explanation: "<h3>タンパク質の必要量</h3><p>健康維持には体重1kgあたり0.8〜1.0g、筋肉増量には1.6〜2.2g、ダイエット中は1.2〜1.6gが推奨されています。</p>",
    faq: [
      { question: "プロテインはいつ飲むべき？", answer: "筋トレ後30分以内と、朝食時が効果的とされています。" },
    ],
    related: ["basal-metabolism", "daily-calorie"], popular: false,
  },
  {
    slug: "visual-acuity", category: "health", subcategory: "body",
    title: "視力換算", description: "小数視力・ジオプトリー・logMARを相互変換",
    metaTitle: "視力換算ツール｜小数視力・度数（ジオプトリー）変換",
    metaDescription: "日本の小数視力とコンタクトレンズのジオプトリー（度数）を相互変換。logMARにも対応。",
    calculatorFunction: "visualAcuity",
    inputs: [
      { id: "acuity", label: "小数視力", type: "number", default: 0.5, min: 0.01, max: 2.0, step: 0.01 },
    ],
    outputs: [
      { id: "diopter", label: "ジオプトリー（目安）", format: "text", primary: true },
      { id: "logMAR", label: "logMAR", format: "text" },
      { id: "category", label: "視力区分", format: "text" },
    ],
    explanation: "<h3>視力の換算</h3><p>小数視力とジオプトリー(D)は直接的な換算式はありませんが、目安として-1/小数視力 + 1に近い値になります。実際のメガネ・コンタクトの度数は眼科で処方を受けてください。</p>",
    faq: [
      { question: "視力0.1はどのくらい？", answer: "裸眼で30cm先の文字がぼやけるレベルです。メガネやコンタクトでの矯正が必要です。" },
    ],
    related: [], popular: false,
  },

  // === health/calorie (expand) ===
  {
    slug: "meal-calorie", category: "health", subcategory: "calorie",
    title: "食事カロリー計算", description: "主な食品のカロリーを合計して1食のカロリーを計算",
    metaTitle: "食事カロリー計算ツール｜1食の総カロリーを自動計算",
    metaDescription: "ご飯・パン・肉・魚など主要食品のカロリーを選んで合計を計算。ダイエットや食事管理に便利な無料ツール。",
    calculatorFunction: "mealCalorie",
    inputs: [
      { id: "rice", label: "ご飯（g）", type: "number", unit: "g", default: 150, min: 0, max: 1000, step: 10 },
      { id: "meat", label: "肉類（g）", type: "number", unit: "g", default: 100, min: 0, max: 1000, step: 10 },
      { id: "fish", label: "魚類（g）", type: "number", unit: "g", default: 0, min: 0, max: 1000, step: 10 },
      { id: "vegetables", label: "野菜（g）", type: "number", unit: "g", default: 100, min: 0, max: 1000, step: 10 },
    ],
    outputs: [
      { id: "totalCalorie", label: "合計カロリー", format: "text", primary: true },
      { id: "protein", label: "推定タンパク質", format: "text" },
    ],
    explanation: "<h3>食品別カロリーの目安</h3><p>ご飯100gで約168kcal、鶏胸肉100gで約108kcal、鮭100gで約133kcal、野菜は種類により10〜30kcal/100gです。調理法（揚げ物・焼き物等）で大きく変わります。</p>",
    faq: [
      { question: "茶碗1杯のご飯は何g？", answer: "普通盛りで約150g（約252kcal）です。" },
    ],
    related: ["daily-calorie", "calories-bmr", "calorie-burn"], popular: false,
  },
  {
    slug: "sugar-intake", category: "health", subcategory: "calorie",
    title: "砂糖摂取量チェック", description: "飲料・食品の砂糖含有量と1日の推奨量を比較",
    metaTitle: "砂糖摂取量チェックツール｜1日の砂糖摂取量を確認",
    metaDescription: "飲料や食品に含まれる砂糖の量と、WHOが推奨する1日の上限を比較。健康管理に役立つ無料ツール。",
    calculatorFunction: "sugarIntake",
    inputs: [
      { id: "sugarG", label: "摂取した砂糖量", type: "number", unit: "g", default: 25, min: 0, max: 500, step: 1 },
    ],
    outputs: [
      { id: "calories", label: "砂糖由来のカロリー", format: "text", primary: true },
      { id: "teaspoons", label: "小さじ換算", format: "text" },
      { id: "percentOfLimit", label: "WHO推奨上限に対する割合", format: "text" },
    ],
    explanation: "<h3>砂糖の摂取目安</h3><p>WHOは遊離糖類を1日のエネルギー摂取量の5%未満（成人で約25g）に抑えることを推奨しています。砂糖1gは約4kcalです。</p>",
    faq: [
      { question: "コーラ1本の砂糖は？", answer: "500mlペットボトルで約55g（小さじ約11杯）含まれています。" },
    ],
    related: ["daily-calorie", "meal-calorie"], popular: false,
  },

  // === health/medical (expand) ===
  {
    slug: "blood-pressure-check", category: "health", subcategory: "medical",
    title: "血圧チェック", description: "血圧の数値から分類と判定を表示",
    metaTitle: "血圧チェックツール｜血圧の数値から正常・高血圧を判定",
    metaDescription: "最高血圧と最低血圧を入力するだけで血圧の分類（正常・正常高値・高血圧）を判定。日本高血圧学会の基準に準拠。",
    calculatorFunction: "bloodPressureCheck",
    inputs: [
      { id: "systolic", label: "最高血圧（収縮期）", type: "number", unit: "mmHg", default: 120, min: 60, max: 300, step: 1 },
      { id: "diastolic", label: "最低血圧（拡張期）", type: "number", unit: "mmHg", default: 80, min: 30, max: 200, step: 1 },
    ],
    outputs: [
      { id: "category", label: "血圧分類", format: "text", primary: true },
      { id: "advice", label: "アドバイス", format: "text" },
    ],
    explanation: "<h3>血圧の分類基準</h3><p>日本高血圧学会(JSH2019)の基準：正常血圧は120/80未満、正常高値血圧は120-129/80未満、高値血圧は130-139/80-89、I度高血圧は140-159/90-99、II度高血圧は160-179/100-109、III度高血圧は180以上/110以上です。</p>",
    faq: [
      { question: "いつ測るのがベスト？", answer: "朝起きてトイレ後、食事前の安静時に測るのが推奨されています。毎日同じ条件で測りましょう。" },
    ],
    related: ["hearing-level"], popular: false,
  },
  {
    slug: "medicine-dosage", category: "health", subcategory: "medical",
    title: "子供の薬用量計算", description: "体重から子供の薬用量の目安を計算",
    metaTitle: "子供の薬用量計算ツール｜体重からお薬の量を目安計算",
    metaDescription: "子供の体重から市販薬の服用量目安を計算。あくまで参考値のため、実際の服用は医師・薬剤師にご相談ください。",
    calculatorFunction: "medicineDosage",
    inputs: [
      { id: "adultDose", label: "大人の用量", type: "number", unit: "mg", default: 200, min: 1, max: 10000, step: 1 },
      { id: "childWeight", label: "子供の体重", type: "number", unit: "kg", default: 20, min: 3, max: 60, step: 0.5 },
    ],
    outputs: [
      { id: "childDose", label: "子供の用量（目安）", format: "text", primary: true },
    ],
    explanation: "<h3>小児薬用量の計算</h3><p>Clarkの式：子供の用量 = 大人の用量 × (子供の体重kg ÷ 70) で計算します。これはあくまで目安であり、実際の投薬は必ず医師・薬剤師にご相談ください。</p>",
    faq: [
      { question: "この計算は正確ですか？", answer: "あくまで目安です。薬によって小児用量は異なるため、必ず添付文書を確認し、医師・薬剤師に相談してください。" },
    ],
    related: [], popular: false,
  },

  // === health/pregnancy (expand) ===
  {
    slug: "baby-name-strokes", category: "health", subcategory: "pregnancy",
    title: "画数計算", description: "名前の画数から姓名判断の総画数を計算",
    metaTitle: "画数計算ツール｜名前の画数を自動カウント",
    metaDescription: "名前の漢字の画数を自動計算。姓名判断に使われる天格・人格・地格・外格・総格を表示。",
    calculatorFunction: "babyNameStrokes",
    inputs: [
      { id: "lastName1", label: "姓（1文字目）画数", type: "number", default: 8, min: 1, max: 30, step: 1 },
      { id: "lastName2", label: "姓（2文字目）画数", type: "number", default: 4, min: 0, max: 30, step: 1 },
      { id: "firstName1", label: "名（1文字目）画数", type: "number", default: 7, min: 1, max: 30, step: 1 },
      { id: "firstName2", label: "名（2文字目）画数", type: "number", default: 3, min: 0, max: 30, step: 1 },
    ],
    outputs: [
      { id: "tenKaku", label: "天格（姓の合計）", format: "text" },
      { id: "jinKaku", label: "人格（姓末+名頭）", format: "text", primary: true },
      { id: "chiKaku", label: "地格（名の合計）", format: "text" },
      { id: "gaiKaku", label: "外格", format: "text" },
      { id: "souKaku", label: "総格", format: "text" },
    ],
    explanation: "<h3>姓名判断の五格</h3><p>天格＝姓の画数合計、人格＝姓の末字+名の頭字、地格＝名の画数合計、外格＝天格+地格-人格、総格＝全画数合計です。人格と総格が特に重要とされています。</p>",
    faq: [
      { question: "1文字の姓・名はどうする？", answer: "2文字目の画数を0にしてください。" },
    ],
    related: ["due-date", "pregnancy-week"], popular: false,
  },
  {
    slug: "weight-gain-pregnancy", category: "health", subcategory: "pregnancy",
    title: "妊娠中の体重増加目安", description: "妊娠前BMIから推奨体重増加量を計算",
    metaTitle: "妊娠中の体重増加目安計算ツール｜BMIから推奨増加量を計算",
    metaDescription: "妊娠前の身長・体重から推奨される体重増加量を計算。厚生労働省の基準に基づく無料ツール。",
    calculatorFunction: "weightGainPregnancy",
    inputs: [
      { id: "height", label: "身長", type: "number", unit: "cm", default: 158, min: 130, max: 200, step: 0.1 },
      { id: "preWeight", label: "妊娠前体重", type: "number", unit: "kg", default: 52, min: 30, max: 150, step: 0.1 },
    ],
    outputs: [
      { id: "preBmi", label: "妊娠前BMI", format: "text" },
      { id: "recommendedGain", label: "推奨体重増加量", format: "text", primary: true },
      { id: "targetWeight", label: "出産時の目標体重", format: "text" },
    ],
    explanation: "<h3>妊娠中の体重管理</h3><p>厚生労働省（2021年改定）の基準：BMI18.5未満は12〜15kg、BMI18.5〜25未満は10〜13kg、BMI25〜30未満は7〜10kg、BMI30以上は個別対応（上限5kg目安）の増加が推奨されています。</p>",
    faq: [
      { question: "体重が増えすぎるとどうなる？", answer: "妊娠高血圧症候群や妊娠糖尿病のリスクが高まります。逆に増えなさすぎると低出生体重児のリスクがあります。" },
    ],
    related: ["due-date", "pregnancy-week", "bmi"], popular: false,
  },

  // === education/school (expand) ===
  {
    slug: "reading-speed", category: "education", subcategory: "school",
    title: "読書速度計算", description: "読書速度から本を読み終わるまでの時間を計算",
    metaTitle: "読書速度計算ツール｜本を読み終わるまでの時間を計算",
    metaDescription: "1分あたりの読書速度と本の文字数から、読了にかかる時間を計算。読書計画に便利な無料ツール。",
    calculatorFunction: "readingSpeed",
    inputs: [
      { id: "totalChars", label: "文字数", type: "number", unit: "文字", default: 100000, min: 100, max: 10000000, step: 100 },
      { id: "wpm", label: "読書速度", type: "number", unit: "文字/分", default: 500, min: 50, max: 5000, step: 10 },
    ],
    outputs: [
      { id: "totalMinutes", label: "所要時間", format: "text", primary: true },
      { id: "pages", label: "推定ページ数（400字/頁）", format: "text" },
    ],
    explanation: "<h3>日本人の平均読書速度</h3><p>日本人の平均読書速度は400〜600文字/分です。速読を習得すると1000文字/分以上も可能です。一般的な文庫本は1冊約10〜12万文字です。</p>",
    faq: [
      { question: "日本人の平均読書速度は？", answer: "約400〜600文字/分です。ビジネス書は500文字/分、小説は600文字/分程度が目安です。" },
    ],
    related: ["exam-score"], popular: false,
  },
  {
    slug: "study-plan", category: "education", subcategory: "study",
    title: "勉強時間計算", description: "目標試験日までの残り日数と必要勉強時間を計算",
    metaTitle: "勉強時間計算ツール｜試験日までの勉強計画を自動計算",
    metaDescription: "試験日と目標勉強時間から1日あたりの必要勉強時間を計算。受験・資格試験の計画に。",
    calculatorFunction: "studyPlan",
    inputs: [
      { id: "totalHours", label: "目標総勉強時間", type: "number", unit: "時間", default: 300, min: 1, max: 10000, step: 1 },
      { id: "daysLeft", label: "残り日数", type: "number", unit: "日", default: 90, min: 1, max: 3650, step: 1 },
      { id: "studyDays", label: "週あたり勉強日数", type: "number", unit: "日/週", default: 6, min: 1, max: 7, step: 1 },
    ],
    outputs: [
      { id: "dailyHours", label: "1日あたり必要勉強時間", format: "text", primary: true },
      { id: "weeklyHours", label: "週あたり勉強時間", format: "text" },
      { id: "totalStudyDays", label: "実質勉強日数", format: "text" },
    ],
    explanation: "<h3>勉強時間の目安</h3><p>主な資格試験の合格目安時間：TOEIC 800点は約600時間、簿記2級は約300時間、宅建は約300時間、行政書士は約600〜800時間です。</p>",
    faq: [
      { question: "効果的な勉強のコツは？", answer: "ポモドーロテクニック（25分集中＋5分休憩）が効果的です。長時間ダラダラより短時間集中を繰り返しましょう。" },
    ],
    related: ["exam-score"], popular: false,
  },
  {
    slug: "typing-speed", category: "education", subcategory: "study",
    title: "タイピング速度計算", description: "入力文字数と所要時間からタイピング速度を計算",
    metaTitle: "タイピング速度計算ツール｜WPM・打鍵数を計算",
    metaDescription: "入力文字数と時間からタイピング速度（WPM・打鍵数/分）を計算。タイピングスキルの評価に。",
    calculatorFunction: "typingSpeed",
    inputs: [
      { id: "characters", label: "入力文字数", type: "number", unit: "文字", default: 300, min: 1, max: 99999, step: 1 },
      { id: "seconds", label: "所要時間", type: "number", unit: "秒", default: 60, min: 1, max: 3600, step: 1 },
    ],
    outputs: [
      { id: "cpm", label: "文字/分", format: "text", primary: true },
      { id: "wpm", label: "WPM（英語換算）", format: "text" },
      { id: "rank", label: "レベル評価", format: "text" },
    ],
    explanation: "<h3>タイピング速度の目安</h3><p>日本語入力の場合、初心者は60〜80文字/分、中級者は150〜200文字/分、上級者は300文字/分以上です。英語のWPMは文字数÷5で求めます。</p>",
    faq: [
      { question: "仕事で求められるタイピング速度は？", answer: "事務職なら150文字/分以上、ライターなら200文字/分以上が目安です。" },
    ],
    related: [], popular: false,
  },

  // === math/basic (expand) ===
  {
    slug: "ratio-calculator", category: "math", subcategory: "basic",
    title: "比率計算", description: "比率（A:B）から実際の数値を計算",
    metaTitle: "比率計算ツール｜比率から数値を自動計算",
    metaDescription: "比率（A:B）と合計値から各部分の実際の数値を計算。配分・按分・割合計算に便利な無料ツール。",
    calculatorFunction: "ratioCalculator",
    inputs: [
      { id: "ratioA", label: "比率A", type: "number", default: 3, min: 0.01, max: 99999, step: 0.01 },
      { id: "ratioB", label: "比率B", type: "number", default: 7, min: 0.01, max: 99999, step: 0.01 },
      { id: "total", label: "合計値", type: "number", default: 1000, min: 0, max: 999999999, step: 1 },
    ],
    outputs: [
      { id: "valueA", label: "Aの値", format: "number", primary: true },
      { id: "valueB", label: "Bの値", format: "number" },
      { id: "percentA", label: "Aの割合", format: "percent" },
    ],
    explanation: "<h3>比率計算の方法</h3><p>A:B = 3:7で合計1000の場合、Aの値 = 1000 × 3/(3+7) = 300、Bの値 = 1000 × 7/(3+7) = 700です。</p>",
    faq: [
      { question: "3:7の比率は何対何？", answer: "合計を10としたとき、3と7の配分です。Aが30%、Bが70%になります。" },
    ],
    related: ["percentage", "fraction"], popular: false,
  },
  {
    slug: "random-number", category: "math", subcategory: "basic",
    title: "乱数生成", description: "指定した範囲内でランダムな数値を生成",
    metaTitle: "乱数生成ツール｜ランダムな数字を生成",
    metaDescription: "指定した範囲内でランダムな整数を生成。抽選・くじ引き・ゲームに使える無料ツール。",
    calculatorFunction: "randomNumber",
    inputs: [
      { id: "min", label: "最小値", type: "number", default: 1, min: -999999, max: 999999, step: 1 },
      { id: "max", label: "最大値", type: "number", default: 100, min: -999999, max: 999999, step: 1 },
    ],
    outputs: [
      { id: "result", label: "生成された数値", format: "number", primary: true },
    ],
    explanation: "<h3>乱数の生成</h3><p>指定された最小値〜最大値の範囲でランダムな整数を1つ生成します。抽選やくじ引き、ゲームの出目決定などにご利用ください。</p>",
    faq: [
      { question: "本当にランダム？", answer: "JavaScriptのMath.random()を使用した疑似乱数です。カジノや暗号用途には適しませんが、一般的な用途には十分です。" },
    ],
    related: ["average"], popular: false,
  },
  {
    slug: "power-calculator", category: "math", subcategory: "basic",
    title: "累乗計算", description: "底と指数を入力して累乗（べき乗）を計算",
    metaTitle: "累乗計算ツール｜べき乗を自動計算",
    metaDescription: "底と指数を入力して累乗（aのn乗）を計算。小数・負の指数にも対応した無料ツール。",
    calculatorFunction: "powerCalculator",
    inputs: [
      { id: "base", label: "底(a)", type: "number", default: 2, min: -9999, max: 9999, step: 0.01 },
      { id: "exponent", label: "指数(n)", type: "number", default: 10, min: -100, max: 100, step: 0.1 },
    ],
    outputs: [
      { id: "result", label: "結果（aのn乗）", format: "text", primary: true },
    ],
    explanation: "<h3>累乗の計算</h3><p>a^n = a × a × ... × a（n回掛ける）です。指数が0のとき結果は1、負の指数は1/a^|n|になります。</p>",
    faq: [
      { question: "2の10乗は？", answer: "1024です。コンピュータの1KB = 1024バイトはここから来ています。" },
    ],
    related: ["logarithm", "square-root"], popular: false,
  },
  {
    slug: "logarithm", category: "math", subcategory: "basic",
    title: "対数計算", description: "対数（log）を計算します",
    metaTitle: "対数計算ツール｜log・ln・log2を自動計算",
    metaDescription: "底と真数を入力して対数（log）を計算。常用対数(log10)、自然対数(ln)、二進対数(log2)に対応。",
    calculatorFunction: "logarithmCalc",
    inputs: [
      { id: "value", label: "真数", type: "number", default: 100, min: 0.001, max: 999999999, step: 0.001 },
      { id: "base", label: "底", type: "select", options: [{ value: "10", label: "10（常用対数）" }, { value: "e", label: "e（自然対数）" }, { value: "2", label: "2（二進対数）" }], default: "10" },
    ],
    outputs: [
      { id: "result", label: "対数の値", format: "text", primary: true },
    ],
    explanation: "<h3>対数とは</h3><p>log_b(x) = y は、b^y = x を意味します。常用対数(log10)は科学計算、自然対数(ln)は微積分、二進対数(log2)は情報理論で使われます。</p>",
    faq: [
      { question: "log100は？", answer: "常用対数(底10)でlog100 = 2です。10^2 = 100だからです。" },
    ],
    related: ["power-calculator"], popular: false,
  },
  {
    slug: "prime-check", category: "math", subcategory: "basic",
    title: "素数判定", description: "入力した数が素数かどうかを判定",
    metaTitle: "素数判定ツール｜素数かどうかを瞬時に判定",
    metaDescription: "数値を入力するだけで素数かどうかを判定。約数一覧と素因数分解の結果も表示する無料ツール。",
    calculatorFunction: "primeCheck",
    inputs: [
      { id: "number", label: "数値", type: "number", default: 97, min: 2, max: 999999999, step: 1 },
    ],
    outputs: [
      { id: "isPrime", label: "素数判定", format: "text", primary: true },
      { id: "factors", label: "約数一覧", format: "text" },
      { id: "primeFactors", label: "素因数分解", format: "text" },
    ],
    explanation: "<h3>素数とは</h3><p>1と自分自身以外に約数を持たない、2以上の自然数です。最初の素数は2, 3, 5, 7, 11, 13, 17, 19, 23, 29...と続きます。</p>",
    faq: [
      { question: "1は素数？", answer: "1は素数ではありません。素数の定義は「2以上の自然数で、1と自分自身以外に約数を持たない数」です。" },
    ],
    related: ["gcd-lcm"], popular: false,
  },

  // === math/geometry (expand) ===
  {
    slug: "parallelogram", category: "math", subcategory: "geometry",
    title: "平行四辺形の面積", description: "底辺と高さから平行四辺形の面積を計算",
    metaTitle: "平行四辺形の面積計算ツール｜底辺と高さから面積を計算",
    metaDescription: "底辺と高さを入力して平行四辺形の面積を計算。対角線からの計算にも対応した無料ツール。",
    calculatorFunction: "parallelogram",
    inputs: [
      { id: "base", label: "底辺", type: "number", default: 10, min: 0.01, max: 99999, step: 0.01 },
      { id: "height", label: "高さ", type: "number", default: 5, min: 0.01, max: 99999, step: 0.01 },
    ],
    outputs: [
      { id: "area", label: "面積", format: "number", primary: true },
    ],
    explanation: "<h3>平行四辺形の面積</h3><p>面積 = 底辺 × 高さです。高さは底辺に対して垂直な距離です。</p>",
    faq: [
      { question: "ひし形も平行四辺形？", answer: "はい。ひし形は4辺が等しい特殊な平行四辺形です。" },
    ],
    related: ["triangle", "rectangle"], popular: false,
  },
  {
    slug: "trapezoid", category: "math", subcategory: "geometry",
    title: "台形の面積", description: "上底・下底・高さから台形の面積を計算",
    metaTitle: "台形の面積計算ツール｜上底・下底・高さから面積を計算",
    metaDescription: "上底と下底と高さを入力して台形の面積を計算。公式(上底+下底)×高さ÷2で自動計算。",
    calculatorFunction: "trapezoid",
    inputs: [
      { id: "topBase", label: "上底", type: "number", default: 5, min: 0.01, max: 99999, step: 0.01 },
      { id: "bottomBase", label: "下底", type: "number", default: 10, min: 0.01, max: 99999, step: 0.01 },
      { id: "height", label: "高さ", type: "number", default: 4, min: 0.01, max: 99999, step: 0.01 },
    ],
    outputs: [
      { id: "area", label: "面積", format: "number", primary: true },
    ],
    explanation: "<h3>台形の面積</h3><p>面積 = (上底 + 下底) × 高さ ÷ 2 で計算します。小学5年生で学ぶ基本的な公式です。</p>",
    faq: [
      { question: "上底と下底の見分け方は？", answer: "平行な2辺のうち、短い方が上底、長い方が下底です。どちらを上底にしても計算結果は同じです。" },
    ],
    related: ["parallelogram", "triangle"], popular: false,
  },

  // === math/statistics (expand) ===
  {
    slug: "standard-deviation", category: "math", subcategory: "statistics",
    title: "標準偏差計算", description: "データの標準偏差を計算します",
    metaTitle: "標準偏差計算ツール｜データの散らばりを計算",
    metaDescription: "数値データを入力して標準偏差・分散・平均を自動計算。統計分析・データ分析に便利な無料ツール。",
    calculatorFunction: "standardDeviation",
    inputs: [
      { id: "data", label: "データ（カンマ区切り）", type: "text", default: "10,20,30,40,50" },
    ],
    outputs: [
      { id: "mean", label: "平均", format: "text" },
      { id: "stdDev", label: "標準偏差（母集団）", format: "text", primary: true },
      { id: "sampleStdDev", label: "標準偏差（標本）", format: "text" },
      { id: "variance", label: "分散", format: "text" },
    ],
    explanation: "<h3>標準偏差とは</h3><p>データのばらつき度合いを表す指標です。値が大きいほどデータが平均から離れていることを意味します。母集団の標準偏差はNで割り、標本の標準偏差はN-1で割ります。</p>",
    faq: [
      { question: "母集団と標本の違いは？", answer: "母集団は調査対象全体、標本はその一部です。標本から母集団を推定する場合はN-1で割る不偏推定量を使います。" },
    ],
    related: ["average", "correlation", "hensachi"], popular: false,
  },
  {
    slug: "probability", category: "math", subcategory: "statistics",
    title: "確率計算", description: "組み合わせ・順列の確率を計算",
    metaTitle: "確率計算ツール｜組み合わせ・順列を自動計算",
    metaDescription: "全体のn個からr個を選ぶ組み合わせ(nCr)と順列(nPr)を計算。くじ引き・宝くじの当選確率にも。",
    calculatorFunction: "probability",
    inputs: [
      { id: "n", label: "全体の数(n)", type: "number", default: 10, min: 1, max: 170, step: 1 },
      { id: "r", label: "選ぶ数(r)", type: "number", default: 3, min: 0, max: 170, step: 1 },
    ],
    outputs: [
      { id: "combination", label: "組み合わせ(nCr)", format: "text", primary: true },
      { id: "permutation", label: "順列(nPr)", format: "text" },
      { id: "probability", label: "1つを選ぶ確率", format: "text" },
    ],
    explanation: "<h3>組み合わせと順列</h3><p>組み合わせ nCr = n! / (r! × (n-r)!) は順番を考えない選び方の数。順列 nPr = n! / (n-r)! は順番を考える並べ方の数です。</p>",
    faq: [
      { question: "ロト6の当選確率は？", answer: "43個から6個を選ぶ組み合わせで、43C6 = 6,096,454通り。1等の当選確率は約609万分の1です。" },
    ],
    related: ["random-number"], popular: false,
  },

  // === money/salary (expand) ===
  {
    slug: "salary-raise", category: "money", subcategory: "salary",
    title: "昇給シミュレーション", description: "昇給率から将来の年収を計算",
    metaTitle: "昇給シミュレーションツール｜将来の年収を予測計算",
    metaDescription: "現在の年収と昇給率から5年後・10年後の年収を自動計算。生涯年収も予測できる無料ツール。",
    calculatorFunction: "salaryRaise",
    inputs: [
      { id: "currentSalary", label: "現在の年収", type: "number", unit: "万円", default: 400, min: 100, max: 10000, step: 10 },
      { id: "raiseRate", label: "年間昇給率", type: "number", unit: "%", default: 2, min: 0, max: 20, step: 0.1 },
      { id: "years", label: "計算年数", type: "number", unit: "年", default: 10, min: 1, max: 40, step: 1 },
    ],
    outputs: [
      { id: "futureSalary", label: "将来の年収", format: "text", primary: true },
      { id: "totalEarnings", label: "累計年収", format: "text" },
      { id: "increasePercent", label: "年収増加率", format: "text" },
    ],
    explanation: "<h3>昇給の計算</h3><p>複利で計算します。年収400万円で年2%昇給の場合、10年後は400 × 1.02^10 = 約487万円です。日本企業の平均昇給率は約2%前後です。</p>",
    faq: [
      { question: "日本の平均昇給率は？", answer: "2023年は大企業で約3.6%、中小企業で約2.0%です。ベースアップと定期昇給を含みます。" },
    ],
    related: ["annual-income", "hourly-wage"], popular: false,
  },
  {
    slug: "overtime-pay", category: "money", subcategory: "salary",
    title: "残業代計算", description: "時給と残業時間から残業代を計算",
    metaTitle: "残業代計算ツール｜残業時間から残業手当を自動計算",
    metaDescription: "月給・所定労働時間・残業時間から残業代を自動計算。25%割増・深夜割増にも対応した無料ツール。",
    calculatorFunction: "overtimePay",
    inputs: [
      { id: "monthlySalary", label: "月給", type: "number", unit: "万円", default: 30, min: 10, max: 500, step: 1 },
      { id: "workHours", label: "月の所定労働時間", type: "number", unit: "時間", default: 160, min: 100, max: 200, step: 1 },
      { id: "overtimeHours", label: "残業時間", type: "number", unit: "時間", default: 20, min: 0, max: 100, step: 0.5 },
      { id: "nightHours", label: "うち深夜（22-5時）", type: "number", unit: "時間", default: 0, min: 0, max: 100, step: 0.5 },
    ],
    outputs: [
      { id: "hourlyRate", label: "基礎時給", format: "currency" },
      { id: "overtimePay", label: "残業代合計", format: "currency", primary: true },
      { id: "totalSalary", label: "月収合計", format: "currency" },
    ],
    explanation: "<h3>残業代の計算</h3><p>残業代 = 基礎時給 × 1.25 × 残業時間です。深夜(22:00-5:00)はさらに25%加算で1.5倍。月60時間超の残業は1.5倍（中小企業も2023年4月〜）。基礎時給 = 月給 ÷ 月所定労働時間。</p>",
    faq: [
      { question: "みなし残業との違いは？", answer: "みなし残業（固定残業代）は一定時間分の残業代が月給に含まれます。その時間を超えた分は別途支払いが必要です。" },
    ],
    related: ["hourly-wage", "annual-income"], popular: false,
  },
  {
    slug: "retirement-age", category: "money", subcategory: "salary",
    title: "定年退職金計算", description: "勤続年数と月給から退職金の目安を計算",
    metaTitle: "退職金計算ツール｜勤続年数から退職金を予測",
    metaDescription: "勤続年数・月給・退職金制度から退職金の目安を計算。退職所得税も自動計算する無料ツール。",
    calculatorFunction: "retirementAge",
    inputs: [
      { id: "monthlySalary", label: "退職時月給", type: "number", unit: "万円", default: 40, min: 10, max: 500, step: 1 },
      { id: "yearsOfService", label: "勤続年数", type: "number", unit: "年", default: 30, min: 1, max: 50, step: 1 },
      { id: "multiplier", label: "支給月数", type: "number", unit: "ヶ月", default: 40, min: 0, max: 100, step: 1 },
    ],
    outputs: [
      { id: "grossRetirement", label: "退職金（税引前）", format: "text", primary: true },
      { id: "deduction", label: "退職所得控除", format: "text" },
      { id: "tax", label: "退職所得税（概算）", format: "text" },
      { id: "netRetirement", label: "手取り額（概算）", format: "text" },
    ],
    explanation: "<h3>退職金の計算</h3><p>退職金 = 退職時月給 × 支給月数が基本です。退職所得控除は勤続20年以下で40万円×年数、20年超で800万円+70万円×(年数-20)です。退職金は税制上有利で、控除後の1/2に課税されます。</p>",
    faq: [
      { question: "退職金の相場は？", answer: "大企業の大卒35年勤続で約2,000〜2,500万円、中小企業で約1,000〜1,500万円が目安です。" },
    ],
    related: ["annual-income", "salary-raise"], popular: false,
  },

  // === money/tax (expand) ===
  {
    slug: "side-job-tax", category: "money", subcategory: "tax",
    title: "副業の税金計算", description: "副業収入にかかる所得税と住民税を計算",
    metaTitle: "副業の税金計算ツール｜副業収入の手取りを自動計算",
    metaDescription: "副業収入と経費を入力して所得税・住民税・手取り額を計算。確定申告が必要かどうかも判定。",
    calculatorFunction: "sideJobTax",
    inputs: [
      { id: "sideIncome", label: "副業の年間収入", type: "number", unit: "万円", default: 100, min: 0, max: 10000, step: 1 },
      { id: "expenses", label: "経費", type: "number", unit: "万円", default: 20, min: 0, max: 10000, step: 1 },
      { id: "mainIncome", label: "本業の年収", type: "number", unit: "万円", default: 500, min: 0, max: 10000, step: 10 },
    ],
    outputs: [
      { id: "sideProfit", label: "副業所得（収入-経費）", format: "text" },
      { id: "additionalTax", label: "追加所得税（概算）", format: "text", primary: true },
      { id: "additionalResident", label: "追加住民税（概算）", format: "text" },
      { id: "netIncome", label: "手取り（概算）", format: "text" },
      { id: "needFiling", label: "確定申告の要否", format: "text" },
    ],
    explanation: "<h3>副業の税金</h3><p>副業の所得（収入-経費）が20万円を超えると確定申告が必要です。所得税は本業と合算して累進税率が適用されます。住民税は所得に関係なく申告が必要です。</p>",
    faq: [
      { question: "20万円以下なら税金ゼロ？", answer: "所得税は確定申告不要ですが、住民税は別途申告が必要で、約10%課税されます。" },
      { question: "会社にバレない方法は？", answer: "住民税を普通徴収（自分で納付）にすれば、副業分の住民税が会社に通知されません。確定申告書の第二表で選択できます。" },
    ],
    related: ["income-tax", "freelance-tax"], popular: false,
  },
  {
    slug: "medical-expense-deduction", category: "money", subcategory: "tax",
    title: "医療費控除計算", description: "年間医療費から控除額と還付金を計算",
    metaTitle: "医療費控除計算ツール｜還付金額を自動計算",
    metaDescription: "年間の医療費と年収から医療費控除の額と確定申告での還付金を計算。セルフメディケーション税制にも対応。",
    calculatorFunction: "medicalExpenseDeduction",
    inputs: [
      { id: "medicalExpenses", label: "年間医療費", type: "number", unit: "万円", default: 20, min: 0, max: 1000, step: 1 },
      { id: "insurance", label: "保険金等で補填された額", type: "number", unit: "万円", default: 0, min: 0, max: 1000, step: 1 },
      { id: "annualIncome", label: "年収", type: "number", unit: "万円", default: 500, min: 100, max: 10000, step: 10 },
    ],
    outputs: [
      { id: "deductionAmount", label: "医療費控除額", format: "text", primary: true },
      { id: "taxRefund", label: "還付金の目安", format: "text" },
      { id: "eligible", label: "控除対象", format: "text" },
    ],
    explanation: "<h3>医療費控除の計算</h3><p>医療費控除額 = 支払った医療費 - 保険金等 - 10万円（所得200万円未満は所得の5%）です。上限は200万円。控除額 × 所得税率 が還付金の目安です。</p>",
    faq: [
      { question: "10万円以下でも控除できる？", answer: "所得が200万円未満なら、所得の5%を超えた分が控除できます。" },
      { question: "市販薬は対象？", answer: "セルフメディケーション税制なら、スイッチOTC医薬品の年間購入額が12,000円を超えた部分が控除対象です（通常の医療費控除との選択制）。" },
    ],
    related: ["income-tax", "high-cost-medical"], popular: false,
  },

  // === money/savings (expand) ===
  {
    slug: "goal-savings", category: "money", subcategory: "savings",
    title: "目標貯金計算", description: "目標額と期間から毎月の必要貯金額を計算",
    metaTitle: "目標貯金計算ツール｜毎月いくら貯めればいいか計算",
    metaDescription: "貯金目標額と達成期間から毎月の必要貯金額を計算。ボーナス加算にも対応した無料ツール。",
    calculatorFunction: "goalSavings",
    inputs: [
      { id: "targetAmount", label: "目標額", type: "number", unit: "万円", default: 500, min: 1, max: 100000, step: 1 },
      { id: "currentSavings", label: "現在の貯金", type: "number", unit: "万円", default: 50, min: 0, max: 100000, step: 1 },
      { id: "months", label: "達成期間", type: "number", unit: "ヶ月", default: 36, min: 1, max: 600, step: 1 },
    ],
    outputs: [
      { id: "monthlySaving", label: "毎月の貯金額", format: "text", primary: true },
      { id: "remaining", label: "あと必要な額", format: "text" },
    ],
    explanation: "<h3>貯金計画の立て方</h3><p>（目標額 - 現在の貯金）÷ 月数 = 毎月の必要貯金額です。給料日に自動振替で先取り貯金するのが確実な方法です。</p>",
    faq: [
      { question: "理想的な貯蓄率は？", answer: "手取りの20〜25%が理想とされています。最低でも10%は貯蓄に回すことが推奨されます。" },
    ],
    related: ["compound-interest", "fire-calculation"], popular: false,
  },
  {
    slug: "72-rule", category: "money", subcategory: "savings",
    title: "72の法則計算", description: "お金が2倍になるまでの年数を計算",
    metaTitle: "72の法則計算ツール｜お金が2倍になる年数を計算",
    metaDescription: "金利（利回り）から資産が2倍になるまでの年数を計算。72÷金利で簡単に求められる複利計算の法則。",
    calculatorFunction: "rule72",
    inputs: [
      { id: "rate", label: "年利回り", type: "number", unit: "%", default: 5, min: 0.1, max: 100, step: 0.1 },
    ],
    outputs: [
      { id: "years", label: "2倍になるまでの年数", format: "text", primary: true },
      { id: "quadrupleYears", label: "4倍になるまでの年数", format: "text" },
    ],
    explanation: "<h3>72の法則</h3><p>72 ÷ 年利回り(%) ≒ 資産が2倍になるまでの年数です。例えば年利5%なら72÷5=約14.4年で2倍になります。複利効果の威力がわかる便利な法則です。</p>",
    faq: [
      { question: "銀行預金（0.02%）だと何年で2倍？", answer: "72÷0.02=3,600年かかります。低金利では預金だけで資産を増やすのは困難です。" },
    ],
    related: ["compound-interest", "goal-savings"], popular: false,
  },

  // === money/loan (expand) ===
  {
    slug: "car-loan-detail", category: "money", subcategory: "loan",
    title: "マイカーローン計算", description: "車のローン返済額と総支払額を計算",
    metaTitle: "マイカーローン計算ツール｜月々の返済額を自動計算",
    metaDescription: "車の購入価格・頭金・金利・返済期間から月々の返済額と総支払額を計算。ディーラーローンと銀行ローンの比較にも。",
    calculatorFunction: "carLoanDetail",
    inputs: [
      { id: "carPrice", label: "車両価格", type: "number", unit: "万円", default: 300, min: 10, max: 10000, step: 10 },
      { id: "downPayment", label: "頭金", type: "number", unit: "万円", default: 50, min: 0, max: 10000, step: 10 },
      { id: "rate", label: "年利", type: "number", unit: "%", default: 3, min: 0, max: 20, step: 0.1 },
      { id: "years", label: "返済期間", type: "number", unit: "年", default: 5, min: 1, max: 10, step: 1 },
    ],
    outputs: [
      { id: "monthlyPayment", label: "月々の返済額", format: "currency", primary: true },
      { id: "totalPayment", label: "返済総額", format: "currency" },
      { id: "totalInterest", label: "利息合計", format: "currency" },
      { id: "loanAmount", label: "借入額", format: "currency" },
    ],
    explanation: "<h3>マイカーローンの選び方</h3><p>ディーラーローン（年利3〜8%）は手続きが簡単、銀行ローン（年利1〜3%）は金利が低い傾向です。残価設定ローンは月々の支払いは安いですが総支払額は多くなることがあります。</p>",
    faq: [
      { question: "頭金はいくら入れるべき？", answer: "車両価格の20〜30%が理想です。頭金が多いほど月々の返済額と利息が減ります。" },
    ],
    related: ["car-loan", "loan-repayment"], popular: false,
  },

  // === money/insurance (expand) ===
  {
    slug: "life-insurance-need", category: "money", subcategory: "insurance",
    title: "必要保障額計算", description: "家族構成から生命保険の必要保障額を計算",
    metaTitle: "必要保障額計算ツール｜生命保険はいくら必要か計算",
    metaDescription: "家族構成・年収・貯蓄額から万一の場合に必要な生命保険の保障額を自動計算。",
    calculatorFunction: "lifeInsuranceNeed",
    inputs: [
      { id: "annualIncome", label: "世帯年収", type: "number", unit: "万円", default: 500, min: 100, max: 10000, step: 10 },
      { id: "savings", label: "現在の貯蓄", type: "number", unit: "万円", default: 500, min: 0, max: 100000, step: 10 },
      { id: "children", label: "子供の人数", type: "number", default: 2, min: 0, max: 10, step: 1 },
      { id: "youngestAge", label: "末子の年齢", type: "number", unit: "歳", default: 5, min: 0, max: 22, step: 1 },
    ],
    outputs: [
      { id: "totalNeed", label: "必要保障額", format: "text", primary: true },
      { id: "livingExpense", label: "遺族生活費", format: "text" },
      { id: "educationCost", label: "教育費", format: "text" },
      { id: "publicPension", label: "遺族年金（概算）", format: "text" },
    ],
    explanation: "<h3>必要保障額の考え方</h3><p>必要保障額 = 遺族の生活費 + 教育費 + 住居費 - 貯蓄 - 遺族年金 - 死亡退職金です。子供が小さいほど保障額は大きく、成長とともに減少します。</p>",
    faq: [
      { question: "子供1人の教育費は？", answer: "全て公立で約1,000万円、全て私立で約2,500万円が目安です。大学の学費が最も大きな割合を占めます。" },
    ],
    related: ["car-insurance", "fire-insurance"], popular: false,
  },

  // === money/real-estate (expand) ===
  {
    slug: "rent-vs-buy", category: "money", subcategory: "real-estate",
    title: "賃貸vs購入シミュレーション", description: "賃貸と持ち家のどちらがお得か比較",
    metaTitle: "賃貸vs購入比較ツール｜どちらがお得か自動計算",
    metaDescription: "賃貸と住宅購入の総コストを比較シミュレーション。住宅ローン・管理費・固定資産税を含む総合比較。",
    calculatorFunction: "rentVsBuy",
    inputs: [
      { id: "monthlyRent", label: "月額家賃", type: "number", unit: "万円", default: 10, min: 1, max: 100, step: 0.5 },
      { id: "propertyPrice", label: "物件価格", type: "number", unit: "万円", default: 4000, min: 500, max: 50000, step: 100 },
      { id: "loanRate", label: "住宅ローン金利", type: "number", unit: "%", default: 1.5, min: 0, max: 10, step: 0.1 },
      { id: "years", label: "比較期間", type: "number", unit: "年", default: 35, min: 5, max: 50, step: 1 },
    ],
    outputs: [
      { id: "rentTotal", label: "賃貸の総コスト", format: "text" },
      { id: "buyTotal", label: "購入の総コスト", format: "text" },
      { id: "difference", label: "差額", format: "text", primary: true },
      { id: "recommendation", label: "判定", format: "text" },
    ],
    explanation: "<h3>賃貸vs購入の比較</h3><p>賃貸の総コスト = 家賃 × 月数 + 更新料。購入の総コスト = 物件価格 + ローン利息 + 管理費・修繕積立金 + 固定資産税 - 売却見込み額。一概にどちらが得とは言えず、ライフプランや地域による違いが大きいです。</p>",
    faq: [
      { question: "一般的にどちらがお得？", answer: "13年以上住む場合は購入、それ以下なら賃貸が有利な傾向がありますが、物件や地域で大きく異なります。" },
    ],
    related: ["loan-repayment", "fixed-asset-tax"], popular: false,
  },

  // === money/investment (expand) ===
  {
    slug: "dividend-reinvestment", category: "money", subcategory: "investment",
    title: "配当再投資シミュレーション", description: "配当金を再投資した場合の資産成長を計算",
    metaTitle: "配当再投資シミュレーションツール｜複利効果を計算",
    metaDescription: "初期投資額・配当利回り・再投資期間から配当再投資による資産成長を計算。複利効果を可視化。",
    calculatorFunction: "dividendReinvestment",
    inputs: [
      { id: "initialInvestment", label: "初期投資額", type: "number", unit: "万円", default: 100, min: 1, max: 100000, step: 1 },
      { id: "dividendYield", label: "年間配当利回り", type: "number", unit: "%", default: 4, min: 0, max: 20, step: 0.1 },
      { id: "years", label: "投資期間", type: "number", unit: "年", default: 20, min: 1, max: 50, step: 1 },
      { id: "monthlyAdd", label: "毎月の追加投資", type: "number", unit: "万円", default: 3, min: 0, max: 100, step: 0.5 },
    ],
    outputs: [
      { id: "totalValue", label: "最終資産額", format: "text", primary: true },
      { id: "totalInvested", label: "投資元本合計", format: "text" },
      { id: "totalDividends", label: "配当金累計", format: "text" },
      { id: "annualDividend", label: "最終年の年間配当", format: "text" },
    ],
    explanation: "<h3>配当再投資の効果</h3><p>配当金を受け取らず再投資することで、翌年の配当基盤が増え、複利効果で資産が加速度的に成長します。長期投資では配当再投資の有無で大きな差が生まれます。</p>",
    faq: [
      { question: "高配当株のリスクは？", answer: "配当利回りが異常に高い銘柄は減配や株価下落のリスクがあります。安定した配当実績のある銘柄を選びましょう。" },
    ],
    related: ["dividend-yield", "compound-interest", "dollar-cost-averaging"], popular: false,
  },

  // === money/pension (expand) ===
  {
    slug: "pension-simulation", category: "money", subcategory: "pension",
    title: "年金受給額シミュレーション", description: "加入年数と年収から将来の年金受給額を概算",
    metaTitle: "年金受給額シミュレーションツール｜将来の年金額を計算",
    metaDescription: "厚生年金の加入年数と平均年収から将来受け取る年金額を概算計算。繰り上げ・繰り下げ受給の比較も。",
    calculatorFunction: "pensionSimulation",
    inputs: [
      { id: "avgSalary", label: "平均年収", type: "number", unit: "万円", default: 500, min: 100, max: 10000, step: 10 },
      { id: "enrollYears", label: "厚生年金加入年数", type: "number", unit: "年", default: 38, min: 1, max: 45, step: 1 },
    ],
    outputs: [
      { id: "annualPension", label: "年間年金額（65歳）", format: "text", primary: true },
      { id: "monthlyPension", label: "月額年金", format: "text" },
      { id: "earlyPension", label: "60歳繰り上げ（月額）", format: "text" },
      { id: "latePension", label: "70歳繰り下げ（月額）", format: "text" },
    ],
    explanation: "<h3>公的年金の計算</h3><p>年金額 = 基礎年金（満額約78万円/年）+ 報酬比例部分（平均標準報酬 × 5.481/1000 × 加入月数）です。繰り上げは1ヶ月あたり0.4%減額、繰り下げは1ヶ月あたり0.7%増額されます。</p>",
    faq: [
      { question: "何歳から受け取るのがお得？", answer: "損益分岐点は繰り上げが約80歳、繰り下げが約82歳です。長生きに自信があれば繰り下げが有利です。" },
    ],
    related: ["corporate-pension", "fire-calculation"], popular: false,
  },

  // === business/accounting (expand) ===
  {
    slug: "invoice-tax", category: "business", subcategory: "accounting",
    title: "インボイス消費税計算", description: "インボイス制度での消費税額を計算",
    metaTitle: "インボイス消費税計算ツール｜適格請求書の税額計算",
    metaDescription: "インボイス制度に対応した消費税額の計算。積み上げ計算・割戻し計算の両方に対応した無料ツール。",
    calculatorFunction: "invoiceTax",
    inputs: [
      { id: "amount", label: "税抜金額", type: "number", unit: "円", default: 100000, min: 0, max: 999999999, step: 1 },
      { id: "taxRate", label: "税率", type: "select", options: [{ value: "10", label: "10%（標準）" }, { value: "8", label: "8%（軽減）" }], default: "10" },
    ],
    outputs: [
      { id: "taxAmount", label: "消費税額", format: "currency", primary: true },
      { id: "totalAmount", label: "税込金額", format: "currency" },
    ],
    explanation: "<h3>インボイス制度の消費税計算</h3><p>2023年10月から開始されたインボイス制度では、適格請求書に正確な消費税額を記載する必要があります。税額は「税率ごとに合計した税抜金額 × 税率」で計算し、1円未満は切り捨てが原則です。</p>",
    faq: [
      { question: "免税事業者はどうなる？", answer: "2029年9月まで経過措置があり、免税事業者からの仕入れでも一定割合の仕入税額控除が認められます。" },
    ],
    related: ["consumption-tax", "consumption-tax-calc"], popular: false,
  },
  {
    slug: "profit-margin", category: "business", subcategory: "accounting",
    title: "利益率計算", description: "売上と原価から各種利益率を計算",
    metaTitle: "利益率計算ツール｜粗利率・営業利益率を自動計算",
    metaDescription: "売上高・原価・経費から粗利率・営業利益率・純利益率を一括計算。経営分析に便利な無料ツール。",
    calculatorFunction: "profitMargin",
    inputs: [
      { id: "revenue", label: "売上高", type: "number", unit: "万円", default: 1000, min: 0, max: 999999999, step: 1 },
      { id: "cogs", label: "売上原価", type: "number", unit: "万円", default: 600, min: 0, max: 999999999, step: 1 },
      { id: "expenses", label: "販管費", type: "number", unit: "万円", default: 250, min: 0, max: 999999999, step: 1 },
    ],
    outputs: [
      { id: "grossProfit", label: "粗利（売上総利益）", format: "text" },
      { id: "grossMarginRate", label: "粗利率", format: "text", primary: true },
      { id: "operatingProfit", label: "営業利益", format: "text" },
      { id: "operatingMarginRate", label: "営業利益率", format: "text" },
    ],
    explanation: "<h3>利益率の種類</h3><p>粗利率 = (売上-原価)/売上×100。営業利益率 = (売上-原価-販管費)/売上×100。業種により目安は異なりますが、営業利益率10%以上は優良企業とされます。</p>",
    faq: [
      { question: "業種別の平均利益率は？", answer: "製造業5〜8%、小売業2〜4%、IT業10〜15%、飲食業3〜5%が目安です。" },
    ],
    related: ["gross-margin", "break-even"], popular: false,
  },

  // === business/freelance (expand) ===
  {
    slug: "freelance-income-sim", category: "business", subcategory: "freelance",
    title: "フリーランス手取り計算", description: "売上から税金・社会保険を引いた手取りを計算",
    metaTitle: "フリーランス手取り計算ツール｜年収から手取りを自動計算",
    metaDescription: "フリーランスの売上から所得税・住民税・国保・年金を差し引いた手取り額を計算。経費率も設定可能。",
    calculatorFunction: "freelanceIncomeSim",
    inputs: [
      { id: "revenue", label: "年間売上", type: "number", unit: "万円", default: 800, min: 100, max: 10000, step: 10 },
      { id: "expenseRate", label: "経費率", type: "number", unit: "%", default: 30, min: 0, max: 80, step: 1 },
      { id: "blueReturn", label: "青色申告", type: "select", options: [{ value: "65", label: "青色申告（65万円控除）" }, { value: "10", label: "青色申告（10万円控除）" }, { value: "0", label: "白色申告" }], default: "65" },
    ],
    outputs: [
      { id: "income", label: "所得（売上-経費）", format: "text" },
      { id: "incomeTax", label: "所得税（概算）", format: "text" },
      { id: "residentTax", label: "住民税（概算）", format: "text" },
      { id: "socialInsurance", label: "国保+年金（概算）", format: "text" },
      { id: "takeHome", label: "手取り額", format: "text", primary: true },
    ],
    explanation: "<h3>フリーランスの手取り計算</h3><p>手取り = 売上 - 経費 - 所得税 - 住民税 - 国保 - 国民年金です。青色申告65万円控除を使うと大幅に節税できます。国保は自治体により異なりますが、所得の10〜14%が目安です。</p>",
    faq: [
      { question: "会社員と比べてどのくらい手取りが減る？", answer: "同じ額面なら、フリーランスは社会保険料の事業主負担がない分、手取りが15〜20%少なくなる傾向です。" },
    ],
    related: ["freelance-tax", "freelance-rate", "blue-return"], popular: false,
  },

  // === business/hr (expand) ===
  {
    slug: "hiring-cost", category: "business", subcategory: "hr",
    title: "採用コスト計算", description: "1人あたりの採用コストを計算",
    metaTitle: "採用コスト計算ツール｜1人あたりの採用単価を計算",
    metaDescription: "求人広告費・人材紹介手数料・面接の人件費から1人あたりの採用コストを計算。採用ROIの改善に。",
    calculatorFunction: "hiringCost",
    inputs: [
      { id: "adCost", label: "求人広告費", type: "number", unit: "万円", default: 100, min: 0, max: 10000, step: 1 },
      { id: "agencyFee", label: "人材紹介手数料", type: "number", unit: "万円", default: 100, min: 0, max: 10000, step: 1 },
      { id: "internalCost", label: "社内人件費（面接等）", type: "number", unit: "万円", default: 30, min: 0, max: 10000, step: 1 },
      { id: "hires", label: "採用人数", type: "number", unit: "人", default: 3, min: 1, max: 100, step: 1 },
    ],
    outputs: [
      { id: "totalCost", label: "採用コスト合計", format: "text" },
      { id: "costPerHire", label: "1人あたり採用コスト", format: "text", primary: true },
    ],
    explanation: "<h3>採用コストの計算</h3><p>採用コスト = (広告費 + 紹介手数料 + 社内人件費) ÷ 採用人数です。日本企業の平均採用コストは新卒1人あたり約93万円、中途1人あたり約104万円です。</p>",
    faq: [
      { question: "人材紹介手数料の相場は？", answer: "年収の30〜35%が一般的です。年収500万円なら150〜175万円が目安です。" },
    ],
    related: ["freelance-rate"], popular: false,
  },

  // === life/car (expand) ===
  {
    slug: "ev-charging-cost", category: "life", subcategory: "car",
    title: "EV充電コスト計算", description: "電気自動車の充電にかかる電気代を計算",
    metaTitle: "EV充電コスト計算ツール｜電気自動車の電気代を計算",
    metaDescription: "電気自動車のバッテリー容量・電気料金・走行距離から充電コストを計算。ガソリン車との比較も。",
    calculatorFunction: "evChargingCost",
    inputs: [
      { id: "batteryCapacity", label: "バッテリー容量", type: "number", unit: "kWh", default: 60, min: 10, max: 200, step: 1 },
      { id: "electricityRate", label: "電気料金", type: "number", unit: "円/kWh", default: 30, min: 10, max: 80, step: 1 },
      { id: "efficiency", label: "電費", type: "number", unit: "km/kWh", default: 6, min: 2, max: 12, step: 0.1 },
      { id: "monthlyKm", label: "月間走行距離", type: "number", unit: "km", default: 1000, min: 0, max: 10000, step: 100 },
    ],
    outputs: [
      { id: "fullChargeCost", label: "フル充電コスト", format: "currency" },
      { id: "monthlyCost", label: "月間電気代", format: "currency", primary: true },
      { id: "costPerKm", label: "1kmあたりコスト", format: "text" },
      { id: "gasolineEquivalent", label: "ガソリン車比（参考）", format: "text" },
    ],
    explanation: "<h3>EVの充電コスト</h3><p>充電コスト = バッテリー容量 × 電気料金で計算します。EV車の電費は一般的に5〜8km/kWhで、1kmあたり約4〜6円です。ガソリン車（燃費15km/L、ガソリン170円/L）は1kmあたり約11円なので、EVは約半分のランニングコストです。</p>",
    faq: [
      { question: "自宅充電と急速充電、どちらが安い？", answer: "自宅充電（深夜電力利用）が最も安く、約15〜25円/kWhです。急速充電は30〜50円/kWh程度です。" },
    ],
    related: ["ev-cost-comparison", "fuel-cost", "car-cost-total"], popular: false,
  },

  // === life/unit (expand) ===
  {
    slug: "cooking-measure", category: "life", subcategory: "unit",
    title: "料理の計量換算", description: "大さじ・小さじ・カップをml・gに換算",
    metaTitle: "料理の計量換算ツール｜大さじ・小さじをml・gに変換",
    metaDescription: "大さじ・小さじ・カップの分量をml・g単位に換算。調味料別の重量にも対応した無料ツール。",
    calculatorFunction: "cookingMeasure",
    inputs: [
      { id: "amount", label: "量", type: "number", default: 1, min: 0.1, max: 100, step: 0.1 },
      { id: "unit", label: "単位", type: "select", options: [{ value: "tablespoon", label: "大さじ" }, { value: "teaspoon", label: "小さじ" }, { value: "cup", label: "カップ" }], default: "tablespoon" },
      { id: "ingredient", label: "調味料", type: "select", options: [{ value: "water", label: "水・酢・酒" }, { value: "soy", label: "醤油・みりん" }, { value: "sugar", label: "砂糖" }, { value: "salt", label: "塩" }, { value: "flour", label: "小麦粉" }, { value: "oil", label: "油" }], default: "water" },
    ],
    outputs: [
      { id: "ml", label: "体積(ml)", format: "text", primary: true },
      { id: "grams", label: "重量(g)", format: "text" },
    ],
    explanation: "<h3>料理の計量単位</h3><p>大さじ1=15ml、小さじ1=5ml、1カップ=200mlです。ただし重量は調味料によって異なります。例えば大さじ1の砂糖は9g、塩は18g、小麦粉は9gです。</p>",
    faq: [
      { question: "大さじ1は何cc？", answer: "15cc（15ml）です。ccとmlは同じ量です。" },
    ],
    related: ["tbsp-to-ml", "tsp-to-ml", "recipe-scale"], popular: false,
  },

  // Add more calculators for remaining gap to 450+

  // === money/savings ===
  {
    slug: "emergency-months", category: "money", subcategory: "savings",
    title: "緊急資金計算", description: "月の支出から必要な緊急予備資金を計算",
    metaTitle: "緊急資金計算ツール｜いくら貯めれば安心か計算",
    metaDescription: "月の固定支出から緊急時に必要な予備資金の目安を計算。失業・病気など万一に備える無料ツール。",
    calculatorFunction: "emergencyMonths",
    inputs: [
      { id: "monthlyExpense", label: "月の生活費", type: "number", unit: "万円", default: 25, min: 5, max: 200, step: 1 },
      { id: "months", label: "確保したい月数", type: "number", unit: "ヶ月", default: 6, min: 1, max: 24, step: 1 },
    ],
    outputs: [
      { id: "targetAmount", label: "必要な緊急資金", format: "text", primary: true },
    ],
    explanation: "<h3>緊急予備資金の目安</h3><p>一般的に生活費の3〜6ヶ月分が推奨されます。フリーランスや自営業なら6〜12ヶ月分が安心です。</p>",
    faq: [
      { question: "どこに預ける？", answer: "すぐに引き出せる普通預金が基本です。一部をネット銀行の定期預金にするのもアリです。" },
    ],
    related: ["goal-savings", "emergency-fund"], popular: false,
  },

  // === money/tax ===
  {
    slug: "withholding-tax", category: "money", subcategory: "tax",
    title: "源泉徴収税額計算", description: "報酬額から源泉徴収税額を計算",
    metaTitle: "源泉徴収税額計算ツール｜報酬の源泉徴収額を自動計算",
    metaDescription: "フリーランス・個人事業主への報酬の源泉徴収税額を計算。100万円以下・100万超で税率が変わる計算に対応。",
    calculatorFunction: "withholdingTax",
    inputs: [
      { id: "amount", label: "報酬額（税抜）", type: "number", unit: "円", default: 500000, min: 0, max: 999999999, step: 1 },
    ],
    outputs: [
      { id: "withholdingAmount", label: "源泉徴収税額", format: "currency", primary: true },
      { id: "netAmount", label: "手取り額", format: "currency" },
    ],
    explanation: "<h3>源泉徴収税額の計算</h3><p>100万円以下の部分は10.21%、100万円を超える部分は20.42%が源泉徴収されます。復興特別所得税(2.1%)を含んだ税率です。</p>",
    faq: [
      { question: "消費税を含めた額に課税される？", answer: "請求書で税抜金額と消費税額を明確に区分していれば、税抜金額に対して源泉徴収されます。" },
    ],
    related: ["income-tax", "freelance-tax"], popular: false,
  },

  // === education/school ===
  {
    slug: "school-fee", category: "education", subcategory: "school",
    title: "学費シミュレーション", description: "幼稚園から大学までの学費総額を計算",
    metaTitle: "学費シミュレーションツール｜教育費の総額を計算",
    metaDescription: "幼稚園・小学校・中学校・高校・大学の公立/私立を選んで教育費の総額を計算。",
    calculatorFunction: "schoolFee",
    inputs: [
      { id: "kindergarten", label: "幼稚園", type: "select", options: [{ value: "public", label: "公立" }, { value: "private", label: "私立" }], default: "public" },
      { id: "elementary", label: "小学校", type: "select", options: [{ value: "public", label: "公立" }, { value: "private", label: "私立" }], default: "public" },
      { id: "juniorHigh", label: "中学校", type: "select", options: [{ value: "public", label: "公立" }, { value: "private", label: "私立" }], default: "public" },
      { id: "highSchool", label: "高校", type: "select", options: [{ value: "public", label: "公立" }, { value: "private", label: "私立" }], default: "public" },
      { id: "university", label: "大学", type: "select", options: [{ value: "national", label: "国立" }, { value: "publicUni", label: "公立" }, { value: "privateSci", label: "私立理系" }, { value: "privateArt", label: "私立文系" }], default: "national" },
    ],
    outputs: [
      { id: "totalCost", label: "教育費総額", format: "text", primary: true },
      { id: "kindergartenCost", label: "幼稚園", format: "text" },
      { id: "elementaryCost", label: "小学校", format: "text" },
      { id: "juniorHighCost", label: "中学校", format: "text" },
      { id: "highSchoolCost", label: "高校", format: "text" },
      { id: "universityCost", label: "大学", format: "text" },
    ],
    explanation: "<h3>教育費の目安</h3><p>文部科学省の調査に基づく目安です。オール公立で約1,000万円、オール私立で約2,500万円が相場です。大学は4年間で国立約250万円、私立文系約400万円、私立理系約550万円です。</p>",
    faq: [
      { question: "塾代は含まれる？", answer: "学校外活動費（塾・習い事）を一部含んでいますが、実際の塾代は別途大きくかかることがあります。" },
    ],
    related: ["education-cost-sim", "education-loan", "child-cost"], popular: false,
  },

  // === health/calorie ===
  {
    slug: "protein-food-compare", category: "health", subcategory: "calorie",
    title: "タンパク質コスパ比較", description: "食品のタンパク質あたりの価格を比較",
    metaTitle: "タンパク質コスパ比較ツール｜食品のプロテインコスパを計算",
    metaDescription: "食品の価格・重量・タンパク質含有量からタンパク質1gあたりのコストを計算。最もコスパの良いタンパク源を見つける。",
    calculatorFunction: "proteinFoodCompare",
    inputs: [
      { id: "price", label: "価格", type: "number", unit: "円", default: 500, min: 1, max: 99999, step: 1 },
      { id: "weight", label: "内容量", type: "number", unit: "g", default: 200, min: 1, max: 99999, step: 1 },
      { id: "proteinPer100g", label: "タンパク質（100gあたり）", type: "number", unit: "g", default: 22, min: 0.1, max: 100, step: 0.1 },
    ],
    outputs: [
      { id: "costPerProteinG", label: "タンパク質1gあたりの価格", format: "text", primary: true },
      { id: "totalProtein", label: "総タンパク質量", format: "text" },
      { id: "costPer20g", label: "タンパク質20gの価格", format: "text" },
    ],
    explanation: "<h3>タンパク質のコスパ比較</h3><p>筋トレやダイエットでタンパク質を多く摂る場合、コスパは重要です。鶏胸肉（100gあたり約23g、約70円→約3円/gタンパク質）は最もコスパの良い食品の一つです。</p>",
    faq: [
      { question: "プロテインパウダーのコスパは？", answer: "一般的なホエイプロテインは1gあたり3〜5円。鶏胸肉とほぼ同等で手軽さがメリットです。" },
    ],
    related: ["protein-intake", "meal-calorie"], popular: false,
  },

  // === math/basic ===
  {
    slug: "number-to-kanji", category: "math", subcategory: "basic",
    title: "数字の漢数字変換", description: "アラビア数字を漢数字に変換",
    metaTitle: "漢数字変換ツール｜数字を漢数字に自動変換",
    metaDescription: "アラビア数字を漢数字（一二三…）に変換。大字（壱弐参…）にも対応。ご祝儀袋・領収書に。",
    calculatorFunction: "numberToKanji",
    inputs: [
      { id: "number", label: "数字", type: "number", default: 30000, min: 0, max: 999999999999, step: 1 },
      { id: "format", label: "形式", type: "select", options: [{ value: "normal", label: "通常（一二三）" }, { value: "formal", label: "大字（壱弐参）" }], default: "normal" },
    ],
    outputs: [
      { id: "kanji", label: "漢数字", format: "text", primary: true },
    ],
    explanation: "<h3>漢数字の使い分け</h3><p>通常の漢数字（一、二、三…）は一般的な文書に使います。大字（壱、弐、参…）は改ざん防止のため、ご祝儀袋、領収書、法的文書で使われます。</p>",
    faq: [
      { question: "30,000円のご祝儀袋の書き方は？", answer: "大字で「金参萬圓」と書きます。" },
    ],
    related: [], popular: false,
  },
  {
    slug: "fibonacci", category: "math", subcategory: "basic",
    title: "フィボナッチ数列", description: "フィボナッチ数列のn番目の値を計算",
    metaTitle: "フィボナッチ数列計算ツール｜n番目の値を自動計算",
    metaDescription: "フィボナッチ数列のn番目の数を計算。数列一覧の表示にも対応した無料ツール。",
    calculatorFunction: "fibonacci",
    inputs: [
      { id: "n", label: "n番目", type: "number", default: 10, min: 1, max: 75, step: 1 },
    ],
    outputs: [
      { id: "value", label: "フィボナッチ数", format: "text", primary: true },
      { id: "sequence", label: "数列（最初からn番目まで）", format: "text" },
    ],
    explanation: "<h3>フィボナッチ数列とは</h3><p>前の2つの数の和が次の数になる数列です：1, 1, 2, 3, 5, 8, 13, 21, 34, 55...。自然界の花びらの数やひまわりの種の並びにも現れる美しい数列です。隣接する2項の比は黄金比（約1.618）に近づきます。</p>",
    faq: [
      { question: "黄金比との関係は？", answer: "フィボナッチ数列のn+1番目÷n番目はnが大きくなるほど黄金比φ≒1.618に近づきます。" },
    ],
    related: ["prime-check"], popular: false,
  },

  // === business/accounting ===
  {
    slug: "roi-calculator", category: "business", subcategory: "accounting",
    title: "ROI計算", description: "投資収益率（ROI）を計算",
    metaTitle: "ROI計算ツール｜投資対効果を自動計算",
    metaDescription: "投資額と利益からROI（投資収益率）を計算。広告投資・設備投資・マーケティングの効果測定に。",
    calculatorFunction: "roiCalculator",
    inputs: [
      { id: "investment", label: "投資額", type: "number", unit: "万円", default: 100, min: 1, max: 999999999, step: 1 },
      { id: "revenue", label: "得られた収益", type: "number", unit: "万円", default: 150, min: 0, max: 999999999, step: 1 },
    ],
    outputs: [
      { id: "roi", label: "ROI", format: "text", primary: true },
      { id: "profit", label: "利益額", format: "text" },
    ],
    explanation: "<h3>ROIの計算</h3><p>ROI = (収益 - 投資額) ÷ 投資額 × 100%です。ROIが正なら投資が利益を生んでおり、負なら損失を出しています。100%なら投資額が2倍になったことを意味します。</p>",
    faq: [
      { question: "ROIとROASの違いは？", answer: "ROIは利益ベース、ROAS（広告費用対効果）は売上ベースです。ROAS = 売上 ÷ 広告費 × 100%。" },
    ],
    related: ["ad-roas", "break-even", "gross-margin"], popular: false,
  },

  // === business/hr ===
  {
    slug: "employee-cost", category: "business", subcategory: "hr",
    title: "従業員コスト計算", description: "給与以外の社会保険料含む総人件費を計算",
    metaTitle: "従業員コスト計算ツール｜1人あたりの総人件費を計算",
    metaDescription: "月給・賞与に加え社会保険料の事業主負担を含めた1人あたりの年間総人件費を計算。",
    calculatorFunction: "employeeCost",
    inputs: [
      { id: "monthlySalary", label: "月給", type: "number", unit: "万円", default: 30, min: 10, max: 500, step: 1 },
      { id: "bonusMonths", label: "賞与（月数）", type: "number", unit: "ヶ月", default: 4, min: 0, max: 12, step: 0.5 },
    ],
    outputs: [
      { id: "annualSalary", label: "年間給与", format: "text" },
      { id: "socialInsurance", label: "社会保険料（事業主負担）", format: "text" },
      { id: "totalCost", label: "年間総人件費", format: "text", primary: true },
      { id: "monthlyCost", label: "月あたり人件費", format: "text" },
    ],
    explanation: "<h3>従業員の総コスト</h3><p>給与の他に、健康保険（約5%）、厚生年金（約9.15%）、雇用保険（約0.6%）、労災保険（約0.3%）の事業主負担があります。合計で給与の約15%が追加コストとなり、年間総人件費は額面給与の約1.15倍になります。</p>",
    faq: [
      { question: "給与30万円の人の本当のコストは？", answer: "社会保険料等を含めると約34.5万円/月、年間で約550万円（賞与4ヶ月の場合）が目安です。" },
    ],
    related: ["hiring-cost", "hourly-wage"], popular: false,
  },

  // === life/date ===
  {
    slug: "school-year", category: "life", subcategory: "date",
    title: "学年計算", description: "生年月日から現在の学年を計算",
    metaTitle: "学年計算ツール｜生年月日から学年を自動判定",
    metaDescription: "生年月日を入力するだけで現在の学年（小1〜高3・大学）を自動計算。早生まれにも対応。",
    calculatorFunction: "schoolYear",
    inputs: [
      { id: "birthDate", label: "生年月日", type: "date", default: "2015-05-01" },
    ],
    outputs: [
      { id: "schoolYear", label: "現在の学年", format: "text", primary: true },
      { id: "graduationDate", label: "卒業予定", format: "text" },
      { id: "isEarlyBorn", label: "早生まれ判定", format: "text" },
    ],
    explanation: "<h3>学年の決め方</h3><p>日本の学校は4月2日〜翌年4月1日生まれが同学年です。4月1日生まれは前の学年に入ります（法律上、誕生日の前日に加齢するため）。</p>",
    faq: [
      { question: "4月1日生まれはなぜ早生まれ？", answer: "法律上「年齢は誕生日の前日に加齢する」ため、4月1日生まれは3月31日に加齢し、前年度の学年に含まれます。" },
    ],
    related: ["age-calculator"], popular: false,
  },
  {
    slug: "wareki-seireki", category: "life", subcategory: "date",
    title: "和暦西暦変換", description: "和暦（令和・平成・昭和）と西暦を相互変換",
    metaTitle: "和暦西暦変換ツール｜令和・平成・昭和を西暦に変換",
    metaDescription: "和暦（令和・平成・昭和・大正・明治）と西暦を簡単に相互変換。書類作成に便利な無料ツール。",
    calculatorFunction: "warekiSeireki",
    inputs: [
      { id: "era", label: "元号", type: "select", options: [{ value: "reiwa", label: "令和" }, { value: "heisei", label: "平成" }, { value: "showa", label: "昭和" }, { value: "taisho", label: "大正" }, { value: "meiji", label: "明治" }], default: "reiwa" },
      { id: "year", label: "年", type: "number", default: 8, min: 1, max: 100, step: 1 },
    ],
    outputs: [
      { id: "seireki", label: "西暦", format: "text", primary: true },
      { id: "allEras", label: "他の元号表記", format: "text" },
    ],
    explanation: "<h3>元号と西暦の対応</h3><p>令和=2018+年、平成=1988+年、昭和=1925+年、大正=1911+年、明治=1867+年です。</p>",
    faq: [
      { question: "令和8年は西暦何年？", answer: "2026年です。" },
      { question: "平成は何年まで？", answer: "平成は31年（2019年4月30日）までです。翌日5月1日から令和元年です。" },
    ],
    related: ["japanese-era", "age-calculator"], popular: false,
  },

  // === health/medical ===
  {
    slug: "fever-check", category: "health", subcategory: "medical",
    title: "発熱判定", description: "体温から発熱レベルを判定",
    metaTitle: "発熱判定ツール｜体温から発熱レベルをチェック",
    metaDescription: "体温を入力して発熱レベル（平熱・微熱・中等度・高熱）を判定。子供と大人の基準に対応。",
    calculatorFunction: "feverCheck",
    inputs: [
      { id: "temperature", label: "体温", type: "number", unit: "℃", default: 37.5, min: 34, max: 43, step: 0.1 },
      { id: "ageGroup", label: "年齢区分", type: "select", options: [{ value: "adult", label: "大人" }, { value: "child", label: "子供（0〜14歳）" }], default: "adult" },
    ],
    outputs: [
      { id: "level", label: "発熱レベル", format: "text", primary: true },
      { id: "advice", label: "対処の目安", format: "text" },
    ],
    explanation: "<h3>発熱の基準</h3><p>一般的に37.5℃以上を発熱、38.0℃以上を高熱とします。平熱には個人差があり36.0〜37.0℃が一般的です。子供は大人より平熱が高い傾向があります。</p>",
    faq: [
      { question: "37.5℃は微熱？", answer: "一般的には37.5〜38.0℃を微熱とします。ただし平熱が低い人は37℃台前半でも辛く感じることがあります。" },
    ],
    related: ["blood-pressure-check"], popular: false,
  },

  // === more life/shopping ===
  {
    slug: "amazon-price-per", category: "life", subcategory: "shopping",
    title: "まとめ買い比較計算", description: "単品vsまとめ買いのどちらがお得か比較",
    metaTitle: "まとめ買い比較計算ツール｜単品とセット買いを比較",
    metaDescription: "単品価格とまとめ買い価格を入力して1個あたりの単価を比較。お得なのはどちらかを瞬時に判定。",
    calculatorFunction: "bulkBuyCompare",
    inputs: [
      { id: "singlePrice", label: "単品価格", type: "number", unit: "円", default: 150, min: 1, max: 999999, step: 1 },
      { id: "bulkPrice", label: "まとめ買い価格", type: "number", unit: "円", default: 1200, min: 1, max: 999999999, step: 1 },
      { id: "bulkQuantity", label: "まとめ買い個数", type: "number", unit: "個", default: 10, min: 2, max: 9999, step: 1 },
    ],
    outputs: [
      { id: "singleUnit", label: "単品の1個あたり", format: "currency" },
      { id: "bulkUnit", label: "まとめ買いの1個あたり", format: "currency", primary: true },
      { id: "savings", label: "1個あたりの差額", format: "currency" },
      { id: "savingsPercent", label: "お得率", format: "text" },
    ],
    explanation: "<h3>まとめ買いの損得</h3><p>単品価格とまとめ買いの1個あたり単価を比較します。まとめ買いが安くても、使い切れなければ無駄になるため、消費期限や使用頻度も考慮しましょう。</p>",
    faq: [
      { question: "まとめ買いは必ずお得？", answer: "1個あたりの単価は安くなることが多いですが、使い切れない場合はかえって損になります。" },
    ],
    related: ["per-unit-price", "price-per-gram", "discount"], popular: false,
  },

  // === money/investment ===
  {
    slug: "sp500-simulation", category: "money", subcategory: "investment",
    title: "S&P500積立シミュレーション", description: "S&P500に毎月積立投資した場合の成長を計算",
    metaTitle: "S&P500積立シミュレーションツール｜インデックス投資の成長を計算",
    metaDescription: "毎月の積立額と期間からS&P500インデックス投資の資産成長を計算。過去の平均リターンに基づくシミュレーション。",
    calculatorFunction: "sp500Simulation",
    inputs: [
      { id: "monthlyInvestment", label: "毎月の積立額", type: "number", unit: "万円", default: 5, min: 0.1, max: 100, step: 0.1 },
      { id: "years", label: "積立期間", type: "number", unit: "年", default: 20, min: 1, max: 50, step: 1 },
      { id: "annualReturn", label: "想定年利回り", type: "number", unit: "%", default: 7, min: 0, max: 20, step: 0.1 },
    ],
    outputs: [
      { id: "totalInvested", label: "投資元本合計", format: "text" },
      { id: "finalValue", label: "最終資産額", format: "text", primary: true },
      { id: "totalReturn", label: "運用益", format: "text" },
      { id: "returnRate", label: "トータルリターン", format: "text" },
    ],
    explanation: "<h3>S&P500の過去実績</h3><p>S&P500の過去30年の年平均リターンは約10%（配当込み、インフレ調整前）です。為替変動やインフレを考慮すると日本円ベースでは7〜8%程度が現実的な想定です。過去の実績は将来を保証しません。</p>",
    faq: [
      { question: "毎月5万円を20年積立するといくら？", answer: "年利7%の場合、元本1,200万円が約2,604万円になります（税引前）。" },
    ],
    related: ["dollar-cost-averaging", "compound-interest", "calculate-nisa-simulation"], popular: false,
  },

  // === education/study ===
  {
    slug: "toeic-score-convert", category: "education", subcategory: "study",
    title: "TOEIC換算計算", description: "TOEICスコアから英検・CEFRレベルを推定",
    metaTitle: "TOEIC換算ツール｜英検・CEFR・TOEFLレベル変換",
    metaDescription: "TOEICスコアから英検の級、CEFRレベル、TOEFLスコアの目安を表示。英語力の指標比較に。",
    calculatorFunction: "toeicScoreConvert",
    inputs: [
      { id: "toeicScore", label: "TOEICスコア", type: "number", default: 700, min: 10, max: 990, step: 5 },
    ],
    outputs: [
      { id: "eiken", label: "英検（目安）", format: "text", primary: true },
      { id: "cefr", label: "CEFRレベル", format: "text" },
      { id: "toefl", label: "TOEFL iBT（目安）", format: "text" },
      { id: "description", label: "レベル説明", format: "text" },
    ],
    explanation: "<h3>英語試験スコアの換算</h3><p>あくまで目安の換算です。各試験は測定する能力が異なるため、完全な互換性はありません。TOEIC 600≒英検2級≒CEFR B1、TOEIC 800≒英検準1級≒CEFR B2が大まかな目安です。</p>",
    faq: [
      { question: "TOEIC何点あれば就活で有利？", answer: "一般的に600点以上でアピール可能、730点以上で英語力を評価されやすくなります。" },
    ],
    related: ["english-score"], popular: false,
  },

  // === more money/tax ===
  {
    slug: "inheritance-tax-sim", category: "money", subcategory: "tax",
    title: "相続税概算計算", description: "相続財産と相続人数から相続税を概算",
    metaTitle: "相続税計算ツール｜遺産総額から相続税を概算計算",
    metaDescription: "遺産総額と法定相続人の数から相続税の概算額を自動計算。基礎控除と税率を適用した無料ツール。",
    calculatorFunction: "inheritanceTaxSim",
    inputs: [
      { id: "totalAssets", label: "遺産総額", type: "number", unit: "万円", default: 8000, min: 0, max: 9999999, step: 100 },
      { id: "heirs", label: "法定相続人の数", type: "number", unit: "人", default: 3, min: 1, max: 10, step: 1 },
    ],
    outputs: [
      { id: "basicDeduction", label: "基礎控除額", format: "text" },
      { id: "taxableAmount", label: "課税遺産総額", format: "text" },
      { id: "totalTax", label: "相続税総額（概算）", format: "text", primary: true },
      { id: "taxPerHeir", label: "1人あたり税額（均等分割の場合）", format: "text" },
    ],
    explanation: "<h3>相続税の計算</h3><p>基礎控除 = 3,000万円 + 600万円 × 法定相続人数。課税遺産総額が基礎控除以下なら相続税はかかりません。税率は1,000万円以下10%〜6億円超55%の超過累進税率です。</p>",
    faq: [
      { question: "相続税がかからないケースは？", answer: "遺産総額が基礎控除以下（例：相続人3人なら4,800万円以下）の場合は非課税です。実際には約9割の人が非課税です。" },
    ],
    related: ["gift-tax", "income-tax"], popular: false,
  },

  // === more health/body ===
  {
    slug: "flexibility-age", category: "health", subcategory: "body",
    title: "体力年齢チェック", description: "簡易テスト結果から体力年齢を推定",
    metaTitle: "体力年齢チェックツール｜あなたの体力年齢を推定",
    metaDescription: "握力・腹筋・柔軟性などの簡易テスト結果から体力年齢を推定。実年齢との差をチェック。",
    calculatorFunction: "flexibilityAge",
    inputs: [
      { id: "actualAge", label: "実年齢", type: "number", unit: "歳", default: 40, min: 20, max: 80, step: 1 },
      { id: "gender", label: "性別", type: "select", options: [{ value: "male", label: "男性" }, { value: "female", label: "女性" }], default: "male" },
      { id: "gripStrength", label: "握力", type: "number", unit: "kg", default: 35, min: 5, max: 80, step: 0.5 },
      { id: "situps", label: "腹筋（30秒）", type: "number", unit: "回", default: 20, min: 0, max: 50, step: 1 },
      { id: "flexibility", label: "前屈", type: "number", unit: "cm", default: 5, min: -30, max: 30, step: 0.5 },
    ],
    outputs: [
      { id: "fitnessAge", label: "推定体力年齢", format: "text", primary: true },
      { id: "ageDifference", label: "実年齢との差", format: "text" },
    ],
    explanation: "<h3>体力年齢の推定</h3><p>文部科学省の新体力テストの基準を参考に、握力・腹筋・柔軟性のスコアから体力年齢を簡易推定します。あくまで目安であり、正確な評価は専門家の指導のもとで行ってください。</p>",
    faq: [
      { question: "体力年齢を若くするには？", answer: "週3回以上の有酸素運動と筋力トレーニングの組み合わせが効果的です。特にスクワットと腹筋運動がおすすめです。" },
    ],
    related: ["bmi", "basal-metabolism"], popular: false,
  },

  // === more business/freelance ===
  {
    slug: "hourly-vs-project", category: "business", subcategory: "freelance",
    title: "時給vs案件単価比較", description: "時給契約と案件単価のどちらが得か比較",
    metaTitle: "時給vs案件単価比較ツール｜フリーランスの報酬比較",
    metaDescription: "時給契約と案件単価（固定報酬）の実質時給を比較。フリーランスの契約判断に便利な無料ツール。",
    calculatorFunction: "hourlyVsProject",
    inputs: [
      { id: "hourlyRate", label: "時給", type: "number", unit: "円", default: 3000, min: 500, max: 50000, step: 100 },
      { id: "projectFee", label: "案件報酬", type: "number", unit: "万円", default: 50, min: 1, max: 10000, step: 1 },
      { id: "estimatedHours", label: "案件の予想作業時間", type: "number", unit: "時間", default: 120, min: 1, max: 2000, step: 1 },
    ],
    outputs: [
      { id: "projectHourlyRate", label: "案件の実質時給", format: "text", primary: true },
      { id: "hourlyTotal", label: "時給契約の同時間稼働額", format: "text" },
      { id: "recommendation", label: "判定", format: "text" },
    ],
    explanation: "<h3>報酬形態の比較</h3><p>案件の実質時給 = 案件報酬 ÷ 予想作業時間で比較します。案件単価は作業効率を上げるほど実質時給が上がるメリットがある反面、想定外の工数が発生するリスクもあります。</p>",
    faq: [
      { question: "どちらを選ぶべき？", answer: "作業量が明確なら案件単価、不確実要素が多いなら時給契約が安全です。経験を積んで効率が上がったら案件単価が有利になります。" },
    ],
    related: ["freelance-rate", "freelance-income-sim"], popular: false,
  },

  // === more life/utility ===
  {
    slug: "bra-size-calc", category: "life", subcategory: "utility",
    title: "ブラサイズ計算", description: "トップとアンダーバストからブラのサイズを計算",
    metaTitle: "ブラサイズ計算ツール｜トップ・アンダーバストからサイズ判定",
    metaDescription: "トップバストとアンダーバストを入力してブラジャーのカップサイズを自動計算。正しいサイズ選びに。",
    calculatorFunction: "braSizeCalc",
    inputs: [
      { id: "topBust", label: "トップバスト", type: "number", unit: "cm", default: 83, min: 60, max: 130, step: 0.5 },
      { id: "underBust", label: "アンダーバスト", type: "number", unit: "cm", default: 70, min: 55, max: 110, step: 0.5 },
    ],
    outputs: [
      { id: "cupSize", label: "カップサイズ", format: "text", primary: true },
      { id: "braSize", label: "ブラサイズ", format: "text" },
    ],
    explanation: "<h3>ブラサイズの計算方法</h3><p>カップサイズ = トップバスト - アンダーバストの差で決まります。差が10cmでA、12.5cmでB、15cmでC、17.5cmでD…と2.5cm刻みです。アンダーは5cm刻み（65, 70, 75, 80...）で四捨五入します。</p>",
    faq: [
      { question: "正しい測り方は？", answer: "ブラをつけずに、トップバストは乳首の位置で水平に、アンダーバストは胸の下の一番細い部分を水平に測ります。" },
    ],
    related: ["clothing-size"], popular: false,
  },
  {
    slug: "internet-speed", category: "life", subcategory: "utility",
    title: "通信速度換算", description: "Mbps・MB/sの変換とダウンロード時間を計算",
    metaTitle: "通信速度換算ツール｜Mbps・MB/s変換＆ダウンロード時間計算",
    metaDescription: "Mbps・Gbps・MB/sを相互変換。ファイルサイズからダウンロード時間も計算できる無料ツール。",
    calculatorFunction: "internetSpeed",
    inputs: [
      { id: "speed", label: "通信速度", type: "number", unit: "Mbps", default: 100, min: 0.1, max: 100000, step: 0.1 },
      { id: "fileSize", label: "ファイルサイズ", type: "number", unit: "MB", default: 1000, min: 0.1, max: 999999, step: 0.1 },
    ],
    outputs: [
      { id: "mbPerSec", label: "MB/s", format: "text", primary: true },
      { id: "gbps", label: "Gbps", format: "text" },
      { id: "downloadTime", label: "ダウンロード時間", format: "text" },
    ],
    explanation: "<h3>通信速度の単位</h3><p>1 Mbps = 0.125 MB/s（1バイト=8ビット）。100Mbpsの回線では理論上12.5MB/sですが、実効速度は60〜80%程度です。1GBのファイルは100Mbpsで約1分20秒かかります。</p>",
    faq: [
      { question: "動画視聴に必要な速度は？", answer: "HD動画は5Mbps、4K動画は25Mbps以上が推奨されます。" },
    ],
    related: ["download-time", "data-size"], popular: false,
  },

  // More to reach the target...
  {
    slug: "timezone-compare", category: "life", subcategory: "date",
    title: "時差計算", description: "2つの都市間の時差と現在時刻を表示",
    metaTitle: "時差計算ツール｜世界の都市の時差を計算",
    metaDescription: "2つの都市の時差と相手都市の現在時刻を計算。海外旅行・ビジネスの連絡に便利な無料ツール。",
    calculatorFunction: "timezoneCompare",
    inputs: [
      { id: "timezone1", label: "都市1のUTCオフセット", type: "number", unit: "時間", default: 9, min: -12, max: 14, step: 0.5 },
      { id: "timezone2", label: "都市2のUTCオフセット", type: "number", unit: "時間", default: -5, min: -12, max: 14, step: 0.5 },
      { id: "hour", label: "都市1の時刻（時）", type: "number", default: 12, min: 0, max: 23, step: 1 },
      { id: "minute", label: "分", type: "number", default: 0, min: 0, max: 59, step: 1 },
    ],
    outputs: [
      { id: "timeDiff", label: "時差", format: "text", primary: true },
      { id: "city2Time", label: "都市2の時刻", format: "text" },
    ],
    explanation: "<h3>主な都市のUTCオフセット</h3><p>東京+9、ニューヨーク-5（EST）/-4（EDT）、ロンドン0/+1（BST）、パリ+1/+2（CEST）、シドニー+10/+11（AEDT）、アスンシオン-3/-4。</p>",
    faq: [
      { question: "サマータイムは考慮される？", answer: "オフセットを手動入力するため、サマータイム適用時は該当する値を入力してください。" },
    ],
    related: ["time-zone", "timezone", "countdown"], popular: false,
  },

  // Add more quick calculators
  {
    slug: "password-strength", category: "life", subcategory: "utility",
    title: "パスワード強度チェック", description: "パスワードの長さと文字種から強度を推定",
    metaTitle: "パスワード強度チェックツール｜安全性を診断",
    metaDescription: "パスワードの長さ・文字種から解読にかかる時間を推定。安全なパスワードの基準を確認。",
    calculatorFunction: "passwordStrength",
    inputs: [
      { id: "length", label: "文字数", type: "number", default: 12, min: 1, max: 128, step: 1 },
      { id: "hasUppercase", label: "大文字を含む", type: "select", options: [{ value: "yes", label: "はい" }, { value: "no", label: "いいえ" }], default: "yes" },
      { id: "hasNumbers", label: "数字を含む", type: "select", options: [{ value: "yes", label: "はい" }, { value: "no", label: "いいえ" }], default: "yes" },
      { id: "hasSymbols", label: "記号を含む", type: "select", options: [{ value: "yes", label: "はい" }, { value: "no", label: "いいえ" }], default: "yes" },
    ],
    outputs: [
      { id: "strength", label: "強度", format: "text", primary: true },
      { id: "combinations", label: "組み合わせ数", format: "text" },
      { id: "crackTime", label: "総当たり解読時間（推定）", format: "text" },
    ],
    explanation: "<h3>パスワードの強度</h3><p>文字種が多く、長いほど安全です。小文字のみ8文字では約2000億通りですが、大小文字+数字+記号の12文字では約475京通りです。最低12文字以上を推奨します。</p>",
    faq: [
      { question: "安全なパスワードの条件は？", answer: "12文字以上、大文字・小文字・数字・記号を含む、辞書にある単語を避ける、サービスごとに異なるパスワードを使う。" },
    ],
    related: [], popular: false,
  },

  {
    slug: "electricity-unit", category: "life", subcategory: "shopping",
    title: "電気料金単価計算", description: "電気使用量と請求額から1kWhあたりの単価を計算",
    metaTitle: "電気料金単価計算ツール｜1kWhあたりの電気代を計算",
    metaDescription: "電気の請求額と使用量から1kWhあたりの単価を計算。電力会社の比較・乗り換え検討に便利。",
    calculatorFunction: "electricityUnit",
    inputs: [
      { id: "bill", label: "電気料金", type: "number", unit: "円", default: 8000, min: 0, max: 999999, step: 1 },
      { id: "usage", label: "使用量", type: "number", unit: "kWh", default: 250, min: 1, max: 99999, step: 1 },
    ],
    outputs: [
      { id: "unitPrice", label: "1kWhあたり単価", format: "text", primary: true },
      { id: "dailyCost", label: "1日あたり電気代", format: "text" },
    ],
    explanation: "<h3>電気料金の単価</h3><p>電気料金 ÷ 使用量(kWh)で1kWhあたりの単価を求めます。2024年の全国平均は約28〜35円/kWhです。</p>",
    faq: [
      { question: "電気代が高い基準は？", answer: "1kWhあたり35円以上は高めです。電力会社の乗り換えや料金プランの見直しを検討しましょう。" },
    ],
    related: ["electricity-bill", "electricity-cost"], popular: false,
  },

  {
    slug: "concrete-volume", category: "life", subcategory: "unit",
    title: "コンクリート量計算", description: "面積と厚さから必要なコンクリート量を計算",
    metaTitle: "コンクリート量計算ツール｜必要なコンクリートの体積を計算",
    metaDescription: "面積と厚さからコンクリートの必要量（立方メートル・キログラム）を計算。DIYや見積もりに。",
    calculatorFunction: "concreteVolume",
    inputs: [
      { id: "length", label: "長さ", type: "number", unit: "m", default: 5, min: 0.1, max: 1000, step: 0.1 },
      { id: "width", label: "幅", type: "number", unit: "m", default: 3, min: 0.1, max: 1000, step: 0.1 },
      { id: "depth", label: "厚さ", type: "number", unit: "cm", default: 10, min: 1, max: 500, step: 1 },
    ],
    outputs: [
      { id: "volume", label: "体積", format: "text", primary: true },
      { id: "weight", label: "重量（概算）", format: "text" },
      { id: "bags", label: "25kgセメント袋数（目安）", format: "text" },
    ],
    explanation: "<h3>コンクリートの計算</h3><p>体積 = 長さ × 幅 × 厚さです。コンクリートの比重は約2.3t/m³。セメント1袋(25kg)で約0.012m³のコンクリートが作れます（砂利・砂を混ぜた場合）。</p>",
    faq: [
      { question: "コンクリートとモルタルの違いは？", answer: "コンクリート=セメント+砂+砂利+水、モルタル=セメント+砂+水です。砂利が入るかどうかの違いで、コンクリートの方が強度が高いです。" },
    ],
    related: ["concrete-calculator", "paint-calculator"], popular: false,
  },

  {
    slug: "gas-mileage", category: "life", subcategory: "car",
    title: "実燃費計算", description: "走行距離と給油量から実燃費を計算",
    metaTitle: "実燃費計算ツール｜給油量と走行距離から燃費を計算",
    metaDescription: "走行距離と給油量を入力して実際の燃費(km/L)を計算。カタログ燃費との比較にも。",
    calculatorFunction: "gasMileage",
    inputs: [
      { id: "distance", label: "走行距離", type: "number", unit: "km", default: 500, min: 1, max: 99999, step: 1 },
      { id: "fuel", label: "給油量", type: "number", unit: "L", default: 35, min: 0.1, max: 999, step: 0.1 },
      { id: "fuelPrice", label: "ガソリン単価", type: "number", unit: "円/L", default: 170, min: 100, max: 300, step: 1 },
    ],
    outputs: [
      { id: "fuelEfficiency", label: "実燃費", format: "text", primary: true },
      { id: "costPerKm", label: "1kmあたりのガソリン代", format: "text" },
      { id: "totalCost", label: "ガソリン代合計", format: "currency" },
    ],
    explanation: "<h3>燃費の計算</h3><p>燃費(km/L) = 走行距離 ÷ 給油量です。満タン法で計算する場合は、満タンにした後走行し、次の給油で満タンにした量で計算します。カタログ燃費の60〜80%が実燃費の目安です。</p>",
    faq: [
      { question: "燃費を良くするコツは？", answer: "急発進・急加速を避ける、タイヤの空気圧を適正に保つ、エアコン使用を控えめにする、不要な荷物を降ろす。" },
    ],
    related: ["fuel-cost", "car-cost-total", "ev-charging-cost"], popular: false,
  },

  // More math
  {
    slug: "matrix-determinant", category: "math", subcategory: "basic",
    title: "行列式計算", description: "2×2行列の行列式を計算",
    metaTitle: "行列式計算ツール｜2×2行列のdetを自動計算",
    metaDescription: "2×2行列の要素を入力して行列式（determinant）を計算。逆行列の存在判定にも。",
    calculatorFunction: "matrixDeterminant",
    inputs: [
      { id: "a", label: "a (左上)", type: "number", default: 1, min: -9999, max: 9999, step: 0.01 },
      { id: "b", label: "b (右上)", type: "number", default: 2, min: -9999, max: 9999, step: 0.01 },
      { id: "c", label: "c (左下)", type: "number", default: 3, min: -9999, max: 9999, step: 0.01 },
      { id: "d", label: "d (右下)", type: "number", default: 4, min: -9999, max: 9999, step: 0.01 },
    ],
    outputs: [
      { id: "determinant", label: "行列式 (ad-bc)", format: "number", primary: true },
      { id: "hasInverse", label: "逆行列の存在", format: "text" },
    ],
    explanation: "<h3>2×2行列の行列式</h3><p>行列[[a,b],[c,d]]の行列式 = ad - bc です。行列式が0でなければ逆行列が存在します。</p>",
    faq: [
      { question: "行列式が0だとどうなる？", answer: "逆行列が存在しない（特異行列）ことを意味します。連立方程式が唯一の解を持たないことに対応します。" },
    ],
    related: ["power-calculator"], popular: false,
  },

  // More money
  {
    slug: "atm-fee-calc", category: "money", subcategory: "savings",
    title: "ATM手数料計算", description: "ATM手数料の年間コストを計算",
    metaTitle: "ATM手数料計算ツール｜年間でいくら損しているか計算",
    metaDescription: "ATM利用回数と手数料から年間のATM手数料総額を計算。ネット銀行との比較に。",
    calculatorFunction: "atmFeeCalc",
    inputs: [
      { id: "feePerUse", label: "1回あたり手数料", type: "number", unit: "円", default: 220, min: 0, max: 1000, step: 10 },
      { id: "monthlyUses", label: "月の利用回数", type: "number", unit: "回", default: 4, min: 0, max: 30, step: 1 },
    ],
    outputs: [
      { id: "monthlyFee", label: "月間手数料", format: "currency" },
      { id: "annualFee", label: "年間手数料", format: "currency", primary: true },
      { id: "tenYearFee", label: "10年間の手数料", format: "currency" },
    ],
    explanation: "<h3>ATM手数料の影響</h3><p>1回220円のATM手数料を週1回使うと年間約11,440円です。ネット銀行なら月数回無料のところが多く、手数料を大幅に節約できます。</p>",
    faq: [
      { question: "手数料を避けるには？", answer: "ネット銀行の利用、コンビニATM無料回数の多い口座への切り替え、まとめて引き出すなどが有効です。" },
    ],
    related: ["goal-savings", "emergency-fund"], popular: false,
  },

  // More education
  {
    slug: "kanji-grade", category: "education", subcategory: "school",
    title: "学年別漢字数チェック", description: "各学年で習う漢字数と累計を表示",
    metaTitle: "学年別漢字数チェックツール｜何年生で何字習うか確認",
    metaDescription: "小学校の各学年で習う漢字の数と累計を表示。常用漢字の学年配当を確認できる無料ツール。",
    calculatorFunction: "kanjiGrade",
    inputs: [
      { id: "grade", label: "学年", type: "select", options: [{ value: "1", label: "小学1年" }, { value: "2", label: "小学2年" }, { value: "3", label: "小学3年" }, { value: "4", label: "小学4年" }, { value: "5", label: "小学5年" }, { value: "6", label: "小学6年" }], default: "1" },
    ],
    outputs: [
      { id: "gradeCount", label: "その学年で習う漢字数", format: "text", primary: true },
      { id: "cumulativeCount", label: "累計漢字数", format: "text" },
      { id: "totalKanji", label: "小学校で習う漢字の総数", format: "text" },
    ],
    explanation: "<h3>学年別配当漢字</h3><p>小学校で習う漢字は全1,026字です。1年生80字、2年生160字、3年生200字、4年生202字、5年生193字、6年生191字です。中学校では常用漢字の残り約1,100字を学びます。</p>",
    faq: [
      { question: "常用漢字は全部で何字？", answer: "2,136字です。小学校1,026字＋中学校で約1,110字を学びます。" },
    ],
    related: ["reading-speed"], popular: false,
  },

  // More health
  {
    slug: "alcohol-calorie-drink", category: "health", subcategory: "calorie",
    title: "お酒のカロリー計算", description: "飲酒量からカロリーとアルコール量を計算",
    metaTitle: "お酒のカロリー計算ツール｜飲酒量のカロリーを自動計算",
    metaDescription: "ビール・ワイン・日本酒・焼酎など、お酒の種類と量からカロリーとアルコール摂取量を計算。",
    calculatorFunction: "alcoholCalorieDrink",
    inputs: [
      { id: "drinkType", label: "お酒の種類", type: "select", options: [{ value: "beer", label: "ビール（5%）" }, { value: "wine", label: "ワイン（12%）" }, { value: "sake", label: "日本酒（15%）" }, { value: "shochu", label: "焼酎（25%）" }, { value: "whiskey", label: "ウイスキー（40%）" }, { value: "chuhai", label: "チューハイ（5%）" }], default: "beer" },
      { id: "amount", label: "量", type: "number", unit: "ml", default: 500, min: 10, max: 10000, step: 10 },
    ],
    outputs: [
      { id: "calories", label: "カロリー", format: "text", primary: true },
      { id: "pureAlcohol", label: "純アルコール量", format: "text" },
      { id: "units", label: "ドリンク数（1ドリンク=10g）", format: "text" },
    ],
    explanation: "<h3>お酒のカロリー</h3><p>アルコール1gは約7kcalです。純アルコール量 = 飲酒量(ml) × アルコール度数 × 0.8(比重)。ビール500mlで約200kcal、日本酒1合(180ml)で約190kcalです。</p>",
    faq: [
      { question: "適量の飲酒量は？", answer: "厚生労働省は1日の純アルコール摂取量20g以下を推奨しています。ビールなら500ml、日本酒なら1合が目安です。" },
    ],
    related: ["alcohol-calorie", "alcohol-breakdown", "blood-alcohol"], popular: false,
  },

  // A few more to hit the target
  {
    slug: "moving-cost-estimate", category: "life", subcategory: "shopping",
    title: "引越し費用概算", description: "距離と荷物量から引越し費用を概算",
    metaTitle: "引越し費用概算ツール｜引越し料金の相場を計算",
    metaDescription: "距離・荷物量・時期から引越し費用の相場を概算。単身・家族別の料金目安を表示。",
    calculatorFunction: "movingCostEstimate",
    inputs: [
      { id: "type", label: "引越しタイプ", type: "select", options: [{ value: "single", label: "単身（荷物少なめ）" }, { value: "singleLarge", label: "単身（荷物多め）" }, { value: "family2", label: "2人家族" }, { value: "family3", label: "3人以上家族" }], default: "single" },
      { id: "distance", label: "距離", type: "select", options: [{ value: "local", label: "同市内（〜20km）" }, { value: "prefecture", label: "同県内（〜50km）" }, { value: "regional", label: "近距離（〜200km）" }, { value: "long", label: "長距離（200km〜）" }], default: "local" },
      { id: "season", label: "時期", type: "select", options: [{ value: "peak", label: "繁忙期（3-4月）" }, { value: "normal", label: "通常期" }], default: "normal" },
    ],
    outputs: [
      { id: "estimatedCost", label: "概算費用", format: "text", primary: true },
      { id: "range", label: "料金レンジ", format: "text" },
    ],
    explanation: "<h3>引越し費用の相場</h3><p>単身同市内で3〜5万円、家族の長距離で15〜30万円が目安です。3〜4月の繁忙期は通常期の1.3〜2倍になります。平日やフリー便を選ぶと安くなります。</p>",
    faq: [
      { question: "引越しを安くするコツは？", answer: "複数社の見積もり比較、平日・午後便の選択、荷物の事前処分、繁忙期を避けるなどが効果的です。" },
    ],
    related: ["moving-estimate", "packing-list"], popular: false,
  },

  {
    slug: "nengajo-cost", category: "life", subcategory: "shopping",
    title: "年賀状費用計算", description: "年賀状の枚数から費用を計算",
    metaTitle: "年賀状費用計算ツール｜枚数から印刷・郵送コストを計算",
    metaDescription: "年賀状の枚数から郵便代・印刷代の総費用を計算。自宅印刷とネット注文の比較も。",
    calculatorFunction: "nengajoCost",
    inputs: [
      { id: "sheets", label: "枚数", type: "number", unit: "枚", default: 50, min: 1, max: 1000, step: 1 },
      { id: "printType", label: "印刷方法", type: "select", options: [{ value: "home", label: "自宅プリンター" }, { value: "order", label: "ネット注文" }], default: "home" },
    ],
    outputs: [
      { id: "postageCost", label: "はがき代", format: "currency" },
      { id: "printCost", label: "印刷代（概算）", format: "currency" },
      { id: "totalCost", label: "合計費用", format: "currency", primary: true },
    ],
    explanation: "<h3>年賀状の費用</h3><p>2024年は年賀はがき1枚63円→85円に値上げ予定です。自宅印刷はインク代＋用紙代で1枚約20〜30円、ネット注文は1枚約30〜60円（枚数により変動）が目安です。</p>",
    faq: [
      { question: "年賀状の発行枚数は？", answer: "2024年度は約14.4億枚で、ピーク時（2003年度 約44億枚）から大幅に減少しています。" },
    ],
    related: ["postal-rate"], popular: false,
  },

  {
    slug: "wedding-budget", category: "life", subcategory: "shopping",
    title: "結婚式費用計算", description: "ゲスト人数から結婚式の費用と自己負担額を計算",
    metaTitle: "結婚式費用計算ツール｜ゲスト人数から費用を概算",
    metaDescription: "ゲスト人数からご祝儀収入を差し引いた結婚式の自己負担額を計算。予算計画に便利な無料ツール。",
    calculatorFunction: "weddingBudget",
    inputs: [
      { id: "guests", label: "ゲスト人数", type: "number", unit: "人", default: 60, min: 10, max: 300, step: 1 },
      { id: "venueGrade", label: "会場グレード", type: "select", options: [{ value: "standard", label: "スタンダード" }, { value: "premium", label: "プレミアム" }, { value: "luxury", label: "ラグジュアリー" }], default: "standard" },
    ],
    outputs: [
      { id: "totalCost", label: "総費用（概算）", format: "text", primary: true },
      { id: "giftMoney", label: "ご祝儀予想合計", format: "text" },
      { id: "selfPayment", label: "自己負担額", format: "text" },
      { id: "perGuest", label: "1人あたり費用", format: "text" },
    ],
    explanation: "<h3>結婚式の費用相場</h3><p>ゲスト1人あたり3〜6万円が相場です。60名のスタンダードな結婚式で約300万円、ご祝儀が約200万円で自己負担約100万円が目安です。</p>",
    faq: [
      { question: "ご祝儀の相場は？", answer: "友人3万円、親族5〜10万円、上司3〜5万円が一般的です。平均すると1人約3.3万円です。" },
    ],
    related: ["split-bill"], popular: false,
  },

  {
    slug: "childbirth-cost", category: "health", subcategory: "pregnancy",
    title: "出産費用計算", description: "出産にかかる費用と公的補助を計算",
    metaTitle: "出産費用計算ツール｜自己負担額を自動計算",
    metaDescription: "出産にかかる費用と出産育児一時金を差し引いた自己負担額を計算。帝王切開の場合も対応。",
    calculatorFunction: "childbirthCost",
    inputs: [
      { id: "deliveryType", label: "出産方法", type: "select", options: [{ value: "normal", label: "自然分娩" }, { value: "caesarean", label: "帝王切開" }], default: "normal" },
      { id: "facility", label: "施設タイプ", type: "select", options: [{ value: "clinic", label: "診療所" }, { value: "hospital", label: "総合病院" }, { value: "university", label: "大学病院" }], default: "clinic" },
    ],
    outputs: [
      { id: "estimatedCost", label: "出産費用（概算）", format: "text", primary: true },
      { id: "subsidy", label: "出産育児一時金", format: "text" },
      { id: "selfPayment", label: "自己負担額（概算）", format: "text" },
    ],
    explanation: "<h3>出産にかかる費用</h3><p>自然分娩で約40〜60万円、帝王切開で約50〜70万円が相場です。出産育児一時金50万円が支給されるため、自己負担は0〜20万円程度です。帝王切開は医療保険の対象で高額療養費制度も使えます。</p>",
    faq: [
      { question: "無痛分娩の追加費用は？", answer: "施設により異なりますが、約10〜20万円の追加費用がかかります。保険適用外です。" },
    ],
    related: ["due-date", "pregnancy-week", "weight-gain-pregnancy"], popular: false,
  },

  // Fill remaining with more useful calculators
  {
    slug: "smartphone-cost", category: "life", subcategory: "shopping",
    title: "スマホ料金計算", description: "月額料金と端末代の総コストを計算",
    metaTitle: "スマホ料金計算ツール｜2年間の総コストを計算",
    metaDescription: "月額基本料・データ量・端末代の分割払いを含めたスマホの2年間総コストを自動計算。",
    calculatorFunction: "smartphoneCost",
    inputs: [
      { id: "monthlyPlan", label: "月額料金", type: "number", unit: "円", default: 3000, min: 0, max: 50000, step: 100 },
      { id: "devicePrice", label: "端末価格", type: "number", unit: "円", default: 100000, min: 0, max: 500000, step: 1000 },
      { id: "months", label: "利用期間", type: "number", unit: "ヶ月", default: 24, min: 1, max: 60, step: 1 },
    ],
    outputs: [
      { id: "monthlyTotal", label: "月々の支払い合計", format: "currency" },
      { id: "totalCost", label: "総コスト", format: "currency", primary: true },
      { id: "dailyCost", label: "1日あたりコスト", format: "text" },
    ],
    explanation: "<h3>スマホの総コスト</h3><p>月額料金 × 月数 + 端末価格 = 総コストです。格安SIMに乗り換えると月額1,000〜3,000円程度に抑えられ、大手キャリアの半額以下になることも。</p>",
    faq: [
      { question: "格安SIMは本当に安い？", answer: "データ3GBプランなら月額1,000円前後で使えます。大手キャリアの3〜7,000円と比べて大幅に節約可能です。" },
    ],
    related: ["subscription-cost"], popular: false,
  },

  {
    slug: "pet-age-general", category: "life", subcategory: "date",
    title: "ペット年齢計算", description: "犬・猫の年齢を人間の年齢に換算",
    metaTitle: "ペット年齢計算ツール｜犬・猫の年齢を人間換算",
    metaDescription: "犬・猫の年齢を人間の年齢に換算。犬は体格別（小型・中型・大型）の計算に対応。",
    calculatorFunction: "petAgeGeneral",
    inputs: [
      { id: "petType", label: "種類", type: "select", options: [{ value: "dogSmall", label: "犬（小型）" }, { value: "dogMedium", label: "犬（中型）" }, { value: "dogLarge", label: "犬（大型）" }, { value: "cat", label: "猫" }], default: "cat" },
      { id: "age", label: "ペットの年齢", type: "number", unit: "歳", default: 5, min: 0.1, max: 25, step: 0.1 },
    ],
    outputs: [
      { id: "humanAge", label: "人間換算年齢", format: "text", primary: true },
      { id: "lifeStage", label: "ライフステージ", format: "text" },
    ],
    explanation: "<h3>ペットの年齢換算</h3><p>犬・猫とも最初の1年で人間の15〜18歳相当に成長し、2年目でさらに6〜9歳分加算。3年目以降は1年につき4〜7歳ずつ加算します。大型犬は小型犬より老化が早い傾向があります。</p>",
    faq: [
      { question: "犬の7歳は人間の何歳？", answer: "小型犬で約44歳、大型犬で約54歳が目安です。" },
    ],
    related: ["cat-age", "dog-age", "pet-age"], popular: false,
  },

  {
    slug: "cloud-storage-cost", category: "life", subcategory: "utility",
    title: "クラウドストレージ料金比較", description: "必要容量から各サービスの月額料金を比較",
    metaTitle: "クラウドストレージ料金比較ツール｜容量別コスト計算",
    metaDescription: "Google Drive・iCloud・OneDrive・Dropboxの容量別料金を比較。最もコスパの良いサービスを見つける。",
    calculatorFunction: "cloudStorageCost",
    inputs: [
      { id: "storageGB", label: "必要容量", type: "number", unit: "GB", default: 200, min: 1, max: 30000, step: 1 },
    ],
    outputs: [
      { id: "googleDrive", label: "Google One", format: "text", primary: true },
      { id: "icloud", label: "iCloud+", format: "text" },
      { id: "onedrive", label: "OneDrive", format: "text" },
      { id: "dropbox", label: "Dropbox", format: "text" },
    ],
    explanation: "<h3>クラウドストレージの料金</h3><p>各サービスの無料容量：Google Drive 15GB、iCloud 5GB、OneDrive 5GB、Dropbox 2GB。有料プランは100GB〜2TB程度で月額200〜1,500円が相場です。</p>",
    faq: [
      { question: "どのサービスがおすすめ？", answer: "AndroidユーザーはGoogle One、iPhoneユーザーはiCloud+、Office利用者はOneDrive(Microsoft 365)がコスパ良好です。" },
    ],
    related: ["data-size", "subscription-cost"], popular: false,
  },

  {
    slug: "taxi-fare", category: "life", subcategory: "car",
    title: "タクシー料金計算", description: "距離からタクシー料金の目安を計算",
    metaTitle: "タクシー料金計算ツール｜距離から料金を概算",
    metaDescription: "走行距離からタクシーの概算料金を計算。初乗り料金・加算料金・深夜割増に対応した無料ツール。",
    calculatorFunction: "taxiFare",
    inputs: [
      { id: "distance", label: "走行距離", type: "number", unit: "km", default: 5, min: 0.1, max: 100, step: 0.1 },
      { id: "isNight", label: "深夜早朝（22-5時）", type: "select", options: [{ value: "no", label: "通常" }, { value: "yes", label: "深夜割増" }], default: "no" },
    ],
    outputs: [
      { id: "estimatedFare", label: "概算料金", format: "currency", primary: true },
      { id: "nightSurcharge", label: "深夜割増額", format: "text" },
    ],
    explanation: "<h3>タクシー料金の計算</h3><p>東京23区の場合、初乗り500円（1.096km）、以後255mごとに100円加算が基本です。深夜早朝（22:00〜5:00）は2割増になります。渋滞時の時間加算もあるため、実際の料金は概算より高くなることがあります。</p>",
    faq: [
      { question: "タクシーアプリで安くなる？", answer: "アプリクーポンで割引されることがあります。また、相乗りサービスを使えば料金を分担できます。" },
    ],
    related: ["commute-cost", "fuel-cost"], popular: false,
  },

  // Last few to push past 450
  {
    slug: "inflation-impact", category: "money", subcategory: "savings",
    title: "インフレ影響計算", description: "インフレ率から将来のお金の実質価値を計算",
    metaTitle: "インフレ影響計算ツール｜お金の実質価値の目減りを計算",
    metaDescription: "インフレ率と年数から現在のお金が将来どのくらい目減りするか計算。資産防衛の参考に。",
    calculatorFunction: "inflationImpact",
    inputs: [
      { id: "amount", label: "現在の金額", type: "number", unit: "万円", default: 1000, min: 1, max: 999999, step: 1 },
      { id: "inflationRate", label: "年間インフレ率", type: "number", unit: "%", default: 2, min: 0.1, max: 20, step: 0.1 },
      { id: "years", label: "年数", type: "number", unit: "年", default: 20, min: 1, max: 50, step: 1 },
    ],
    outputs: [
      { id: "realValue", label: "実質的な価値", format: "text", primary: true },
      { id: "purchasingPowerLoss", label: "購買力の低下", format: "text" },
    ],
    explanation: "<h3>インフレの影響</h3><p>年2%のインフレが20年続くと、1,000万円の実質価値は約672万円に目減りします。銀行預金の金利がインフレ率を下回ると、実質的にお金は減っていることになります。</p>",
    faq: [
      { question: "インフレ対策は？", answer: "株式・不動産・金などインフレに強い資産への投資が基本です。現金のみの保有はインフレで目減りします。" },
    ],
    related: ["inflation-calculator", "compound-interest", "rule-72"], popular: false,
  },

  {
    slug: "rain-probability", category: "life", subcategory: "utility",
    title: "降水確率と傘の判断", description: "降水確率から傘を持つべきかを判定",
    metaTitle: "降水確率と傘の判断ツール｜傘を持つべきか計算",
    metaDescription: "降水確率から傘を持って行くべきか判定。期待値計算で合理的な判断をサポート。",
    calculatorFunction: "rainProbability",
    inputs: [
      { id: "probability", label: "降水確率", type: "number", unit: "%", default: 40, min: 0, max: 100, step: 10 },
      { id: "outing", label: "外出時間", type: "select", options: [{ value: "short", label: "短時間（1時間以内）" }, { value: "medium", label: "半日程度" }, { value: "long", label: "終日" }], default: "medium" },
    ],
    outputs: [
      { id: "recommendation", label: "判定", format: "text", primary: true },
      { id: "reason", label: "理由", format: "text" },
    ],
    explanation: "<h3>降水確率の意味</h3><p>降水確率40%は「同じ条件の日を10回経験すると4回は1mm以上の雨が降る」という意味です。傘を持つかどうかの分岐点は一般的に30〜40%とされています。</p>",
    faq: [
      { question: "降水確率30%は傘いる？", answer: "短時間の外出なら不要ですが、終日外出なら折りたたみ傘を推奨します。30%でも3回に1回は降ります。" },
    ],
    related: [], popular: false,
  },

  {
    slug: "screen-size-compare", category: "life", subcategory: "utility",
    title: "画面サイズ比較", description: "インチ数から画面の実際の寸法を計算",
    metaTitle: "画面サイズ比較ツール｜インチから実寸を計算",
    metaDescription: "画面のインチ数とアスペクト比から実際の幅・高さ・面積を計算。テレビ・モニターの比較に。",
    calculatorFunction: "screenSizeCompare",
    inputs: [
      { id: "diagonal", label: "画面サイズ", type: "number", unit: "インチ", default: 55, min: 1, max: 200, step: 0.1 },
      { id: "aspectRatio", label: "アスペクト比", type: "select", options: [{ value: "16:9", label: "16:9（TV・一般モニター）" }, { value: "21:9", label: "21:9（ウルトラワイド）" }, { value: "4:3", label: "4:3（旧型）" }, { value: "16:10", label: "16:10（MacBook等）" }], default: "16:9" },
    ],
    outputs: [
      { id: "widthCm", label: "幅", format: "text", primary: true },
      { id: "heightCm", label: "高さ", format: "text" },
      { id: "areaCm2", label: "面積", format: "text" },
    ],
    explanation: "<h3>画面サイズの計算</h3><p>インチは対角線の長さです。16:9の55インチTVは幅約121.7cm×高さ約68.5cmです。面積を比較すると、55インチは40インチの約1.9倍の表示面積があります。</p>",
    faq: [
      { question: "テレビの適切なサイズは？", answer: "視聴距離の1/3がインチ数の目安です。2mの距離なら55インチ、3mなら65インチがおすすめです。" },
    ],
    related: ["cm-to-inch"], popular: false,
  },
];

// Create JSON files
let createdCount = 0;
for (const calc of newCalculators) {
  const dir = path.join(DATA_DIR, calc.category, calc.subcategory);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  const filePath = path.join(dir, `${calc.slug}.json`);
  if (fs.existsSync(filePath)) {
    console.log(`SKIP (exists): ${calc.slug}`);
    continue;
  }
  fs.writeFileSync(filePath, JSON.stringify(calc, null, 2) + '\n');
  createdCount++;
  console.log(`CREATED: ${calc.slug}`);
}
console.log(`\nTotal created: ${createdCount} JSON files`);
