"""Generate batch 2 of calculator JSON files (102+ more to reach 300+)"""
import json, os

BASE = os.path.join(os.path.dirname(__file__), "data", "calculators")

def write_calc(calc):
    cat = calc["category"]
    sub = calc["subcategory"]
    slug = calc["slug"]
    dirpath = os.path.join(BASE, cat, sub)
    os.makedirs(dirpath, exist_ok=True)
    filepath = os.path.join(dirpath, f"{slug}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(calc, f, ensure_ascii=False, indent=2)

def c(slug,cat,sub,title,desc,mt,md,func,inputs,outputs,expl,faq,related):
    return {"slug":slug,"category":cat,"subcategory":sub,"title":title,"description":desc,"metaTitle":mt,"metaDescription":md,"calculatorFunction":func,"inputs":inputs,"outputs":outputs,"explanation":expl,"faq":faq,"related":related,"popular":False}

def ni(id,label,type="number",unit="",default=0,min=0,max=99999,step=1,**kw):
    r = {"id":id,"label":label,"type":type,"unit":unit,"default":default,"min":min,"max":max,"step":step}
    r.update(kw)
    return r

def si(id,label,options,default):
    return {"id":id,"label":label,"type":"select","options":options,"default":default}

def o(id,label,fmt="number",primary=False):
    return {"id":id,"label":label,"format":fmt,"primary":primary}

calcs = [
# ===== money/tax (5) =====
c("city-planning-tax","money","tax","都市計画税計算","固定資産税評価額から都市計画税を計算。","都市計画税計算ツール｜固定資産税評価額から自動計算【2026年版】","固定資産税評価額を入力して都市計画税を自動計算。","cityPlanningTax",
  [ni("landValue","土地の評価額",unit="万円",default=2000,max=500000,step=10),ni("buildingValue","建物の評価額",unit="万円",default=1500,max=500000,step=10)],
  [o("tax","都市計画税","currency",True),o("withFixedAsset","固定資産税+都市計画税","currency")],
  "<h3>都市計画税</h3><p>市街化区域内の土地・建物に課される税金。税率は上限0.3%（自治体により異なる）。固定資産税と一緒に課税されます。</p>",
  [{"question":"どこでかかる？","answer":"市街化区域内の不動産に課税。市街化調整区域は非課税です。"},{"question":"固定資産税との違い？","answer":"固定資産税は全ての不動産、都市計画税は市街化区域のみです。"}],
  ["fixed-asset-tax","real-estate-acquisition-tax"]),

c("individual-enterprise-tax","money","tax","個人事業税計算","個人事業主の事業税を計算。業種ごとの税率対応。","個人事業税計算ツール｜事業所得から事業税を自動計算【2026年版】","事業所得と業種を入力して個人事業税を自動計算。","individualEnterpriseTax",
  [ni("income","事業所得",unit="万円",default=500,max=50000,step=10),si("industry","業種",[{"value":"type1","label":"第1種（5%: 物品販売、飲食等）"},{"value":"type2","label":"第2種（4%: 畜産、水産等）"},{"value":"type3","label":"第3種（5%: 医業、弁護士等）"},{"value":"type3b","label":"第3種（3%: あんま、マッサージ等）"}],"type1")],
  [o("enterpriseTax","個人事業税","currency",True),o("deduction","事業主控除","currency")],
  "<h3>個人事業税</h3><p>事業所得が290万円を超える個人事業主に課税。290万円の事業主控除あり。税率は業種により3〜5%。</p>",
  [{"question":"290万以下なら非課税？","answer":"はい。事業主控除290万円以下なら非課税です。"},{"question":"フリーランスも対象？","answer":"はい。ただし業種によっては非課税のものもあります。"}],
  ["freelance-tax","blue-return"]),

c("capital-gains-tax","money","tax","譲渡所得税計算","不動産・株式の売却益にかかる譲渡所得税を計算。","譲渡所得税計算ツール｜売却益から税額を自動計算【2026年版】","不動産や株式の売却益を入力して譲渡所得税を自動計算。","capitalGainsTax",
  [ni("salePrice","売却価格",unit="万円",default=5000,max=1000000,step=10),ni("purchasePrice","取得費",unit="万円",default=3000,max=1000000,step=10),ni("expenses","譲渡費用",unit="万円",default=200,max=100000,step=10),si("assetType","資産の種類",[{"value":"stock","label":"上場株式"},{"value":"realestate_short","label":"不動産（短期: 5年以下）"},{"value":"realestate_long","label":"不動産（長期: 5年超）"}],"stock")],
  [o("gain","譲渡所得","currency"),o("incomeTax","所得税","currency",True),o("residentTax","住民税","currency"),o("totalTax","税額合計","currency")],
  "<h3>譲渡所得の税率</h3><p>上場株式: 20.315%（所得税15.315%+住民税5%）。不動産短期: 39.63%、不動産長期: 20.315%。</p>",
  [{"question":"3000万円特別控除とは？","answer":"自宅の売却では譲渡所得から3,000万円を控除できる特例があります。"},{"question":"損失は繰り越せる？","answer":"株式の譲渡損失は翌年以降3年間繰り越して利益と相殺できます。"}],
  ["stock-profit","income-tax"]),

c("alcohol-tobacco-tax","money","tax","酒税・たばこ税計算","ビール・ワイン・たばこの税額を計算。","酒税・たばこ税計算ツール｜1本あたりの税額を自動計算","お酒やたばこの税額を自動計算。価格に占める税金の割合も表示。","alcoholTobaccoTax",
  [si("product","商品",[{"value":"beer","label":"ビール（350ml）"},{"value":"happoshu","label":"発泡酒（350ml）"},{"value":"new_genre","label":"第3のビール（350ml）"},{"value":"wine","label":"ワイン（750ml）"},{"value":"sake","label":"日本酒（720ml）"},{"value":"cigarette","label":"たばこ（1箱20本）"}],"beer"),ni("price","購入価格",unit="円",default=250,max=100000,step=1)],
  [o("taxAmount","税額","currency",True),o("taxRatio","価格に占める税率","percent"),o("preTaxPrice","税抜価格","currency")],
  "<h3>酒税</h3><p>ビール350ml: 約63円、発泡酒: 約47円、第3のビール: 約38円。2026年10月にビール系飲料の税率が一本化予定。</p>",
  [{"question":"ビールの税金はいくら？","answer":"350ml缶で約63円。価格の約25%が酒税です。"},{"question":"たばこの税金は？","answer":"1箱（600円）のうち約370円が税金（約62%）です。"}],
  ["consumption-tax"]),

c("crypto-tax","money","tax","仮想通貨の税金計算","仮想通貨の売却益・交換益にかかる税金を計算。","仮想通貨の税金計算ツール｜暗号資産の利益から税額を自動計算【2026年版】","仮想通貨の利益を入力して所得税・住民税を自動計算。","cryptoTax",
  [ni("profit","仮想通貨の利益","万円",default=100,max=100000,step=1),ni("otherIncome","その他の所得",unit="万円",default=500,max=100000,step=10)],
  [o("taxableIncome","課税所得","currency"),o("incomeTax","所得税","currency",True),o("residentTax","住民税","currency"),o("totalTax","税額合計","currency"),o("effectiveRate","実効税率","percent")],
  "<h3>仮想通貨の税金</h3><p>雑所得として総合課税。他の所得と合算して累進税率（5〜45%）+住民税10%が適用されます。</p>",
  [{"question":"株と同じ税率？","answer":"いいえ。株は分離課税20.315%ですが、仮想通貨は総合課税で最大55%になります。"},{"question":"損失の繰越は？","answer":"2026年時点では仮想通貨の損失繰越は認められていません。"}],
  ["income-tax","side-job-tax"]),

# ===== money/salary (4) =====
c("maternity-benefit","money","salary","出産手当金計算","出産前後の出産手当金の支給額を計算。","出産手当金計算ツール｜産休中の手当金を自動計算","標準報酬月額を入力して出産手当金の支給額を自動計算。","maternityBenefit",
  [ni("monthlySalary","標準報酬月額",unit="万円",default=30,max=500,step=1)],
  [o("dailyAmount","日額","currency"),o("totalAmount","総支給額（98日分）","currency",True),o("preBirth","産前（42日分）","currency"),o("postBirth","産後（56日分）","currency")],
  "<h3>出産手当金</h3><p>健康保険加入者が出産で休業した期間に支給。日額 = 標準報酬日額 × 2/3。産前42日+産後56日=最大98日分。</p>",
  [{"question":"誰がもらえる？","answer":"健康保険に加入している被保険者本人が出産のため休業した場合に支給されます。"},{"question":"退職後でももらえる？","answer":"退職日までに継続して1年以上加入しており、退職日に出勤していなければ受給可能です。"}],
  ["take-home-pay","social-insurance"]),

c("childcare-benefit","money","salary","育児休業給付金計算","育休中の給付金の支給額を計算。","育児休業給付金計算ツール｜育休中の手取りを自動計算","月給を入力して育児休業給付金の支給額を自動計算。","childcareBenefit",
  [ni("monthlySalary","休業前の月給",unit="万円",default=30,max=500,step=1)],
  [o("first6months","最初の6ヶ月（月額）","currency",True),o("after6months","7ヶ月目以降（月額）","currency"),o("totalYear","1年間の総額","currency")],
  "<h3>育児休業給付金</h3><p>最初の180日: 月給の67%、181日目以降: 月給の50%。上限額あり（2026年: 約31万円/月）。</p>",
  [{"question":"男性でも受給できる？","answer":"はい。男女問わず雇用保険加入者が育休を取得すれば受給できます。"},{"question":"社会保険料は？","answer":"育休中は社会保険料が免除されます。"}],
  ["maternity-benefit","take-home-pay"]),

c("unemployment-benefit","money","salary","失業手当計算","雇用保険の失業手当（基本手当）の日額と受給期間を計算。","失業手当計算ツール｜失業保険の給付額を自動計算","年齢と前職の給与を入力して失業手当の日額と受給日数を自動計算。","unemploymentBenefit",
  [ni("age","年齢",unit="歳",default=35,min=18,max=65,step=1),ni("monthlySalary","離職前6ヶ月の月給平均",unit="万円",default=30,max=500,step=1),ni("yearsWorked","雇用保険加入年数",unit="年",default=10,min=1,max=40,step=1),si("reason","離職理由",[{"value":"self","label":"自己都合"},{"value":"company","label":"会社都合"}],"self")],
  [o("dailyAmount","基本手当日額","currency",True),o("totalDays","所定給付日数","number"),o("totalAmount","給付総額（概算）","currency"),o("waitingPeriod","給付制限期間","text")],
  "<h3>失業手当</h3><p>基本手当日額 = 離職前賃金日額 × 給付率（50〜80%）。年齢・加入年数・離職理由で給付日数が決まります。</p>",
  [{"question":"自己都合と会社都合の違いは？","answer":"自己都合は2ヶ月の給付制限あり。会社都合は7日の待期期間後すぐ受給可能です。"},{"question":"アルバイトしながら受給できる？","answer":"週20時間未満なら一定の範囲でアルバイト可能ですが、収入に応じて減額されます。"}],
  ["take-home-pay","social-insurance"]),

c("workers-comp","money","salary","労災保険給付計算","労災の休業補償給付の日額を計算。","労災保険給付計算ツール｜休業補償給付の日額を自動計算","平均賃金を入力して労災の休業補償給付の日額を自動計算。","workersComp",
  [ni("avgDailyWage","平均賃金（日額）",unit="円",default=12000,max=100000,step=100)],
  [o("compensationDaily","休業補償給付（日額）","currency",True),o("specialDaily","休業特別支給金（日額）","currency"),o("totalDaily","合計日額（80%）","currency"),o("monthly30","30日分の合計","currency")],
  "<h3>労災の休業補償</h3><p>休業4日目から支給。休業補償給付（60%）+ 休業特別支給金（20%）= 平均賃金の80%が支給されます。</p>",
  [{"question":"いつから支給？","answer":"休業4日目から。最初の3日間は会社が休業補償を支払います。"},{"question":"通勤中の怪我も対象？","answer":"はい。通勤災害として労災の対象になります。"}],
  ["overtime-pay","social-insurance"]),

# ===== money/investment (5) =====
c("bond-yield","money","investment","債券利回り計算","債券の価格と利率から利回りを計算。","債券利回り計算ツール｜最終利回り・直接利回りを自動計算","債券の額面と購入価格から利回りを自動計算。","bondYield",
  [ni("faceValue","額面",unit="万円",default=100,max=100000,step=1),ni("purchasePrice","購入価格",unit="万円",default=98,max=100000,step=0.01),ni("couponRate","利率",unit="%",default=1,max=20,step=0.01),ni("yearsToMaturity","残存期間",unit="年",default=5,min=1,max=30,step=1)],
  [o("directYield","直接利回り","percent",True),o("yieldToMaturity","最終利回り","percent"),o("annualIncome","年間利息","currency")],
  "<h3>債券の利回り</h3><p>直接利回り = 利息÷購入価格。最終利回り = (利息±償還差益/残存期間)÷購入価格。</p>",
  [{"question":"債券価格が下がると利回りは？","answer":"上がります。債券価格と利回りは逆の関係です。"},{"question":"個人向け国債の利率は？","answer":"変動10年は最低0.05%保証。2026年は0.5〜1%程度で推移しています。"}],
  ["compound-interest","dividend-yield"]),

c("reit-yield","money","investment","REIT利回り計算","不動産投資信託(REIT)の分配金利回りを計算。","REIT利回り計算ツール｜分配金利回りを自動計算","REITの投資口価格と分配金を入力して利回りを自動計算。","reitYield",
  [ni("price","投資口価格",unit="円",default=150000,max=10000000,step=100),ni("annualDistribution","年間分配金",unit="円",default=6000,max=1000000,step=100),ni("units","保有口数",unit="口",default=10,min=1,max=10000,step=1)],
  [o("yield","分配金利回り","percent",True),o("monthlyIncome","月額分配金収入","currency"),o("annualIncome","年間分配金収入","currency")],
  "<h3>REIT投資</h3><p>不動産投資信託。利益の90%超を分配するため高利回り。J-REITの平均利回りは4〜5%程度。</p>",
  [{"question":"REITのリスクは？","answer":"不動産市況の変動、金利上昇、テナント退去などがリスクです。"},{"question":"NISAで買える？","answer":"はい。成長投資枠でJ-REITを購入できます。"}],
  ["dividend-yield","property-yield"]),

c("etf-cost","money","investment","ETF経費率計算","ETFの経費率が長期投資に与える影響を計算。","ETF経費率計算ツール｜信託報酬の長期影響を自動計算","ETFの経費率と投資額から長期的なコストを自動計算。","etfCost",
  [ni("investAmount","投資額",unit="万円",default=1000,max=100000,step=10),ni("expenseRatio","経費率",unit="%",default=0.1,min=0,max=5,step=0.01),ni("years","投資期間",unit="年",default=20,min=1,max=40,step=1),ni("annualReturn","想定リターン",unit="%",default=5,max=30,step=0.1)],
  [o("totalCost","累計コスト","currency",True),o("costImpact","コストによるリターン減少","currency"),o("withoutCost","コストなしの場合の資産","currency"),o("withCost","コスト込みの最終資産","currency")],
  "<h3>経費率の影響</h3><p>経費率0.1%と1%の差は20年で投資額の20%以上のリターン差になることがあります。</p>",
  [{"question":"経費率0.1%と1%の差は？","answer":"1000万円を20年運用すると、約200万円以上の差になります。"},{"question":"低コストETFの目安は？","answer":"インデックスETFは0.1%以下が優秀。0.3%以下なら合格ラインです。"}],
  ["compound-interest","nisa-simulation"]),

c("margin-trading","money","investment","信用取引計算","信用取引の証拠金・レバレッジ・損益を計算。","信用取引計算ツール｜証拠金とレバレッジの損益を自動計算","信用取引の条件を入力して必要証拠金と損益を自動計算。","marginTrading",
  [ni("stockPrice","株価",unit="円",default=2000,max=10000000,step=1),ni("shares","株数",unit="株",default=100,min=1,max=100000,step=100),ni("marginRate","委託保証金率",unit="%",default=30,min=20,max=100,step=1),ni("priceChange","値動き",unit="%",default=5,min=-50,max=100,step=0.1)],
  [o("tradeAmount","約定代金","currency"),o("requiredMargin","必要証拠金","currency",True),o("leverage","レバレッジ","number"),o("profitLoss","損益","currency"),o("returnRate","証拠金に対するリターン","percent")],
  "<h3>信用取引</h3><p>証拠金の約3.3倍の取引が可能。利益も損失も約3.3倍に。追証（追加証拠金）のリスクあり。</p>",
  [{"question":"追証とは？","answer":"保証金率が維持率（通常20%）を下回ると追加入金が必要になります。"},{"question":"信用取引のリスクは？","answer":"レバレッジにより損失が拡大します。投資額以上の損失が出る可能性もあります。"}],
  ["stock-profit","forex-profit"]),

c("gold-investment","money","investment","金投資計算","金の購入量・価格から投資額と損益を計算。","金投資計算ツール｜金の投資損益を自動計算","金の購入・売却価格を入力して投資損益を自動計算。","goldInvestment",
  [ni("purchasePrice","購入時の金価格",unit="円/g",default=10000,max=100000,step=100),ni("currentPrice","現在の金価格",unit="円/g",default=12000,max=100000,step=100),ni("grams","保有量",unit="g",default=100,min=0.1,max=100000,step=0.1)],
  [o("investmentAmount","投資額","currency"),o("currentValue","現在の評価額","currency"),o("profitLoss","損益","currency",True),o("returnRate","リターン","percent")],
  "<h3>金投資</h3><p>インフレヘッジ・有事の資産として人気。現物、ETF、積立など投資方法は多様です。</p>",
  [{"question":"金に投資するメリットは？","answer":"インフレに強い、通貨価値の下落ヘッジ、株式との相関が低い分散効果があります。"},{"question":"純金積立とは？","answer":"毎月一定額で金を購入する積立投資。少額（月1,000円〜）から始められます。"}],
  ["compound-interest","asset-allocation"]),

# ===== money/loan (3) =====
c("personal-loan","money","loan","フリーローン計算","フリーローンの月返済額と利息を計算。","フリーローン計算ツール｜月返済額と利息を自動計算","フリーローンの借入額と金利から月返済額を自動計算。","personalLoan",
  [ni("amount","借入額",unit="万円",default=100,max=10000,step=1),ni("rate","年利",unit="%",default=8,max=20,step=0.1),ni("years","返済期間",unit="年",default=5,min=1,max=10,step=1)],
  [o("monthlyPayment","月返済額","currency",True),o("totalPayment","返済総額","currency"),o("totalInterest","利息合計","currency")],
  "<h3>フリーローン</h3><p>使途自由のローン。金利は銀行系3〜14%、消費者金融系3〜18%程度。</p>",
  [{"question":"カードローンとの違いは？","answer":"フリーローンは一度の借入、カードローンは限度額内で繰り返し借入可能です。"},{"question":"審査は厳しい？","answer":"銀行系は厳しめ、消費者金融系は比較的通りやすいですが金利が高いです。"}],
  ["credit-card-interest","debt-repayment"]),

c("advance-payment","money","loan","繰上返済効果計算","住宅ローンの繰上返済による利息削減効果を計算。","繰上返済効果計算ツール｜住宅ローンの利息削減額を自動計算","繰上返済額を入力して利息削減効果と返済期間短縮を自動計算。","advancePayment",
  [ni("loanBalance","ローン残高",unit="万円",default=3000,max=100000,step=10),ni("rate","金利",unit="%",default=1,max=10,step=0.01),ni("remainingYears","残り返済期間",unit="年",default=25,min=1,max=35,step=1),ni("advanceAmount","繰上返済額",unit="万円",default=200,max=50000,step=10),si("type","繰上返済の種類",[{"value":"term","label":"期間短縮型"},{"value":"amount","label":"返済額軽減型"}],"term")],
  [o("interestSaved","利息削減額","currency",True),o("termReduction","期間短縮","text"),o("monthlyReduction","月返済額の変化","currency")],
  "<h3>繰上返済</h3><p>期間短縮型: 返済期間が短くなり利息削減効果が大きい。返済額軽減型: 月々の返済額が減る。</p>",
  [{"question":"どちらの型がお得？","answer":"利息削減効果は期間短縮型の方が大きいです。月の負担を減らしたいなら返済額軽減型。"},{"question":"手数料はかかる？","answer":"銀行により異なります。ネット銀行は無料のところが多いです。"}],
  ["housing-loan","refinance"]),

c("car-lease","money","loan","カーリース計算","カーリースの月額と購入の比較計算。","カーリース計算ツール｜リースと購入の総コストを自動比較","カーリースと現金購入・ローン購入の総コストを自動比較計算。","carLease",
  [ni("carPrice","車両価格",unit="万円",default=300,max=10000,step=10),ni("leaseMonthly","リース月額",unit="万円",default=3.5,max=20,step=0.1),ni("leaseYears","リース期間",unit="年",default=5,min=1,max=9,step=1),ni("residualRate","残価率",unit="%",default=30,min=0,max=80,step=1)],
  [o("leaseTotalCost","リース総額","currency"),o("purchaseTotalCost","購入の場合の総コスト","currency"),o("difference","差額","currency",True),o("monthlyDiff","月額差額","currency")],
  "<h3>カーリース vs 購入</h3><p>リースは頭金不要で月々定額。ただし走行距離制限あり。5年以上乗るなら購入の方がお得なことが多いです。</p>",
  [{"question":"リースのメリットは？","answer":"頭金不要、税金・車検込みで月々定額、常に新しい車に乗れることです。"},{"question":"リースのデメリットは？","answer":"走行距離制限、カスタマイズ不可、中途解約で違約金が発生します。"}],
  ["car-loan","car-cost"]),

# ===== money/insurance (3) =====
c("disability-insurance","money","insurance","就業不能保険計算","就業不能時に必要な保障額を計算。","就業不能保険計算ツール｜必要な保障額を自動計算","月収と固定費を入力して就業不能時に必要な保障額を自動計算。","disabilityInsurance",
  [ni("monthlyIncome","月収",unit="万円",default=30,max=500,step=1),ni("monthlyExpense","月の固定費",unit="万円",default=20,max=300,step=1),ni("publicBenefit","公的給付（傷病手当金等）",unit="万円",default=15,max=200,step=1)],
  [o("monthlyShortfall","月額不足額","currency",True),o("annualShortfall","年間不足額","currency"),o("recommendedCoverage","推奨保障額（月額）","currency")],
  "<h3>就業不能リスク</h3><p>病気やケガで働けなくなった場合、傷病手当金（給与の2/3、最長1年6ヶ月）の後は収入が途絶えます。</p>",
  [{"question":"傷病手当金とは？","answer":"健保加入者が病気で休業した場合、標準報酬日額の2/3が最長1年6ヶ月支給されます。"},{"question":"自営業者は？","answer":"国保には傷病手当金がないため、民間の就業不能保険の重要性が高いです。"}],
  ["life-insurance","social-insurance"]),

c("pet-insurance","money","insurance","ペット保険料計算","ペットの年齢・種類から保険料の概算を計算。","ペット保険料計算ツール｜犬猫の保険料を自動概算","ペットの年齢と種類から保険料の月額目安を自動計算。","petInsurance",
  [si("petType","ペットの種類",[{"value":"dog_small","label":"小型犬"},{"value":"dog_medium","label":"中型犬"},{"value":"dog_large","label":"大型犬"},{"value":"cat","label":"猫"}],"dog_small"),ni("age","年齢",unit="歳",default=3,min=0,max=15,step=1),si("coverage","補償割合",[{"value":"50","label":"50%"},{"value":"70","label":"70%"},{"value":"100","label":"100%"}],"70")],
  [o("monthlyPremium","月額保険料（概算）","currency",True),o("annualPremium","年額保険料","currency"),o("lifetime","生涯保険料（概算）","currency")],
  "<h3>ペット保険</h3><p>年齢が上がるほど保険料UP。大型犬>小型犬>猫の順で高い傾向。補償割合は50〜100%。</p>",
  [{"question":"ペット保険は必要？","answer":"手術費は数十万円になることも。高齢になるほど加入しにくいため早めの検討を。"},{"question":"いくらくらい？","answer":"小型犬・猫で月2,000〜5,000円、大型犬で月3,000〜8,000円程度です。"}],
  ["life-insurance","car-insurance"]),

c("travel-insurance","money","insurance","海外旅行保険計算","渡航先・日数から海外旅行保険料の概算を計算。","海外旅行保険計算ツール｜渡航先から保険料を自動概算","渡航先と旅行日数を入力して海外旅行保険料の目安を自動計算。","travelInsurance",
  [si("destination","渡航先",[{"value":"asia","label":"アジア"},{"value":"europe","label":"ヨーロッパ"},{"value":"usa","label":"アメリカ"},{"value":"oceania","label":"オセアニア"}],"asia"),ni("days","旅行日数",unit="日",default=7,min=1,max=90,step=1),si("plan","プラン",[{"value":"basic","label":"エコノミー"},{"value":"standard","label":"スタンダード"},{"value":"premium","label":"プレミアム"}],"standard")],
  [o("premium","保険料","currency",True),o("medicalCoverage","治療費用保障","currency"),o("liabilityCoverage","賠償責任保障","currency")],
  "<h3>海外旅行保険</h3><p>海外の医療費は高額。アメリカでは盲腸手術で300万円以上かかることも。クレジットカード付帯保険では不十分な場合が多いです。</p>",
  [{"question":"クレカ付帯で十分？","answer":"治療費の上限が低い（100〜300万円）ため、アメリカ等では不十分です。"},{"question":"持病があっても入れる？","answer":"告知事項によりますが、持病のある方向けのプランもあります。"}],
  ["car-insurance","life-insurance"]),

# ===== money/real-estate (3) =====
c("initial-cost","money","real-estate","賃貸初期費用計算","賃貸契約の初期費用（敷金・礼金・仲介手数料等）を概算。","賃貸初期費用計算ツール｜引越しに必要な初期費用を自動計算","家賃を入力するだけで賃貸契約にかかる初期費用の概算を自動計算。","initialCost",
  [ni("rent","月額家賃",unit="円",default=80000,max=500000,step=1000),ni("deposit","敷金",unit="ヶ月",default=1,max=6,step=0.5),ni("keyMoney","礼金",unit="ヶ月",default=1,max=3,step=0.5),ni("agentFee","仲介手数料",unit="ヶ月",default=1,max=1,step=0.5)],
  [o("depositAmount","敷金","currency"),o("keyMoneyAmount","礼金","currency"),o("agentFeeAmount","仲介手数料","currency"),o("firstMonth","前家賃","currency"),o("totalInitial","初期費用合計","currency",True)],
  "<h3>賃貸の初期費用</h3><p>一般的に家賃の4〜6ヶ月分。敷金1+礼金1+仲介手数料1+前家賃1+保証料0.5+火災保険=約4.5ヶ月分。</p>",
  [{"question":"初期費用を抑えるには？","answer":"敷金・礼金ゼロ物件、フリーレント、仲介手数料半額の不動産会社を探しましょう。"},{"question":"保証料とは？","answer":"保証会社に支払う費用。家賃の0.5〜1ヶ月分。連帯保証人の代わりです。"}],
  ["rent-calculator","moving-cost"]),

c("land-price","money","real-estate","坪単価・㎡単価変換","坪単価と㎡単価を相互変換。面積からの総額計算。","坪単価⇔㎡単価変換ツール｜不動産の価格を自動変換","坪単価と㎡単価を自動変換。土地面積からの総額計算にも対応。","landPrice",
  [ni("pricePerTsubo","坪単価",unit="万円/坪",default=100,max=10000,step=1),ni("areaTsubo","面積",unit="坪",default=30,max=10000,step=0.1)],
  [o("pricePerM2","㎡単価","currency",True),o("totalPrice","総額","currency"),o("areaM2","面積（㎡）","number")],
  "<h3>坪と㎡の換算</h3><p>1坪 = 約3.3058㎡。坪単価×3.3 ≒ ㎡単価。</p>",
  [{"question":"1坪は何㎡？","answer":"約3.3058㎡です。畳2枚分が1坪です。"},{"question":"坪単価100万円は高い？","answer":"東京23区の住宅地平均は200〜400万円/坪。地方都市は10〜50万円/坪程度です。"}],
  ["property-yield","rent-vs-buy"]),

c("yield-comparison","money","real-estate","不動産利回り比較","表面利回りと実質利回りを比較計算。","不動産利回り比較ツール｜表面利回りと実質利回りを自動計算","物件価格と家賃から表面利回りと実質利回りを比較計算。","yieldComparison",
  [ni("propertyPrice","物件価格",unit="万円",default=3000,max=1000000,step=10),ni("monthlyRent","月額家賃",unit="万円",default=15,max=500,step=0.5),ni("annualExpense","年間経費",unit="万円",default=50,max=10000,step=1),ni("vacancy","空室率",unit="%",default=5,max=50,step=1)],
  [o("grossYield","表面利回り","percent",True),o("netYield","実質利回り","percent"),o("annualIncome","年間家賃収入","currency"),o("annualNetIncome","年間純収益","currency")],
  "<h3>不動産利回り</h3><p>表面利回り = 年間家賃÷物件価格。実質利回り = (年間家賃−経費)÷物件価格。実質利回りで判断すべきです。</p>",
  [{"question":"利回り何%なら投資すべき？","answer":"実質利回り4%以上が目安。5%以上なら優秀です。"},{"question":"表面利回りだけで判断していい？","answer":"いいえ。管理費・修繕費・税金・空室損失を引いた実質利回りで判断しましょう。"}],
  ["property-yield","rent-vs-buy"]),

# ===== life (various) 15 =====
c("bmi-pet","health","body","ペットBCS計算","犬猫の体型スコア（BCS）と適正体重を概算。","犬猫の体型スコア計算ツール｜ペットの適正体重を自動計算","犬猫の体重と理想体重を入力して体型スコアを自動判定。","bmiPet",
  [ni("weight","現在の体重",unit="kg",default=5,min=0.1,max=100,step=0.1),ni("idealWeight","理想体重",unit="kg",default=4.5,min=0.1,max=100,step=0.1)],
  [o("bcsScore","BCS（体型スコア）","text",True),o("weightDiff","理想体重との差","number"),o("overweightPercent","肥満度","percent")],
  "<h3>BCS（Body Condition Score）</h3><p>1〜9の9段階。4〜5が理想。6以上は肥満傾向。犬猫の肥満は関節疾患や糖尿病のリスクを高めます。</p>",
  [{"question":"犬猫の理想体重は？","answer":"品種により異なります。成犬・成猫になった時の体重が目安。かかりつけ獣医に確認しましょう。"},{"question":"ダイエットさせるには？","answer":"フード量を10〜20%減らす、低カロリーフードに切り替える、遊び時間を増やすのが基本です。"}],
  ["bmi","pet-age"]),

c("packing-list","life","shopping","旅行持ち物チェック計算","旅行日数・渡航先から必要な着替え・持ち物量を計算。","旅行持ち物計算ツール｜日数に応じた持ち物量を自動計算","旅行日数を入力して必要な着替え枚数や荷物の目安量を自動計算。","packingList",
  [ni("days","旅行日数",unit="日",default=5,min=1,max=30,step=1),si("season","季節",[{"value":"spring","label":"春"},{"value":"summer","label":"夏"},{"value":"autumn","label":"秋"},{"value":"winter","label":"冬"}],"summer"),si("laundry","洗濯可能",[{"value":"yes","label":"あり"},{"value":"no","label":"なし"}],"no")],
  [o("tops","トップス","number",True),o("bottoms","ボトムス","number"),o("underwear","下着","number"),o("socks","靴下","number")],
  "<h3>持ち物の目安</h3><p>洗濯なし: トップス=日数分、下着=日数分。洗濯あり: 3日分+予備1でOK。</p>",
  [{"question":"7日間で洗濯なしの場合？","answer":"トップス7枚、ボトムス3枚、下着7セットが目安です。"},{"question":"荷物を減らすコツは？","answer":"圧縮袋、着回しやすい色で統一、現地調達を活用しましょう。"}],
  ["tip-calculator","currency-convert"]),

c("screen-size","life","unit","画面サイズ計算","インチから画面の実寸（cm）を計算。","画面サイズ計算ツール｜インチから実際のサイズ（cm）を自動計算","画面のインチ数とアスペクト比から実際の縦横サイズを自動計算。","screenSize",
  [ni("inches","画面サイズ",unit="インチ",default=27,min=1,max=200,step=0.1),si("ratio","アスペクト比",[{"value":"16:9","label":"16:9（一般的）"},{"value":"16:10","label":"16:10"},{"value":"21:9","label":"21:9（ウルトラワイド）"},{"value":"4:3","label":"4:3（旧型）"}],"16:9")],
  [o("widthCm","横幅","number",True),o("heightCm","縦幅","number"),o("areaCm2","画面面積","number"),o("diagonalCm","対角線","number")],
  "<h3>画面サイズの計算</h3><p>インチは対角線の長さ。1インチ=2.54cm。同じインチでもアスペクト比で実寸が変わります。</p>",
  [{"question":"27インチの実際のサイズは？","answer":"16:9の場合、横約60cm×縦約34cmです。"},{"question":"テレビの視聴距離の目安は？","answer":"4K: 画面高さの1.5倍、フルHD: 3倍が推奨距離です。"}],
  ["length","area"]),

c("tsubo-m2","life","unit","坪・畳・㎡変換","坪・畳・㎡・平方フィートを相互変換。","坪⇔畳⇔㎡変換ツール｜面積の単位を自動変換","坪・畳・㎡・平方フィートを相互変換。部屋の広さの確認に。","tsuboM2",
  [ni("value","数値",default=6,max=100000,step=0.1),si("fromUnit","変換元",[{"value":"tsubo","label":"坪"},{"value":"jo","label":"畳（帖）"},{"value":"m2","label":"㎡"},{"value":"sqft","label":"平方フィート"}],"jo")],
  [o("tsubo","坪","number"),o("jo","畳","number",True),o("m2","㎡","number"),o("sqft","平方フィート","number")],
  "<h3>面積の換算</h3><p>1坪 ≒ 3.306㎡ ≒ 2畳。6畳 = 約3坪 = 約9.9㎡。</p>",
  [{"question":"6畳は何㎡？","answer":"約9.72㎡（1畳=約1.62㎡）。ただし地域により畳のサイズが異なります。"},{"question":"京間と江戸間の違い？","answer":"京間(191×95.5cm)は江戸間(176×88cm)より約10%広いです。"}],
  ["area","land-price"]),

c("postal-rate","life","shopping","郵便料金計算","封書・はがき・荷物の郵便料金を計算。","郵便料金計算ツール｜サイズと重さから送料を自動計算","郵便物のサイズと重さを入力して郵便料金を自動計算。","postalRate",
  [si("type","郵便の種類",[{"value":"letter_standard","label":"定形郵便"},{"value":"letter_nonstandard","label":"定形外郵便"},{"value":"postcard","label":"はがき"},{"value":"parcel","label":"ゆうパック"}],"letter_standard"),ni("weight","重さ",unit="g",default=25,max=30000,step=1)],
  [o("postage","郵便料金","currency",True)],
  "<h3>郵便料金（2026年）</h3><p>定形郵便: 110円（25g以下）、定形外: 120円〜。はがき: 85円。ゆうパック: サイズ・地域により異なる。</p>",
  [{"question":"定形と定形外の違い？","answer":"定形: 長辺23.5cm以内、短辺12cm以内、厚さ1cm以内、50g以内。それ以外は定形外です。"},{"question":"速達はいくら追加？","answer":"250gまで+260円、1kgまで+350円、4kgまで+600円です。"}],
  ["per-unit-price","discount"]),

c("paper-size","life","unit","用紙サイズ一覧","A判・B判の用紙サイズをmm/cm/inchで表示。","用紙サイズ一覧ツール｜A4・B5等のサイズを自動表示","用紙の規格を選んでサイズをmm・cm・inchで表示。面積計算も。","paperSize",
  [si("size","用紙規格",[{"value":"A3","label":"A3"},{"value":"A4","label":"A4"},{"value":"A5","label":"A5"},{"value":"B4","label":"B4"},{"value":"B5","label":"B5"},{"value":"letter","label":"レター（US）"}],"A4")],
  [o("widthMm","幅（mm）","number",True),o("heightMm","高さ（mm）","number"),o("widthInch","幅（inch）","number"),o("heightInch","高さ（inch）","number"),o("areaCm2","面積（cm²）","number")],
  "<h3>主な用紙サイズ</h3><p>A4: 210×297mm、A3: 297×420mm、B5: 182×257mm、B4: 257×364mm。</p>",
  [{"question":"A4とレターの違い？","answer":"A4は210×297mm、レターは215.9×279.4mm。レターの方が幅広で短いです。"},{"question":"A判の法則は？","answer":"A0（841×1189mm）を半分にするとA1、さらに半分でA2…と続きます。面積が半分ずつ。"}],
  ["area","length"]),

# ===== health (5) =====
c("caffeine","health","calorie","カフェイン摂取量計算","コーヒー・お茶の摂取量からカフェイン量を計算。","カフェイン摂取量計算ツール｜1日のカフェイン量を自動計算","コーヒーやお茶の杯数からカフェイン摂取量を自動計算。","caffeine",
  [ni("coffee","コーヒー",unit="杯",default=3,max=20,step=1),ni("tea","紅茶",unit="杯",default=1,max=20,step=1),ni("greenTea","緑茶",unit="杯",default=2,max=20,step=1),ni("energyDrink","エナジードリンク",unit="本",default=0,max=10,step=1)],
  [o("totalCaffeine","1日のカフェイン合計","number",True),o("status","判定","text"),o("safeLimit","安全上限との差","number")],
  "<h3>カフェイン含有量の目安</h3><p>コーヒー1杯(150ml): 90mg、紅茶1杯: 50mg、緑茶1杯: 30mg、エナジードリンク1本: 80〜150mg。</p>",
  [{"question":"1日の安全上限は？","answer":"健康な成人で400mg以下（コーヒー約4杯分）。妊婦は200mg以下が推奨です。"},{"question":"カフェインの効果持続時間は？","answer":"約3〜5時間。半減期は約5時間。午後3時以降は睡眠に影響する可能性があります。"}],
  ["alcohol-calorie","daily-calorie"]),

c("protein-need","health","calorie","タンパク質必要量計算","体重と活動量から1日に必要なタンパク質量を計算。","タンパク質必要量計算ツール｜1日の適正摂取量を自動計算","体重と運動量を入力して1日に必要なタンパク質量を自動計算。","proteinNeed",
  [ni("weight","体重",unit="kg",default=65,min=30,max=200,step=1),si("activity","活動レベル",[{"value":"sedentary","label":"デスクワーク"},{"value":"moderate","label":"週2〜3回運動"},{"value":"active","label":"週4〜5回運動"},{"value":"athlete","label":"アスリート"}],"moderate")],
  [o("dailyProtein","1日の推奨タンパク質量","number",True),o("perMeal","1食あたり（3食の場合）","number"),o("chickenBreast","鶏むね肉換算","number"),o("eggs","卵換算","number")],
  "<h3>タンパク質の必要量</h3><p>一般成人: 体重×0.8〜1g、運動する人: 体重×1.2〜1.6g、アスリート: 体重×1.6〜2g。</p>",
  [{"question":"プロテインは必要？","answer":"食事だけで十分な量を摂れるなら不要。食事で足りない場合の補助として有効です。"},{"question":"タンパク質の摂りすぎは？","answer":"腎臓に負担がかかる可能性。体重×2gを超えないのが目安です。"}],
  ["meal-calorie","daily-calorie","basal-metabolism"]),

c("vision-test","health","medical","視力換算","小数視力・分数視力・logMAR値を相互換算。","視力換算ツール｜小数視力⇔分数視力を自動変換","日本式の小数視力と海外の分数視力を自動換算。","visionTest",
  [ni("decimalVision","小数視力",default=1.0,min=0.01,max=2.0,step=0.01)],
  [o("fraction","分数視力（米国式）","text",True),o("logmar","logMAR値","number"),o("status","区分","text")],
  "<h3>視力の表記</h3><p>日本: 小数視力（1.0が正常）。米国: 分数視力（20/20が正常）。1.0 = 20/20 = logMAR 0.0。</p>",
  [{"question":"視力1.0は良い方？","answer":"正常視力です。2.0は非常に良い視力。0.3以下は矯正が推奨されます。"},{"question":"20/20とは？","answer":"20フィート（約6m）離れて20フィート相当の文字が見える=正常視力です。"}],
  ["medical-expense"]),

c("hearing-level","health","medical","騒音レベル計算","日常の音のデシベル値と聴覚への影響を表示。","騒音レベル計算ツール｜デシベル値と聴覚リスクを自動表示","デシベル値を入力して音の大きさの目安と聴覚への影響を自動判定。","hearingLevel",
  [ni("decibel","音の大きさ",unit="dB",default=80,max=200,step=1)],
  [o("comparison","音の比較例","text",True),o("risk","聴覚リスク","text"),o("safeExposure","安全な曝露時間","text")],
  "<h3>デシベルの目安</h3><p>30dB: ささやき声、50dB: 静かな事務所、70dB: 掃除機、85dB: 騒がしい交通、100dB: ライブ会場、120dB: ジェット機（苦痛レベル）</p>",
  [{"question":"何dBから危険？","answer":"85dB以上の長時間曝露で聴覚に影響。100dB以上は短時間でもリスクがあります。"},{"question":"イヤホンは何dB？","answer":"最大音量の60%で約80〜85dB。1日1時間以内が推奨です。"}],
  ["blood-alcohol"]),

c("menstrual-cycle","health","pregnancy","生理周期計算","生理周期のパターンから次回生理日を予測。","生理周期計算ツール｜次回の生理開始日を自動予測","過去の生理開始日から周期パターンを分析して次回を予測。","menstrualCycle",
  [{"id":"lastPeriod","label":"前回の生理開始日","type":"date","default":"2026-03-01"},ni("cycleLength","生理周期",unit="日",default=28,min=21,max=45,step=1),ni("periodLength","生理期間",unit="日",default=5,min=2,max=10,step=1)],
  [o("nextPeriod","次回生理予定日","text",True),o("lutealPhase","黄体期開始","text"),o("pmsStart","PMS開始目安","text")],
  "<h3>生理周期</h3><p>正常な周期は25〜38日。黄体期（排卵後〜次の生理まで）は約14日で比較的安定しています。</p>",
  [{"question":"正常な周期は？","answer":"25〜38日で、周期のばらつきが6日以内なら正常です。"},{"question":"PMSとは？","answer":"月経前症候群。生理の3〜10日前に起こる身体的・精神的な症状です。"}],
  ["ovulation-day","due-date"]),

# ===== business (5) =====
c("payback-period","business","accounting","回収期間計算","投資の回収期間（ペイバック期間）を計算。","回収期間計算ツール｜投資の元が取れる期間を自動計算","投資額と年間収益を入力して投資の回収期間を自動計算。","paybackPeriod",
  [ni("investment","初期投資額",unit="万円",default=1000,max=10000000,step=10),ni("annualReturn","年間利益",unit="万円",default=300,max=10000000,step=10),ni("annualCost","年間コスト",unit="万円",default=100,max=10000000,step=10)],
  [o("paybackYears","回収期間","number",True),o("annualNetReturn","年間純利益","currency"),o("roi5year","5年ROI","percent")],
  "<h3>回収期間とは</h3><p>投資額÷年間純利益。短いほど良い投資。一般的に3年以内が望ましいとされます。</p>",
  [{"question":"何年以内なら良い投資？","answer":"業種により異なりますが、一般的に3〜5年以内が基準です。"},{"question":"NPVとの違いは？","answer":"回収期間は時間価値を考慮しない簡便な方法。正確にはNPV(正味現在価値)で判断すべきです。"}],
  ["roi","break-even"]),

c("ltv","business","accounting","顧客生涯価値（LTV）計算","顧客のLTV（ライフタイムバリュー）を計算。","LTV計算ツール｜顧客生涯価値を自動計算","平均購入額と購入頻度からLTVを自動計算。","ltv",
  [ni("avgOrderValue","平均購入単価",unit="円",default=5000,max=10000000,step=100),ni("purchaseFrequency","年間購入回数",unit="回",default=4,max=365,step=1),ni("customerLifespan","顧客継続年数",unit="年",default=3,min=0.5,max=30,step=0.5),ni("grossMarginRate","粗利率",unit="%",default=40,max=100,step=1)],
  [o("ltv","LTV（売上ベース）","currency",True),o("ltvProfit","LTV（利益ベース）","currency"),o("annualRevenue","年間売上/顧客","currency"),o("cac_limit","許容CAC上限","currency")],
  "<h3>LTVとは</h3><p>LTV = 平均購入単価 × 購入頻度 × 継続年数。CACの3倍以上が健全な水準。</p>",
  [{"question":"LTVが重要な理由は？","answer":"新規顧客獲得コスト(CAC)の上限を決める指標。LTV > CACでないと赤字です。"},{"question":"LTVを上げるには？","answer":"購入単価UP、購入頻度UP、継続率UP（解約率DOWN）の3つのレバーがあります。"}],
  ["roi","break-even"]),

c("churn-rate","business","accounting","解約率計算","月次・年次の解約率（チャーンレート）を計算。","解約率計算ツール｜SaaSのチャーンレートを自動計算","期首顧客数と解約数から月次・年次の解約率を自動計算。","churnRate",
  [ni("startCustomers","期首の顧客数",unit="人",default=100,max=1000000,step=1),ni("churned","期間中の解約数",unit="人",default=5,max=1000000,step=1),ni("period","計算期間",unit="ヶ月",default=1,min=1,max=12,step=1)],
  [o("monthlyChurn","月次解約率","percent",True),o("annualChurn","年間解約率（概算）","percent"),o("avgLifespan","平均顧客寿命","number"),o("retentionRate","継続率","percent")],
  "<h3>解約率（チャーンレート）</h3><p>月次解約率 = 解約数÷期首顧客数。SaaSでは月3%以下が目安。1%以下なら優秀。</p>",
  [{"question":"月3%の年間解約率は？","answer":"1-(1-0.03)^12 ≒ 30.7%。年間で約3割の顧客が離脱します。"},{"question":"チャーンを下げるには？","answer":"オンボーディング強化、カスタマーサクセス、プロダクト改善が3大施策です。"}],
  ["ltv","break-even"]),

c("email-marketing","business","freelance","メルマガ配信効果計算","メールマーケティングの開封率・クリック率から売上予測。","メルマガ効果計算ツール｜配信数からの売上を自動予測","配信数と開封率・CVRを入力してメルマガの売上効果を自動計算。","emailMarketing",
  [ni("subscribers","配信数",unit="通",default=10000,max=10000000,step=100),ni("openRate","開封率",unit="%",default=20,max=100,step=0.1),ni("clickRate","クリック率",unit="%",default=3,max=100,step=0.1),ni("cvr","CVR（購入率）",unit="%",default=2,max=100,step=0.1),ni("avgOrderValue","平均購入単価",unit="円",default=5000,max=1000000,step=100)],
  [o("opens","開封数","number"),o("clicks","クリック数","number"),o("conversions","CV数","number",True),o("revenue","売上予測","currency")],
  "<h3>メルマガの平均値</h3><p>開封率: 15〜25%、クリック率: 2〜5%、CVR: 1〜3%。業種により大きく異なります。</p>",
  [{"question":"開封率を上げるには？","answer":"件名の工夫、配信時間の最適化、セグメント配信が効果的です。"},{"question":"配信頻度の目安は？","answer":"ECなら週1〜2回、BtoBなら月2〜4回が一般的です。"}],
  ["freelance-rate","roi"]),

c("ad-roas","business","freelance","広告ROAS計算","広告費に対するROAS（費用対効果）を計算。","広告ROAS計算ツール｜広告費用対効果を自動計算","広告費と売上を入力してROASとCPAを自動計算。","adRoas",
  [ni("adSpend","広告費","万円",default=50,max=10000000,step=1),ni("revenue","広告経由売上",unit="万円",default=200,max=10000000,step=1),ni("conversions","CV数",unit="件",default=50,max=1000000,step=1)],
  [o("roas","ROAS","percent",True),o("cpa","CPA（顧客獲得単価）","currency"),o("profit","利益（広告費差引後）","currency")],
  "<h3>ROAS</h3><p>ROAS = 広告経由売上÷広告費×100。200%以上（2倍以上）が目安。粗利率を考慮して判断。</p>",
  [{"question":"ROASとROIの違いは？","answer":"ROASは売上ベース、ROIは利益ベース。ROAS 200%でも粗利率50%ならROI 0%です。"},{"question":"CPAの目安は？","answer":"LTVの1/3以下が健全。商材により数百円〜数万円まで幅があります。"}],
  ["roi","ltv"]),

# ===== math (5) =====
c("matrix","math","basic","行列計算","2×2行列の加算・乗算・行列式・逆行列を計算。","行列計算ツール｜2×2行列の演算を自動計算","2×2行列の要素を入力して行列式や逆行列を自動計算。","matrix",
  [ni("a11","a₁₁",default=1,min=-999,max=999),ni("a12","a₁₂",default=2,min=-999,max=999),ni("a21","a₂₁",default=3,min=-999,max=999),ni("a22","a₂₂",default=4,min=-999,max=999)],
  [o("determinant","行列式","number",True),o("inverse","逆行列","text"),o("trace","トレース","number")],
  "<h3>行列の基本</h3><p>行列式(det) = a₁₁×a₂₂ - a₁₂×a₂₁。det≠0なら逆行列が存在します。</p>",
  [{"question":"行列式が0だと？","answer":"逆行列が存在しません（特異行列）。連立方程式が解なしまたは無限解になります。"},{"question":"行列は何に使う？","answer":"連立方程式、CG、機械学習、量子力学、経済学など幅広く使われます。"}],
  ["power","logarithm"]),

c("quadratic","math","basic","二次方程式の解計算","ax²+bx+c=0の解を計算。判別式で解の種類も判定。","二次方程式の解計算ツール｜解の公式を自動計算","係数a,b,cを入力して二次方程式の解を自動計算。","quadratic",
  [ni("a","係数a",default=1,min=-999,max=999),ni("b","係数b",default=-5,min=-999,max=999),ni("c_val","係数c",default=6,min=-999,max=999)],
  [o("x1","解x₁","number",True),o("x2","解x₂","number"),o("discriminant","判別式D","number"),o("solutionType","解の種類","text")],
  "<h3>解の公式</h3><p>x = (-b ± √(b²-4ac)) / 2a。判別式D = b²-4ac。D>0: 異なる2実数解、D=0: 重解、D<0: 虚数解。</p>",
  [{"question":"判別式が負だと？","answer":"実数解なし。虚数解（複素数解）になります。"},{"question":"解と係数の関係は？","answer":"x₁+x₂ = -b/a、x₁×x₂ = c/a"}],
  ["power","square-root"]),

c("trigonometry","math","basic","三角関数計算","角度からsin・cos・tanの値を計算。","三角関数計算ツール｜sin・cos・tanを自動計算","角度を入力してsin・cos・tanの値を自動計算。","trigonometry",
  [ni("angle","角度",unit="度",default=30,min=-360,max=360,step=1)],
  [o("sin","sin","number",True),o("cos","cos","number"),o("tan","tan","number"),o("radian","ラジアン","number")],
  "<h3>主な三角関数の値</h3><p>sin30°=0.5、cos30°=√3/2、tan30°=1/√3。sin45°=cos45°=1/√2。sin60°=√3/2。</p>",
  [{"question":"度とラジアンの違い？","answer":"360度=2πラジアン。ラジアン=度×π/180。"},{"question":"三角関数は何に使う？","answer":"物理学（波・振動）、工学（電気回路）、測量、CG、音声処理などに使われます。"}],
  ["pythagorean","circle"]),

c("polygon-area","math","geometry","正多角形の面積計算","正n角形の一辺から面積を計算。","正多角形の面積計算ツール｜辺の数と長さから面積を自動計算","正多角形の辺の数と一辺の長さを入力して面積を自動計算。","polygonArea",
  [ni("sides","辺の数",unit="辺",default=5,min=3,max=100,step=1),ni("sideLength","一辺の長さ",unit="cm",default=5,max=99999,step=0.1)],
  [o("area","面積","number",True),o("perimeter","周長","number"),o("inradius","内接円の半径","number"),o("circumradius","外接円の半径","number")],
  "<h3>正多角形の面積</h3><p>面積 = (n × a² × cot(π/n)) / 4。nが大きくなるほど円に近づきます。</p>",
  [{"question":"正100角形は円に近い？","answer":"はい。辺の数が増えるほど面積は円に近づきます。正100角形は円との差が0.03%以下です。"},{"question":"内角の計算は？","answer":"正n角形の1つの内角 = (n-2)×180°/n。正五角形は108度。"}],
  ["hexagon","circle","triangle"]),

c("normal-distribution","math","statistics","正規分布計算","平均と標準偏差から正規分布の確率を計算。","正規分布計算ツール｜z値と確率を自動計算","平均・標準偏差・値を入力してz値と確率を自動計算。","normalDistribution",
  [ni("mean","平均値",default=0,min=-1000,max=1000,step=0.1),ni("stddev","標準偏差",default=1,min=0.01,max=1000,step=0.1),ni("x","値",default=1,min=-1000,max=1000,step=0.1)],
  [o("zScore","z値","number",True),o("probability","P(X≤x)","percent"),o("upperProbability","P(X>x)","percent")],
  "<h3>正規分布</h3><p>平均±1σに約68%、±2σに約95%、±3σに約99.7%のデータが含まれます。</p>",
  [{"question":"z値とは？","answer":"データが平均から標準偏差何個分離れているかを示す値。z=(x-μ)/σ。"},{"question":"偏差値との関係は？","answer":"偏差値 = z×10+50。z=1なら偏差値60、z=2なら偏差値70です。"}],
  ["hensachi","standard-deviation","average"]),

# ===== education (5) =====
c("vocab-size","education","study","英単語数レベル判定","知っている英単語数から英語レベルを判定。","英単語レベル判定ツール｜語彙数から英語力を自動判定","英単語数を入力して英語レベルとTOEIC目安スコアを自動判定。","vocabSize",
  [ni("words","推定語彙数",unit="語",default=5000,min=100,max=100000,step=100)],
  [o("level","英語レベル","text",True),o("cefrLevel","CEFR","text"),o("toeicEstimate","TOEIC目安","number"),o("equivalent","相当する学年","text")],
  "<h3>語彙数の目安</h3><p>中学卒: 約1,200語、高校卒: 約3,000語、大学卒: 約5,000語、TOEIC900: 約10,000語、ネイティブ: 20,000〜35,000語。</p>",
  [{"question":"何語あればTOEIC700取れる？","answer":"約5,000〜7,000語が目安です。"},{"question":"効率的な単語の覚え方は？","answer":"頻出順に学習、文脈で覚える、間隔反復法（Anki等）が効果的です。"}],
  ["english-score","reading-speed"]),

c("study-plan","education","study","学習計画計算","試験日までに必要な1日の勉強時間を計算。","学習計画計算ツール｜試験日までの勉強時間を自動計算","試験日と総学習時間を入力して1日に必要な勉強時間を自動計算。","studyPlan",
  [ni("totalHours","必要な総学習時間",unit="時間",default=300,max=10000,step=10),ni("daysUntilExam","試験までの日数",unit="日",default=90,min=1,max=365,step=1),ni("availableDays","週の勉強可能日数",unit="日",default=6,min=1,max=7,step=1)],
  [o("dailyHours","1日の勉強時間","number",True),o("weeklyHours","週の勉強時間","number"),o("totalStudyDays","総勉強日数","number")],
  "<h3>学習時間の目安</h3><p>TOEIC700: 約500時間、日商簿記2級: 約300時間、宅建: 約300時間、FP2級: 約200時間。</p>",
  [{"question":"1日何時間が限界？","answer":"集中力は90分が限界。休憩を挟んで1日4〜6時間が効率的な上限です。"},{"question":"毎日やるべき？","answer":"毎日少しずつ（1〜2時間）>週末まとめて（10時間）。記憶の定着に差が出ます。"}],
  ["study-time","reading-speed"]),

c("school-supplies","education","school","入学準備費用計算","小学校・中学校の入学準備にかかる費用を概算。","入学準備費用計算ツール｜必要な費用を項目別に自動計算","入学する学校の種類を選んで準備費用の概算を自動計算。","schoolSupplies",
  [si("schoolType","学校",[{"value":"elementary_public","label":"公立小学校"},{"value":"elementary_private","label":"私立小学校"},{"value":"junior_public","label":"公立中学校"},{"value":"junior_private","label":"私立中学校"},{"value":"high_public","label":"公立高校"},{"value":"high_private","label":"私立高校"}],"elementary_public")],
  [o("uniformCost","制服・体操着","currency"),o("suppliesCost","学用品","currency"),o("otherCost","その他","currency"),o("totalCost","合計","currency",True)],
  "<h3>入学準備費用の目安</h3><p>公立小学校: 5〜10万円、私立小学校: 20〜40万円、公立中学校: 10〜15万円、私立中学校: 25〜50万円。</p>",
  [{"question":"就学援助制度とは？","answer":"経済的に困難な家庭に学用品費・給食費等を援助する制度です。各自治体に申請します。"},{"question":"ランドセルの相場は？","answer":"2〜8万円。平均は約5〜6万円。5年間使うことを考えて選びましょう。"}],
  ["tuition-cost","child-cost"]),

c("certification-cost","education","study","資格取得費用計算","主要資格の受験料と学習費用を概算。","資格取得費用計算ツール｜受験料と学習費用を自動計算","資格を選んで受験料と一般的な学習費用を自動概算。","certificationCost",
  [si("cert","資格",[{"value":"toeic","label":"TOEIC"},{"value":"bookkeeping2","label":"日商簿記2級"},{"value":"fp2","label":"FP2級"},{"value":"takken","label":"宅建"},{"value":"ipa_fe","label":"基本情報技術者"},{"value":"cpa","label":"公認会計士"},{"value":"lawyer","label":"司法試験"}],"bookkeeping2"),si("studyMethod","学習方法",[{"value":"self","label":"独学"},{"value":"online","label":"オンライン講座"},{"value":"school","label":"スクール通学"}],"self")],
  [o("examFee","受験料","currency"),o("studyCost","学習費用（概算）","currency",True),o("totalCost","総費用","currency"),o("studyHours","標準学習時間","number")],
  "<h3>主要資格の費用</h3><p>TOEIC: 受験7,810円+教材5,000円〜。簿記2級: 受験5,500円+教材10,000円〜。宅建: 受験8,200円+教材20,000円〜。</p>",
  [{"question":"独学で合格できる？","answer":"簿記2級、FP2級、ITパスポートなどは独学で十分可能です。会計士・司法試験はスクール推奨。"},{"question":"費用対効果の高い資格は？","answer":"宅建（不動産）、FP2級（金融）、日商簿記2級（経理）は汎用性が高くコスパ良好です。"}],
  ["tuition-cost","study-plan"]),

c("school-commute","education","school","通学時間計算","通学距離と手段から所要時間と年間コストを計算。","通学時間計算ツール｜通学の所要時間と年間コストを自動計算","通学距離と手段を入力して所要時間と交通費を自動計算。","schoolCommute",
  [ni("distance","通学距離",unit="km",default=10,max=100,step=0.1),si("method","通学手段",[{"value":"walk","label":"徒歩"},{"value":"bike","label":"自転車"},{"value":"bus","label":"バス"},{"value":"train","label":"電車"},{"value":"car","label":"送迎（車）"}],"train"),ni("monthlyCost","定期代/交通費",unit="円",default=10000,max=100000,step=100)],
  [o("commuteTime","片道所要時間","number",True),o("dailyTime","往復時間","number"),o("annualTime","年間通学時間","number"),o("annualCost","年間交通費","currency")],
  "<h3>通学時間の目安</h3><p>徒歩: 時速4km、自転車: 時速15km、バス: 時速20km、電車: 時速40km（乗換含む）。</p>",
  [{"question":"通学時間の平均は？","answer":"中学生: 約20分、高校生: 約40分、大学生: 約60分が全国平均です。"},{"question":"長時間通学のデメリットは？","answer":"睡眠時間の減少、放課後活動の制限、体力の消耗。片道90分超は検討が必要です。"}],
  ["commute-cost","fuel-cost"]),
]

count = 0
for calc in calcs:
    write_calc(calc)
    count += 1

print(f"Created {count} JSON files")
