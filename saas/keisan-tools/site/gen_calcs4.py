#!/usr/bin/env python3
"""Batch 4: 15 more calculators to reach 300+."""
import json, os

BASE = os.path.join(os.path.dirname(__file__), "data", "calculators")

def c(slug, cat, sub, title, desc, mt, md, fn, inputs, outputs, explanation, faq, related=[]):
    d = os.path.join(BASE, cat, sub)
    os.makedirs(d, exist_ok=True)
    fp = os.path.join(d, f"{slug}.json")
    if os.path.exists(fp):
        return 0
    obj = {"slug":slug,"category":cat,"subcategory":sub,"title":title,"description":desc,
           "metaTitle":mt,"metaDescription":md,"calculatorFunction":fn,
           "inputs":inputs,"outputs":outputs,"explanation":explanation,"faq":faq,
           "related":related,"popular":False}
    with open(fp,"w",encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return 1

def ni(id,label,unit="",default=0,mn=0,mx=999999,step=1):
    r = {"id":id,"label":label,"type":"number","default":default,"min":mn,"max":mx,"step":step}
    if unit: r["unit"] = unit
    return r

def si(id,label,options):
    return {"id":id,"label":label,"type":"select","options":options}

def o(id,label,fmt="number",primary=False):
    r = {"id":id,"label":label,"format":fmt}
    if primary: r["primary"] = True
    return r

count = 0

count += c("rent-vs-buy","money","real-estate","賃貸vs購入シミュレーション","賃貸と購入の総コストを比較",
    "賃貸vs購入比較ツール｜keisan.tools","家賃と住宅ローンの総コストを比較シミュレーション。","rentVsBuy",
    [ni("rent","月額家賃","万円",10,0,100,1),ni("purchasePrice","物件価格","万円",4000,0,100000,100),ni("downPayment","頭金","万円",400,0,50000,10),ni("loanRate","住宅ローン金利","%",1,0,10,0.1),ni("years","比較期間","年",30,1,50,1)],
    [o("rentTotal","賃貸総コスト","currency",True),o("buyTotal","購入総コスト","currency"),o("difference","差額","currency")],
    "<h3>賃貸vs購入</h3><p>一定期間の総コストで賃貸と購入を比較します。</p>",
    [{"question":"どちらがお得？","answer":"期間・金利・物件価値の変動により異なります。一般的に15年以上なら購入が有利な傾向です。"},{"question":"購入の隠れコストは？","answer":"固定資産税、管理費、修繕積立金、火災保険等が必要です。"}])

count += c("nisa-simulation","money","investment","新NISA積立シミュレーション","新NISAの非課税メリットをシミュレーション",
    "新NISA積立シミュレーション｜keisan.tools","毎月の積立額と想定利回りから新NISAの運用成果を計算。","nisaSimulation",
    [ni("monthly","毎月積立額","万円",3,0,10,0.5),ni("years","積立期間","年",20,1,30,1),ni("returnRate","想定年利回り","%",5,0,20,0.5)],
    [o("totalInvested","積立総額","currency",True),o("futureValue","運用成果","currency"),o("profit","運用益","currency"),o("taxSaved","非課税メリット","currency")],
    "<h3>新NISAシミュレーション</h3><p>新NISAのつみたて投資枠（年120万円）の非課税メリットを計算します。</p>",
    [{"question":"新NISAの上限は？","answer":"つみたて投資枠120万円/年+成長投資枠240万円/年、生涯1,800万円です。"},{"question":"非課税のメリットは？","answer":"通常約20%課税される運用益が非課税になります。"}])

count += c("electricity-bill","life","shopping","電気料金計算","消費電力と使用時間から電気代を計算",
    "電気料金計算ツール｜keisan.tools","家電の消費電力と使用時間を入力して電気代を自動計算。","electricityBill",
    [ni("watt","消費電力","W",1000,1,99999,1),ni("hoursPerDay","1日の使用時間","時間",3,0,24,0.5),ni("days","使用日数","日",30,1,365,1),ni("pricePerKwh","電力単価","円/kWh",31,10,100,1)],
    [o("monthlyCost","電気代","currency",True),o("kwhUsed","消費電力量","number"),o("dailyCost","1日あたり","currency")],
    "<h3>電気料金の計算</h3><p>消費電力(kW)×使用時間(h)×電力単価(円/kWh)で計算します。</p>",
    [{"question":"電力単価の目安は？","answer":"2026年現在、全国平均で約31円/kWhです。"},{"question":"エアコンの電気代は？","answer":"6畳用で1時間約15-25円が目安です。"}])

count += c("paint-area","life","unit","塗装面積計算","部屋の壁・天井の塗装面積を計算",
    "塗装面積計算ツール｜keisan.tools","部屋のサイズから壁と天井の塗装面積を自動計算。ペンキ量の目安も。","paintArea",
    [ni("width","部屋の幅","m",4,0,50,0.1),ni("depth","部屋の奥行","m",5,0,50,0.1),ni("height","天井高","m",2.4,1,10,0.1),ni("windows","窓の数","個",2,0,10,1),ni("doors","ドアの数","個",1,0,10,1)],
    [o("wallArea","壁面積","number",True),o("ceilingArea","天井面積","number"),o("totalArea","合計面積","number"),o("paintLiters","必要ペンキ量","number")],
    "<h3>塗装面積の計算</h3><p>壁と天井の面積から窓・ドアの面積を引いて計算します。</p>",
    [{"question":"ペンキの使用量は？","answer":"1Lで約5-7㎡塗れるのが一般的です。2度塗りの場合は倍量必要です。"},{"question":"窓の面積の目安は？","answer":"一般的な窓は約1.5㎡、ドアは約1.8㎡で計算しています。"}])

count += c("tile-calculator","life","unit","タイル枚数計算","床面積からタイルの必要枚数を計算",
    "タイル枚数計算ツール｜keisan.tools","床面積とタイルサイズから必要枚数を自動計算。ロス率込み。","tileCalculator",
    [ni("areaWidth","施工幅","m",3,0,100,0.1),ni("areaDepth","施工奥行","m",4,0,100,0.1),ni("tileSize","タイル1辺","cm",30,1,100,1),ni("lossRate","ロス率","%",10,0,30,1)],
    [o("tilesNeeded","必要枚数","number",True),o("area","施工面積","number"),o("boxes","必要箱数（10枚/箱）","number")],
    "<h3>タイル枚数の計算</h3><p>施工面積÷タイル面積にロス率を加えて必要枚数を算出します。</p>",
    [{"question":"ロス率とは？","answer":"カットや破損で無駄になる分です。10-15%が一般的です。"},{"question":"目地幅は考慮される？","answer":"このツールでは目地幅は考慮していません。実際は若干少なくなります。"}])

count += c("wallpaper-calculator","life","unit","壁紙必要量計算","部屋のサイズから壁紙の必要量を計算",
    "壁紙必要量計算ツール｜keisan.tools","部屋のサイズを入力して壁紙の必要m数を自動計算。","wallpaperCalculator",
    [ni("width","部屋の幅","m",4,0,30,0.1),ni("depth","部屋の奥行","m",5,0,30,0.1),ni("height","天井高","m",2.4,1,5,0.1),ni("rollWidth","壁紙幅","cm",92,50,120,1)],
    [o("totalLength","必要m数","number",True),o("rolls","必要本数（10m巻）","number"),o("wallArea","壁面積","number")],
    "<h3>壁紙の必要量</h3><p>壁の周囲長と天井高から壁紙の必要量を計算します。</p>",
    [{"question":"壁紙1本は何m？","answer":"一般的な国産壁紙は10m巻です。"},{"question":"柄合わせの分は？","answer":"柄のある壁紙は10-20%多めに見積もりましょう。"}])

count += c("salary-after-tax","money","salary","手取り早見表","年収別の手取り額を一覧表示",
    "年収別手取り額早見表｜keisan.tools","年収200万〜2000万の手取り額を一覧表示。税金・社会保険料の内訳つき。","salaryAfterTax",
    [ni("income","年収","万円",500,100,5000,50),ni("dependents","扶養人数","人",0,0,5,1)],
    [o("takeHome","手取り年収","currency",True),o("monthlyTakeHome","手取り月収","currency"),o("totalTax","税金合計","currency"),o("socialInsurance","社会保険料","currency"),o("ratio","手取り率","percent")],
    "<h3>手取り額の計算</h3><p>年収から所得税・住民税・社会保険料を差し引いた手取り額を計算します。</p>",
    [{"question":"年収500万の手取りは？","answer":"扶養なしで約390-400万円が目安です。"},{"question":"手取り率は？","answer":"年収400-600万円で約75-80%が一般的です。"}])

count += c("bmi-detailed","health","body","BMI計算（詳細版）","BMIと肥満度を詳細に判定",
    "BMI計算ツール（詳細版）｜keisan.tools","身長と体重からBMIを計算し、WHO基準と日本基準で判定。","bmiDetailed",
    [ni("height","身長","cm",170,100,250,0.1),ni("weight","体重","kg",65,20,300,0.1)],
    [o("bmi","BMI","number",True),o("category","判定（日本基準）","text"),o("idealWeight","適正体重","number"),o("weightDiff","適正体重との差","number")],
    "<h3>BMIの詳細判定</h3><p>BMI＝体重(kg)÷身長(m)²で計算します。日本肥満学会の基準で判定します。</p>",
    [{"question":"日本の肥満基準は？","answer":"18.5未満:低体重、18.5-25:普通体重、25-30:肥満1度、30-35:肥満2度、35-40:肥満3度、40以上:肥満4度"},{"question":"WHOと日本の基準の違いは？","answer":"WHOは25以上を過体重、30以上を肥満としますが、日本は25以上を肥満としています。"}])

count += c("concrete-calculator","life","unit","コンクリート量計算","施工面積からコンクリートの必要量を計算",
    "コンクリート量計算ツール｜keisan.tools","施工面積と厚さからコンクリートの必要量を自動計算。","concreteCalculator",
    [ni("width","幅","m",3,0,100,0.1),ni("depth","奥行","m",5,0,100,0.1),ni("thickness","厚さ","cm",10,1,100,1)],
    [o("volume","必要体積","number",True),o("weight","概算重量","number"),o("bags","セメント袋数（25kg）","number")],
    "<h3>コンクリート量の計算</h3><p>幅×奥行×厚さで体積を算出します。</p>",
    [{"question":"コンクリートの比重は？","answer":"約2.3t/m³です。"},{"question":"DIYで何袋必要？","answer":"25kgのセメント1袋で約0.012m³のコンクリートが作れます。"}])

count += c("swimming-calorie","health","calorie","水泳消費カロリー計算","泳ぎ方と時間から消費カロリーを計算",
    "水泳消費カロリー計算ツール｜keisan.tools","泳法と時間を入力して水泳の消費カロリーを自動計算。","swimmingCalorie",
    [ni("weight","体重","kg",65,20,200,0.1),ni("minutes","時間","分",30,1,300,1),si("stroke","泳法",[{"value":"crawl","label":"クロール（8METs）"},{"value":"breaststroke","label":"平泳ぎ（6METs）"},{"value":"backstroke","label":"背泳ぎ（5METs）"},{"value":"butterfly","label":"バタフライ（10METs）"},{"value":"water_walk","label":"水中ウォーキング（4METs）"}])],
    [o("calories","消費カロリー","number",True),o("fatBurn","脂肪燃焼量","number")],
    "<h3>水泳の消費カロリー</h3><p>泳法ごとのMETs値を使用して消費カロリーを計算します。</p>",
    [{"question":"一番カロリーを消費する泳法は？","answer":"バタフライが最も消費カロリーが高く、次いでクロールです。"},{"question":"水泳はダイエットに効果的？","answer":"全身運動で関節への負担が少なく、効率的な有酸素運動です。"}])

count += c("power-consumption","life","shopping","家電消費電力比較","家電の年間電気代を比較",
    "家電消費電力比較ツール｜keisan.tools","2つの家電の消費電力を入力して年間電気代を比較。買い替え判断に。","powerConsumption",
    [ni("watt1","旧家電の消費電力","W",800,1,99999,1),ni("watt2","新家電の消費電力","W",500,1,99999,1),ni("hoursPerDay","1日の使用時間","時間",4,0,24,0.5),ni("pricePerKwh","電力単価","円/kWh",31,10,100,1)],
    [o("annualCost1","旧家電の年間電気代","currency",True),o("annualCost2","新家電の年間電気代","currency"),o("annualSaving","年間節約額","currency"),o("tenYearSaving","10年間の節約額","currency")],
    "<h3>消費電力比較</h3><p>家電の買い替えによる電気代の節約効果を計算します。</p>",
    [{"question":"家電の買い替え目安は？","answer":"10年前の家電は最新型と比べて30-50%電力消費が多いことがあります。"},{"question":"待機電力は？","answer":"待機電力は年間で数千円のコストになることがあります。"}])

count += c("room-brightness","life","unit","照明の明るさ計算","部屋の広さから必要な照明の明るさを計算",
    "照明の明るさ計算ツール｜keisan.tools","部屋の広さを入力して必要なルーメン数・ワット数を自動計算。","roomBrightness",
    [ni("area","部屋の広さ","畳",6,1,30,1),si("roomType","部屋の用途",[{"value":"living","label":"リビング"},{"value":"bedroom","label":"寝室"},{"value":"study","label":"書斎"},{"value":"kitchen","label":"キッチン"}])],
    [o("lumens","必要ルーメン数","number",True),o("ledWatt","LEDワット目安","number"),o("fixtures","シーリングライト数","number")],
    "<h3>照明の明るさ</h3><p>部屋の広さと用途に応じた適切な明るさを計算します。</p>",
    [{"question":"1畳あたり何ルーメン？","answer":"リビングは約400lm/畳、寝室は約200lm/畳が目安です。"},{"question":"LEDの選び方は？","answer":"色温度は電球色(3000K)がリラックス、昼白色(5000K)が作業向きです。"}])

count += c("cycling-calorie","health","calorie","サイクリング消費カロリー計算","自転車の消費カロリーを計算",
    "サイクリング消費カロリー計算｜keisan.tools","体重と走行時間から自転車の消費カロリーを自動計算。","cyclingCalorie",
    [ni("weight","体重","kg",65,20,200,0.1),ni("minutes","時間","分",30,1,300,1),si("intensity","強度",[{"value":"light","label":"軽い（10km/h）4METs"},{"value":"moderate","label":"普通（16km/h）6METs"},{"value":"vigorous","label":"速い（25km/h）10METs"}])],
    [o("calories","消費カロリー","number",True),o("distance","推定走行距離","number"),o("fatBurn","脂肪燃焼量","number")],
    "<h3>サイクリングの消費カロリー</h3><p>METs×体重(kg)×時間(h)×1.05で消費カロリーを計算します。</p>",
    [{"question":"自転車通勤のカロリーは？","answer":"片道30分（普通速度）で体重65kgの人は約200kcal消費します。"},{"question":"ランニングとどちらが効果的？","answer":"同じ時間ならランニングの方が消費カロリーは高いですが、自転車は関節への負担が少ないです。"}])

count += c("air-conditioner-cost","life","shopping","エアコン電気代計算","エアコンの電気代を計算",
    "エアコン電気代計算ツール｜keisan.tools","エアコンの消費電力と使用時間から月額電気代を自動計算。","airConditionerCost",
    [ni("capacity","畳数","畳",8,4,30,2),ni("hoursPerDay","1日の使用時間","時間",8,0,24,1),ni("days","使用日数","日",30,1,90,1),ni("pricePerKwh","電力単価","円/kWh",31,10,100,1)],
    [o("monthlyCost","月額電気代","currency",True),o("dailyCost","1日あたり","currency"),o("seasonCost","シーズン合計","currency")],
    "<h3>エアコン電気代</h3><p>畳数に応じた消費電力と使用時間から電気代を計算します。</p>",
    [{"question":"つけっぱなしの方が安い？","answer":"30分以内の外出ならつけっぱなしの方が、それ以上なら切った方が省エネです。"},{"question":"設定温度で電気代は変わる？","answer":"冷房を1℃上げると約10%、暖房を1℃下げると約10%の節電になります。"}])

print(f"Created {count} JSON files")
