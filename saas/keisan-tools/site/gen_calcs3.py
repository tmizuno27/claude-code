#!/usr/bin/env python3
"""Batch 3: Generate 35 more calculator JSON files to reach 300+."""
import json, os

BASE = os.path.join(os.path.dirname(__file__), "data", "calculators")

def c(slug, cat, sub, title, desc, mt, md, fn, inputs, outputs, explanation, faq, related=[], popular=False, **kw):
    d = os.path.join(BASE, cat, sub)
    os.makedirs(d, exist_ok=True)
    fp = os.path.join(d, f"{slug}.json")
    if os.path.exists(fp):
        return 0
    obj = {"slug":slug,"category":cat,"subcategory":sub,"title":title,"description":desc,
           "metaTitle":mt,"metaDescription":md,"calculatorFunction":fn,
           "inputs":inputs,"outputs":outputs,"explanation":explanation,"faq":faq,
           "related":related,"popular":popular}
    if "popularOrder" in kw: obj["popularOrder"] = kw["popularOrder"]
    with open(fp,"w",encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return 1

def ni(id,label,unit="",default=0,mn=0,mx=999999,step=1,**kw):
    r = {"id":id,"label":label,"type":"number","default":default,"min":mn,"max":mx,"step":step}
    if unit: r["unit"] = unit
    if "hint" in kw: r["hint"] = kw["hint"]
    return r

def si(id,label,options):
    return {"id":id,"label":label,"type":"select","options":options}

def o(id,label,fmt="number",primary=False):
    r = {"id":id,"label":label,"format":fmt}
    if primary: r["primary"] = True
    return r

count = 0

# --- money/tax ---
count += c("gift-tax","money","tax","贈与税計算","贈与額から贈与税を計算します",
    "贈与税計算ツール｜keisan.tools","贈与額を入力して贈与税額を自動計算。暦年課税・特例税率対応。","giftTax",
    [ni("amount","贈与額","万円",500,0,100000,10),si("relationship","贈与者との関係",[{"value":"general","label":"一般"},{"value":"lineal","label":"直系尊属（20歳以上）"}])],
    [o("tax","贈与税額","currency",True),o("effectiveRate","実効税率","percent"),o("afterDeduction","基礎控除後の課税価格","currency")],
    "<h3>贈与税の計算</h3><p>年間110万円の基礎控除を超える贈与に対して課税されます。直系尊属からの贈与は特例税率が適用されます。</p>",
    [{"question":"贈与税の基礎控除はいくら？","answer":"年間110万円です。"},{"question":"親から子への贈与は税率が低い？","answer":"20歳以上の子が直系尊属から受ける贈与は特例税率が適用され、一般税率より低くなります。"}])

count += c("fixed-asset-tax","money","tax","固定資産税計算","固定資産の評価額から固定資産税を計算します",
    "固定資産税計算ツール｜keisan.tools","固定資産の評価額を入力して固定資産税額を自動計算。住宅用地特例対応。","fixedAssetTax",
    [ni("assessment","固定資産評価額","万円",2000,0,100000,10),si("landType","土地の種類",[{"value":"residential_small","label":"小規模住宅用地（200㎡以下）"},{"value":"residential_general","label":"一般住宅用地"},{"value":"non_residential","label":"非住宅用地"}])],
    [o("tax","固定資産税額","currency",True),o("cityPlanningTax","都市計画税","currency"),o("total","合計年額","currency")],
    "<h3>固定資産税の計算</h3><p>固定資産税は評価額×1.4%が標準税率です。住宅用地には軽減特例があります。</p>",
    [{"question":"固定資産税の税率は？","answer":"標準税率は1.4%です。都市計画税は0.3%が上限です。"},{"question":"住宅用地の特例とは？","answer":"小規模住宅用地（200㎡以下）は評価額が1/6に、一般住宅用地は1/3に軽減されます。"}])

count += c("consumption-tax-calc","money","tax","消費税計算","税抜価格と税込価格を相互変換します",
    "消費税計算ツール｜税込・税抜変換","税抜価格または税込価格を入力して消費税額を自動計算。軽減税率8%にも対応。","consumptionTaxCalc",
    [ni("price","金額","円",1000,0,999999999,1),si("direction","変換方向",[{"value":"excl_to_incl","label":"税抜→税込"},{"value":"incl_to_excl","label":"税込→税抜"}]),si("rate","税率",[{"value":"10","label":"10%（標準）"},{"value":"8","label":"8%（軽減税率）"}])],
    [o("result","変換後金額","currency",True),o("taxAmount","消費税額","currency")],
    "<h3>消費税の計算</h3><p>標準税率10%と軽減税率8%（食料品等）に対応しています。</p>",
    [{"question":"軽減税率の対象は？","answer":"飲食料品（酒類・外食除く）と新聞（定期購読）が対象です。"},{"question":"消費税の内税計算は？","answer":"税込価格÷1.1（10%の場合）で税抜価格が求められます。"}])

# --- money/salary ---
count += c("hourly-wage","money","salary","時給換算計算","月給・年収から時給を計算します",
    "時給換算ツール｜月給から時給を自動計算","月給や年収を入力して時給に換算。残業代の基礎単価確認にも。","hourlyWage",
    [ni("monthlySalary","月給","万円",25,0,1000,1),ni("workDays","月の勤務日数","日",20,1,31,1),ni("workHours","1日の労働時間","時間",8,1,24,0.5)],
    [o("hourlyWage","時給","currency",True),o("annualSalary","年収換算","currency"),o("dailyWage","日給","currency")],
    "<h3>時給換算の計算</h3><p>月給を月の勤務日数と1日の労働時間で割って時給を算出します。</p>",
    [{"question":"残業代の計算に使える？","answer":"はい。時給を基礎に、残業は25%増し、深夜は50%増しで計算できます。"},{"question":"パートと正社員の比較は？","answer":"正社員の月給を時給換算すると、福利厚生を含めた実質比較ができます。"}])

count += c("overtime-pay","money","salary","残業代計算","残業時間から残業代を計算します",
    "残業代計算ツール｜keisan.tools","月給と残業時間を入力して残業代を自動計算。深夜・休日割増にも対応。","overtimePay",
    [ni("monthlySalary","月給","万円",25,0,1000,1),ni("monthlyHours","月所定労働時間","時間",160,100,200,1),ni("overtimeHours","残業時間","時間",20,0,200,1),si("type","残業の種類",[{"value":"normal","label":"通常残業（25%増）"},{"value":"night","label":"深夜残業（50%増）"},{"value":"holiday","label":"休日残業（35%増）"}])],
    [o("overtimePay","残業代","currency",True),o("baseHourly","基礎時給","currency"),o("totalSalary","残業込み月給","currency")],
    "<h3>残業代の計算</h3><p>基礎時給に割増率を掛けて残業代を算出します。</p>",
    [{"question":"残業の割増率は？","answer":"通常残業25%、深夜残業50%、休日残業35%、休日深夜60%です。"},{"question":"基礎時給の計算方法は？","answer":"月給÷月所定労働時間で算出します。"}])

# --- money/savings ---
count += c("compound-interest-detail","money","savings","複利計算（詳細版）","元本・利率・期間から複利の将来価値を計算",
    "複利計算ツール｜keisan.tools","元本と利率・期間を入力して複利の将来価値を自動計算。毎月積立にも対応。","compoundInterestDetail",
    [ni("principal","元本","万円",100,0,100000,10),ni("rate","年利率","%",3,0,100,0.1),ni("years","運用期間","年",10,1,50,1),ni("monthly","毎月積立額","万円",0,0,1000,1)],
    [o("futureValue","将来価値","currency",True),o("totalDeposit","元本+積立合計","currency"),o("interest","利益額","currency"),o("returnRate","収益率","percent")],
    "<h3>複利計算</h3><p>元本に利息が加算され、翌年はその合計に利息がつく仕組みです。</p>",
    [{"question":"単利と複利の違いは？","answer":"単利は元本のみに利息がつき、複利は元本+利息に利息がつきます。長期では大きな差になります。"},{"question":"72の法則とは？","answer":"72÷金利≒資産が倍になる年数の目安です。"}])

count += c("inflation-calculator","money","savings","インフレ計算","インフレ率を考慮した将来の実質価値を計算",
    "インフレ計算ツール｜将来の実質価値を自動計算","現在の金額とインフレ率から将来の実質価値を計算。老後資金計画に。","inflationCalculator",
    [ni("amount","現在の金額","万円",1000,0,100000,10),ni("inflationRate","年間インフレ率","%",2,0,20,0.1),ni("years","年数","年",20,1,50,1)],
    [o("futureNominal","将来の名目価値","currency",True),o("realValue","実質価値（購買力）","currency"),o("purchasingPowerLoss","購買力の低下率","percent")],
    "<h3>インフレの影響</h3><p>インフレにより同じ金額でも将来の購買力は低下します。</p>",
    [{"question":"日本のインフレ率は？","answer":"2024-2025年は約2-3%で推移しています。"},{"question":"老後資金にどう影響？","answer":"年2%のインフレで20年後の100万円の購買力は約67万円になります。"}])

# --- money/investment ---
count += c("dividend-yield","money","investment","配当利回り計算","株価と配当金から配当利回りを計算",
    "配当利回り計算ツール｜keisan.tools","株価と1株配当を入力して配当利回りを自動計算。","dividendYield",
    [ni("stockPrice","株価","円",2000,1,9999999,1),ni("dividend","1株あたり年間配当","円",50,0,99999,1),ni("shares","保有株数","株",100,1,999999,1)],
    [o("yield","配当利回り","percent",True),o("annualDividend","年間配当金額","currency"),o("monthlyDividend","月換算配当","currency")],
    "<h3>配当利回り</h3><p>配当利回り＝1株配当÷株価×100で計算します。</p>",
    [{"question":"高配当の目安は？","answer":"一般的に3%以上が高配当とされます。"},{"question":"配当金の税金は？","answer":"約20.315%（所得税15.315%+住民税5%）が源泉徴収されます。"}])

count += c("dollar-cost-averaging","money","investment","ドルコスト平均法シミュレーション","定額積立投資の効果をシミュレーション",
    "ドルコスト平均法シミュレーター｜keisan.tools","毎月の積立額と期間からドルコスト平均法の効果を計算。","dollarCostAveraging",
    [ni("monthlyAmount","毎月積立額","万円",3,0,100,1),ni("years","積立期間","年",20,1,40,1),ni("expectedReturn","想定年利回り","%",5,0,30,0.5)],
    [o("totalInvested","積立総額","currency",True),o("futureValue","将来の評価額","currency"),o("profit","運用益","currency"),o("profitRate","収益率","percent")],
    "<h3>ドルコスト平均法</h3><p>毎月一定額を投資することで、購入価格を平準化する手法です。</p>",
    [{"question":"一括投資とどちらが有利？","answer":"相場が右肩上がりなら一括投資、変動が大きい場合はドルコスト平均法が有利な傾向です。"},{"question":"新NISAとの相性は？","answer":"新NISAのつみたて投資枠はドルコスト平均法と相性が良いです。"}])

# --- money/loan ---
count += c("education-loan","money","loan","教育ローン計算","教育ローンの返済額を計算します",
    "教育ローン返済シミュレーション｜keisan.tools","借入額と金利から教育ローンの月々の返済額を計算。","educationLoan",
    [ni("amount","借入額","万円",300,0,5000,10),ni("rate","年利率","%",2,0,15,0.1),ni("years","返済期間","年",15,1,30,1)],
    [o("monthlyPayment","月々の返済額","currency",True),o("totalPayment","返済総額","currency"),o("totalInterest","利息総額","currency")],
    "<h3>教育ローン</h3><p>国の教育ローンは固定金利で最大350万円まで借入可能です。</p>",
    [{"question":"国の教育ローンの金利は？","answer":"2026年現在、年2.25%前後（固定金利）です。"},{"question":"奨学金との違いは？","answer":"教育ローンは保護者が借りる、奨学金は学生本人が借りるのが主な違いです。"}])

# --- health/body ---
count += c("body-fat-percentage","health","body","体脂肪率計算","身長・体重・年齢から体脂肪率を推定",
    "体脂肪率計算ツール｜keisan.tools","身長・体重・年齢から体脂肪率を推定計算。BMIベースの推定式。","bodyFatPercentage",
    [ni("height","身長","cm",170,100,250,0.1),ni("weight","体重","kg",65,20,300,0.1),ni("age","年齢","歳",30,10,100,1),si("gender","性別",[{"value":"male","label":"男性"},{"value":"female","label":"女性"}])],
    [o("bodyFat","推定体脂肪率","percent",True),o("bmi","BMI","number"),o("category","判定","text")],
    "<h3>体脂肪率の推定</h3><p>BMIと年齢・性別から体脂肪率を推定します。正確な値は体組成計で測定してください。</p>",
    [{"question":"理想的な体脂肪率は？","answer":"男性10-20%、女性20-30%が標準的な範囲です。"},{"question":"BMIと体脂肪率の関係は？","answer":"BMIが高くても筋肉量が多ければ体脂肪率は低い場合があります。"}])

count += c("ideal-weight","health","body","適正体重計算","身長から適正体重・美容体重を計算",
    "適正体重計算ツール｜BMI別の理想体重","身長を入力してBMI22の適正体重、BMI20の美容体重を自動計算。","idealWeight",
    [ni("height","身長","cm",165,100,250,0.1)],
    [o("standardWeight","適正体重（BMI22）","number",True),o("beautyWeight","美容体重（BMI20）","number"),o("modelWeight","モデル体重（BMI18）","number"),o("obeseWeight","肥満基準（BMI25）","number")],
    "<h3>各種理想体重</h3><p>BMIの値別に目標体重を算出します。BMI22が最も病気になりにくいとされます。</p>",
    [{"question":"適正体重とは？","answer":"BMI22の体重で、最も病気のリスクが低いとされる体重です。"},{"question":"美容体重とは？","answer":"BMI20の体重で、見た目がスリムに見える体重の目安です。"}])

count += c("basal-metabolism","health","body","基礎代謝計算","年齢・体重・身長から基礎代謝量を計算",
    "基礎代謝計算ツール｜keisan.tools","年齢・身長・体重から基礎代謝量を計算。ハリス・ベネディクト方程式。","basalMetabolism",
    [ni("height","身長","cm",170,100,250,0.1),ni("weight","体重","kg",65,20,300,0.1),ni("age","年齢","歳",30,10,100,1),si("gender","性別",[{"value":"male","label":"男性"},{"value":"female","label":"女性"}])],
    [o("bmr","基礎代謝量","number",True),o("sedentary","活動量少（×1.2）","number"),o("moderate","活動量普通（×1.55）","number"),o("active","活動量多（×1.725）","number")],
    "<h3>基礎代謝</h3><p>ハリス・ベネディクト方程式で基礎代謝量を計算し、活動係数を掛けて1日の消費カロリーを算出します。</p>",
    [{"question":"基礎代謝とは？","answer":"生命維持に必要な最低限のエネルギー消費量です。"},{"question":"基礎代謝を上げるには？","answer":"筋肉量を増やすことが最も効果的です。"}])

# --- health/calorie ---
count += c("walking-calorie","health","calorie","ウォーキング消費カロリー計算","歩行時間・体重から消費カロリーを計算",
    "ウォーキング消費カロリー計算｜keisan.tools","体重と歩行時間を入力してウォーキングの消費カロリーを自動計算。","walkingCalorie",
    [ni("weight","体重","kg",65,20,200,0.1),ni("minutes","歩行時間","分",30,1,600,1),si("speed","歩行速度",[{"value":"slow","label":"ゆっくり（3km/h）"},{"value":"normal","label":"普通（4km/h）"},{"value":"fast","label":"速歩き（6km/h）"}])],
    [o("calories","消費カロリー","number",True),o("distance","歩行距離","number"),o("steps","推定歩数","number")],
    "<h3>ウォーキングの消費カロリー</h3><p>METsを使用して消費カロリーを計算します。</p>",
    [{"question":"1万歩で何kcal消費？","answer":"体重60kgの人で約300-400kcalが目安です。"},{"question":"ダイエットに効果的な歩き方は？","answer":"速歩き（6km/h以上）で20分以上が脂肪燃焼に効果的です。"}])

count += c("exercise-calorie","health","calorie","運動消費カロリー計算","各種運動の消費カロリーを計算",
    "運動消費カロリー計算ツール｜keisan.tools","運動の種類と時間を入力して消費カロリーを自動計算。","exerciseCalorie",
    [ni("weight","体重","kg",65,20,200,0.1),ni("minutes","運動時間","分",30,1,600,1),si("exercise","運動の種類",[{"value":"jogging","label":"ジョギング（7METs）"},{"value":"cycling","label":"サイクリング（6METs）"},{"value":"swimming","label":"水泳（8METs）"},{"value":"yoga","label":"ヨガ（3METs）"},{"value":"tennis","label":"テニス（7METs）"},{"value":"dancing","label":"ダンス（5METs）"}])],
    [o("calories","消費カロリー","number",True),o("fatBurn","脂肪燃焼量","number")],
    "<h3>運動の消費カロリー</h3><p>METs（運動強度）×体重×時間で消費カロリーを算出します。</p>",
    [{"question":"METsとは？","answer":"安静時を1とした運動強度の指標です。ジョギングは約7METsです。"},{"question":"1kg痩せるには？","answer":"体脂肪1kgは約7,200kcalに相当します。"}])

# --- life/date ---
count += c("countdown","life","date","カウントダウン計算","目標日までの残り日数を計算",
    "カウントダウン計算ツール｜keisan.tools","目標日を入力して残り日数・週数・月数を自動計算。","countdown",
    [ni("targetYear","目標年","年",2027,2026,2100,1),ni("targetMonth","目標月","月",1,1,12,1),ni("targetDay","目標日","日",1,1,31,1)],
    [o("days","残り日数","number",True),o("weeks","残り週数","number"),o("hours","残り時間","number")],
    "<h3>カウントダウン</h3><p>今日から目標日までの残り日数を計算します。</p>",
    [{"question":"過去の日付も計算できる？","answer":"はい。過去の日付の場合は経過日数として表示されます。"},{"question":"営業日で計算できる？","answer":"このツールは暦日で計算します。営業日計算は営業日計算ツールをご利用ください。"}])

count += c("age-calculator","life","date","年齢計算","生年月日から現在の年齢を正確に計算",
    "年齢計算ツール｜生年月日から年齢を自動計算","生年月日を入力して現在の年齢（年・月・日）を正確に計算。","ageCalculator",
    [ni("birthYear","生まれ年","年",1990,1900,2026,1),ni("birthMonth","生まれ月","月",1,1,12,1),ni("birthDay","生まれ日","日",1,1,31,1)],
    [o("age","年齢","number",True),o("months","月齢","number"),o("days","生まれてからの日数","number"),o("nextBirthday","次の誕生日まで","number")],
    "<h3>年齢計算</h3><p>生年月日から現在の正確な年齢を計算します。</p>",
    [{"question":"満年齢と数え年の違いは？","answer":"満年齢は生まれた日を0歳、数え年は生まれた日を1歳として計算します。"},{"question":"日本の年齢計算は？","answer":"日本では法律上、誕生日の前日に年齢が加算されます。"}])

# --- life/unit ---
count += c("speed-convert","life","unit","速度変換","km/h・m/s・マイル/h・ノットを相互変換",
    "速度変換ツール｜keisan.tools","各種速度単位（km/h、m/s、マイル/h、ノット）を相互変換。","speedConvert",
    [ni("value","数値","",100,0,999999,0.1),si("fromUnit","変換元",[{"value":"kmh","label":"km/h"},{"value":"ms","label":"m/s"},{"value":"mph","label":"マイル/h"},{"value":"knot","label":"ノット"}])],
    [o("kmh","km/h","number",True),o("ms","m/s","number"),o("mph","マイル/h","number"),o("knot","ノット","number")],
    "<h3>速度の変換</h3><p>1 km/h = 0.2778 m/s = 0.6214 マイル/h = 0.5400 ノット</p>",
    [{"question":"マッハとは？","answer":"音速（約1,225 km/h）を基準とした速度の単位です。"},{"question":"ノットはどこで使う？","answer":"航空・海上で使われる速度単位で、1ノット=1.852 km/hです。"}])

count += c("data-size-convert","life","unit","データ容量変換","B・KB・MB・GB・TBを相互変換",
    "データ容量変換ツール｜keisan.tools","バイト・キロバイト・メガバイト・ギガバイト・テラバイトを相互変換。","dataSizeConvert",
    [ni("value","数値","",1,0,999999999,0.1),si("fromUnit","変換元",[{"value":"B","label":"B（バイト）"},{"value":"KB","label":"KB"},{"value":"MB","label":"MB"},{"value":"GB","label":"GB"},{"value":"TB","label":"TB"}])],
    [o("B","バイト","number"),o("KB","KB","number",True),o("MB","MB","number"),o("GB","GB","number"),o("TB","TB","number")],
    "<h3>データ容量の変換</h3><p>1 KB = 1,024 B、1 MB = 1,024 KB、1 GB = 1,024 MB、1 TB = 1,024 GB</p>",
    [{"question":"GBとGiBの違いは？","answer":"GB（ギガバイト）は10^9、GiB（ギビバイト）は2^30です。OSとメーカーで表記が異なることがあります。"},{"question":"スマホの1GBでどのくらい使える？","answer":"動画は約2時間、音楽は約250曲、Webページは約3,500ページが目安です。"}])

# --- life/shopping ---
count += c("split-bill","life","shopping","割り勘計算","合計金額を人数で割り勘計算",
    "割り勘計算ツール｜keisan.tools","合計金額と人数を入力して1人あたりの支払額を自動計算。端数処理対応。","splitBill",
    [ni("total","合計金額","円",10000,0,9999999,1),ni("people","人数","人",4,2,100,1),si("rounding","端数処理",[{"value":"ceil","label":"切り上げ"},{"value":"floor","label":"切り捨て"},{"value":"round","label":"四捨五入"}])],
    [o("perPerson","1人あたり","currency",True),o("remainder","端数","currency"),o("adjustedTotal","調整後合計","currency")],
    "<h3>割り勘計算</h3><p>合計金額を人数で均等に分割します。端数の処理方法を選択できます。</p>",
    [{"question":"端数は誰が払う？","answer":"幹事が負担するか、切り上げて余りを次回に繰り越すのが一般的です。"},{"question":"傾斜配分はできる？","answer":"このツールは均等割りです。役職や年齢で傾斜をつける場合は手動で調整してください。"}])

count += c("unit-price","life","shopping","単価比較計算","異なるサイズ・容量の商品を単価で比較",
    "単価比較ツール｜お買い得はどっち？","2つの商品の価格と容量を入力して単価を比較。お買い得判定。","unitPrice",
    [ni("price1","商品Aの価格","円",298,0,999999,1),ni("amount1","商品Aの量","g/ml",500,0,99999,1),ni("price2","商品Bの価格","円",498,0,999999,1),ni("amount2","商品Bの量","g/ml",1000,0,99999,1)],
    [o("unitPriceA","商品A単価（100gあたり）","currency",True),o("unitPriceB","商品B単価（100gあたり）","currency"),o("savings","差額（100gあたり）","currency"),o("verdict","判定","text")],
    "<h3>単価比較</h3><p>100gまたは100mlあたりの単価を計算して比較します。</p>",
    [{"question":"大容量の方がお得？","answer":"一般的にはそうですが、賞味期限や保管スペースも考慮しましょう。"},{"question":"セールの割引と比較できる？","answer":"割引後の価格を入力すれば比較できます。"}])

# --- life/car ---
count += c("fuel-cost","life","car","ガソリン代計算","走行距離と燃費からガソリン代を計算",
    "ガソリン代計算ツール｜keisan.tools","走行距離と燃費を入力してガソリン代を自動計算。","fuelCost",
    [ni("distance","走行距離","km",100,0,99999,1),ni("fuelEfficiency","燃費","km/L",15,1,50,0.1),ni("gasPrice","ガソリン単価","円/L",170,50,500,1)],
    [o("fuelCost","ガソリン代","currency",True),o("fuelAmount","必要ガソリン量","number"),o("costPerKm","1kmあたりコスト","currency")],
    "<h3>ガソリン代の計算</h3><p>走行距離÷燃費×ガソリン単価で計算します。</p>",
    [{"question":"燃費の調べ方は？","answer":"カタログ燃費（WLTC）の7-8割が実燃費の目安です。"},{"question":"高速と一般道の燃費差は？","answer":"一般的に高速道路の方が10-20%燃費が良くなります。"}])

# --- business/accounting ---
count += c("break-even","business","accounting","損益分岐点計算","固定費と変動費から損益分岐点を計算",
    "損益分岐点計算ツール｜keisan.tools","固定費・変動費率を入力して損益分岐点売上高を自動計算。","breakEven",
    [ni("fixedCost","固定費","万円",100,0,100000,1),ni("variableRate","変動費率","%",60,0,100,1)],
    [o("breakEvenSales","損益分岐点売上高","currency",True),o("marginRate","限界利益率","percent"),o("safetyMargin","安全余裕率の目安","percent")],
    "<h3>損益分岐点</h3><p>損益分岐点＝固定費÷（1−変動費率）で計算します。</p>",
    [{"question":"損益分岐点とは？","answer":"売上と費用が等しくなる点。これを超えると利益が出ます。"},{"question":"変動費率を下げるには？","answer":"仕入コスト削減、外注費見直し、生産効率改善が主な方法です。"}])

count += c("depreciation","business","accounting","減価償却計算","取得価額から減価償却費を計算",
    "減価償却計算ツール｜定額法・定率法対応","取得価額と耐用年数を入力して年間の減価償却費を自動計算。","depreciation",
    [ni("cost","取得価額","万円",100,0,100000,1),ni("usefulLife","耐用年数","年",5,2,50,1),si("method","償却方法",[{"value":"straight","label":"定額法"},{"value":"declining","label":"定率法"}])],
    [o("annualDepreciation","年間償却費","currency",True),o("monthlyDepreciation","月間償却費","currency"),o("bookValue","1年後の帳簿価額","currency")],
    "<h3>減価償却</h3><p>定額法は毎年同額、定率法は初年度に多く償却する方法です。</p>",
    [{"question":"定額法と定率法の違いは？","answer":"定額法は毎年均等に償却、定率法は初期に多く償却します。法人は原則定率法、個人は定額法です。"},{"question":"耐用年数の調べ方は？","answer":"国税庁の「減価償却資産の耐用年数表」で確認できます。"}])

# --- business/freelance ---
count += c("invoice-tax","business","freelance","インボイス消費税計算","フリーランスのインボイス制度の消費税を計算",
    "インボイス消費税計算ツール｜keisan.tools","売上高から消費税の納付額を簡易課税・2割特例で計算。","invoiceTax",
    [ni("revenue","年間売上","万円",500,0,50000,10),si("method","計算方法",[{"value":"simplified","label":"簡易課税（みなし仕入率50%）"},{"value":"special","label":"2割特例"},{"value":"actual","label":"本則課税"}]),ni("expenses","課税仕入（本則課税時）","万円",200,0,50000,10)],
    [o("taxPayment","消費税納付額","currency",True),o("taxCollected","預かり消費税","currency"),o("taxDeducted","仕入税額控除","currency")],
    "<h3>インボイス制度の消費税</h3><p>2023年10月開始のインボイス制度に基づく消費税の計算です。</p>",
    [{"question":"2割特例とは？","answer":"免税事業者からインボイス登録した事業者が、納税額を売上税額の2割にできる経過措置です（2026年9月まで）。"},{"question":"簡易課税の条件は？","answer":"前々年の課税売上が5,000万円以下の事業者が届出により選択できます。"}])

# --- math/basic ---
count += c("fraction-calculator","math","basic","分数計算","分数の四則演算を計算",
    "分数計算ツール｜keisan.tools","分数の足し算・引き算・掛け算・割り算を自動計算。約分・通分対応。","fractionCalculator",
    [ni("num1","分子1","",1,0,9999,1),ni("den1","分母1","",2,1,9999,1),si("operator","演算子",[{"value":"add","label":"＋"},{"value":"sub","label":"−"},{"value":"mul","label":"×"},{"value":"div","label":"÷"}]),ni("num2","分子2","",1,0,9999,1),ni("den2","分母2","",3,1,9999,1)],
    [o("resultNum","結果の分子","number",True),o("resultDen","結果の分母","number"),o("decimal","小数値","number")],
    "<h3>分数の計算</h3><p>2つの分数の四則演算を行い、結果を既約分数で表示します。</p>",
    [{"question":"通分とは？","answer":"分母を揃えることです。足し算・引き算の際に必要です。"},{"question":"約分とは？","answer":"分子と分母を最大公約数で割って簡単にすることです。"}])

count += c("percentage-calculator","math","basic","パーセント計算","各種パーセント計算を実行",
    "パーセント計算ツール｜keisan.tools","AはBの何%？BのA%はいくら？など各種パーセント計算。","percentageCalculator",
    [ni("valueA","値A","",50,0,999999999,0.1),ni("valueB","値B","",200,0,999999999,0.1),si("calcType","計算タイプ",[{"value":"of","label":"BのA%はいくら？"},{"value":"is","label":"AはBの何%？"},{"value":"change","label":"AからBへの変化率"}])],
    [o("result","計算結果","number",True),o("explanation","計算式","text")],
    "<h3>パーセント計算</h3><p>3種類のパーセント計算に対応しています。</p>",
    [{"question":"パーセントポイントとは？","answer":"割合の差を表す単位です。10%から15%への変化は「5パーセントポイント増」です。"},{"question":"増加率と増加ポイントの違いは？","answer":"10%→15%は「50%増加」ですが「5ポイント増加」です。"}])

count += c("gcd-lcm","math","basic","最大公約数・最小公倍数計算","2つの数の最大公約数と最小公倍数を計算",
    "最大公約数・最小公倍数計算ツール｜keisan.tools","2つの数を入力してGCDとLCMを自動計算。ユークリッドの互除法。","gcdLcm",
    [ni("numA","数値A","",12,1,999999999,1),ni("numB","数値B","",18,1,999999999,1)],
    [o("gcd","最大公約数（GCD）","number",True),o("lcm","最小公倍数（LCM）","number")],
    "<h3>最大公約数と最小公倍数</h3><p>ユークリッドの互除法で最大公約数を求め、GCD×LCM=A×Bの関係から最小公倍数を求めます。</p>",
    [{"question":"最大公約数の求め方は？","answer":"ユークリッドの互除法：大きい数を小さい数で割り、余りが0になるまで繰り返します。"},{"question":"何に使う？","answer":"分数の約分（GCD）、周期の計算（LCM）などに使います。"}])

# --- math/geometry ---
count += c("cone","math","geometry","円錐の体積・表面積","円錐の体積と表面積を計算",
    "円錐計算ツール｜keisan.tools","底面の半径と高さから円錐の体積と表面積を自動計算。","cone",
    [ni("radius","底面の半径","cm",5,0,99999,0.1),ni("height","高さ","cm",10,0,99999,0.1)],
    [o("volume","体積","number",True),o("surfaceArea","表面積","number"),o("slantHeight","母線の長さ","number")],
    "<h3>円錐の計算</h3><p>体積＝πr²h/3、表面積＝πr²+πrl（lは母線の長さ）</p>",
    [{"question":"母線とは？","answer":"円錐の頂点から底面の円周上の点までの距離です。√(r²+h²)で求めます。"},{"question":"円錐と円柱の体積の関係は？","answer":"同じ底面・高さの場合、円錐の体積は円柱の1/3です。"}])

count += c("sphere","math","geometry","球の体積・表面積","球の体積と表面積を計算",
    "球の体積・表面積計算ツール｜keisan.tools","半径を入力して球の体積と表面積を自動計算。","sphere",
    [ni("radius","半径","cm",5,0,99999,0.1)],
    [o("volume","体積","number",True),o("surfaceArea","表面積","number"),o("diameter","直径","number")],
    "<h3>球の計算</h3><p>体積＝4πr³/3、表面積＝4πr²</p>",
    [{"question":"半球の体積は？","answer":"球の体積の半分、つまり2πr³/3です。"},{"question":"円と球の関係は？","answer":"円は2次元、球は3次元の図形です。円を回転させると球になります。"}])

# --- math/statistics ---
count += c("standard-deviation","math","statistics","標準偏差計算","データセットから標準偏差を計算",
    "標準偏差計算ツール｜keisan.tools","データを入力して平均・分散・標準偏差を自動計算。","standardDeviation",
    [ni("n","データ数","個",5,2,20,1),ni("v1","データ1","",10,0,999999,0.1),ni("v2","データ2","",20,0,999999,0.1),ni("v3","データ3","",30,0,999999,0.1),ni("v4","データ4","",40,0,999999,0.1),ni("v5","データ5","",50,0,999999,0.1)],
    [o("mean","平均","number",True),o("variance","分散","number"),o("stdDev","標準偏差","number"),o("cv","変動係数","percent")],
    "<h3>標準偏差</h3><p>データのばらつきを表す指標です。値が大きいほどデータが散らばっています。</p>",
    [{"question":"標準偏差と分散の違いは？","answer":"分散は偏差の二乗の平均、標準偏差は分散の平方根です。単位が元データと同じになります。"},{"question":"偏差値との関係は？","answer":"偏差値＝50+10×（得点−平均）÷標準偏差です。"}])

# --- education/school ---
count += c("gpa-calculator","education","school","GPA計算","科目の成績からGPAを計算",
    "GPA計算ツール｜keisan.tools","科目数と各成績を入力してGPAを自動計算。4段階・5段階対応。","gpaCalculator",
    [ni("subjects","科目数","科目",5,1,20,1),ni("s1","科目1の評点","",4,0,4,1),ni("s2","科目2の評点","",3,0,4,1),ni("s3","科目3の評点","",4,0,4,1),ni("s4","科目4の評点","",2,0,4,1),ni("s5","科目5の評点","",3,0,4,1),ni("c1","科目1の単位数","",2,1,6,1),ni("c2","科目2の単位数","",2,1,6,1),ni("c3","科目3の単位数","",2,1,6,1),ni("c4","科目4の単位数","",2,1,6,1),ni("c5","科目5の単位数","",2,1,6,1)],
    [o("gpa","GPA","number",True),o("totalCredits","合計単位数","number"),o("totalPoints","合計ポイント","number")],
    "<h3>GPAの計算</h3><p>GPA＝Σ（評点×単位数）÷Σ単位数で計算します。</p>",
    [{"question":"GPAの満点は？","answer":"4段階評価の場合、最高は4.0です。"},{"question":"就活で必要なGPAは？","answer":"一般的に3.0以上が望ましいとされます。外資系は3.5以上を求めることもあります。"}])

# --- education/study ---
count += c("reading-speed","education","study","読書速度計算","ページ数と時間から読書速度を計算",
    "読書速度計算ツール｜keisan.tools","ページ数と読書時間を入力して読書速度を自動計算。","readingSpeed",
    [ni("pages","ページ数","ページ",200,1,9999,1),ni("minutes","読書時間","分",120,1,9999,1),ni("charsPerPage","1ページの文字数","文字",600,100,2000,100)],
    [o("pagesPerHour","1時間あたりページ数","number",True),o("charsPerMinute","1分あたり文字数","number"),o("totalTime","全体の読了時間","number")],
    "<h3>読書速度</h3><p>日本人の平均読書速度は約400-600文字/分と言われています。</p>",
    [{"question":"速読のコツは？","answer":"音読をやめる、視野を広げる、キーワードを拾い読みする方法があります。"},{"question":"平均的な読書速度は？","answer":"日本語の場合、一般的に400-600文字/分が平均です。"}])

# --- life/shopping (more) ---
count += c("mortgage-comparison","life","shopping","住宅ローン比較","2つの住宅ローン条件を比較",
    "住宅ローン比較ツール｜keisan.tools","2つの住宅ローン条件を入力して月々の返済額・総返済額を比較。","mortgageComparison",
    [ni("amount","借入額","万円",3000,0,100000,10),ni("rate1","金利A","%",0.5,0,15,0.01),ni("years1","期間A","年",35,1,50,1),ni("rate2","金利B","%",1.5,0,15,0.01),ni("years2","期間B","年",25,1,50,1)],
    [o("monthlyA","月々返済A","currency",True),o("totalA","総返済額A","currency"),o("monthlyB","月々返済B","currency"),o("totalB","総返済額B","currency"),o("difference","総返済額の差","currency")],
    "<h3>住宅ローン比較</h3><p>異なる金利・期間の住宅ローンを比較します。</p>",
    [{"question":"変動金利と固定金利どちらがいい？","answer":"金利上昇リスクを避けたいなら固定、低金利を活かしたいなら変動です。"},{"question":"返済期間は長い方がいい？","answer":"月々の負担は減りますが、総返済額は増えます。"}])

count += c("subscription-cost","life","shopping","サブスク月額合計計算","各種サブスクリプションの月額合計を計算",
    "サブスク月額合計計算ツール｜keisan.tools","各サブスクの月額を入力して合計・年額を自動計算。","subscriptionCost",
    [ni("sub1","サブスク1","円",1000,0,99999,1),ni("sub2","サブスク2","円",500,0,99999,1),ni("sub3","サブスク3","円",2000,0,99999,1),ni("sub4","サブスク4","円",0,0,99999,1),ni("sub5","サブスク5","円",0,0,99999,1)],
    [o("monthlyTotal","月額合計","currency",True),o("annualTotal","年額合計","currency"),o("dailyCost","1日あたりコスト","currency")],
    "<h3>サブスク費用の管理</h3><p>毎月の固定費を見える化して家計を管理しましょう。</p>",
    [{"question":"サブスクの見直しポイントは？","answer":"使用頻度が低いもの、重複しているものを優先的に見直しましょう。"},{"question":"年間でいくら節約できる？","answer":"月500円のサブスクを解約するだけで年間6,000円の節約になります。"}])

print(f"Created {count} JSON files")
