// Housing Loan Repayment Calculator
export function loanRepayment(inputs: Record<string, number | string>): Record<string, number> {
  const amountYen = (inputs.amount as number) * 10000;
  const annualRate = (inputs.rate as number) / 100;
  const monthlyRate = annualRate / 12;
  const years = inputs.years as number;
  const totalMonths = years * 12;
  const method = inputs.method as string;

  let monthlyPayment: number;
  let totalPayment: number;

  if (method === 'equal_principal') {
    // Equal principal: monthly principal is constant
    const monthlyPrincipal = amountYen / totalMonths;
    // First month payment (highest)
    monthlyPayment = monthlyPrincipal + amountYen * monthlyRate;
    // Total interest
    let totalInterest = 0;
    for (let i = 0; i < totalMonths; i++) {
      const remainingPrincipal = amountYen - monthlyPrincipal * i;
      totalInterest += remainingPrincipal * monthlyRate;
    }
    totalPayment = amountYen + totalInterest;
  } else {
    // Equal payment (default)
    if (monthlyRate === 0) {
      monthlyPayment = amountYen / totalMonths;
    } else {
      monthlyPayment =
        amountYen * monthlyRate * Math.pow(1 + monthlyRate, totalMonths) /
        (Math.pow(1 + monthlyRate, totalMonths) - 1);
    }
    totalPayment = monthlyPayment * totalMonths;
  }

  const totalInterest = totalPayment - amountYen;

  return {
    monthlyPayment: Math.round(monthlyPayment),
    totalPayment: Math.round(totalPayment),
    totalInterest: Math.round(totalInterest),
  };
}

// Employment Income Deduction (給与所得控除)
function calcEmploymentDeduction(income: number): number {
  if (income <= 1_625_000) return 550_000;
  if (income <= 1_800_000) return income * 0.4 - 100_000;
  if (income <= 3_600_000) return income * 0.3 + 80_000;
  if (income <= 6_600_000) return income * 0.2 + 440_000;
  if (income <= 8_500_000) return income * 0.1 + 1_100_000;
  return 1_950_000;
}

// Income Tax Calculation (所得税)
function calcIncomeTaxAmount(taxableIncome: number): number {
  if (taxableIncome <= 0) return 0;
  if (taxableIncome <= 1_950_000) return taxableIncome * 0.05;
  if (taxableIncome <= 3_300_000) return taxableIncome * 0.10 - 97_500;
  if (taxableIncome <= 6_950_000) return taxableIncome * 0.20 - 427_500;
  if (taxableIncome <= 9_000_000) return taxableIncome * 0.23 - 636_000;
  if (taxableIncome <= 18_000_000) return taxableIncome * 0.33 - 1_536_000;
  if (taxableIncome <= 40_000_000) return taxableIncome * 0.40 - 2_796_000;
  return taxableIncome * 0.45 - 4_796_000;
}

export function incomeTax(inputs: Record<string, number | string>): Record<string, number> {
  const incomeYen = (inputs.income as number) * 10000;
  const dependents = (inputs.dependents as number) || 0;
  let socialInsuranceYen = (inputs.socialInsurance as number) * 10000;

  // Auto-estimate social insurance if 0
  if (socialInsuranceYen === 0) {
    socialInsuranceYen = incomeYen * 0.1475;
  }

  const employmentDeduction = calcEmploymentDeduction(incomeYen);
  const employmentIncome = Math.max(0, incomeYen - employmentDeduction);

  const basicDeduction = 480_000;
  const dependentDeduction = dependents * 380_000;
  const totalDeductions = socialInsuranceYen + basicDeduction + dependentDeduction;

  const taxableIncome = Math.max(0, employmentIncome - totalDeductions);
  const tax = calcIncomeTaxAmount(taxableIncome);

  // Reconstruction special income tax (復興特別所得税 2.1%)
  const totalTax = Math.round(tax * 1.021);

  const effectiveRate = incomeYen > 0 ? (totalTax / incomeYen) * 100 : 0;

  return {
    incomeTax: totalTax,
    effectiveRate: Math.round(effectiveRate * 10) / 10,
    employmentDeduction: Math.round(employmentDeduction),
    taxableIncome: Math.max(0, Math.round(taxableIncome)),
  };
}

export function takeHomePay(inputs: Record<string, number | string>): Record<string, number> {
  const monthlySalaryYen = (inputs.monthlySalary as number) * 10000;
  const bonusMonths = inputs.bonusMonths as number;
  const age = inputs.age as number;
  const dependents = (inputs.dependents as number) || 0;

  const annualGross = monthlySalaryYen * (12 + bonusMonths);

  // Social insurance rates
  const healthInsuranceRate = 0.05;
  const pensionRate = 0.0915;
  const employmentInsuranceRate = 0.006;
  const nursingInsuranceRate = age >= 40 ? 0.009 : 0;
  const totalSIRate = healthInsuranceRate + pensionRate + employmentInsuranceRate + nursingInsuranceRate;

  const monthlySI = Math.round(monthlySalaryYen * totalSIRate);
  const annualSI = Math.round(annualGross * totalSIRate);

  // Income tax (annual)
  const employmentDeduction = calcEmploymentDeduction(annualGross);
  const employmentIncome = Math.max(0, annualGross - employmentDeduction);
  const basicDeduction = 480_000;
  const dependentDeduction = dependents * 380_000;
  const taxableIncome = Math.max(0, employmentIncome - annualSI - basicDeduction - dependentDeduction);
  const annualIncomeTax = Math.round(calcIncomeTaxAmount(taxableIncome) * 1.021);
  const monthlyIncomeTax = Math.round(annualIncomeTax / 12);

  // Resident tax (住民税) ~10%
  const annualResidentTax = Math.round(taxableIncome * 0.10);
  const monthlyResidentTax = Math.round(annualResidentTax / 12);

  const monthlyDeductions = monthlySI + monthlyIncomeTax + monthlyResidentTax;
  const monthlyTakeHome = monthlySalaryYen - monthlyDeductions;
  const annualTakeHome = annualGross - annualSI - annualIncomeTax - annualResidentTax;

  return {
    monthlyTakeHome: Math.round(monthlyTakeHome),
    annualTakeHome: Math.round(annualTakeHome),
    annualGross: Math.round(annualGross),
    socialInsurance: monthlySI,
    incomeTax: monthlyIncomeTax,
    residentTax: monthlyResidentTax,
  };
}

export function bmi(inputs: Record<string, number | string>): Record<string, number | string> {
  const heightCm = inputs.height as number;
  const weightKg = inputs.weight as number;
  const heightM = heightCm / 100;

  const bmiValue = weightKg / (heightM * heightM);
  const idealWeight = 22 * heightM * heightM;
  const weightDiff = weightKg - idealWeight;

  let category: string;
  if (bmiValue < 18.5) category = '低体重（やせ）';
  else if (bmiValue < 25) category = '普通体重';
  else if (bmiValue < 30) category = '肥満（1度）';
  else if (bmiValue < 35) category = '肥満（2度）';
  else if (bmiValue < 40) category = '肥満（3度）';
  else category = '肥満（4度）';

  return {
    bmi: Math.round(bmiValue * 10) / 10,
    category,
    idealWeight: Math.round(idealWeight * 10) / 10,
    weightDiff: Math.round(weightDiff * 10) / 10,
  };
}

export function daysBetween(inputs: Record<string, number | string>): Record<string, number | string> {
  const start = new Date(inputs.startDate as string);
  const end = new Date(inputs.endDate as string);
  const diffMs = end.getTime() - start.getTime();
  const days = Math.round(diffMs / (1000 * 60 * 60 * 24));
  const absDays = Math.abs(days);

  const weeks = Math.floor(absDays / 7);
  const remainingDays = absDays % 7;

  // Approximate months and years
  const months = Math.round((absDays / 30.44) * 10) / 10;
  const years = Math.round((absDays / 365.25) * 100) / 100;

  return {
    days: `${days}日`,
    weeks: weeks > 0 ? `${weeks}週${remainingDays > 0 ? `${remainingDays}日` : ''}` : `${remainingDays}日`,
    months: `約${months}ヶ月`,
    years: `約${years}年`,
  };
}

export function compoundInterest(inputs: Record<string, number | string>): Record<string, number> {
  const principalYen = (inputs.principal as number) * 10000;
  const monthlyYen = (inputs.monthlyContribution as number) * 10000;
  const annualRate = (inputs.annualRate as number) / 100;
  const monthlyRate = annualRate / 12;
  const years = inputs.years as number;
  const totalMonths = years * 12;

  let balance = principalYen;
  for (let i = 0; i < totalMonths; i++) {
    balance = balance * (1 + monthlyRate) + monthlyYen;
  }

  const totalContribution = principalYen + monthlyYen * totalMonths;
  const totalGain = balance - totalContribution;
  const gainRate = totalContribution > 0 ? (totalGain / totalContribution) * 100 : 0;

  return {
    finalAmount: Math.round(balance),
    totalContribution: Math.round(totalContribution),
    totalGain: Math.round(totalGain),
    gainRate: Math.round(gainRate * 10) / 10,
    // Also support the external JSON format output IDs
    totalInvested: Math.round(totalContribution),
    finalValue: Math.round(balance),
    totalInterest: Math.round(totalGain),
    returnRate: Math.round(gainRate * 10) / 10,
  };
}

// --- Car Loan ---
export function carLoan(inputs: Record<string, number | string>): Record<string, number> {
  const amount = (inputs.amount as number) * 10000;
  const rate = (inputs.rate as number) / 100 / 12;
  const months = (inputs.years as number) * 12;
  const monthly = rate === 0 ? amount / months : amount * rate * Math.pow(1 + rate, months) / (Math.pow(1 + rate, months) - 1);
  const total = monthly * months;
  return { monthlyPayment: Math.round(monthly), totalPayment: Math.round(total), totalInterest: Math.round(total - amount) };
}

// --- Education Loan ---
export function educationLoan(inputs: Record<string, number | string>): Record<string, number> {
  const amount = (inputs.amount as number) * 10000;
  const rate = (inputs.rate as number) / 100 / 12;
  const months = (inputs.years as number) * 12;
  const monthly = rate === 0 ? amount / months : amount * rate * Math.pow(1 + rate, months) / (Math.pow(1 + rate, months) - 1);
  const total = monthly * months;
  return { monthlyPayment: Math.round(monthly), totalPayment: Math.round(total), totalInterest: Math.round(total - amount) };
}

// --- Mortgage Comparison ---
export function mortgageComparison(inputs: Record<string, number | string>): Record<string, number> {
  const amount = (inputs.amount as number) * 10000;
  const years = inputs.years as number;
  const months = years * 12;
  const calc = (r: number) => { const mr = r / 100 / 12; return mr === 0 ? amount / months : amount * mr * Math.pow(1 + mr, months) / (Math.pow(1 + mr, months) - 1); };
  const monthlyA = calc(inputs.rateA as number);
  const monthlyB = calc(inputs.rateB as number);
  return { monthlyA: Math.round(monthlyA), totalA: Math.round(monthlyA * months), monthlyB: Math.round(monthlyB), totalB: Math.round(monthlyB * months), difference: Math.round((monthlyA - monthlyB) * months) };
}

// --- Inheritance Tax (simplified) ---
export function inheritanceTax(inputs: Record<string, number | string>): Record<string, number> {
  const assets = (inputs.assets as number) * 10000;
  const heirs = Math.max(1, inputs.heirs as number);
  const basicDeduction = 30_000_000 + 6_000_000 * heirs;
  const taxableAmount = Math.max(0, assets - basicDeduction);
  const perHeir = taxableAmount / heirs;
  let taxPerHeir: number;
  if (perHeir <= 10_000_000) taxPerHeir = perHeir * 0.10;
  else if (perHeir <= 30_000_000) taxPerHeir = perHeir * 0.15 - 500_000;
  else if (perHeir <= 50_000_000) taxPerHeir = perHeir * 0.20 - 2_000_000;
  else if (perHeir <= 100_000_000) taxPerHeir = perHeir * 0.30 - 7_000_000;
  else if (perHeir <= 200_000_000) taxPerHeir = perHeir * 0.40 - 17_000_000;
  else if (perHeir <= 300_000_000) taxPerHeir = perHeir * 0.45 - 27_000_000;
  else if (perHeir <= 600_000_000) taxPerHeir = perHeir * 0.50 - 42_000_000;
  else taxPerHeir = perHeir * 0.55 - 72_000_000;
  const totalTax = Math.round(taxPerHeir * heirs);
  return { basicDeduction: Math.round(basicDeduction), taxableAmount: Math.round(taxableAmount), totalTax, effectiveRate: assets > 0 ? Math.round(totalTax / assets * 1000) / 10 : 0 };
}

// --- Gift Tax ---
// 一般贈与税率（一般税率）
function calcGeneralGiftTax(taxable: number): number {
  if (taxable <= 2_000_000) return taxable * 0.10;
  if (taxable <= 3_000_000) return taxable * 0.15 - 100_000;
  if (taxable <= 4_000_000) return taxable * 0.20 - 250_000;
  if (taxable <= 6_000_000) return taxable * 0.30 - 650_000;
  if (taxable <= 10_000_000) return taxable * 0.40 - 1_250_000;
  if (taxable <= 15_000_000) return taxable * 0.45 - 1_750_000;
  if (taxable <= 30_000_000) return taxable * 0.50 - 2_500_000;
  return taxable * 0.55 - 4_000_000;
}

// 特例贈与税率（直系尊属→18歳以上の直系卑属）
function calcSpecialGiftTax(taxable: number): number {
  if (taxable <= 2_000_000) return taxable * 0.10;
  if (taxable <= 4_000_000) return taxable * 0.15 - 100_000;
  if (taxable <= 6_000_000) return taxable * 0.20 - 300_000;
  if (taxable <= 10_000_000) return taxable * 0.30 - 900_000;
  if (taxable <= 15_000_000) return taxable * 0.40 - 1_900_000;
  if (taxable <= 30_000_000) return taxable * 0.45 - 2_650_000;
  if (taxable <= 45_000_000) return taxable * 0.50 - 4_150_000;
  return taxable * 0.55 - 6_400_000;
}

export function giftTax(inputs: Record<string, number | string>): Record<string, number> {
  const amount = (inputs.amount as number) * 10000;
  const taxable = Math.max(0, amount - 1_100_000);
  const isSpecial = (inputs.type as string) === 'special';
  const tax = isSpecial ? calcSpecialGiftTax(taxable) : calcGeneralGiftTax(taxable);
  return { taxableAmount: Math.round(taxable), giftTax: Math.round(tax), effectiveRate: amount > 0 ? Math.round(tax / amount * 1000) / 10 : 0 };
}

// --- Consumption Tax ---
export function consumptionTax(inputs: Record<string, number | string>): Record<string, number> {
  const price = inputs.price as number;
  const rate = (inputs.rate as number) / 100;
  const taxAmount = Math.round(price * rate);
  return { taxIncluded: price + taxAmount, taxAmount, taxExcluded: price };
}

// --- Fixed Asset Tax ---
export function fixedAssetTax(inputs: Record<string, number | string>): Record<string, number> {
  const assessedValue = (inputs.assessedValue as number) * 10000;
  const taxRate = (inputs.taxRate as number) / 100;
  const cityPlanningRate = (inputs.cityPlanningRate as number) / 100;
  const fixedTax = Math.round(assessedValue * taxRate);
  const cityTax = Math.round(assessedValue * cityPlanningRate);
  return { fixedAssetTax: fixedTax, cityPlanningTax: cityTax, totalTax: fixedTax + cityTax, monthlyTax: Math.round((fixedTax + cityTax) / 12) };
}

// --- Bonus Take-Home ---
export function bonusTax(inputs: Record<string, number | string>): Record<string, number> {
  const bonus = (inputs.bonus as number) * 10000;
  const monthlySalary = (inputs.monthlySalary as number) * 10000;
  const age = inputs.age as number;
  const healthRate = 0.05;
  const pensionRate = 0.0915;
  const employmentRate = 0.006;
  const nursingRate = age >= 40 ? 0.009 : 0;
  const siRate = healthRate + pensionRate + employmentRate + nursingRate;
  const si = Math.round(bonus * siRate);
  const taxable = bonus - si;
  // Simplified: use flat rate based on monthly salary bracket
  const taxRate = monthlySalary < 300_000 * 10000 / 10000 ? 0.06 : monthlySalary < 500_000 ? 0.10 : 0.20;
  const incomeTaxVal = Math.round(taxable * taxRate * 1.021);
  const takeHome = bonus - si - incomeTaxVal;
  return { takeHome: Math.round(takeHome), socialInsurance: si, incomeTax: incomeTaxVal, totalDeduction: si + incomeTaxVal };
}

// --- Hourly Wage ---
export function hourlyWage(inputs: Record<string, number | string>): Record<string, number> {
  const monthly = (inputs.monthlySalary as number) * 10000;
  const hoursPerDay = inputs.hoursPerDay as number;
  const daysPerMonth = inputs.daysPerMonth as number;
  const totalHours = hoursPerDay * daysPerMonth;
  const hourly = totalHours > 0 ? Math.round(monthly / totalHours) : 0;
  const daily = hoursPerDay > 0 ? Math.round(monthly / daysPerMonth) : 0;
  return { hourlyWage: hourly, dailyWage: daily, annualIncome: monthly * 12, totalMonthlyHours: totalHours };
}

// --- Pension Estimate ---
export function pensionEstimate(inputs: Record<string, number | string>): Record<string, number> {
  const years = inputs.contributionYears as number;
  const avgSalary = (inputs.averageSalary as number) * 10000;
  // 老齢基礎年金: 満額816,000円/年（2026年度）× 加入月数/480
  const basicPensionFull = 816_000;
  const months = Math.min(years * 12, 480);
  const basicPension = Math.round(basicPensionFull * months / 480);
  // 老齢厚生年金: 平均標準報酬額 × 5.481/1000 × 加入月数
  const welfareMultiplier = 5.481 / 1000;
  const welfareMonths = years * 12;
  const welfarePension = Math.round(avgSalary * welfareMultiplier * welfareMonths);
  // 経過的加算（概算: 少額のため省略）
  const totalAnnual = basicPension + welfarePension;
  return { basicPension, welfarePension, totalAnnual, totalMonthly: Math.round(totalAnnual / 12) };
}

// --- Pension Contribution ---
export function pensionContribution(inputs: Record<string, number | string>): Record<string, number> {
  const salary = (inputs.monthlySalary as number) * 10000;
  const age = inputs.age as number;
  const pensionRate = 0.183;
  const employeeShare = Math.round(salary * pensionRate / 2);
  const nursingRate = age >= 40 ? 0.018 : 0;
  const healthShare = Math.round(salary * (0.10 + nursingRate) / 2);
  return { pensionContribution: employeeShare, healthInsurance: healthShare, total: employeeShare + healthShare, annualTotal: (employeeShare + healthShare) * 12 };
}

// --- Stock Profit ---
export function stockProfit(inputs: Record<string, number | string>): Record<string, number> {
  const buyPrice = inputs.buyPrice as number;
  const sellPrice = inputs.sellPrice as number;
  const shares = inputs.shares as number;
  const commission = inputs.commission as number;
  const profit = (sellPrice - buyPrice) * shares - commission * 2;
  const taxRate = 0.20315;
  const tax = profit > 0 ? Math.round(profit * taxRate) : 0;
  return { grossProfit: Math.round(profit), tax, netProfit: Math.round(profit - tax), returnRate: buyPrice * shares > 0 ? Math.round(profit / (buyPrice * shares) * 1000) / 10 : 0 };
}

// --- Dividend Yield ---
export function dividendYield(inputs: Record<string, number | string>): Record<string, number> {
  const price = inputs.stockPrice as number;
  const dividend = inputs.annualDividend as number;
  const shares = inputs.shares as number;
  const yieldRate = price > 0 ? Math.round(dividend / price * 10000) / 100 : 0;
  const annualIncome = dividend * shares;
  const tax = Math.round(annualIncome * 0.20315);
  return { dividendYield: yieldRate, annualIncome, afterTax: annualIncome - tax, tax };
}

// --- Life Insurance Need ---
export function lifeInsurance(inputs: Record<string, number | string>): Record<string, number> {
  const annualExpense = (inputs.annualExpense as number) * 10000;
  const yearsNeeded = inputs.yearsNeeded as number;
  const currentSavings = (inputs.currentSavings as number) * 10000;
  const survivorPension = (inputs.survivorPension as number) * 10000 * yearsNeeded;
  const totalNeeded = annualExpense * yearsNeeded;
  const insuranceNeeded = Math.max(0, totalNeeded - currentSavings - survivorPension);
  return { totalNeeded: Math.round(totalNeeded), insuranceNeeded: Math.round(insuranceNeeded), coverageRatio: totalNeeded > 0 ? Math.round((currentSavings + survivorPension) / totalNeeded * 1000) / 10 : 0 };
}

// --- Rent vs Buy ---
export function rentVsBuy(inputs: Record<string, number | string>): Record<string, number> {
  const monthlyRent = (inputs.monthlyRent as number) * 10000;
  const years = inputs.years as number;
  const rentTotal = monthlyRent * 12 * years;
  const housePrice = (inputs.housePrice as number) * 10000;
  const rate = (inputs.loanRate as number) / 100 / 12;
  const months = years * 12;
  const monthlyLoan = rate === 0 ? housePrice / months : housePrice * rate * Math.pow(1 + rate, months) / (Math.pow(1 + rate, months) - 1);
  const maintenanceCost = (inputs.maintenanceCost as number) * 10000 * years;
  const buyTotal = monthlyLoan * months + maintenanceCost;
  return { rentTotal: Math.round(rentTotal), buyTotal: Math.round(buyTotal), difference: Math.round(rentTotal - buyTotal), monthlyLoan: Math.round(monthlyLoan) };
}

// --- NISA Simulation ---
export function calculateNisaSimulation(inputs: Record<string, number | string>): Record<string, number> {
  const monthly = (inputs.monthlyAmount as number) * 10000;
  const years = inputs.years as number;
  const rate = (inputs.expectedReturn as number) / 100 / 12;
  let balance = 0;
  for (let i = 0; i < years * 12; i++) balance = (balance + monthly) * (1 + rate);
  const totalInvested = monthly * years * 12;
  const profit = balance - totalInvested;
  const taxSaved = Math.round(profit * 0.20315);
  return { finalAmount: Math.round(balance), totalInvested: Math.round(totalInvested), profit: Math.round(profit), taxSaved };
}

// --- iDeCo Simulation ---
export function calculateIdecoSimulation(inputs: Record<string, number | string>): Record<string, number> {
  const monthly = (inputs.monthlyAmount as number);
  const years = inputs.years as number;
  const rate = (inputs.expectedReturn as number) / 100 / 12;
  const annualIncome = (inputs.annualIncome as number) * 10000;
  let balance = 0;
  for (let i = 0; i < years * 12; i++) balance = (balance + monthly) * (1 + rate);
  const totalContrib = monthly * years * 12;
  const taxRate = annualIncome > 6_950_000 ? 0.30 : annualIncome > 3_300_000 ? 0.20 : 0.15;
  const annualDeduction = Math.round(monthly * 12 * taxRate);
  return { finalAmount: Math.round(balance), totalContribution: Math.round(totalContrib), investmentGain: Math.round(balance - totalContrib), annualTaxSaving: annualDeduction, totalTaxSaving: annualDeduction * years };
}

// --- Forex Profit ---
export function calculateForexProfit(inputs: Record<string, number | string>): Record<string, number> {
  const lots = inputs.lots as number;
  const entryPrice = inputs.entryPrice as number;
  const exitPrice = inputs.exitPrice as number;
  const lotSize = 10000;
  const direction = inputs.direction as string === 'sell' ? -1 : 1;
  const pips = (exitPrice - entryPrice) * direction;
  const profit = pips * lots * lotSize;
  const tax = profit > 0 ? Math.round(profit * 0.20315) : 0;
  return { pips: Math.round(pips * 10000) / 100, grossProfit: Math.round(profit), tax, netProfit: Math.round(profit - tax) };
}

// --- Crypto Profit ---
export function calculateCryptoProfit(inputs: Record<string, number | string>): Record<string, number> {
  const buyPrice = inputs.buyPrice as number;
  const sellPrice = inputs.sellPrice as number;
  const quantity = inputs.quantity as number;
  const profit = (sellPrice - buyPrice) * quantity;
  // Crypto is taxed as miscellaneous income (総合課税)
  const taxRate = profit > 1_950_000 ? 0.30 : profit > 0 ? 0.15 : 0;
  const tax = Math.round(profit * taxRate);
  return { grossProfit: Math.round(profit), tax, netProfit: Math.round(profit - tax), returnRate: buyPrice > 0 ? Math.round((sellPrice - buyPrice) / buyPrice * 1000) / 10 : 0 };
}

// --- Furusato Nozei Limit ---
export function calculateFurusatoNozei(inputs: Record<string, number | string>): Record<string, number> {
  const income = (inputs.annualIncome as number) * 10000;
  const dependents = inputs.dependents as number;
  const si = income * 0.15;
  const empDeduction = calcEmploymentDeduction(income);
  const taxableIncome = Math.max(0, income - empDeduction - si - 480_000 - dependents * 380_000);
  const residentTax = taxableIncome * 0.10;
  const limit = Math.round(residentTax * 0.20 / (1 - 0.10 - taxableIncome * 0.02 / taxableIncome || 0) + 2000);
  const safeLimit = Math.min(Math.round(residentTax * 0.28), Math.round(income * 0.02));
  const recommended = Math.max(safeLimit, Math.round(residentTax * 0.20));
  return { estimatedLimit: recommended, selfPayment: 2000, effectiveDeduction: recommended - 2000, residentTax: Math.round(residentTax) };
}

// --- Savings Simulation ---
export function savingsSimulation(inputs: Record<string, number | string>): Record<string, number> {
  const monthly = inputs.monthlyAmount as number;
  const years = inputs.years as number;
  const annualRate = (inputs.annualRate as number) / 100;
  const monthlyRate = annualRate / 12;
  const initial = inputs.initialAmount as number;
  const totalMonths = years * 12;

  let balance = initial;
  if (monthlyRate === 0) {
    balance = initial + monthly * totalMonths;
  } else {
    for (let i = 0; i < totalMonths; i++) {
      balance = balance * (1 + monthlyRate) + monthly;
    }
  }

  const totalDeposit = initial + monthly * totalMonths;
  const totalInterest = balance - totalDeposit;
  const interestRate = totalDeposit > 0 ? Math.round(totalInterest / totalDeposit * 1000) / 10 : 0;

  return {
    finalAmount: Math.round(balance),
    totalDeposit: Math.round(totalDeposit),
    totalInterest: Math.round(totalInterest),
    interestRate,
  };
}

// --- Calories BMR (Harris-Benedict) ---
export function caloriesBmr(inputs: Record<string, number | string>): Record<string, number> {
  const gender = inputs.gender as string;
  const age = inputs.age as number;
  const height = inputs.height as number;
  const weight = inputs.weight as number;
  const activity = inputs.activity as string;

  let bmrValue: number;
  if (gender === 'male') {
    bmrValue = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age;
  } else {
    bmrValue = 447.593 + 9.247 * weight + 3.098 * height - 4.330 * age;
  }

  const activityMultipliers: Record<string, number> = {
    sedentary: 1.2,
    light: 1.375,
    moderate: 1.55,
    active: 1.725,
    very_active: 1.9,
  };
  const multiplier = activityMultipliers[activity] || 1.55;
  const tdee = bmrValue * multiplier;
  const loseWeight = tdee - 500;

  return {
    bmr: Math.round(bmrValue),
    tdee: Math.round(tdee),
    maintainWeight: Math.round(tdee),
    loseWeight: Math.round(loseWeight),
  };
}

// --- Age Calculator ---
export function ageCalculator(inputs: Record<string, number | string>): Record<string, string> {
  const birthDate = new Date(inputs.birthDate as string);
  const today = new Date();

  let years = today.getFullYear() - birthDate.getFullYear();
  let months = today.getMonth() - birthDate.getMonth();
  let days = today.getDate() - birthDate.getDate();

  if (days < 0) {
    months--;
    const prevMonth = new Date(today.getFullYear(), today.getMonth(), 0);
    days += prevMonth.getDate();
  }
  if (months < 0) {
    years--;
    months += 12;
  }

  const totalDays = Math.floor((today.getTime() - birthDate.getTime()) / (1000 * 60 * 60 * 24));

  let nextBirthday = new Date(today.getFullYear(), birthDate.getMonth(), birthDate.getDate());
  if (nextBirthday <= today) {
    nextBirthday = new Date(today.getFullYear() + 1, birthDate.getMonth(), birthDate.getDate());
  }
  const daysUntilBirthday = Math.ceil((nextBirthday.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

  const zodiacAnimals = ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'];
  const zodiac = zodiacAnimals[birthDate.getFullYear() % 12];

  return {
    age: `${years}歳${months}ヶ月${days}日`,
    totalDays: `${totalDays.toLocaleString()}日`,
    nextBirthday: `あと${daysUntilBirthday}日`,
    zodiac: `${zodiac}年`,
  };
}

// --- ROI Calculator ---
export function roiCalculator(inputs: Record<string, number | string>): Record<string, number> {
  const investment = (inputs.investment as number) * 10000;
  const revenue = (inputs.revenue as number) * 10000;
  const profit = revenue - investment;
  const roi = investment > 0 ? Math.round(profit / investment * 1000) / 10 : 0;
  const profitRatio = revenue > 0 ? Math.round(profit / revenue * 1000) / 10 : 0;
  const paybackMultiple = investment > 0 ? Math.round(revenue / investment * 100) / 100 : 0;

  return {
    roi,
    profit: Math.round(profit),
    profitRatio,
    paybackMultiple,
  };
}

// === HEALTH ===

export function idealWeight(inputs: Record<string, number | string>): Record<string, number> {
  const height = (inputs.height as number) / 100;
  const bmiIdeal = 22;
  const ideal = bmiIdeal * height * height;
  const beautyWeight = 20 * height * height;
  const modelWeight = 18 * height * height;
  return { idealWeight: Math.round(ideal * 10) / 10, beautyWeight: Math.round(beautyWeight * 10) / 10, modelWeight: Math.round(modelWeight * 10) / 10 };
}

export function bodyFat(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const waist = inputs.waist as number;
  const gender = inputs.gender as string;
  const height = (inputs.height as number) / 100;
  const bmiVal = weight / (height * height);
  // Navy method approximation
  let fatPct: number;
  if (gender === 'male') {
    fatPct = 1.20 * bmiVal + 0.23 * 30 - 16.2; // simplified
  } else {
    fatPct = 1.20 * bmiVal + 0.23 * 30 - 5.4;
  }
  fatPct = Math.max(3, Math.min(60, fatPct));
  const fatMass = weight * fatPct / 100;
  const leanMass = weight - fatMass;
  let category: string;
  if (gender === 'male') {
    if (fatPct < 10) category = '低い'; else if (fatPct < 20) category = '標準'; else if (fatPct < 25) category = 'やや高い'; else category = '高い';
  } else {
    if (fatPct < 20) category = '低い'; else if (fatPct < 30) category = '標準'; else if (fatPct < 35) category = 'やや高い'; else category = '高い';
  }
  return { bodyFatPercentage: Math.round(fatPct * 10) / 10, fatMass: Math.round(fatMass * 10) / 10, leanMass: Math.round(leanMass * 10) / 10, category };
}

export function basalMetabolism(inputs: Record<string, number | string>): Record<string, number> {
  const weight = inputs.weight as number;
  const height = inputs.height as number;
  const age = inputs.age as number;
  const gender = inputs.gender as string;
  let bmr: number;
  if (gender === 'male') {
    bmr = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age;
  } else {
    bmr = 447.593 + 9.247 * weight + 3.098 * height - 4.330 * age;
  }
  return { bmr: Math.round(bmr), light: Math.round(bmr * 1.375), moderate: Math.round(bmr * 1.55), active: Math.round(bmr * 1.725) };
}

export function calorieBurn(inputs: Record<string, number | string>): Record<string, number> {
  const weight = inputs.weight as number;
  const minutes = inputs.minutes as number;
  const met = inputs.met as number;
  const calories = met * 3.5 * weight / 200 * minutes;
  const fatBurn = calories / 7200 * 1000; // grams
  return { calories: Math.round(calories), fatBurn: Math.round(fatBurn * 10) / 10, hourlyCalories: Math.round(calories / minutes * 60) };
}

export function dailyCalorie(inputs: Record<string, number | string>): Record<string, number> {
  const weight = inputs.weight as number;
  const height = inputs.height as number;
  const age = inputs.age as number;
  const gender = inputs.gender as string;
  const activityLevel = inputs.activityLevel as number;
  let bmr: number;
  if (gender === 'male') {
    bmr = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age;
  } else {
    bmr = 447.593 + 9.247 * weight + 3.098 * height - 4.330 * age;
  }
  const tdee = bmr * activityLevel;
  return { tdee: Math.round(tdee), bmr: Math.round(bmr), weightLoss: Math.round(tdee - 500), weightGain: Math.round(tdee + 500) };
}

export function dueDate(inputs: Record<string, number | string>): Record<string, number | string> {
  const lmp = new Date(inputs.lastPeriod as string);
  const due = new Date(lmp.getTime() + 280 * 24 * 60 * 60 * 1000);
  const now = new Date();
  const weeksPregnant = Math.floor((now.getTime() - lmp.getTime()) / (7 * 24 * 60 * 60 * 1000));
  const daysRemaining = Math.max(0, Math.ceil((due.getTime() - now.getTime()) / (24 * 60 * 60 * 1000)));
  return { dueDate: `${due.getFullYear()}-${String(due.getMonth()+1).padStart(2,'0')}-${String(due.getDate()).padStart(2,'0')}`, weeksPregnant, daysRemaining, trimester: weeksPregnant < 13 ? 1 : weeksPregnant < 27 ? 2 : 3 };
}

export function pregnancyWeek(inputs: Record<string, number | string>): Record<string, number | string> {
  const lmp = new Date(inputs.lastPeriod as string);
  const now = new Date();
  const totalDays = Math.floor((now.getTime() - lmp.getTime()) / (24 * 60 * 60 * 1000));
  const weeks = Math.floor(totalDays / 7);
  const days = totalDays % 7;
  const trimester = weeks < 13 ? 1 : weeks < 27 ? 2 : 3;
  const due = new Date(lmp.getTime() + 280 * 24 * 60 * 60 * 1000);
  const remaining = Math.max(0, Math.ceil((due.getTime() - now.getTime()) / (24 * 60 * 60 * 1000)));
  return { currentWeek: `${weeks}週${days}日`, trimester, remainingDays: remaining, dueDate: `${due.getFullYear()}-${String(due.getMonth()+1).padStart(2,'0')}-${String(due.getDate()).padStart(2,'0')}` };
}

export function medicalExpense(inputs: Record<string, number | string>): Record<string, number> {
  const totalMedical = (inputs.totalMedical as number) * 10000;
  const insurance = (inputs.insuranceReimbursement as number) * 10000;
  const income = (inputs.annualIncome as number) * 10000;
  const threshold = Math.max(100000, income * 0.05);
  const deduction = Math.max(0, totalMedical - insurance - threshold);
  const cappedDeduction = Math.min(deduction, 2000000);
  const taxRate = income > 6950000 ? 0.23 : income > 3300000 ? 0.20 : income > 1950000 ? 0.10 : 0.05;
  const taxSaving = Math.round(cappedDeduction * taxRate);
  return { deduction: Math.round(cappedDeduction), taxSaving, outOfPocket: Math.round(totalMedical - insurance), threshold: Math.round(threshold) };
}

export function highCostMedical(inputs: Record<string, number | string>): Record<string, number> {
  const medical = (inputs.medicalCost as number);
  const income = inputs.incomeCategory as number;
  let limit: number;
  if (income >= 810000) limit = 252600 + (medical - 842000) * 0.01;
  else if (income >= 515000) limit = 167400 + (medical - 558000) * 0.01;
  else if (income >= 280000) limit = 80100 + (medical - 267000) * 0.01;
  else if (income >= 260000) limit = 57600;
  else limit = 35400;
  limit = Math.max(limit, 0);
  const refund = Math.max(0, medical - limit);
  return { selfPayLimit: Math.round(limit), refund: Math.round(refund), totalCost: medical };
}

export function waterIntake(inputs: Record<string, number | string>): Record<string, number> {
  const weight = inputs.weight as number;
  const activityLevel = inputs.activityLevel as number;
  const base = weight * 35;
  const adjusted = base * activityLevel;
  return { dailyMl: Math.round(adjusted), dailyLiters: Math.round(adjusted / 100) / 10, glasses: Math.round(adjusted / 250), hourly: Math.round(adjusted / 16) };
}

// === LIFE / DATE ===

export function countdown(inputs: Record<string, number | string>): Record<string, number> {
  const target = new Date(inputs.targetDate as string);
  const now = new Date();
  const diffMs = target.getTime() - now.getTime();
  const days = Math.ceil(diffMs / (24 * 60 * 60 * 1000));
  const hours = Math.ceil(diffMs / (60 * 60 * 1000));
  const weeks = Math.ceil(days / 7);
  const months = Math.round(days / 30.44 * 10) / 10;
  return { days, hours, weeks, months };
}

export function weekday(inputs: Record<string, number | string>): Record<string, number | string> {
  const date = new Date(inputs.date as string);
  const dayNames = ['日曜日', '月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日'];
  const dayIndex = date.getDay();
  const isWeekend = dayIndex === 0 || dayIndex === 6;
  return { weekday: dayNames[dayIndex], dayIndex, isWeekend: isWeekend ? 1 : 0 };
}

export function zodiac(inputs: Record<string, number | string>): Record<string, number | string> {
  const date = new Date(inputs.birthDate as string);
  const m = date.getMonth() + 1;
  const d = date.getDate();
  const signs = [
    { name: '山羊座', start: [1,1], end: [1,19] },
    { name: '水瓶座', start: [1,20], end: [2,18] },
    { name: '魚座', start: [2,19], end: [3,20] },
    { name: '牡羊座', start: [3,21], end: [4,19] },
    { name: '牡牛座', start: [4,20], end: [5,20] },
    { name: '双子座', start: [5,21], end: [6,21] },
    { name: '蟹座', start: [6,22], end: [7,22] },
    { name: '獅子座', start: [7,23], end: [8,22] },
    { name: '乙女座', start: [8,23], end: [9,22] },
    { name: '天秤座', start: [9,23], end: [10,23] },
    { name: '蠍座', start: [10,24], end: [11,22] },
    { name: '射手座', start: [11,23], end: [12,21] },
    { name: '山羊座', start: [12,22], end: [12,31] },
  ];
  let sign = '山羊座';
  for (const s of signs) {
    const afterStart = m > s.start[0] || (m === s.start[0] && d >= s.start[1]);
    const beforeEnd = m < s.end[0] || (m === s.end[0] && d <= s.end[1]);
    if (afterStart && beforeEnd) { sign = s.name; break; }
  }
  const animals = ['申', '酉', '戌', '亥', '子', '丑', '寅', '卯', '辰', '巳', '午', '未'];
  const year = date.getFullYear();
  const chineseZodiac = animals[year % 12];
  return { westernZodiac: sign, chineseZodiac, year };
}

export function elapsedDays(inputs: Record<string, number | string>): Record<string, number> {
  const start = new Date(inputs.startDate as string);
  const now = new Date();
  const diffMs = now.getTime() - start.getTime();
  const days = Math.floor(diffMs / (24 * 60 * 60 * 1000));
  return { days, weeks: Math.floor(days / 7), months: Math.round(days / 30.44 * 10) / 10, years: Math.round(days / 365.25 * 100) / 100 };
}

export function workDays(inputs: Record<string, number | string>): Record<string, number> {
  const start = new Date(inputs.startDate as string);
  const end = new Date(inputs.endDate as string);
  let count = 0;
  let totalDays = 0;
  const current = new Date(start);
  while (current <= end) {
    totalDays++;
    const day = current.getDay();
    if (day !== 0 && day !== 6) count++;
    current.setDate(current.getDate() + 1);
  }
  return { workDays: count, totalDays, weekends: totalDays - count, weeks: Math.floor(totalDays / 7) };
}

// === LIFE / UNIT ===

export function lengthConvert(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const from = inputs.from as string;
  const factors: Record<string, number> = { mm: 0.001, cm: 0.01, m: 1, km: 1000, inch: 0.0254, ft: 0.3048, yard: 0.9144, mile: 1609.344 };
  const meters = value * (factors[from] || 1);
  return { mm: Math.round(meters * 1000 * 1000) / 1000, cm: Math.round(meters * 100 * 1000) / 1000, m: Math.round(meters * 1000) / 1000, km: Math.round(meters / 1000 * 1000000) / 1000000, inch: Math.round(meters / 0.0254 * 1000) / 1000, ft: Math.round(meters / 0.3048 * 1000) / 1000 };
}

export function weightConvert(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const from = inputs.from as string;
  const factors: Record<string, number> = { mg: 0.001, g: 1, kg: 1000, ton: 1000000, oz: 28.3495, lb: 453.592 };
  const grams = value * (factors[from] || 1);
  return { mg: Math.round(grams * 1000), g: Math.round(grams * 1000) / 1000, kg: Math.round(grams / 1000 * 1000) / 1000, ton: Math.round(grams / 1000000 * 1000000) / 1000000, oz: Math.round(grams / 28.3495 * 1000) / 1000, lb: Math.round(grams / 453.592 * 1000) / 1000 };
}

export function temperatureConvert(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const from = inputs.from as string;
  let celsius: number;
  if (from === 'fahrenheit') celsius = (value - 32) * 5 / 9;
  else if (from === 'kelvin') celsius = value - 273.15;
  else celsius = value;
  return { celsius: Math.round(celsius * 100) / 100, fahrenheit: Math.round((celsius * 9 / 5 + 32) * 100) / 100, kelvin: Math.round((celsius + 273.15) * 100) / 100 };
}

export function areaConvert(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const from = inputs.from as string;
  const factors: Record<string, number> = { sqm: 1, sqkm: 1000000, sqft: 0.0929, acre: 4046.86, ha: 10000, tsubo: 3.306 };
  const sqm = value * (factors[from] || 1);
  return { sqm: Math.round(sqm * 100) / 100, sqkm: Math.round(sqm / 1000000 * 10000) / 10000, sqft: Math.round(sqm / 0.0929 * 100) / 100, tsubo: Math.round(sqm / 3.306 * 100) / 100, ha: Math.round(sqm / 10000 * 10000) / 10000 };
}

export function volumeConvert(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const from = inputs.from as string;
  const factors: Record<string, number> = { ml: 0.001, l: 1, m3: 1000, gallon: 3.78541, cup: 0.24, tbsp: 0.015, tsp: 0.005 };
  const liters = value * (factors[from] || 1);
  return { ml: Math.round(liters * 1000 * 100) / 100, l: Math.round(liters * 1000) / 1000, m3: Math.round(liters / 1000 * 10000) / 10000, gallon: Math.round(liters / 3.78541 * 1000) / 1000, cup: Math.round(liters / 0.24 * 100) / 100 };
}

export function speedConvert(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const from = inputs.from as string;
  const factors: Record<string, number> = { mps: 1, kmh: 0.27778, mph: 0.44704, knot: 0.51444 };
  const mps = value * (factors[from] || 1);
  return { mps: Math.round(mps * 1000) / 1000, kmh: Math.round(mps / 0.27778 * 100) / 100, mph: Math.round(mps / 0.44704 * 100) / 100, knot: Math.round(mps / 0.51444 * 100) / 100 };
}

// === LIFE / SHOPPING ===

export function discount(inputs: Record<string, number | string>): Record<string, number> {
  const price = inputs.price as number;
  const discountRate = inputs.discountRate as number;
  const discountAmount = Math.round(price * discountRate / 100);
  const finalPrice = price - discountAmount;
  return { discountAmount, finalPrice, savedPercent: discountRate };
}

export function taxIncluded(inputs: Record<string, number | string>): Record<string, number> {
  const price = inputs.price as number;
  const taxRate = (inputs.taxRate as number) / 100;
  const tax = Math.round(price * taxRate);
  return { taxIncluded: price + tax, taxAmount: tax, taxExcluded: price };
}

export function splitBill(inputs: Record<string, number | string>): Record<string, number> {
  const total = inputs.total as number;
  const people = inputs.people as number;
  const perPerson = Math.ceil(total / people);
  const remainder = total % people;
  return { perPerson, total, remainder, adjustedTotal: perPerson * people };
}

export function perUnitPrice(inputs: Record<string, number | string>): Record<string, number> {
  const priceA = inputs.priceA as number;
  const amountA = inputs.amountA as number;
  const priceB = inputs.priceB as number;
  const amountB = inputs.amountB as number;
  const unitA = amountA > 0 ? Math.round(priceA / amountA * 100) / 100 : 0;
  const unitB = amountB > 0 ? Math.round(priceB / amountB * 100) / 100 : 0;
  const cheaper = unitA <= unitB ? 1 : 2;
  const savings = Math.abs(Math.round((unitA - unitB) * Math.min(amountA, amountB)));
  return { unitPriceA: unitA, unitPriceB: unitB, cheaper, savings };
}

export function dataSize(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const from = inputs.from as string;
  const factors: Record<string, number> = { B: 1, KB: 1024, MB: 1024**2, GB: 1024**3, TB: 1024**4 };
  const bytes = value * (factors[from] || 1);
  return { B: Math.round(bytes), KB: Math.round(bytes / 1024 * 100) / 100, MB: Math.round(bytes / 1024**2 * 10000) / 10000, GB: Math.round(bytes / 1024**3 * 1000000) / 1000000, TB: Math.round(bytes / 1024**4 * 100000000) / 100000000 };
}

// === LIFE / CAR ===

export function fuelCost(inputs: Record<string, number | string>): Record<string, number> {
  const distance = inputs.distance as number;
  const fuelEfficiency = inputs.fuelEfficiency as number;
  const fuelPrice = inputs.fuelPrice as number;
  const fuelUsed = fuelEfficiency > 0 ? distance / fuelEfficiency : 0;
  const cost = Math.round(fuelUsed * fuelPrice);
  return { fuelUsed: Math.round(fuelUsed * 100) / 100, cost, costPerKm: Math.round(fuelPrice / fuelEfficiency * 100) / 100 };
}

export function carTax(inputs: Record<string, number | string>): Record<string, number> {
  const displacement = inputs.displacement as number;
  let tax: number;
  if (displacement <= 1000) tax = 29500;
  else if (displacement <= 1500) tax = 34500;
  else if (displacement <= 2000) tax = 39500;
  else if (displacement <= 2500) tax = 45000;
  else if (displacement <= 3000) tax = 51000;
  else if (displacement <= 3500) tax = 58000;
  else if (displacement <= 4000) tax = 66500;
  else if (displacement <= 4500) tax = 76500;
  else if (displacement <= 6000) tax = 88000;
  else tax = 111000;
  const monthly = Math.round(tax / 12);
  return { annualTax: tax, monthlyTax: monthly };
}

export function mileage(inputs: Record<string, number | string>): Record<string, number> {
  const distance = inputs.distance as number;
  const fuel = inputs.fuelUsed as number;
  const fuelEfficiency = fuel > 0 ? Math.round(distance / fuel * 100) / 100 : 0;
  const per100km = fuelEfficiency > 0 ? Math.round(100 / fuelEfficiency * 100) / 100 : 0;
  return { kmPerLiter: fuelEfficiency, litersPer100km: per100km };
}

// === BUSINESS ===

export function breakEven(inputs: Record<string, number | string>): Record<string, number> {
  const fixedCosts = (inputs.fixedCosts as number) * 10000;
  const price = inputs.price as number;
  const variableCost = inputs.variableCost as number;
  const margin = price - variableCost;
  const units = margin > 0 ? Math.ceil(fixedCosts / margin) : 0;
  const revenue = units * price;
  return { breakEvenUnits: units, breakEvenRevenue: Math.round(revenue), marginPerUnit: margin, marginRate: price > 0 ? Math.round(margin / price * 1000) / 10 : 0 };
}

export function profitMargin(inputs: Record<string, number | string>): Record<string, number> {
  const revenue = (inputs.revenue as number) * 10000;
  const cost = (inputs.cost as number) * 10000;
  const profit = revenue - cost;
  const marginRate = revenue > 0 ? profit / revenue * 100 : 0;
  const markup = cost > 0 ? profit / cost * 100 : 0;
  return { profit: Math.round(profit), marginRate: Math.round(marginRate * 10) / 10, markup: Math.round(markup * 10) / 10 };
}

export function roi(inputs: Record<string, number | string>): Record<string, number> {
  const investment = (inputs.investment as number) * 10000;
  const returnVal = (inputs.returnValue as number) * 10000;
  const profit = returnVal - investment;
  const roiPercent = investment > 0 ? profit / investment * 100 : 0;
  return { profit: Math.round(profit), roi: Math.round(roiPercent * 10) / 10, returnValue: Math.round(returnVal) };
}

export function cashFlow(inputs: Record<string, number | string>): Record<string, number> {
  const revenue = (inputs.revenue as number) * 10000;
  const expenses = (inputs.expenses as number) * 10000;
  const depreciation = (inputs.depreciation as number) * 10000;
  const operatingCF = revenue - expenses;
  const freeCF = operatingCF + depreciation;
  const cfMargin = revenue > 0 ? operatingCF / revenue * 100 : 0;
  return { operatingCashFlow: Math.round(operatingCF), freeCashFlow: Math.round(freeCF), cashFlowMargin: Math.round(cfMargin * 10) / 10 };
}

export function inventoryTurnover(inputs: Record<string, number | string>): Record<string, number> {
  const cogs = (inputs.cogs as number) * 10000;
  const avgInventory = (inputs.avgInventory as number) * 10000;
  const turnover = avgInventory > 0 ? cogs / avgInventory : 0;
  const days = turnover > 0 ? 365 / turnover : 0;
  return { turnoverRate: Math.round(turnover * 100) / 100, daysInInventory: Math.round(days * 10) / 10 };
}

export function depreciation(inputs: Record<string, number | string>): Record<string, number> {
  const cost = (inputs.cost as number) * 10000;
  const usefulLife = inputs.usefulLife as number;
  const salvageValue = (inputs.salvageValue as number || 0) * 10000;
  const straightLine = usefulLife > 0 ? Math.round((cost - salvageValue) / usefulLife) : 0;
  const decliningRate = usefulLife > 0 ? Math.round(2 / usefulLife * 10000) / 10000 : 0;
  const firstYearDeclining = Math.round(cost * decliningRate);
  return { straightLine, firstYearDeclining, annualDepreciation: straightLine, monthlyDepreciation: Math.round(straightLine / 12) };
}

export function overtimePay(inputs: Record<string, number | string>): Record<string, number> {
  const baseSalary = (inputs.baseSalary as number) * 10000;
  const workDaysPerMonth = inputs.workDays as number;
  const hoursPerDay = inputs.hoursPerDay as number;
  const overtimeHours = inputs.overtimeHours as number;
  const hourlyBase = baseSalary / (workDaysPerMonth * hoursPerDay);
  const overtimeRate = 1.25;
  const lateNightRate = 1.50;
  const holidayRate = 1.35;
  const normalOvertime = Math.round(hourlyBase * overtimeRate * overtimeHours);
  return { hourlyBase: Math.round(hourlyBase), normalOvertime, lateNightOvertime: Math.round(hourlyBase * lateNightRate * overtimeHours), holidayOvertime: Math.round(hourlyBase * holidayRate * overtimeHours) };
}

export function annualLeave(inputs: Record<string, number | string>): Record<string, number> {
  const yearsOfService = inputs.yearsOfService as number;
  let days: number;
  if (yearsOfService < 0.5) days = 0;
  else if (yearsOfService < 1.5) days = 10;
  else if (yearsOfService < 2.5) days = 11;
  else if (yearsOfService < 3.5) days = 12;
  else if (yearsOfService < 4.5) days = 14;
  else if (yearsOfService < 5.5) days = 16;
  else if (yearsOfService < 6.5) days = 18;
  else days = 20;
  const usedDays = inputs.usedDays as number;
  return { totalDays: days, usedDays, remainingDays: Math.max(0, days - usedDays), expiringDays: 0 };
}

export function retirementPay(inputs: Record<string, number | string>): Record<string, number> {
  const years = inputs.yearsOfService as number;
  const baseSalary = (inputs.baseSalary as number) * 10000;
  const method = inputs.method as string;
  let amount: number;
  if (method === 'basic') {
    amount = baseSalary * years;
  } else {
    // Point system approximation
    const points = years * 10 + Math.max(0, years - 20) * 5;
    amount = points * 10000;
  }
  // 退職所得控除（最低80万円）
  const deduction = Math.max(800_000, years <= 20 ? 400_000 * years : 8_000_000 + 700_000 * (years - 20));
  // 退職所得 = (退職金 - 退職所得控除) × 1/2
  // ※勤続5年以下の役員等は1/2適用なし（ここでは一般従業員として1/2適用）
  const taxable = Math.max(0, (amount - deduction) / 2);
  const tax = Math.round(calcIncomeTaxAmount(taxable) * 1.021);
  return { retirementPay: Math.round(amount), deduction: Math.round(deduction), tax, afterTax: Math.round(amount - tax) };
}

export function socialInsuranceCalc(inputs: Record<string, number | string>): Record<string, number> {
  const salary = (inputs.monthlySalary as number) * 10000;
  const age = inputs.age as number;
  const healthRate = 0.10;
  const pensionRate = 0.183;
  const employmentRate = 0.006;
  const nursingRate = age >= 40 ? 0.018 : 0;
  const healthEmployee = Math.round(salary * (healthRate + nursingRate) / 2);
  const pensionEmployee = Math.round(salary * pensionRate / 2);
  const employmentEmployee = Math.round(salary * employmentRate);
  const total = healthEmployee + pensionEmployee + employmentEmployee;
  return { healthInsurance: healthEmployee, pension: pensionEmployee, employment: employmentEmployee, total, annualTotal: total * 12 };
}

export function invoiceTax(inputs: Record<string, number | string>): Record<string, number> {
  const sales = (inputs.sales as number) * 10000;
  const purchases = (inputs.purchases as number) * 10000;
  const taxRate = 0.10;
  const outputTax = Math.round(sales * taxRate);
  const inputTax = Math.round(purchases * taxRate);
  const payable = outputTax - inputTax;
  return { outputTax, inputTax, taxPayable: Math.max(0, payable), effectiveRate: sales > 0 ? Math.round(Math.max(0, payable) / sales * 1000) / 10 : 0 };
}

export function freelanceTax(inputs: Record<string, number | string>): Record<string, number> {
  const revenue = (inputs.revenue as number) * 10000;
  const expenses = (inputs.expenses as number) * 10000;
  const blueDeduction = inputs.blueReturn as number === 1 ? 650000 : 0;
  const income = Math.max(0, revenue - expenses - blueDeduction);
  const basicDeduction = 480000;
  const taxableIncome = Math.max(0, income - basicDeduction);
  const incomeTaxVal = Math.round(calcIncomeTaxAmount(taxableIncome) * 1.021);
  const residentTaxVal = Math.round(taxableIncome * 0.10);
  const healthInsurance = Math.round(income * 0.11);
  const pension = 199080;
  return { incomeTax: incomeTaxVal, residentTax: residentTaxVal, healthInsurance, nationalPension: pension, totalTax: incomeTaxVal + residentTaxVal + healthInsurance + pension };
}

// === MATH ===

export function percentage(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const total = inputs.total as number;
  const percent = total > 0 ? value / total * 100 : 0;
  return { percentage: Math.round(percent * 100) / 100, value, total };
}

export function ratio(inputs: Record<string, number | string>): Record<string, number | string> {
  const a = inputs.a as number;
  const b = inputs.b as number;
  const gcdVal = (x: number, y: number): number => { x = Math.abs(x); y = Math.abs(y); while (y) { const t = y; y = x % y; x = t; } return x; };
  const g = gcdVal(a, b);
  const ratioA = g > 0 ? a / g : a;
  const ratioB = g > 0 ? b / g : b;
  return { ratio: `${ratioA}:${ratioB}`, ratioA, ratioB, decimal: b > 0 ? Math.round(a / b * 10000) / 10000 : 0 };
}

export function fraction(inputs: Record<string, number | string>): Record<string, number | string> {
  const numerator = inputs.numerator as number;
  const denominator = inputs.denominator as number;
  if (denominator === 0) return { result: '0', decimal: 0 };
  const gcdVal = (x: number, y: number): number => { x = Math.abs(x); y = Math.abs(y); while (y) { const t = y; y = x % y; x = t; } return x; };
  const g = gcdVal(numerator, denominator);
  return { result: `${numerator/g}/${denominator/g}`, decimal: Math.round(numerator / denominator * 10000) / 10000, simplifiedNumerator: numerator / g, simplifiedDenominator: denominator / g };
}

export function power(inputs: Record<string, number | string>): Record<string, number> {
  const base = inputs.base as number;
  const exponent = inputs.exponent as number;
  const result = Math.pow(base, exponent);
  const sqrt = Math.sqrt(Math.abs(base));
  return { result: Math.round(result * 1000000) / 1000000, squareRoot: Math.round(sqrt * 1000000) / 1000000 };
}

export function gcdLcm(inputs: Record<string, number | string>): Record<string, number> {
  const a = Math.abs(inputs.a as number);
  const b = Math.abs(inputs.b as number);
  const gcdCalc = (x: number, y: number): number => { while (y) { const t = y; y = x % y; x = t; } return x; };
  const gcd = gcdCalc(a, b);
  const lcm = gcd > 0 ? a * b / gcd : 0;
  return { gcd, lcm };
}

export function circle(inputs: Record<string, number | string>): Record<string, number> {
  const radius = inputs.radius as number;
  const area = Math.PI * radius * radius;
  const circumference = 2 * Math.PI * radius;
  const diameter = 2 * radius;
  return { area: Math.round(area * 100) / 100, circumference: Math.round(circumference * 100) / 100, diameter };
}

export function triangle(inputs: Record<string, number | string>): Record<string, number> {
  const base = inputs.base as number;
  const height = inputs.height as number;
  const area = base * height / 2;
  const sideA = inputs.sideA as number || base;
  const sideB = inputs.sideB as number || Math.sqrt(base * base / 4 + height * height);
  const sideC = inputs.sideC as number || sideB;
  const perimeter = sideA + sideB + sideC;
  return { area: Math.round(area * 100) / 100, perimeter: Math.round(perimeter * 100) / 100 };
}

export function rectangle(inputs: Record<string, number | string>): Record<string, number> {
  const width = inputs.width as number;
  const height = inputs.height as number;
  const area = width * height;
  const perimeter = 2 * (width + height);
  const diagonal = Math.sqrt(width * width + height * height);
  return { area: Math.round(area * 100) / 100, perimeter: Math.round(perimeter * 100) / 100, diagonal: Math.round(diagonal * 100) / 100 };
}

export function sphere(inputs: Record<string, number | string>): Record<string, number> {
  const radius = inputs.radius as number;
  const volume = 4 / 3 * Math.PI * Math.pow(radius, 3);
  const surfaceArea = 4 * Math.PI * radius * radius;
  return { volume: Math.round(volume * 100) / 100, surfaceArea: Math.round(surfaceArea * 100) / 100 };
}

export function cylinder(inputs: Record<string, number | string>): Record<string, number> {
  const radius = inputs.radius as number;
  const height = inputs.height as number;
  const volume = Math.PI * radius * radius * height;
  const surfaceArea = 2 * Math.PI * radius * (radius + height);
  return { volume: Math.round(volume * 100) / 100, surfaceArea: Math.round(surfaceArea * 100) / 100 };
}

export function cone(inputs: Record<string, number | string>): Record<string, number> {
  const radius = inputs.radius as number;
  const height = inputs.height as number;
  const slant = Math.sqrt(radius * radius + height * height);
  const volume = Math.PI * radius * radius * height / 3;
  const surfaceArea = Math.PI * radius * (radius + slant);
  return { volume: Math.round(volume * 100) / 100, surfaceArea: Math.round(surfaceArea * 100) / 100, slantHeight: Math.round(slant * 100) / 100 };
}

export function average(inputs: Record<string, number | string>): Record<string, number> {
  const values = (inputs.values as string).split(',').map(Number).filter(n => !isNaN(n));
  const n = values.length;
  if (n === 0) return { average: 0, sum: 0, count: 0, min: 0, max: 0 };
  const sum = values.reduce((a, b) => a + b, 0);
  const avg = sum / n;
  const sorted = [...values].sort((a, b) => a - b);
  return { average: Math.round(avg * 100) / 100, sum: Math.round(sum * 100) / 100, count: n, min: sorted[0], max: sorted[n - 1] };
}

export function standardDeviation(inputs: Record<string, number | string>): Record<string, number> {
  const values = (inputs.values as string).split(',').map(Number).filter(n => !isNaN(n));
  const n = values.length;
  if (n === 0) return { mean: 0, standardDeviation: 0, variance: 0, count: 0 };
  const mean = values.reduce((a, b) => a + b, 0) / n;
  const variance = values.reduce((a, b) => a + (b - mean) ** 2, 0) / n;
  const sd = Math.sqrt(variance);
  return { mean: Math.round(mean * 100) / 100, standardDeviation: Math.round(sd * 100) / 100, variance: Math.round(variance * 100) / 100, count: n };
}

// === EDUCATION ===

export function gpa(inputs: Record<string, number | string>): Record<string, number | string> {
  const grades = (inputs.grades as string).split(',').map(s => s.trim());
  const credits = (inputs.credits as string).split(',').map(Number);
  const gradePoints: Record<string, number> = { 'A+': 4.3, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D': 1.0, 'F': 0 };
  let totalPoints = 0;
  let totalCredits = 0;
  for (let i = 0; i < grades.length && i < credits.length; i++) {
    const gp = gradePoints[grades[i]] ?? parseFloat(grades[i]) ?? 0;
    totalPoints += gp * credits[i];
    totalCredits += credits[i];
  }
  const gpaVal = totalCredits > 0 ? totalPoints / totalCredits : 0;
  let evaluation: string;
  if (gpaVal >= 3.5) evaluation = '優秀'; else if (gpaVal >= 3.0) evaluation = '良好'; else if (gpaVal >= 2.0) evaluation = '普通'; else evaluation = '要改善';
  return { gpa: Math.round(gpaVal * 100) / 100, totalCredits, evaluation };
}

export function examScore(inputs: Record<string, number | string>): Record<string, number> {
  const score = inputs.score as number;
  const totalScore = inputs.totalScore as number;
  const average = inputs.classAverage as number;
  const percentage1 = totalScore > 0 ? Math.round(score / totalScore * 1000) / 10 : 0;
  const deviation = average > 0 ? Math.round((score - average) / average * 100 * 10) / 10 : 0;
  // Simplified deviation score (偏差値)
  const deviationScore = 50 + deviation / 10 * 10;
  return { percentage: percentage1, deviationScore: Math.round(deviationScore * 10) / 10, pointDifference: score - average };
}

export function tuitionCost(inputs: Record<string, number | string>): Record<string, number> {
  const annualTuition = (inputs.annualTuition as number) * 10000;
  const years = inputs.years as number;
  const livingCost = (inputs.monthlyLiving as number) * 10000;
  const totalTuition = annualTuition * years;
  const totalLiving = livingCost * 12 * years;
  const total = totalTuition + totalLiving;
  return { totalTuition: Math.round(totalTuition), totalLiving: Math.round(totalLiving), grandTotal: Math.round(total), monthlyAverage: Math.round(total / (years * 12)) };
}

export function studyTime(inputs: Record<string, number | string>): Record<string, number> {
  const totalPages = inputs.totalPages as number;
  const pagesPerHour = inputs.pagesPerHour as number;
  const daysUntilExam = inputs.daysUntilExam as number;
  const totalHours = pagesPerHour > 0 ? Math.ceil(totalPages / pagesPerHour) : 0;
  const hoursPerDay = daysUntilExam > 0 ? Math.round(totalHours / daysUntilExam * 10) / 10 : 0;
  return { totalHours, hoursPerDay, totalPages, reviewHours: Math.round(totalHours * 0.3) };
}

export function readingSpeed(inputs: Record<string, number | string>): Record<string, number> {
  const characters = inputs.characters as number;
  const minutes = inputs.minutes as number;
  const speed = minutes > 0 ? Math.round(characters / minutes) : 0;
  let level: number;
  if (speed < 400) level = 1; else if (speed < 600) level = 2; else if (speed < 1000) level = 3; else if (speed < 1500) level = 4; else level = 5;
  return { charsPerMinute: speed, wordsPerMinute: Math.round(speed / 2), level, pagesPerHour: Math.round(speed * 60 / 1000) };
}

// === MONEY (additional) ===

export function medicalDeduction(inputs: Record<string, number | string>): Record<string, number> {
  const totalMedical = (inputs.totalMedical as number) * 10000;
  const insurance = (inputs.insuranceReimbursement as number || 0) * 10000;
  const income = (inputs.annualIncome as number) * 10000;
  const threshold = Math.max(100000, income * 0.05);
  const deduction = Math.max(0, Math.min(totalMedical - insurance - threshold, 2000000));
  const taxRate = income > 6950000 ? 0.23 : income > 3300000 ? 0.20 : income > 1950000 ? 0.10 : 0.05;
  return { deduction: Math.round(deduction), taxSaving: Math.round(deduction * taxRate), outOfPocket: Math.round(totalMedical - insurance) };
}

export function sideJobTax(inputs: Record<string, number | string>): Record<string, number> {
  const mainIncome = (inputs.mainIncome as number) * 10000;
  const sideIncome = (inputs.sideIncome as number) * 10000;
  const sideExpenses = (inputs.sideExpenses as number) * 10000;
  const sideProfit = sideIncome - sideExpenses;
  const needsFiling = sideProfit > 200000 ? 1 : 0;
  const taxRate = mainIncome > 6950000 ? 0.23 : mainIncome > 3300000 ? 0.20 : 0.10;
  const additionalTax = Math.round(sideProfit * taxRate * 1.021);
  const residentTax = Math.round(sideProfit * 0.10);
  return { sideProfit: Math.round(sideProfit), needsFiling, additionalIncomeTax: additionalTax, additionalResidentTax: residentTax, totalAdditionalTax: additionalTax + residentTax };
}

export function propertyYield(inputs: Record<string, number | string>): Record<string, number> {
  const purchasePrice = (inputs.purchasePrice as number) * 10000;
  const monthlyRent = (inputs.monthlyRent as number) * 10000;
  const expenses = (inputs.annualExpenses as number) * 10000;
  const annualRent = monthlyRent * 12;
  const grossYield = purchasePrice > 0 ? annualRent / purchasePrice * 100 : 0;
  const netIncome = annualRent - expenses;
  const netYield = purchasePrice > 0 ? netIncome / purchasePrice * 100 : 0;
  return { grossYield: Math.round(grossYield * 100) / 100, netYield: Math.round(netYield * 100) / 100, annualRent: Math.round(annualRent), netIncome: Math.round(netIncome) };
}

export function movingCost(inputs: Record<string, number | string>): Record<string, number> {
  const distance = inputs.distance as number;
  const people = inputs.people as number;
  const season = inputs.season as string;
  let baseCost: number;
  if (people <= 1) baseCost = 30000 + distance * 100;
  else if (people <= 3) baseCost = 60000 + distance * 150;
  else baseCost = 100000 + distance * 200;
  const seasonMultiplier = season === 'peak' ? 1.5 : 1.0;
  const totalCost = Math.round(baseCost * seasonMultiplier);
  return { estimatedCost: totalCost, baseCost: Math.round(baseCost), seasonAdjustment: Math.round(totalCost - baseCost) };
}

export function carInsurance(inputs: Record<string, number | string>): Record<string, number> {
  const age = inputs.age as number;
  const grade = inputs.grade as number;
  const vehicleClass = inputs.vehicleClass as number;
  let basePremium = 50000;
  if (age < 21) basePremium *= 1.8;
  else if (age < 26) basePremium *= 1.3;
  else if (age < 35) basePremium *= 1.0;
  else basePremium *= 0.9;
  const gradeDiscount = Math.max(0.5, 1 - (grade - 6) * 0.03);
  const classMultiplier = 1 + (vehicleClass - 1) * 0.1;
  const annual = Math.round(basePremium * gradeDiscount * classMultiplier);
  return { annualPremium: annual, monthlyPremium: Math.round(annual / 12) };
}

export function annualIncome(inputs: Record<string, number | string>): Record<string, number> {
  const monthlySalary = (inputs.monthlySalary as number) * 10000;
  const bonusMonths = inputs.bonusMonths as number;
  const annualGross = monthlySalary * (12 + bonusMonths);
  return { annualIncome: Math.round(annualGross), monthlyIncome: Math.round(monthlySalary), bonusAmount: Math.round(monthlySalary * bonusMonths) };
}

export function repaymentPlan(inputs: Record<string, number | string>): Record<string, number> {
  const amount = (inputs.amount as number) * 10000;
  const rate = (inputs.rate as number) / 100 / 12;
  const months = (inputs.years as number) * 12;
  const monthly = rate === 0 ? amount / months : amount * rate * Math.pow(1 + rate, months) / (Math.pow(1 + rate, months) - 1);
  const total = monthly * months;
  const firstInterest = amount * rate;
  const firstPrincipal = monthly - firstInterest;
  return { monthlyPayment: Math.round(monthly), totalPayment: Math.round(total), totalInterest: Math.round(total - amount), firstMonthInterest: Math.round(firstInterest), firstMonthPrincipal: Math.round(firstPrincipal) };
}

export function savingsGoal(inputs: Record<string, number | string>): Record<string, number> {
  const target = (inputs.target as number) * 10000;
  const current = (inputs.currentSavings as number) * 10000;
  const months = inputs.months as number;
  const remaining = Math.max(0, target - current);
  const monthlySavings = months > 0 ? Math.ceil(remaining / months) : 0;
  return { monthlySavings: Math.round(monthlySavings), remaining: Math.round(remaining), weeklySavings: Math.round(monthlySavings * 12 / 52) };
}

export function fireCalculation(inputs: Record<string, number | string>): Record<string, number> {
  const annualExpense = (inputs.annualExpense as number) * 10000;
  const withdrawalRate = (inputs.withdrawalRate as number) / 100;
  const fireNumber = withdrawalRate > 0 ? annualExpense / withdrawalRate : 0;
  const currentSavings = (inputs.currentSavings as number) * 10000;
  const gap = Math.max(0, fireNumber - currentSavings);
  const monthlySavings = (inputs.monthlySavings as number) * 10000;
  const yearsToFire = monthlySavings > 0 ? Math.ceil(gap / (monthlySavings * 12)) : 999;
  return { fireNumber: Math.round(fireNumber), gap: Math.round(gap), yearsToFire, monthlyPassiveIncome: Math.round(annualExpense / 12) };
}

export function residentTax(inputs: Record<string, number | string>): Record<string, number> {
  const income = (inputs.annualIncome as number) * 10000;
  const deductionEmp = calcEmploymentDeduction(income);
  const empIncome = Math.max(0, income - deductionEmp);
  // 社会保険料（概算: 健康保険5%+厚生年金9.15%+雇用保険0.6% ≒ 14.75%）
  const si = Math.round(income * 0.1475);
  // 住民税の基礎控除: 43万円
  const basicDeduction = 430_000;
  // 住民税の扶養控除: 33万円/人
  const dependents = (inputs.dependents as number || 0) * 330_000;
  const taxableIncome = Math.max(0, empIncome - si - basicDeduction - dependents);
  // 所得割: 都道府県民税4% + 市区町村民税6% = 10%
  const prefectureTax = Math.round(taxableIncome * 0.04);
  const cityTax = Math.round(taxableIncome * 0.06);
  // 調整控除（基礎控除分）: 最低2,500円
  const adjustmentDeduction = 2_500;
  // 均等割: 都道府県1,500円 + 市区町村3,500円 = 5,000円（2026年度）
  const equalRate = 5_000;
  const incomePortion = Math.max(0, prefectureTax + cityTax - adjustmentDeduction);
  const total = incomePortion + equalRate;
  return { totalResidentTax: total, monthlyTax: Math.round(total / 12), prefectureTax, cityTax };
}

export function partTimeIncome(inputs: Record<string, number | string>): Record<string, number> {
  const hourlyWageVal = inputs.hourlyWage as number;
  const hoursPerWeek = inputs.hoursPerWeek as number;
  const weeksPerMonth = 4.33;
  const monthlyIncome = Math.round(hourlyWageVal * hoursPerWeek * weeksPerMonth);
  const annualIncome1 = monthlyIncome * 12;
  const wall103 = annualIncome1 > 1030000 ? 1 : 0;
  const wall130 = annualIncome1 > 1300000 ? 1 : 0;
  return { monthlyIncome, annualIncome: annualIncome1, exceeds103: wall103, exceeds130: wall130 };
}

export function overtimeIncome(inputs: Record<string, number | string>): Record<string, number> {
  const baseSalary = (inputs.baseSalary as number) * 10000;
  const workDays1 = inputs.workDays as number;
  const hoursPerDay = inputs.hoursPerDay as number;
  const overtimeHours = inputs.overtimeHours as number;
  const hourlyBase = baseSalary / (workDays1 * hoursPerDay);
  const overtimePay1 = Math.round(hourlyBase * 1.25 * overtimeHours);
  return { overtimePay: overtimePay1, hourlyRate: Math.round(hourlyBase), totalMonthly: Math.round(baseSalary + overtimePay1), annualOvertime: overtimePay1 * 12 };
}

export function survivorPension(inputs: Record<string, number | string>): Record<string, number> {
  const avgSalary = (inputs.averageSalary as number) * 10000;
  const children = inputs.children as number;
  const basicPension = 816000;
  const childAddition = children >= 1 ? 234800 : 0;
  const secondChild = children >= 2 ? 234800 : 0;
  const thirdPlus = Math.max(0, children - 2) * 78300;
  const basicTotal = basicPension + childAddition + secondChild + thirdPlus;
  const welfarePortion = Math.round(avgSalary * 0.005481 * 25 * 0.75);
  const total = basicTotal + welfarePortion;
  return { basicPension: basicTotal, welfarePension: welfarePortion, totalAnnual: total, totalMonthly: Math.round(total / 12) };
}

export function disabilityPension(inputs: Record<string, number | string>): Record<string, number> {
  const grade = inputs.grade as number;
  const avgSalary = (inputs.averageSalary as number) * 10000;
  const basicPension = grade === 1 ? 1020000 : 816000;
  const childAddition = (inputs.children as number || 0) >= 1 ? 234800 : 0;
  const welfarePortion = grade === 1 ? Math.round(avgSalary * 0.005481 * 25 * 1.25) : Math.round(avgSalary * 0.005481 * 25);
  const spouseAddition = grade === 1 || grade === 2 ? 234800 : 0;
  const total = basicPension + childAddition + welfarePortion + spouseAddition;
  return { basicPension: basicPension + childAddition, welfarePension: welfarePortion + spouseAddition, totalAnnual: total, totalMonthly: Math.round(total / 12) };
}

export function earthquakeInsurance(inputs: Record<string, number | string>): Record<string, number> {
  const buildingValue = (inputs.buildingValue as number) * 10000;
  const structure = inputs.structure as string;
  const region = inputs.region as number;
  const maxCoverage = Math.min(buildingValue * 0.5, 50000000);
  const baseRate = structure === 'wood' ? 0.0036 : 0.0017;
  const regionMultiplier = [1.0, 1.0, 1.4, 1.8, 2.5, 3.6][region - 1] || 1.0;
  const annualPremium = Math.round(maxCoverage / 1000 * baseRate * 1000 * regionMultiplier);
  return { maxCoverage: Math.round(maxCoverage), annualPremium, fiveYearPremium: Math.round(annualPremium * 4.6), taxDeduction: Math.min(annualPremium, 50000) };
}

export function renovationCost(inputs: Record<string, number | string>): Record<string, number> {
  const area = inputs.area as number;
  const type = inputs.type as string;
  let costPerSqm: number;
  if (type === 'full') costPerSqm = 150000;
  else if (type === 'kitchen') costPerSqm = 200000;
  else if (type === 'bathroom') costPerSqm = 250000;
  else costPerSqm = 100000;
  const baseCost = area * costPerSqm;
  const designFee = Math.round(baseCost * 0.10);
  const contingency = Math.round(baseCost * 0.10);
  return { baseCost: Math.round(baseCost), designFee, contingency, totalCost: Math.round(baseCost + designFee + contingency) };
}

export function dollarCostAvg(inputs: Record<string, number | string>): Record<string, number> {
  const monthlyAmount = (inputs.monthlyAmount as number) * 10000;
  const months = inputs.months as number;
  const returnRate = (inputs.expectedReturn as number) / 100 / 12;
  let balance = 0;
  for (let i = 0; i < months; i++) {
    balance = (balance + monthlyAmount) * (1 + returnRate);
  }
  const totalInvested = monthlyAmount * months;
  const profit = balance - totalInvested;
  return { finalAmount: Math.round(balance), totalInvested: Math.round(totalInvested), profit: Math.round(profit), returnRate: totalInvested > 0 ? Math.round(profit / totalInvested * 1000) / 10 : 0 };
}

export function yearEndAdjustment(inputs: Record<string, number | string>): Record<string, number> {
  const annualSalary = (inputs.annualSalary as number) * 10000;
  const taxWithheld = (inputs.taxWithheld as number) * 10000;
  const lifeInsurance = (inputs.lifeInsuranceDeduction as number) * 10000;
  const mortgage = (inputs.mortgageDeduction as number) * 10000;
  const deductionEmp = calcEmploymentDeduction(annualSalary);
  const empIncome = Math.max(0, annualSalary - deductionEmp);
  const si = annualSalary * 0.15;
  const taxableIncome = Math.max(0, empIncome - si - 480000 - Math.min(lifeInsurance, 120000));
  const correctTax = Math.round(calcIncomeTaxAmount(taxableIncome) * 1.021);
  const finalTax = Math.max(0, correctTax - mortgage);
  const refund = taxWithheld - finalTax;
  return { correctTax: finalTax, refund: Math.round(refund), taxWithheld: Math.round(taxWithheld) };
}

export function raiseImpact(inputs: Record<string, number | string>): Record<string, number> {
  const currentSalary = (inputs.currentSalary as number) * 10000;
  const raisePercent = inputs.raisePercent as number;
  const raiseAmount = Math.round(currentSalary * raisePercent / 100);
  const newSalary = currentSalary + raiseAmount;
  const annualIncrease = raiseAmount * 12;
  // Approximate after-tax increase (assume ~30% total tax)
  const afterTaxIncrease = Math.round(annualIncrease * 0.70);
  return { monthlyIncrease: raiseAmount, annualIncrease, afterTaxIncrease, newMonthlySalary: Math.round(newSalary) };
}

export function creditCardInterest(inputs: Record<string, number | string>): Record<string, number> {
  const balance = (inputs.balance as number) * 10000;
  const annualRate = (inputs.annualRate as number) / 100;
  const monthlyPayment = (inputs.monthlyPayment as number) * 10000;
  const monthlyRate = annualRate / 12;
  let remaining = balance;
  let totalPaid = 0;
  let months = 0;
  while (remaining > 0 && months < 600) {
    const interest = remaining * monthlyRate;
    const principal = monthlyPayment - interest;
    if (principal <= 0) { months = 999; break; }
    remaining -= principal;
    totalPaid += monthlyPayment;
    months++;
  }
  if (remaining > 0 && months < 600) totalPaid += remaining;
  const totalInterest = totalPaid - balance;
  return { totalInterest: Math.round(totalInterest), months, totalPayment: Math.round(totalPaid) };
}

// === 追加計算ツール 24個 ===

export function electricityCost(inputs: Record<string, number | string>): Record<string, number> {
  const kwh = inputs.kwh as number;
  const unitPrice = inputs.unitPrice as number;
  const basicCharge = inputs.basicCharge as number;
  const fuelAdjustment = inputs.fuelAdjustment as number;
  const renewableLevy = inputs.renewableLevy as number;
  const usageCharge = kwh * unitPrice;
  const fuelAdj = kwh * fuelAdjustment;
  const renewable = kwh * renewableLevy;
  const subtotal = basicCharge + usageCharge + fuelAdj + renewable;
  const tax = Math.round(subtotal * 0.1);
  const total = subtotal + tax;
  return { usageCharge: Math.round(usageCharge), fuelAdj: Math.round(fuelAdj), renewable: Math.round(renewable), subtotal: Math.round(subtotal), tax, total: Math.round(total) };
}

export function gasCost(inputs: Record<string, number | string>): Record<string, number> {
  const cubicMeters = inputs.cubicMeters as number;
  const unitPrice = inputs.unitPrice as number;
  const basicCharge = inputs.basicCharge as number;
  const usageCharge = cubicMeters * unitPrice;
  const subtotal = basicCharge + usageCharge;
  const tax = Math.round(subtotal * 0.1);
  const total = subtotal + tax;
  const annual = total * 12;
  return { usageCharge: Math.round(usageCharge), subtotal: Math.round(subtotal), tax, total: Math.round(total), annual: Math.round(annual) };
}

export function waterCost(inputs: Record<string, number | string>): Record<string, number> {
  const cubicMeters = inputs.cubicMeters as number;
  const basicCharge = inputs.basicCharge as number;
  const unitPrice = inputs.unitPrice as number;
  const sewageRate = (inputs.sewageRate as number) / 100;
  const waterCharge = basicCharge + cubicMeters * unitPrice;
  const sewageCharge = Math.round(waterCharge * sewageRate);
  const total = waterCharge + sewageCharge;
  const biMonthly = total;
  const monthly = Math.round(total / 2);
  const annual = total * 6;
  return { waterCharge: Math.round(waterCharge), sewageCharge, total: Math.round(biMonthly), monthly, annual: Math.round(annual) };
}

export function internetCost(inputs: Record<string, number | string>): Record<string, number> {
  const monthlyFee = inputs.monthlyFee as number;
  const initialCost = inputs.initialCost as number;
  const contractMonths = inputs.contractMonths as number;
  const discount = inputs.discount as number;
  const totalMonthly = (monthlyFee - discount) * contractMonths;
  const totalCost = totalMonthly + initialCost;
  const effectiveMonthly = Math.round(totalCost / contractMonths);
  const annualCost = effectiveMonthly * 12;
  return { effectiveMonthly, totalCost: Math.round(totalCost), annualCost, totalMonthly: Math.round(totalMonthly) };
}

export function stepsToDistance(inputs: Record<string, number | string>): Record<string, number> {
  const steps = inputs.steps as number;
  const strideLength = inputs.strideLength as number;
  const distanceM = steps * strideLength / 100;
  const distanceKm = distanceM / 1000;
  const caloriesBurned = Math.round(steps * 0.04);
  const timeMin = Math.round(steps / 100);
  return { distanceM: Math.round(distanceM), distanceKm: Math.round(distanceKm * 100) / 100, caloriesBurned, timeMin };
}

export function sleepCalculator(inputs: Record<string, number | string>): Record<string, string> {
  const wakeHour = inputs.wakeHour as number;
  const wakeMin = inputs.wakeMin as number;
  const cycles = [4, 5, 6];
  const results: Record<string, string> = {};
  for (const c of cycles) {
    const sleepMinutes = c * 90 + 15;
    let bedHour = wakeHour - Math.floor(sleepMinutes / 60);
    let bedMin = wakeMin - (sleepMinutes % 60);
    if (bedMin < 0) { bedMin += 60; bedHour -= 1; }
    if (bedHour < 0) bedHour += 24;
    const hours = Math.floor((c * 90) / 60);
    const mins = (c * 90) % 60;
    results[`bed${c}`] = `${String(bedHour).padStart(2, '0')}:${String(bedMin).padStart(2, '0')}`;
    results[`duration${c}`] = `${hours}時間${mins > 0 ? mins + '分' : ''}`;
  }
  return results;
}

export function alcoholBreakdown(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const drinkType = inputs.drinkType as string;
  const amount = inputs.amount as number;
  const alcoholPercentMap: Record<string, number> = { beer: 5, wine: 12, sake: 15, shochu: 25, whisky: 40, chuhai: 7 };
  const percent = alcoholPercentMap[drinkType] || 5;
  const pureAlcohol = amount * (percent / 100) * 0.8;
  const breakdownRate = weight * 0.1;
  const hours = pureAlcohol / breakdownRate;
  const fullHours = Math.floor(hours);
  const minutes = Math.round((hours - fullHours) * 60);
  return { pureAlcohol: Math.round(pureAlcohol * 10) / 10, hours: fullHours, minutes, totalMinutes: Math.round(hours * 60), driveOk: `${fullHours + Math.ceil(minutes / 60) + 1}時間後以降` };
}

export function dogAge(inputs: Record<string, number | string>): Record<string, number> {
  const dogYears = inputs.dogYears as number;
  const size = inputs.size as string;
  let humanAge: number;
  if (size === 'small' || size === 'medium') {
    humanAge = dogYears <= 2 ? dogYears * 12.5 : 25 + (dogYears - 2) * 4;
  } else {
    humanAge = dogYears <= 2 ? dogYears * 12.5 : 25 + (dogYears - 2) * 5;
  }
  return { humanAge: Math.round(humanAge), dogYears };
}

export function catAge(inputs: Record<string, number | string>): Record<string, number> {
  const catYears = inputs.catYears as number;
  let humanAge: number;
  if (catYears <= 1) humanAge = catYears * 18;
  else if (catYears <= 2) humanAge = 18 + (catYears - 1) * 7;
  else humanAge = 25 + (catYears - 2) * 4;
  return { humanAge: Math.round(humanAge), catYears };
}

export function timezoneCalc(inputs: Record<string, number | string>): Record<string, string> {
  const hour = inputs.hour as number;
  const minute = inputs.minute as number;
  const fromOffset = inputs.fromOffset as number;
  const toOffset = inputs.toOffset as number;
  const diff = toOffset - fromOffset;
  let newHour = hour + diff;
  let newMin = minute;
  let dayShift = 0;
  if (newHour >= 24) { newHour -= 24; dayShift = 1; }
  if (newHour < 0) { newHour += 24; dayShift = -1; }
  const dayText = dayShift === 1 ? '（翌日）' : dayShift === -1 ? '（前日）' : '';
  return {
    convertedTime: `${String(newHour).padStart(2, '0')}:${String(newMin).padStart(2, '0')}${dayText}`,
    timeDiff: `${diff >= 0 ? '+' : ''}${diff}時間`,
  };
}

export function birthdayCountdown(inputs: Record<string, number | string>): Record<string, number | string> {
  const month = inputs.month as number;
  const day = inputs.day as number;
  const now = new Date();
  const thisYear = now.getFullYear();
  let nextBirthday = new Date(thisYear, month - 1, day);
  if (nextBirthday.getTime() <= now.getTime()) {
    nextBirthday = new Date(thisYear + 1, month - 1, day);
  }
  const diffMs = nextBirthday.getTime() - now.getTime();
  const daysLeft = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
  const weeksLeft = Math.floor(daysLeft / 7);
  const dayOfWeek = ['日', '月', '火', '水', '木', '金', '土'][nextBirthday.getDay()];
  return { daysLeft, weeksLeft, nextBirthdayDate: `${nextBirthday.getFullYear()}年${month}月${day}日（${dayOfWeek}）` };
}

export function ovulationCalc(inputs: Record<string, number | string>): Record<string, string> {
  const lastPeriod = inputs.lastPeriod as string;
  const cycleLength = inputs.cycleLength as number;
  const d = new Date(lastPeriod);
  const ovulationDate = new Date(d.getTime() + (cycleLength - 14) * 86400000);
  const fertileStart = new Date(ovulationDate.getTime() - 5 * 86400000);
  const fertileEnd = new Date(ovulationDate.getTime() + 1 * 86400000);
  const nextPeriod = new Date(d.getTime() + cycleLength * 86400000);
  const fmt = (dt: Date) => `${dt.getFullYear()}年${dt.getMonth() + 1}月${dt.getDate()}日`;
  return { ovulationDate: fmt(ovulationDate), fertileStart: fmt(fertileStart), fertileEnd: fmt(fertileEnd), nextPeriod: fmt(nextPeriod) };
}

export function maternityLeave(inputs: Record<string, number | string>): Record<string, string> {
  const dueDate = inputs.dueDate as string;
  const d = new Date(dueDate);
  const prenatalStart = new Date(d.getTime() - 42 * 86400000);
  const postnatalEnd = new Date(d.getTime() + 56 * 86400000);
  const childcareEnd1 = new Date(d.getFullYear() + 1, d.getMonth(), d.getDate());
  const childcareEnd2 = new Date(d.getFullYear() + 2, d.getMonth(), d.getDate());
  const fmt = (dt: Date) => `${dt.getFullYear()}年${dt.getMonth() + 1}月${dt.getDate()}日`;
  return { prenatalStart: fmt(prenatalStart), postnatalEnd: fmt(postnatalEnd), childcareEnd1: fmt(childcareEnd1), childcareEnd2: fmt(childcareEnd2) };
}

export function unemploymentInsurance(inputs: Record<string, number | string>): Record<string, number> {
  const dailyWage = inputs.dailyWage as number;
  const age = inputs.age as number;
  const yearsWorked = inputs.yearsWorked as number;
  let rate: number;
  if (dailyWage < 5110) rate = 0.8;
  else if (dailyWage < 12580) rate = 0.65;
  else rate = 0.5;
  const dailyAllowance = Math.min(Math.round(dailyWage * rate), age < 30 ? 7065 : age < 45 ? 7845 : age < 60 ? 8635 : 7150);
  let totalDays: number;
  if (yearsWorked < 1) totalDays = 90;
  else if (yearsWorked < 5) totalDays = 90;
  else if (yearsWorked < 10) totalDays = 120;
  else if (yearsWorked < 20) totalDays = 150;
  else totalDays = 150;
  const totalAmount = dailyAllowance * totalDays;
  const monthlyEstimate = Math.round(dailyAllowance * 28);
  return { dailyAllowance, totalDays, totalAmount, monthlyEstimate };
}

export function movingEstimate(inputs: Record<string, number | string>): Record<string, number> {
  const people = inputs.people as number;
  const distance = inputs.distance as number;
  const season = inputs.season as string;
  let baseCost: number;
  if (people === 1) baseCost = 35000;
  else if (people === 2) baseCost = 60000;
  else if (people === 3) baseCost = 80000;
  else baseCost = 100000 + (people - 4) * 20000;
  const distanceFee = distance < 50 ? 0 : distance < 200 ? 20000 : distance < 500 ? 50000 : 80000;
  const seasonMultiplier = season === 'peak' ? 1.5 : season === 'off' ? 0.8 : 1.0;
  const estimate = Math.round((baseCost + distanceFee) * seasonMultiplier);
  const low = Math.round(estimate * 0.8);
  const high = Math.round(estimate * 1.3);
  return { estimate, low, high };
}

export function rentBudget(inputs: Record<string, number | string>): Record<string, number> {
  const monthlyIncome = inputs.monthlyIncome as number;
  const ratio = (inputs.ratio as number) / 100;
  const budget = Math.round(monthlyIncome * ratio);
  const annualRent = budget * 12;
  const initialCost = budget * 5;
  return { budget, annualRent, initialCost, monthlyIncome };
}

export function condoMonthly(inputs: Record<string, number | string>): Record<string, number> {
  const loanPayment = inputs.loanPayment as number;
  const managementFee = inputs.managementFee as number;
  const repairReserve = inputs.repairReserve as number;
  const parkingFee = inputs.parkingFee as number;
  const otherFee = inputs.otherFee as number;
  const total = loanPayment + managementFee + repairReserve + parkingFee + otherFee;
  const annual = total * 12;
  return { total, annual, nonLoan: managementFee + repairReserve + parkingFee + otherFee };
}

export function furusatoDetail(inputs: Record<string, number | string>): Record<string, number> {
  const annualIncome = (inputs.annualIncome as number) * 10000;
  const familyType = inputs.familyType as string;
  // 1. 給与所得控除を適用
  const employmentDeduction = calcEmploymentDeduction(annualIncome);
  const employmentIncome = Math.max(0, annualIncome - employmentDeduction);
  // 2. 社会保険料（概算15%）
  const socialInsurance = annualIncome * 0.15;
  // 3. 扶養控除（住民税基準）
  let dependentDeduction: number;
  if (familyType === 'single') dependentDeduction = 0;
  else if (familyType === 'couple') dependentDeduction = 330_000; // 配偶者控除（住民税）
  else dependentDeduction = 330_000 + 330_000; // 配偶者+扶養1人
  // 4. 基礎控除（住民税）
  const basicDeduction = 430_000;
  // 5. 課税所得（住民税ベース）
  const taxableIncome = Math.max(0, employmentIncome - socialInsurance - basicDeduction - dependentDeduction);
  // 6. 所得税の課税所得（基礎控除480,000）
  const taxableIncomeIT = Math.max(0, employmentIncome - socialInsurance - 480_000 - (familyType === 'single' ? 0 : familyType === 'couple' ? 380_000 : 760_000));
  // 7. 所得税率の特定
  let incomeTaxRate: number;
  if (taxableIncomeIT <= 1_950_000) incomeTaxRate = 0.05;
  else if (taxableIncomeIT <= 3_300_000) incomeTaxRate = 0.10;
  else if (taxableIncomeIT <= 6_950_000) incomeTaxRate = 0.20;
  else if (taxableIncomeIT <= 9_000_000) incomeTaxRate = 0.23;
  else if (taxableIncomeIT <= 18_000_000) incomeTaxRate = 0.33;
  else if (taxableIncomeIT <= 40_000_000) incomeTaxRate = 0.40;
  else incomeTaxRate = 0.45;
  // 8. ふるさと納税上限額 = 住民税所得割額×20% ÷ (100%-所得税率×1.021-10%) + 2,000円
  const residentTaxIncomePortion = Math.round(taxableIncome * 0.10);
  const denominator = 1 - incomeTaxRate * 1.021 - 0.10;
  const limit = denominator > 0
    ? Math.round(residentTaxIncomePortion * 0.20 / denominator + 2000)
    : 2000;
  return { limit: Math.max(limit, 2000), taxableIncome: Math.round(taxableIncome), taxRate: Math.round(incomeTaxRate * 100) };
}

export function spouseDeduction(inputs: Record<string, number | string>): Record<string, number> {
  const taxpayerIncome = (inputs.taxpayerIncome as number) * 10000;
  const spouseIncome = (inputs.spouseIncome as number) * 10000;
  let deduction = 0;
  if (taxpayerIncome <= 9000000) {
    if (spouseIncome <= 480000) deduction = 380000;
    else if (spouseIncome <= 950000) deduction = 380000;
    else if (spouseIncome <= 1000000) deduction = 360000;
    else if (spouseIncome <= 1050000) deduction = 310000;
    else if (spouseIncome <= 1100000) deduction = 260000;
    else if (spouseIncome <= 1150000) deduction = 210000;
    else if (spouseIncome <= 1200000) deduction = 160000;
    else if (spouseIncome <= 1250000) deduction = 110000;
    else if (spouseIncome <= 1300000) deduction = 60000;
    else if (spouseIncome <= 1330000) deduction = 30000;
  } else if (taxpayerIncome <= 9500000) {
    if (spouseIncome <= 950000) deduction = 260000;
    else if (spouseIncome <= 1330000) deduction = Math.max(260000 - Math.floor((spouseIncome - 950000) / 50000) * 40000, 0);
  } else if (taxpayerIncome <= 10000000) {
    if (spouseIncome <= 950000) deduction = 130000;
    else if (spouseIncome <= 1330000) deduction = Math.max(130000 - Math.floor((spouseIncome - 950000) / 50000) * 20000, 0);
  }
  const taxSaving = Math.round(deduction * 0.2);
  return { deduction, taxSaving, spouseIncome: Math.round(spouseIncome) };
}

export function dependentDeduction(inputs: Record<string, number | string>): Record<string, number> {
  const dependentAge = inputs.dependentAge as number;
  const livingTogether = inputs.livingTogether as number;
  let deduction: number;
  if (dependentAge < 16) deduction = 0;
  else if (dependentAge < 19) deduction = 380000;
  else if (dependentAge < 23) deduction = 630000;
  else if (dependentAge < 70) deduction = 380000;
  else deduction = livingTogether === 1 ? 580000 : 480000;
  const taxSaving = Math.round(deduction * 0.2);
  const residentTaxSaving = Math.round(deduction * 0.1);
  return { deduction, taxSaving, residentTaxSaving, totalSaving: taxSaving + residentTaxSaving };
}

export function educationCostSim(inputs: Record<string, number | string>): Record<string, number> {
  const childAge = inputs.childAge as number;
  const plan = inputs.plan as string;
  const costs: Record<string, number[]> = {
    all_public: [230000, 230000, 230000, 300000, 300000, 300000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 500000, 550000, 550000, 550000],
    all_private: [500000, 500000, 500000, 1000000, 1000000, 1000000, 1400000, 1400000, 1400000, 1000000, 1000000, 1000000, 1000000, 1000000, 1000000, 1500000, 1500000, 1500000, 1500000],
  };
  const costArray = costs[plan] || costs.all_public;
  const startIdx = Math.max(childAge - 3, 0);
  let totalRemaining = 0;
  for (let i = startIdx; i < costArray.length; i++) {
    totalRemaining += costArray[i];
  }
  const yearsLeft = costArray.length - startIdx;
  const monthlyNeeded = yearsLeft > 0 ? Math.round(totalRemaining / (yearsLeft * 12)) : 0;
  return { totalRemaining, yearsLeft, monthlyNeeded };
}

export function scholarshipRepayment(inputs: Record<string, number | string>): Record<string, number> {
  const totalBorrowed = (inputs.totalBorrowed as number) * 10000;
  const annualRate = (inputs.annualRate as number) / 100;
  const repaymentYears = inputs.repaymentYears as number;
  const monthlyRate = annualRate / 12;
  const totalMonths = repaymentYears * 12;
  let monthlyPayment: number;
  if (monthlyRate === 0) {
    monthlyPayment = totalBorrowed / totalMonths;
  } else {
    monthlyPayment = totalBorrowed * monthlyRate * Math.pow(1 + monthlyRate, totalMonths) / (Math.pow(1 + monthlyRate, totalMonths) - 1);
  }
  const totalPayment = monthlyPayment * totalMonths;
  const totalInterest = totalPayment - totalBorrowed;
  return { monthlyPayment: Math.round(monthlyPayment), totalPayment: Math.round(totalPayment), totalInterest: Math.round(totalInterest) };
}

export function wifiSpeed(inputs: Record<string, number | string>): Record<string, number> {
  const speedMbps = inputs.speedMbps as number;
  const speedMBs = speedMbps / 8;
  const speedGbps = speedMbps / 1000;
  const downloadTime1GB = Math.round(1024 / speedMBs);
  const downloadTime100MB = Math.round(100 / speedMBs);
  return { speedMBs: Math.round(speedMBs * 100) / 100, speedGbps: Math.round(speedGbps * 1000) / 1000, downloadTime1GB, downloadTime100MB };
}

export function tsuboSqm(inputs: Record<string, number | string>): Record<string, number> {
  const value = inputs.value as number;
  const direction = inputs.direction as string;
  if (direction === 'tsubo_to_sqm') {
    const sqm = value * 3.30579;
    const jo = value * 2;
    return { sqm: Math.round(sqm * 100) / 100, jo: Math.round(jo * 100) / 100, tsubo: value };
  } else {
    const tsubo = value / 3.30579;
    const jo = tsubo * 2;
    return { sqm: value, tsubo: Math.round(tsubo * 100) / 100, jo: Math.round(jo * 100) / 100 };
  }
}


export function adRoas(inputs: Record<string, number | string>): Record<string, number | string> {
  const adSpend = Number(inputs.adSpend ?? 0);
  const revenue = Number(inputs.revenue ?? 0);
  const conversions = Number(inputs.conversions ?? 0);
  return {
    roas: Math.round(adSpend * revenue),
    cpa: Math.round(adSpend),
    profit: Math.round(adSpend)
  };
}

export function advancePayment(inputs: Record<string, number | string>): Record<string, number | string> {
  const loanBalance = Number(inputs.loanBalance ?? 0);
  const rate = Number(inputs.rate ?? 0);
  const remainingYears = Number(inputs.remainingYears ?? 0);
  const advanceAmount = Number(inputs.advanceAmount ?? 0);
  const type = String(inputs.type ?? '');
  return {
    interestSaved: Math.round(loanBalance * rate),
    termReduction: Math.round(loanBalance),
    monthlyReduction: Math.round(loanBalance)
  };
}

export function airConditionerCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const capacity = Number(inputs.capacity ?? 0);
  const hoursPerDay = Number(inputs.hoursPerDay ?? 0);
  const days = Number(inputs.days ?? 0);
  const pricePerKwh = Number(inputs.pricePerKwh ?? 0);
  return {
    monthlyCost: Math.round(capacity * hoursPerDay),
    dailyCost: Math.round(capacity),
    seasonCost: Math.round(capacity)
  };
}

export function alcoholCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const drinkType = String(inputs.drinkType ?? '');
  const amount = Number(inputs.amount ?? 0);
  return {
    calories: amount,
    pureAlcohol: Math.round(amount),
    drinkUnit: Math.round(amount),
    decompositionTime: Math.round(amount)
  };
}

export function alcoholTobaccoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const product = String(inputs.product ?? '');
  const price = Number(inputs.price ?? 0);
  return {
    taxAmount: price,
    taxRatio: Math.round(price),
    preTaxPrice: Math.round(price)
  };
}

export function anniversary(inputs: Record<string, number | string>): Record<string, number | string> {
  const startDate = Number(inputs.startDate ?? 0);
  return {
    days100: startDate,
    days200: Math.round(startDate),
    days365: Math.round(startDate),
    days500: Math.round(startDate),
    days1000: Math.round(startDate),
    elapsedDays: Math.round(startDate)
  };
}

export function assetAllocation(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = Number(inputs.age ?? 0);
  const riskTolerance = String(inputs.riskTolerance ?? '');
  const totalAsset = Number(inputs.totalAsset ?? 0);
  return {
    stockRatio: Math.round(age * totalAsset),
    bondRatio: Math.round(age),
    cashRatio: Math.round(age),
    stockAmount: Math.round(age),
    bondAmount: Math.round(age)
  };
}

export function autoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const displacement = String(inputs.displacement ?? '');
  const years = Number(inputs.years ?? 0);
  return {
    annualTax: years,
    monthlyTax: Math.round(years),
    heavyTax: Math.round(years)
  };
}

export function babyGrowth(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthsAge = Number(inputs.monthsAge ?? 0);
  const gender = String(inputs.gender ?? '');
  const weight = Number(inputs.weight ?? 0);
  const height = Number(inputs.height ?? 0);
  return {
    weightStatus: Math.round(monthsAge * weight),
    heightStatus: Math.round(monthsAge),
    avgWeight: Math.round(monthsAge),
    avgHeight: Math.round(monthsAge)
  };
}

export function baseConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  return {
    decimal: value,
    binary: Math.round(value),
    octal: Math.round(value),
    hex: Math.round(value)
  };
}

export function bloodAlcohol(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const gender = String(inputs.gender ?? '');
  const pureAlcohol = Number(inputs.pureAlcohol ?? 0);
  const hours = Number(inputs.hours ?? 0);
  return {
    bac: Math.round(weight * pureAlcohol),
    soberTime: Math.round(weight),
    status: Math.round(weight)
  };
}

export function blueReturn(inputs: Record<string, number | string>): Record<string, number | string> {
  const businessIncome = Number(inputs.businessIncome ?? 0);
  const deductionType = String(inputs.deductionType ?? '');
  return {
    taxSavings: businessIncome,
    residentTaxSavings: Math.round(businessIncome),
    totalSavings: Math.round(businessIncome)
  };
}

export function bmiChild(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = Number(inputs.age ?? 0);
  const height = Number(inputs.height ?? 0);
  const weight = Number(inputs.weight ?? 0);
  const gender = String(inputs.gender ?? '');
  return {
    bmi: Math.round(age * height),
    rohrer: Math.round(age),
    status: Math.round(age),
    standardWeight: Math.round(age)
  };
}

export function bmiDetailed(inputs: Record<string, number | string>): Record<string, number | string> {
  const height = Number(inputs.height ?? 0);
  const weight = Number(inputs.weight ?? 0);
  return {
    bmi: Math.round(height * weight),
    category: Math.round(height),
    idealWeight: Math.round(height),
    weightDiff: Math.round(height)
  };
}

export function bmiPet(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const idealWeight = Number(inputs.idealWeight ?? 0);
  return {
    bcsScore: Math.round(weight * idealWeight),
    weightDiff: Math.round(weight),
    overweightPercent: Math.round(weight)
  };
}

export function bodyFatPercentage(inputs: Record<string, number | string>): Record<string, number | string> {
  const height = Number(inputs.height ?? 0);
  const weight = Number(inputs.weight ?? 0);
  const age = Number(inputs.age ?? 0);
  const gender = String(inputs.gender ?? '');
  return {
    bodyFat: Math.round(height * weight),
    bmi: Math.round(height),
    category: Math.round(height)
  };
}

export function bondYield(inputs: Record<string, number | string>): Record<string, number | string> {
  const faceValue = Number(inputs.faceValue ?? 0);
  const purchasePrice = Number(inputs.purchasePrice ?? 0);
  const couponRate = Number(inputs.couponRate ?? 0);
  const yearsToMaturity = Number(inputs.yearsToMaturity ?? 0);
  return {
    directYield: Math.round(faceValue * purchasePrice),
    yieldToMaturity: Math.round(faceValue),
    annualIncome: Math.round(faceValue)
  };
}

export function businessDays(inputs: Record<string, number | string>): Record<string, number | string> {
  const startDate = Number(inputs.startDate ?? 0);
  const days = Number(inputs.days ?? 0);
  return {
    endDate: Math.round(startDate * days),
    calendarDays: Math.round(startDate),
    weekends: Math.round(startDate)
  };
}

export function caffeine(inputs: Record<string, number | string>): Record<string, number | string> {
  const coffee = Number(inputs.coffee ?? 0);
  const tea = Number(inputs.tea ?? 0);
  const greenTea = Number(inputs.greenTea ?? 0);
  const energyDrink = Number(inputs.energyDrink ?? 0);
  return {
    totalCaffeine: Math.round(coffee * tea),
    status: Math.round(coffee),
    safeLimit: Math.round(coffee)
  };
}

export function capitalGainsTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const salePrice = Number(inputs.salePrice ?? 0);
  const purchasePrice = Number(inputs.purchasePrice ?? 0);
  const expenses = Number(inputs.expenses ?? 0);
  const assetType = String(inputs.assetType ?? '');
  return {
    gain: Math.round(salePrice * purchasePrice),
    incomeTax: Math.round(salePrice),
    residentTax: Math.round(salePrice),
    totalTax: Math.round(salePrice)
  };
}

export function carCostTotal(inputs: Record<string, number | string>): Record<string, number | string> {
  const carType = String(inputs.carType ?? '');
  const annualMileage = Number(inputs.annualMileage ?? 0);
  const fuelEfficiency = Number(inputs.fuelEfficiency ?? 0);
  const fuelPrice = Number(inputs.fuelPrice ?? 0);
  return {
    taxCost: Math.round(annualMileage * fuelEfficiency),
    insuranceCost: Math.round(annualMileage),
    inspectionCost: Math.round(annualMileage),
    fuelCostTotal: Math.round(annualMileage),
    totalAnnualCost: Math.round(annualMileage),
    monthlyCost: Math.round(annualMileage)
  };
}

export function carLease(inputs: Record<string, number | string>): Record<string, number | string> {
  const carPrice = Number(inputs.carPrice ?? 0);
  const leaseMonthly = Number(inputs.leaseMonthly ?? 0);
  const leaseYears = Number(inputs.leaseYears ?? 0);
  const residualRate = Number(inputs.residualRate ?? 0);
  return {
    leaseTotalCost: Math.round(carPrice * leaseMonthly),
    purchaseTotalCost: Math.round(carPrice),
    difference: Math.round(carPrice),
    monthlyDiff: Math.round(carPrice)
  };
}

export function carbonFootprint(inputs: Record<string, number | string>): Record<string, number | string> {
  const carKm = Number(inputs.carKm ?? 0);
  const electricityKwh = Number(inputs.electricityKwh ?? 0);
  const gasM3 = Number(inputs.gasM3 ?? 0);
  return {
    carCo2: Math.round(carKm * electricityKwh),
    electricityCo2: Math.round(carKm),
    gasCo2: Math.round(carKm),
    totalCo2: Math.round(carKm),
    annualCo2: Math.round(carKm)
  };
}

export function carpetCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = Number(inputs.width ?? 0);
  const depth = Number(inputs.depth ?? 0);
  return {
    area: Math.round(width * depth),
    tatami: Math.round(width),
    cost: Math.round(width)
  };
}

export function certificationCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const cert = String(inputs.cert ?? '');
  const studyMethod = String(inputs.studyMethod ?? '');
  return {
    examFee: 0,
    studyCost: 0,
    totalCost: 0,
    studyHours: 0
  };
}

export function childCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const childAge = Number(inputs.childAge ?? 0);
  const schoolType = String(inputs.schoolType ?? '');
  const university = String(inputs.university ?? '');
  return {
    educationCost: childAge,
    livingCost: Math.round(childAge),
    totalCost: Math.round(childAge),
    monthlySaving: Math.round(childAge)
  };
}

export function childcareBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = Number(inputs.monthlySalary ?? 0);
  return {
    first6months: monthlySalary,
    after6months: Math.round(monthlySalary),
    totalYear: Math.round(monthlySalary)
  };
}

export function chineseZodiac(inputs: Record<string, number | string>): Record<string, number | string> {
  const year = Number(inputs.year ?? 0);
  return {
    zodiac: year,
    element: Math.round(year),
    compatibility: Math.round(year),
    nextYear: Math.round(year)
  };
}

export function churnRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const startCustomers = Number(inputs.startCustomers ?? 0);
  const churned = Number(inputs.churned ?? 0);
  const period = Number(inputs.period ?? 0);
  return {
    monthlyChurn: Math.round(startCustomers * churned),
    annualChurn: Math.round(startCustomers),
    avgLifespan: Math.round(startCustomers),
    retentionRate: Math.round(startCustomers)
  };
}

export function cityPlanningTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const landValue = Number(inputs.landValue ?? 0);
  const buildingValue = Number(inputs.buildingValue ?? 0);
  return {
    tax: Math.round(landValue * buildingValue),
    withFixedAsset: Math.round(landValue)
  };
}

export function clothingSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const jpSize = String(inputs.jpSize ?? '');
  const gender = String(inputs.gender ?? '');
  return {
    us: 0,
    uk: 0,
    eu: 0,
    chest: 0
  };
}

export function commuteCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const method = String(inputs.method ?? '');
  const monthlyCost = Number(inputs.monthlyCost ?? 0);
  const distance = Number(inputs.distance ?? 0);
  return {
    monthlyTotal: Math.round(monthlyCost * distance),
    annualTotal: Math.round(monthlyCost),
    taxFreeLimit: Math.round(monthlyCost),
    taxableAmount: Math.round(monthlyCost)
  };
}

export function compoundInterestDetail(inputs: Record<string, number | string>): Record<string, number | string> {
  const principal = Number(inputs.principal ?? 0);
  const rate = Number(inputs.rate ?? 0);
  const years = Number(inputs.years ?? 0);
  const monthly = Number(inputs.monthly ?? 0);
  return {
    futureValue: Math.round(principal * rate),
    totalDeposit: Math.round(principal),
    interest: Math.round(principal),
    returnRate: Math.round(principal)
  };
}

export function concreteCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = Number(inputs.width ?? 0);
  const depth = Number(inputs.depth ?? 0);
  const thickness = Number(inputs.thickness ?? 0);
  return {
    volume: Math.round(width * depth),
    weight: Math.round(width),
    bags: Math.round(width)
  };
}

export function consumptionTaxCalc(inputs: Record<string, number | string>): Record<string, number | string> {
  const price = Number(inputs.price ?? 0);
  const direction = String(inputs.direction ?? '');
  const rate = String(inputs.rate ?? '');
  return {
    result: price,
    taxAmount: Math.round(price)
  };
}

export function corporatePension(inputs: Record<string, number | string>): Record<string, number | string> {
  const years = Number(inputs.years ?? 0);
  const avgSalary = Number(inputs.avgSalary ?? 0);
  const type = String(inputs.type ?? '');
  const dcContribution = Number(inputs.dcContribution ?? 0);
  return {
    lumpSum: Math.round(years * avgSalary),
    annuity: Math.round(years),
    monthlyPension: Math.round(years)
  };
}

export function corporateTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const taxableIncome = Number(inputs.taxableIncome ?? 0);
  const isSmall = String(inputs.isSmall ?? '');
  return {
    corporateTax: taxableIncome,
    effectiveRate: Math.round(taxableIncome),
    localTax: Math.round(taxableIncome),
    totalTax: Math.round(taxableIncome)
  };
}

export function correlation(inputs: Record<string, number | string>): Record<string, number | string> {
  const dataX = Number(inputs.dataX ?? 0);
  const dataY = Number(inputs.dataY ?? 0);
  return {
    r: Math.round(dataX * dataY),
    r2: Math.round(dataX),
    interpretation: Math.round(dataX)
  };
}

export function cryptoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const profit = Number(inputs.profit ?? 0);
  const otherIncome = Number(inputs.otherIncome ?? 0);
  return {
    taxableIncome: Math.round(profit * otherIncome),
    incomeTax: Math.round(profit),
    residentTax: Math.round(profit),
    totalTax: Math.round(profit),
    effectiveRate: Math.round(profit)
  };
}

export function currencyConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = Number(inputs.amount ?? 0);
  const rate = Number(inputs.rate ?? 0);
  const direction = String(inputs.direction ?? '');
  return {
    converted: Math.round(amount * rate),
    inverse: Math.round(amount)
  };
}

export function cyclingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const minutes = Number(inputs.minutes ?? 0);
  const intensity = String(inputs.intensity ?? '');
  return {
    calories: Math.round(weight * minutes),
    distance: Math.round(weight),
    fatBurn: Math.round(weight)
  };
}

export function dataSizeConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  const fromUnit = String(inputs.fromUnit ?? '');
  return {
    B: value,
    KB: Math.round(value),
    MB: Math.round(value),
    GB: Math.round(value),
    TB: Math.round(value)
  };
}

export function debtRepayment(inputs: Record<string, number | string>): Record<string, number | string> {
  const balance = Number(inputs.balance ?? 0);
  const rate = Number(inputs.rate ?? 0);
  const monthlyPayment = Number(inputs.monthlyPayment ?? 0);
  return {
    months: Math.round(balance * rate),
    totalPayment: Math.round(balance),
    totalInterest: Math.round(balance),
    interestRatio: Math.round(balance)
  };
}

export function disabilityInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlyIncome = Number(inputs.monthlyIncome ?? 0);
  const monthlyExpense = Number(inputs.monthlyExpense ?? 0);
  const publicBenefit = Number(inputs.publicBenefit ?? 0);
  return {
    monthlyShortfall: Math.round(monthlyIncome * monthlyExpense),
    annualShortfall: Math.round(monthlyIncome),
    recommendedCoverage: Math.round(monthlyIncome)
  };
}

export function dollarCostAveraging(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlyAmount = Number(inputs.monthlyAmount ?? 0);
  const years = Number(inputs.years ?? 0);
  const expectedReturn = Number(inputs.expectedReturn ?? 0);
  return {
    totalInvested: Math.round(monthlyAmount * years),
    futureValue: Math.round(monthlyAmount),
    profit: Math.round(monthlyAmount),
    profitRate: Math.round(monthlyAmount)
  };
}

export function downloadTime(inputs: Record<string, number | string>): Record<string, number | string> {
  const fileSize = Number(inputs.fileSize ?? 0);
  const speed = Number(inputs.speed ?? 0);
  return {
    seconds: Math.round(fileSize * speed),
    minutes: Math.round(fileSize),
    hours: Math.round(fileSize)
  };
}

export function electricityBill(inputs: Record<string, number | string>): Record<string, number | string> {
  const watt = Number(inputs.watt ?? 0);
  const hoursPerDay = Number(inputs.hoursPerDay ?? 0);
  const days = Number(inputs.days ?? 0);
  const pricePerKwh = Number(inputs.pricePerKwh ?? 0);
  return {
    monthlyCost: Math.round(watt * hoursPerDay),
    kwhUsed: Math.round(watt),
    dailyCost: Math.round(watt)
  };
}

export function ellipse(inputs: Record<string, number | string>): Record<string, number | string> {
  const a = Number(inputs.a ?? 0);
  const b = Number(inputs.b ?? 0);
  return {
    area: Math.round(a * b),
    circumference: Math.round(a)
  };
}

export function emailMarketing(inputs: Record<string, number | string>): Record<string, number | string> {
  const subscribers = Number(inputs.subscribers ?? 0);
  const openRate = Number(inputs.openRate ?? 0);
  const clickRate = Number(inputs.clickRate ?? 0);
  const cvr = Number(inputs.cvr ?? 0);
  const avgOrderValue = Number(inputs.avgOrderValue ?? 0);
  return {
    opens: Math.round(subscribers * openRate),
    clicks: Math.round(subscribers),
    conversions: Math.round(subscribers),
    revenue: Math.round(subscribers)
  };
}

export function emergencyFund(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlyExpense = Number(inputs.monthlyExpense ?? 0);
  const employmentType = String(inputs.employmentType ?? '');
  return {
    minimumFund: monthlyExpense,
    recommendedFund: Math.round(monthlyExpense),
    idealFund: Math.round(monthlyExpense),
    months: Math.round(monthlyExpense)
  };
}

export function energyConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  const fromUnit = String(inputs.fromUnit ?? '');
  return {
    cal: value,
    kcal: Math.round(value),
    J: Math.round(value),
    kJ: Math.round(value),
    kWh: Math.round(value)
  };
}

export function englishScore(inputs: Record<string, number | string>): Record<string, number | string> {
  const toeicScore = Number(inputs.toeicScore ?? 0);
  return {
    toeflIbt: toeicScore,
    eiken: Math.round(toeicScore),
    ielts: Math.round(toeicScore),
    cefr: Math.round(toeicScore)
  };
}

export function etfCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const investAmount = Number(inputs.investAmount ?? 0);
  const expenseRatio = Number(inputs.expenseRatio ?? 0);
  const years = Number(inputs.years ?? 0);
  const annualReturn = Number(inputs.annualReturn ?? 0);
  return {
    totalCost: Math.round(investAmount * expenseRatio),
    costImpact: Math.round(investAmount),
    withoutCost: Math.round(investAmount),
    withCost: Math.round(investAmount)
  };
}

export function evCostComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const annualMileage = Number(inputs.annualMileage ?? 0);
  const evEfficiency = Number(inputs.evEfficiency ?? 0);
  const electricityPrice = Number(inputs.electricityPrice ?? 0);
  const gasEfficiency = Number(inputs.gasEfficiency ?? 0);
  const gasPrice = Number(inputs.gasPrice ?? 0);
  return {
    evFuelCost: Math.round(annualMileage * evEfficiency),
    gasFuelCost: Math.round(annualMileage),
    annualSavings: Math.round(annualMileage),
    tenYearSavings: Math.round(annualMileage)
  };
}

export function exerciseCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const minutes = Number(inputs.minutes ?? 0);
  const exercise = String(inputs.exercise ?? '');
  return {
    calories: Math.round(weight * minutes),
    fatBurn: Math.round(weight)
  };
}

export function fabricCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = Number(inputs.width ?? 0);
  const height = Number(inputs.height ?? 0);
  const fabricWidth = Number(inputs.fabricWidth ?? 0);
  const seam = Number(inputs.seam ?? 0);
  return {
    fabricLength: Math.round(width * height),
    totalArea: Math.round(width)
  };
}

export function fireInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const buildingType = String(inputs.buildingType ?? '');
  const area = Number(inputs.area ?? 0);
  const coverage = Number(inputs.coverage ?? 0);
  return {
    annualPremium: Math.round(area * coverage),
    fiveYearPremium: Math.round(area)
  };
}

export function fractionCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const num1 = Number(inputs.num1 ?? 0);
  const den1 = Number(inputs.den1 ?? 0);
  const operator = String(inputs.operator ?? '');
  const num2 = Number(inputs.num2 ?? 0);
  const den2 = Number(inputs.den2 ?? 0);
  return {
    resultNum: Math.round(num1 * den1),
    resultDen: Math.round(num1),
    decimal: Math.round(num1)
  };
}

export function freelanceRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const targetIncome = Number(inputs.targetIncome ?? 0);
  const workDays = Number(inputs.workDays ?? 0);
  const workHours = Number(inputs.workHours ?? 0);
  const expenseRate = Number(inputs.expenseRate ?? 0);
  return {
    requiredRevenue: Math.round(targetIncome * workDays),
    monthlyRate: Math.round(targetIncome),
    dailyRate: Math.round(targetIncome),
    hourlyRate: Math.round(targetIncome)
  };
}

export function gardenSoil(inputs: Record<string, number | string>): Record<string, number | string> {
  const area = Number(inputs.area ?? 0);
  const depth = Number(inputs.depth ?? 0);
  const pricePerBag = Number(inputs.pricePerBag ?? 0);
  const bagVolume = Number(inputs.bagVolume ?? 0);
  return {
    volumeL: Math.round(area * depth),
    bags: Math.round(area),
    totalCost: Math.round(area)
  };
}

export function goldInvestment(inputs: Record<string, number | string>): Record<string, number | string> {
  const purchasePrice = Number(inputs.purchasePrice ?? 0);
  const currentPrice = Number(inputs.currentPrice ?? 0);
  const grams = Number(inputs.grams ?? 0);
  return {
    investmentAmount: Math.round(purchasePrice * currentPrice),
    currentValue: Math.round(purchasePrice),
    profitLoss: Math.round(purchasePrice),
    returnRate: Math.round(purchasePrice)
  };
}

export function gpaCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const subjects = Number(inputs.subjects ?? 0);
  const s1 = Number(inputs.s1 ?? 0);
  const s2 = Number(inputs.s2 ?? 0);
  const s3 = Number(inputs.s3 ?? 0);
  const s4 = Number(inputs.s4 ?? 0);
  const s5 = Number(inputs.s5 ?? 0);
  const c1 = Number(inputs.c1 ?? 0);
  const c2 = Number(inputs.c2 ?? 0);
  const c3 = Number(inputs.c3 ?? 0);
  const c4 = Number(inputs.c4 ?? 0);
  const c5 = Number(inputs.c5 ?? 0);
  return {
    gpa: Math.round(subjects * s1),
    totalCredits: Math.round(subjects),
    totalPoints: Math.round(subjects)
  };
}

export function gradeCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const subject1 = Number(inputs.subject1 ?? 0);
  const subject2 = Number(inputs.subject2 ?? 0);
  const subject3 = Number(inputs.subject3 ?? 0);
  const subject4 = Number(inputs.subject4 ?? 0);
  const subject5 = Number(inputs.subject5 ?? 0);
  return {
    totalScore: Math.round(subject1 * subject2),
    averageScore: Math.round(subject1),
    highest: Math.round(subject1),
    lowest: Math.round(subject1)
  };
}

export function grossMargin(inputs: Record<string, number | string>): Record<string, number | string> {
  const revenue = Number(inputs.revenue ?? 0);
  const cogs = Number(inputs.cogs ?? 0);
  return {
    grossProfit: Math.round(revenue * cogs),
    grossMarginRate: Math.round(revenue),
    markupRate: Math.round(revenue)
  };
}

export function hearingLevel(inputs: Record<string, number | string>): Record<string, number | string> {
  const decibel = Number(inputs.decibel ?? 0);
  return {
    comparison: decibel,
    risk: Math.round(decibel),
    safeExposure: Math.round(decibel)
  };
}

export function hensachi(inputs: Record<string, number | string>): Record<string, number | string> {
  const score = Number(inputs.score ?? 0);
  const average = Number(inputs.average ?? 0);
  const sd = Number(inputs.sd ?? 0);
  return {
    hensachi: Math.round(score * average),
    percentile: Math.round(score),
    rank: Math.round(score)
  };
}

export function hexagon(inputs: Record<string, number | string>): Record<string, number | string> {
  const side = Number(inputs.side ?? 0);
  return {
    area: side,
    perimeter: Math.round(side),
    inradius: Math.round(side)
  };
}

export function housingDeduction(inputs: Record<string, number | string>): Record<string, number | string> {
  const loanBalance = Number(inputs.loanBalance ?? 0);
  const houseType = String(inputs.houseType ?? '');
  const moveInYear = Number(inputs.moveInYear ?? 0);
  return {
    annualDeduction: Math.round(loanBalance * moveInYear),
    controlLimit: Math.round(loanBalance),
    totalDeduction: Math.round(loanBalance)
  };
}

export function individualEnterpriseTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = Number(inputs.income ?? 0);
  const industry = String(inputs.industry ?? '');
  return {
    enterpriseTax: income,
    deduction: Math.round(income)
  };
}

export function inflationCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = Number(inputs.amount ?? 0);
  const inflationRate = Number(inputs.inflationRate ?? 0);
  const years = Number(inputs.years ?? 0);
  return {
    futureNominal: Math.round(amount * inflationRate),
    realValue: Math.round(amount),
    purchasingPowerLoss: Math.round(amount)
  };
}

export function inheritanceTaxSimulation(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalAssets = Number(inputs.totalAssets ?? 0);
  const heirs = Number(inputs.heirs ?? 0);
  const spouse = String(inputs.spouse ?? '');
  return {
    basicDeduction: Math.round(totalAssets * heirs),
    taxableAmount: Math.round(totalAssets),
    totalTax: Math.round(totalAssets),
    perPersonTax: Math.round(totalAssets)
  };
}

export function initialCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const rent = Number(inputs.rent ?? 0);
  const deposit = Number(inputs.deposit ?? 0);
  const keyMoney = Number(inputs.keyMoney ?? 0);
  const agentFee = Number(inputs.agentFee ?? 0);
  return {
    depositAmount: Math.round(rent * deposit),
    keyMoneyAmount: Math.round(rent),
    agentFeeAmount: Math.round(rent),
    firstMonth: Math.round(rent),
    totalInitial: Math.round(rent)
  };
}

export function investmentReturn(inputs: Record<string, number | string>): Record<string, number | string> {
  const initialAmount = Number(inputs.initialAmount ?? 0);
  const monthlyAmount = Number(inputs.monthlyAmount ?? 0);
  const annualReturn = Number(inputs.annualReturn ?? 0);
  const years = Number(inputs.years ?? 0);
  return {
    finalAmount: Math.round(initialAmount * monthlyAmount),
    totalInvested: Math.round(initialAmount),
    totalProfit: Math.round(initialAmount),
    profitRate: Math.round(initialAmount)
  };
}

export function japaneseEra(inputs: Record<string, number | string>): Record<string, number | string> {
  const year = Number(inputs.year ?? 0);
  return {
    era: year,
    eraYear: Math.round(year),
    eto: Math.round(year)
  };
}

export function joggingPace(inputs: Record<string, number | string>): Record<string, number | string> {
  const distance = Number(inputs.distance ?? 0);
  const minutes = Number(inputs.minutes ?? 0);
  return {
    pace: Math.round(distance * minutes),
    speed: Math.round(distance),
    calories: Math.round(distance)
  };
}

export function laborCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = Number(inputs.monthlySalary ?? 0);
  const bonusMonths = Number(inputs.bonusMonths ?? 0);
  return {
    annualSalary: Math.round(monthlySalary * bonusMonths),
    companyInsurance: Math.round(monthlySalary),
    totalCost: Math.round(monthlySalary),
    costRatio: Math.round(monthlySalary)
  };
}

export function landPrice(inputs: Record<string, number | string>): Record<string, number | string> {
  const pricePerTsubo = Number(inputs.pricePerTsubo ?? 0);
  const areaTsubo = Number(inputs.areaTsubo ?? 0);
  return {
    pricePerM2: Math.round(pricePerTsubo * areaTsubo),
    totalPrice: Math.round(pricePerTsubo),
    areaM2: Math.round(pricePerTsubo)
  };
}

export function logarithm(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  const base = Number(inputs.base ?? 0);
  return {
    log10: Math.round(value * base),
    ln: Math.round(value),
    logBase: Math.round(value)
  };
}

export function ltv(inputs: Record<string, number | string>): Record<string, number | string> {
  const avgOrderValue = Number(inputs.avgOrderValue ?? 0);
  const purchaseFrequency = Number(inputs.purchaseFrequency ?? 0);
  const customerLifespan = Number(inputs.customerLifespan ?? 0);
  const grossMarginRate = Number(inputs.grossMarginRate ?? 0);
  return {
    ltv: Math.round(avgOrderValue * purchaseFrequency),
    ltvProfit: Math.round(avgOrderValue),
    annualRevenue: Math.round(avgOrderValue),
    cac_limit: Math.round(avgOrderValue)
  };
}

export function mansionCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const managementFee = Number(inputs.managementFee ?? 0);
  const repairReserve = Number(inputs.repairReserve ?? 0);
  const parkingFee = Number(inputs.parkingFee ?? 0);
  const ownershipYears = Number(inputs.ownershipYears ?? 0);
  return {
    monthlyTotal: Math.round(managementFee * repairReserve),
    annualTotal: Math.round(managementFee),
    lifetimeTotal: Math.round(managementFee)
  };
}

export function marginTrading(inputs: Record<string, number | string>): Record<string, number | string> {
  const stockPrice = Number(inputs.stockPrice ?? 0);
  const shares = Number(inputs.shares ?? 0);
  const marginRate = Number(inputs.marginRate ?? 0);
  const priceChange = Number(inputs.priceChange ?? 0);
  return {
    tradeAmount: Math.round(stockPrice * shares),
    requiredMargin: Math.round(stockPrice),
    leverage: Math.round(stockPrice),
    profitLoss: Math.round(stockPrice),
    returnRate: Math.round(stockPrice)
  };
}

export function maternityBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = Number(inputs.monthlySalary ?? 0);
  return {
    dailyAmount: monthlySalary,
    totalAmount: Math.round(monthlySalary),
    preBirth: Math.round(monthlySalary),
    postBirth: Math.round(monthlySalary)
  };
}

export function matrix(inputs: Record<string, number | string>): Record<string, number | string> {
  const a11 = Number(inputs.a11 ?? 0);
  const a12 = Number(inputs.a12 ?? 0);
  const a21 = Number(inputs.a21 ?? 0);
  const a22 = Number(inputs.a22 ?? 0);
  return {
    determinant: Math.round(a11 * a12),
    inverse: Math.round(a11),
    trace: Math.round(a11)
  };
}

export function mealCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const rice = Number(inputs.rice ?? 0);
  const meat = Number(inputs.meat ?? 0);
  const fish = Number(inputs.fish ?? 0);
  const vegetables = Number(inputs.vegetables ?? 0);
  const oil = Number(inputs.oil ?? 0);
  return {
    totalCalorie: Math.round(rice * meat),
    protein: Math.round(rice),
    fat: Math.round(rice),
    carbs: Math.round(rice)
  };
}

export function medianMode(inputs: Record<string, number | string>): Record<string, number | string> {
  const data = Number(inputs.data ?? 0);
  return {
    median: data,
    mode: Math.round(data),
    q1: Math.round(data),
    q3: Math.round(data),
    range: Math.round(data)
  };
}

export function medicineDose(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const dosePerKg = Number(inputs.dosePerKg ?? 0);
  const timesPerDay = Number(inputs.timesPerDay ?? 0);
  return {
    singleDose: Math.round(weight * dosePerKg),
    dailyDose: Math.round(weight),
    weeklyDose: Math.round(weight)
  };
}

export function meetingCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const participants = Number(inputs.participants ?? 0);
  const avgHourlyRate = Number(inputs.avgHourlyRate ?? 0);
  const durationMinutes = Number(inputs.durationMinutes ?? 0);
  return {
    meetingCost: Math.round(participants * avgHourlyRate),
    perMinuteCost: Math.round(participants),
    annualCost: Math.round(participants)
  };
}

export function menstrualCycle(inputs: Record<string, number | string>): Record<string, number | string> {
  const lastPeriod = Number(inputs.lastPeriod ?? 0);
  const cycleLength = Number(inputs.cycleLength ?? 0);
  const periodLength = Number(inputs.periodLength ?? 0);
  return {
    nextPeriod: Math.round(lastPeriod * cycleLength),
    lutealPhase: Math.round(lastPeriod),
    pmsStart: Math.round(lastPeriod)
  };
}

export function minimumWage(inputs: Record<string, number | string>): Record<string, number | string> {
  const hourlyWage = Number(inputs.hourlyWage ?? 0);
  const region = String(inputs.region ?? '');
  return {
    minimumWage: hourlyWage,
    isAbove: Math.round(hourlyWage),
    difference: Math.round(hourlyWage)
  };
}

export function nationalHealthInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = Number(inputs.income ?? 0);
  const members = Number(inputs.members ?? 0);
  const age = Number(inputs.age ?? 0);
  return {
    medicalPart: Math.round(income * members),
    supportPart: Math.round(income),
    carePart: Math.round(income),
    totalPremium: Math.round(income),
    monthlyPremium: Math.round(income)
  };
}

export function normalDistribution(inputs: Record<string, number | string>): Record<string, number | string> {
  const mean = Number(inputs.mean ?? 0);
  const stddev = Number(inputs.stddev ?? 0);
  const x = Number(inputs.x ?? 0);
  return {
    zScore: Math.round(mean * stddev),
    probability: Math.round(mean),
    upperProbability: Math.round(mean)
  };
}

export function ovulationDay(inputs: Record<string, number | string>): Record<string, number | string> {
  const lastPeriod = Number(inputs.lastPeriod ?? 0);
  const cycleLength = Number(inputs.cycleLength ?? 0);
  return {
    ovulationDate: Math.round(lastPeriod * cycleLength),
    fertileStart: Math.round(lastPeriod),
    fertileEnd: Math.round(lastPeriod),
    nextPeriod: Math.round(lastPeriod)
  };
}

export function packingList(inputs: Record<string, number | string>): Record<string, number | string> {
  const days = Number(inputs.days ?? 0);
  const season = String(inputs.season ?? '');
  const laundry = String(inputs.laundry ?? '');
  return {
    tops: days,
    bottoms: Math.round(days),
    underwear: Math.round(days),
    socks: Math.round(days)
  };
}

export function paintArea(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = Number(inputs.width ?? 0);
  const depth = Number(inputs.depth ?? 0);
  const height = Number(inputs.height ?? 0);
  const windows = Number(inputs.windows ?? 0);
  const doors = Number(inputs.doors ?? 0);
  return {
    wallArea: Math.round(width * depth),
    ceilingArea: Math.round(width),
    totalArea: Math.round(width),
    paintLiters: Math.round(width)
  };
}

export function paintCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const wallArea = Number(inputs.wallArea ?? 0);
  const coats = Number(inputs.coats ?? 0);
  const coveragePerLiter = Number(inputs.coveragePerLiter ?? 0);
  const canSize = Number(inputs.canSize ?? 0);
  return {
    totalLiters: Math.round(wallArea * coats),
    cans: Math.round(wallArea),
    actualArea: Math.round(wallArea)
  };
}

export function paperSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const size = String(inputs.size ?? '');
  return {
    widthMm: 0,
    heightMm: 0,
    widthInch: 0,
    heightInch: 0,
    areaCm2: 0
  };
}

export function partyFood(inputs: Record<string, number | string>): Record<string, number | string> {
  const guests = Number(inputs.guests ?? 0);
  const duration = Number(inputs.duration ?? 0);
  const style = String(inputs.style ?? '');
  return {
    foodKg: Math.round(guests * duration),
    drinksL: Math.round(guests),
    alcoholL: Math.round(guests),
    budgetPerPerson: Math.round(guests)
  };
}

export function paybackPeriod(inputs: Record<string, number | string>): Record<string, number | string> {
  const investment = Number(inputs.investment ?? 0);
  const annualReturn = Number(inputs.annualReturn ?? 0);
  const annualCost = Number(inputs.annualCost ?? 0);
  return {
    paybackYears: Math.round(investment * annualReturn),
    annualNetReturn: Math.round(investment),
    roi5year: Math.round(investment)
  };
}

export function perPbr(inputs: Record<string, number | string>): Record<string, number | string> {
  const stockPrice = Number(inputs.stockPrice ?? 0);
  const eps = Number(inputs.eps ?? 0);
  const bps = Number(inputs.bps ?? 0);
  return {
    per: Math.round(stockPrice * eps),
    pbr: Math.round(stockPrice),
    earningsYield: Math.round(stockPrice),
    evaluation: Math.round(stockPrice)
  };
}

export function percentageCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const valueA = Number(inputs.valueA ?? 0);
  const valueB = Number(inputs.valueB ?? 0);
  const calcType = String(inputs.calcType ?? '');
  return {
    result: Math.round(valueA * valueB),
    explanation: Math.round(valueA)
  };
}

export function personalLoan(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = Number(inputs.amount ?? 0);
  const rate = Number(inputs.rate ?? 0);
  const years = Number(inputs.years ?? 0);
  return {
    monthlyPayment: Math.round(amount * rate),
    totalPayment: Math.round(amount),
    totalInterest: Math.round(amount)
  };
}

export function petAge(inputs: Record<string, number | string>): Record<string, number | string> {
  const petType = String(inputs.petType ?? '');
  const age = Number(inputs.age ?? 0);
  return {
    humanAge: age,
    lifeStage: Math.round(age),
    avgLifespan: Math.round(age)
  };
}

export function petInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const petType = String(inputs.petType ?? '');
  const age = Number(inputs.age ?? 0);
  const coverage = String(inputs.coverage ?? '');
  return {
    monthlyPremium: age,
    annualPremium: Math.round(age),
    lifetime: Math.round(age)
  };
}

export function photoPrint(inputs: Record<string, number | string>): Record<string, number | string> {
  const widthPx = Number(inputs.widthPx ?? 0);
  const heightPx = Number(inputs.heightPx ?? 0);
  const dpi = Number(inputs.dpi ?? 0);
  return {
    widthCm: Math.round(widthPx * heightPx),
    heightCm: Math.round(widthPx),
    megapixels: Math.round(widthPx),
    aspectRatio: Math.round(widthPx)
  };
}

export function pointValue(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = Number(inputs.amount ?? 0);
  const rate = Number(inputs.rate ?? 0);
  const monthlySpend = Number(inputs.monthlySpend ?? 0);
  return {
    pointsEarned: Math.round(amount * rate),
    discountEquivalent: Math.round(amount),
    annualSavings: Math.round(amount)
  };
}

export function polygonArea(inputs: Record<string, number | string>): Record<string, number | string> {
  const sides = Number(inputs.sides ?? 0);
  const sideLength = Number(inputs.sideLength ?? 0);
  return {
    area: Math.round(sides * sideLength),
    perimeter: Math.round(sides),
    inradius: Math.round(sides),
    circumradius: Math.round(sides)
  };
}

export function postalRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const type = String(inputs.type ?? '');
  const weight = Number(inputs.weight ?? 0);
  return {
    postage: weight
  };
}

export function powerConsumption(inputs: Record<string, number | string>): Record<string, number | string> {
  const watt1 = Number(inputs.watt1 ?? 0);
  const watt2 = Number(inputs.watt2 ?? 0);
  const hoursPerDay = Number(inputs.hoursPerDay ?? 0);
  const pricePerKwh = Number(inputs.pricePerKwh ?? 0);
  return {
    annualCost1: Math.round(watt1 * watt2),
    annualCost2: Math.round(watt1),
    annualSaving: Math.round(watt1),
    tenYearSaving: Math.round(watt1)
  };
}

export function pressureConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  const fromUnit = String(inputs.fromUnit ?? '');
  return {
    hPa: value,
    atm: Math.round(value),
    psi: Math.round(value),
    mmHg: Math.round(value)
  };
}

export function pricingMarkup(inputs: Record<string, number | string>): Record<string, number | string> {
  const cost = Number(inputs.cost ?? 0);
  const price = Number(inputs.price ?? 0);
  return {
    costRate: Math.round(cost * price),
    markupRate: Math.round(cost),
    profitPerUnit: Math.round(cost),
    grossMargin: Math.round(cost)
  };
}

export function primeFactorization(inputs: Record<string, number | string>): Record<string, number | string> {
  const number = Number(inputs.number ?? 0);
  return {
    factorization: number,
    divisorCount: Math.round(number),
    isPrime: Math.round(number)
  };
}

export function probability(inputs: Record<string, number | string>): Record<string, number | string> {
  const n = Number(inputs.n ?? 0);
  const r = Number(inputs.r ?? 0);
  return {
    permutation: Math.round(n * r),
    combination: Math.round(n),
    factorial: Math.round(n)
  };
}

export function proteinNeed(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const activity = String(inputs.activity ?? '');
  return {
    dailyProtein: weight,
    perMeal: Math.round(weight),
    chickenBreast: Math.round(weight),
    eggs: Math.round(weight)
  };
}

export function pythagorean(inputs: Record<string, number | string>): Record<string, number | string> {
  const sideA = Number(inputs.sideA ?? 0);
  const sideB = Number(inputs.sideB ?? 0);
  return {
    hypotenuse: Math.round(sideA * sideB),
    area: Math.round(sideA),
    perimeter: Math.round(sideA)
  };
}

export function quadratic(inputs: Record<string, number | string>): Record<string, number | string> {
  const a = Number(inputs.a ?? 0);
  const b = Number(inputs.b ?? 0);
  const c_val = Number(inputs.c_val ?? 0);
  return {
    x1: Math.round(a * b),
    x2: Math.round(a),
    discriminant: Math.round(a),
    solutionType: Math.round(a)
  };
}

export function randomNumber(inputs: Record<string, number | string>): Record<string, number | string> {
  const min = Number(inputs.min ?? 0);
  const max = Number(inputs.max ?? 0);
  const count = Number(inputs.count ?? 0);
  return {
    result: Math.round(min * max),
    sum: Math.round(min),
    avg: Math.round(min)
  };
}

export function realEstateAcquisitionTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const landValue = Number(inputs.landValue ?? 0);
  const buildingValue = Number(inputs.buildingValue ?? 0);
  const isResidential = String(inputs.isResidential ?? '');
  return {
    landTax: Math.round(landValue * buildingValue),
    buildingTax: Math.round(landValue),
    totalTax: Math.round(landValue)
  };
}

export function rebalance(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalAsset = Number(inputs.totalAsset ?? 0);
  const currentStock = Number(inputs.currentStock ?? 0);
  const currentBond = Number(inputs.currentBond ?? 0);
  const targetStock = Number(inputs.targetStock ?? 0);
  const targetBond = Number(inputs.targetBond ?? 0);
  return {
    stockAdjust: Math.round(totalAsset * currentStock),
    bondAdjust: Math.round(totalAsset),
    cashAdjust: Math.round(totalAsset)
  };
}

export function recipeScale(inputs: Record<string, number | string>): Record<string, number | string> {
  const originalServings = Number(inputs.originalServings ?? 0);
  const newServings = Number(inputs.newServings ?? 0);
  const ingredientAmount = Number(inputs.ingredientAmount ?? 0);
  return {
    scaledAmount: Math.round(originalServings * newServings),
    ratio: Math.round(originalServings)
  };
}

export function refinance(inputs: Record<string, number | string>): Record<string, number | string> {
  const remainingBalance = Number(inputs.remainingBalance ?? 0);
  const currentRate = Number(inputs.currentRate ?? 0);
  const newRate = Number(inputs.newRate ?? 0);
  const remainingYears = Number(inputs.remainingYears ?? 0);
  const refinanceCost = Number(inputs.refinanceCost ?? 0);
  return {
    currentTotal: Math.round(remainingBalance * currentRate),
    newTotal: Math.round(remainingBalance),
    savings: Math.round(remainingBalance),
    monthlyDiff: Math.round(remainingBalance)
  };
}

export function registrationTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const propertyValue = Number(inputs.propertyValue ?? 0);
  const regType = String(inputs.regType ?? '');
  const loanAmount = Number(inputs.loanAmount ?? 0);
  return {
    registrationTax: Math.round(propertyValue * loanAmount)
  };
}

export function reitYield(inputs: Record<string, number | string>): Record<string, number | string> {
  const price = Number(inputs.price ?? 0);
  const annualDistribution = Number(inputs.annualDistribution ?? 0);
  const units = Number(inputs.units ?? 0);
  return {
    yield: Math.round(price * annualDistribution),
    monthlyIncome: Math.round(price),
    annualIncome: Math.round(price)
  };
}

export function rentCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = Number(inputs.income ?? 0);
  const familySize = Number(inputs.familySize ?? 0);
  return {
    conservative: Math.round(income * familySize),
    standard: Math.round(income),
    max: Math.round(income),
    estimatedTakeHome: Math.round(income)
  };
}

export function roomBrightness(inputs: Record<string, number | string>): Record<string, number | string> {
  const area = Number(inputs.area ?? 0);
  const roomType = String(inputs.roomType ?? '');
  return {
    lumens: area,
    ledWatt: Math.round(area),
    fixtures: Math.round(area)
  };
}

export function rule72(inputs: Record<string, number | string>): Record<string, number | string> {
  const rate = Number(inputs.rate ?? 0);
  return {
    yearsToDouble: rate,
    yearsToTriple: Math.round(rate),
    actual: Math.round(rate)
  };
}

export function runningPace(inputs: Record<string, number | string>): Record<string, number | string> {
  const distance = Number(inputs.distance ?? 0);
  const hours = Number(inputs.hours ?? 0);
  const minutes = Number(inputs.minutes ?? 0);
  return {
    pace: Math.round(distance * hours),
    speed: Math.round(distance),
    marathon: Math.round(distance),
    half: Math.round(distance)
  };
}

export function salaryAfterTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = Number(inputs.income ?? 0);
  const dependents = Number(inputs.dependents ?? 0);
  return {
    takeHome: Math.round(income * dependents),
    monthlyTakeHome: Math.round(income),
    totalTax: Math.round(income),
    socialInsurance: Math.round(income),
    ratio: Math.round(income)
  };
}

export function salaryComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = Number(inputs.monthlySalary ?? 0);
  const bonusMonths = Number(inputs.bonusMonths ?? 0);
  return {
    annualSalary: Math.round(monthlySalary * bonusMonths),
    bonusTotal: Math.round(monthlySalary),
    dailyWage: Math.round(monthlySalary)
  };
}

export function scholarship(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalBorrowed = Number(inputs.totalBorrowed ?? 0);
  const rate = Number(inputs.rate ?? 0);
  const years = Number(inputs.years ?? 0);
  return {
    monthlyPayment: Math.round(totalBorrowed * rate),
    totalPayment: Math.round(totalBorrowed),
    totalInterest: Math.round(totalBorrowed)
  };
}

export function schoolCommute(inputs: Record<string, number | string>): Record<string, number | string> {
  const distance = Number(inputs.distance ?? 0);
  const method = String(inputs.method ?? '');
  const monthlyCost = Number(inputs.monthlyCost ?? 0);
  return {
    commuteTime: Math.round(distance * monthlyCost),
    dailyTime: Math.round(distance),
    annualTime: Math.round(distance),
    annualCost: Math.round(distance)
  };
}

export function schoolSupplies(inputs: Record<string, number | string>): Record<string, number | string> {
  const schoolType = String(inputs.schoolType ?? '');
  return {
    uniformCost: 0,
    suppliesCost: 0,
    otherCost: 0,
    totalCost: 0
  };
}

export function screenSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const inches = Number(inputs.inches ?? 0);
  const ratio = String(inputs.ratio ?? '');
  return {
    widthCm: inches,
    heightCm: Math.round(inches),
    areaCm2: Math.round(inches),
    diagonalCm: Math.round(inches)
  };
}

export function severanceTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const severance = Number(inputs.severance ?? 0);
  const years = Number(inputs.years ?? 0);
  return {
    deduction: Math.round(severance * years),
    taxableRetirement: Math.round(severance),
    incomeTax: Math.round(severance),
    residentTax: Math.round(severance),
    netSeverance: Math.round(severance)
  };
}

export function shoeSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const jpSize = Number(inputs.jpSize ?? 0);
  const gender = String(inputs.gender ?? '');
  return {
    us: jpSize,
    uk: Math.round(jpSize),
    eu: Math.round(jpSize)
  };
}

export function sleepCycle(inputs: Record<string, number | string>): Record<string, number | string> {
  const wakeUpHour = Number(inputs.wakeUpHour ?? 0);
  const wakeUpMinute = Number(inputs.wakeUpMinute ?? 0);
  return {
    bedtime6: Math.round(wakeUpHour * wakeUpMinute),
    bedtime5: Math.round(wakeUpHour),
    bedtime4: Math.round(wakeUpHour),
    bedtime3: Math.round(wakeUpHour)
  };
}

export function squareRoot(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  return {
    squareRoot: value,
    cubeRoot: Math.round(value),
    square: Math.round(value),
    cube: Math.round(value)
  };
}

export function stampDuty(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = Number(inputs.amount ?? 0);
  const docType = String(inputs.docType ?? '');
  return {
    stampTax: amount
  };
}

export function stretchTimer(inputs: Record<string, number | string>): Record<string, number | string> {
  const deskHours = Number(inputs.deskHours ?? 0);
  return {
    stretchMinutes: deskHours,
    exercises: Math.round(deskHours),
    breakInterval: Math.round(deskHours)
  };
}

export function studyPlan(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalHours = Number(inputs.totalHours ?? 0);
  const daysUntilExam = Number(inputs.daysUntilExam ?? 0);
  const availableDays = Number(inputs.availableDays ?? 0);
  return {
    dailyHours: Math.round(totalHours * daysUntilExam),
    weeklyHours: Math.round(totalHours),
    totalStudyDays: Math.round(totalHours)
  };
}

export function subscriptionCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const sub1 = Number(inputs.sub1 ?? 0);
  const sub2 = Number(inputs.sub2 ?? 0);
  const sub3 = Number(inputs.sub3 ?? 0);
  const sub4 = Number(inputs.sub4 ?? 0);
  const sub5 = Number(inputs.sub5 ?? 0);
  return {
    monthlyTotal: Math.round(sub1 * sub2),
    annualTotal: Math.round(sub1),
    dailyCost: Math.round(sub1)
  };
}

export function swimmingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const minutes = Number(inputs.minutes ?? 0);
  const stroke = String(inputs.stroke ?? '');
  return {
    calories: Math.round(weight * minutes),
    fatBurn: Math.round(weight)
  };
}

export function targetHeartRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = Number(inputs.age ?? 0);
  const restingHR = Number(inputs.restingHR ?? 60);
  // Karvonen method: Target HR = ((MaxHR - RestingHR) × intensity%) + RestingHR
  const maxHR = 220 - age;
  const hrReserve = maxHR - restingHR;
  // Fat burn zone: 50-70%, Cardio zone: 70-80%, High intensity: 80-90%
  const fatBurnLow = Math.round(hrReserve * 0.50 + restingHR);
  const fatBurnHigh = Math.round(hrReserve * 0.70 + restingHR);
  const cardioLow = Math.round(hrReserve * 0.70 + restingHR);
  const cardioHigh = Math.round(hrReserve * 0.80 + restingHR);
  const highIntensityLow = Math.round(hrReserve * 0.80 + restingHR);
  const highIntensityHigh = Math.round(hrReserve * 0.90 + restingHR);
  return {
    maxHR,
    fatBurnZone: `${fatBurnLow}〜${fatBurnHigh}`,
    cardioZone: `${cardioLow}〜${cardioHigh}`,
    highIntensity: `${highIntensityLow}〜${highIntensityHigh}`
  };
}

export function tileCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const areaWidth = Number(inputs.areaWidth ?? 0);
  const areaDepth = Number(inputs.areaDepth ?? 0);
  const tileSize = Number(inputs.tileSize ?? 0);
  const lossRate = Number(inputs.lossRate ?? 0);
  return {
    tilesNeeded: Math.round(areaWidth * areaDepth),
    area: Math.round(areaWidth),
    boxes: Math.round(areaWidth)
  };
}

export function timeConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  const fromUnit = String(inputs.fromUnit ?? '');
  return {
    seconds: value,
    minutes: Math.round(value),
    hours: Math.round(value),
    days: Math.round(value)
  };
}

export function timeZone(inputs: Record<string, number | string>): Record<string, number | string> {
  const fromOffset = Number(inputs.fromOffset ?? 0);
  const toOffset = Number(inputs.toOffset ?? 0);
  const hour = Number(inputs.hour ?? 0);
  return {
    timeDiff: Math.round(fromOffset * toOffset),
    destinationTime: Math.round(fromOffset),
    dayChange: Math.round(fromOffset)
  };
}

export function tipCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const billAmount = Number(inputs.billAmount ?? 0);
  const tipRate = Number(inputs.tipRate ?? 0);
  const people = Number(inputs.people ?? 0);
  return {
    tipAmount: Math.round(billAmount * tipRate),
    totalBill: Math.round(billAmount),
    perPerson: Math.round(billAmount)
  };
}

export function trapezoid(inputs: Record<string, number | string>): Record<string, number | string> {
  const topBase = Number(inputs.topBase ?? 0);
  const bottomBase = Number(inputs.bottomBase ?? 0);
  const height = Number(inputs.height ?? 0);
  return {
    area: Math.round(topBase * bottomBase)
  };
}

export function travelInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const destination = String(inputs.destination ?? '');
  const days = Number(inputs.days ?? 0);
  const plan = String(inputs.plan ?? '');
  return {
    premium: days,
    medicalCoverage: Math.round(days),
    liabilityCoverage: Math.round(days)
  };
}

export function trigonometry(inputs: Record<string, number | string>): Record<string, number | string> {
  const angle = Number(inputs.angle ?? 0);
  return {
    sin: angle,
    cos: Math.round(angle),
    tan: Math.round(angle),
    radian: Math.round(angle)
  };
}

export function tsuboM2(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = Number(inputs.value ?? 0);
  const fromUnit = String(inputs.fromUnit ?? '');
  return {
    tsubo: value,
    jo: Math.round(value),
    m2: Math.round(value),
    sqft: Math.round(value)
  };
}

export function typingSpeed(inputs: Record<string, number | string>): Record<string, number | string> {
  const characters = Number(inputs.characters ?? 0);
  const minutes = Number(inputs.minutes ?? 0);
  return {
    cpm: Math.round(characters * minutes),
    wpm: Math.round(characters),
    level: Math.round(characters)
  };
}

export function unemploymentBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = Number(inputs.age ?? 0);
  const monthlySalary = Number(inputs.monthlySalary ?? 0);
  const yearsWorked = Number(inputs.yearsWorked ?? 0);
  const reason = String(inputs.reason ?? '');
  return {
    dailyAmount: Math.round(age * monthlySalary),
    totalDays: Math.round(age),
    totalAmount: Math.round(age),
    waitingPeriod: Math.round(age)
  };
}

export function unitPrice(inputs: Record<string, number | string>): Record<string, number | string> {
  const price1 = Number(inputs.price1 ?? 0);
  const amount1 = Number(inputs.amount1 ?? 0);
  const price2 = Number(inputs.price2 ?? 0);
  const amount2 = Number(inputs.amount2 ?? 0);
  return {
    unitPriceA: Math.round(price1 * amount1),
    unitPriceB: Math.round(price1),
    savings: Math.round(price1),
    verdict: Math.round(price1)
  };
}

export function visionTest(inputs: Record<string, number | string>): Record<string, number | string> {
  const decimalVision = Number(inputs.decimalVision ?? 0);
  return {
    fraction: decimalVision,
    logmar: Math.round(decimalVision),
    status: Math.round(decimalVision)
  };
}

export function vocabSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const words = Number(inputs.words ?? 0);
  return {
    level: words,
    cefrLevel: Math.round(words),
    toeicEstimate: Math.round(words),
    equivalent: Math.round(words)
  };
}

export function waistHipRatio(inputs: Record<string, number | string>): Record<string, number | string> {
  const waist = Number(inputs.waist ?? 0);
  const hip = Number(inputs.hip ?? 0);
  const gender = String(inputs.gender ?? '');
  return {
    whr: Math.round(waist * hip),
    risk: Math.round(waist),
    bodyType: Math.round(waist)
  };
}

export function walkingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = Number(inputs.weight ?? 0);
  const minutes = Number(inputs.minutes ?? 0);
  const speed = String(inputs.speed ?? '');
  return {
    calories: Math.round(weight * minutes),
    distance: Math.round(weight),
    steps: Math.round(weight)
  };
}

export function wallpaperCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = Number(inputs.width ?? 0);
  const depth = Number(inputs.depth ?? 0);
  const height = Number(inputs.height ?? 0);
  const rollWidth = Number(inputs.rollWidth ?? 0);
  return {
    totalLength: Math.round(width * depth),
    rolls: Math.round(width),
    wallArea: Math.round(width)
  };
}

export function weddingCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const guests = Number(inputs.guests ?? 0);
  const style = String(inputs.style ?? '');
  const giftPerPerson = Number(inputs.giftPerPerson ?? 0);
  return {
    totalCost: Math.round(guests * giftPerPerson),
    giftTotal: Math.round(guests),
    selfPayment: Math.round(guests),
    perGuest: Math.round(guests)
  };
}

export function workersComp(inputs: Record<string, number | string>): Record<string, number | string> {
  const avgDailyWage = Number(inputs.avgDailyWage ?? 0);
  return {
    compensationDaily: avgDailyWage,
    specialDaily: Math.round(avgDailyWage),
    totalDaily: Math.round(avgDailyWage),
    monthly30: Math.round(avgDailyWage)
  };
}

export function workingCapital(inputs: Record<string, number | string>): Record<string, number | string> {
  const receivables = Number(inputs.receivables ?? 0);
  const inventory = Number(inputs.inventory ?? 0);
  const payables = Number(inputs.payables ?? 0);
  return {
    workingCapital: Math.round(receivables * inventory),
    turnoverDays: Math.round(receivables)
  };
}

export function yieldComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const propertyPrice = Number(inputs.propertyPrice ?? 0);
  const monthlyRent = Number(inputs.monthlyRent ?? 0);
  const annualExpense = Number(inputs.annualExpense ?? 0);
  const vacancy = Number(inputs.vacancy ?? 0);
  return {
    grossYield: Math.round(propertyPrice * monthlyRent),
    netYield: Math.round(propertyPrice),
    annualIncome: Math.round(propertyPrice),
    annualNetIncome: Math.round(propertyPrice)
  };
}

// === UNIT CONVERSION CATEGORY ===

function unitConvert(value: number, direction: string, factor: number, precision: number = 6): { result: number; formula: number } {
  const result = direction === 'a_to_b' ? value / factor : value * factor;
  const rounded = Math.round(result * Math.pow(10, precision)) / Math.pow(10, precision);
  return { result: rounded, formula: rounded };
}

// Length
export function cmToInch(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 2.54, 6);
}
export function mToFeet(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 0.3048, 6);
}
export function kmToMile(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 1.60934, 6);
}
export function mmToInch(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 25.4, 6);
}
export function mToYard(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 0.9144, 6);
}
export function cmToFeet(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 30.48, 6);
}
export function mToKm(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 1000, 6);
}
export function inchToFeet(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 12, 6);
}
export function shakuToCm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 30.303 : v / 30.303;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function sunToMm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 30.303 : v / 30.303;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function riToKm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 3.92727 : v / 3.92727;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function nauticalMileToKm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 1.852 : v / 1.852;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function micronToMm(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 1000, 6);
}
export function nmToMm(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 1000000, 10);
}
export function kenToM(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 1.81818 : v / 1.81818;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}

// Weight
export function kgToLb(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 0.453592 : v * 0.453592;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function gToOz(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 28.3495 : v * 28.3495;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function kgToStone(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 6.35029 : v * 6.35029;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function tonToKg(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 1000 : v / 1000;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function mgToG(inputs: Record<string, number | string>): Record<string, number> {
  return unitConvert(inputs.value as number, inputs.direction as string, 1000, 6);
}
export function kanToKg(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 3.75 : v / 3.75;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function monmeToG(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 3.75 : v / 3.75;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function caratToG(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 0.2 : v / 0.2;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function lbToOz(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 16 : v / 16;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function grainToMg(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 64.79891 : v / 64.79891;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}

// Temperature
export function celsiusToFahrenheit(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 9 / 5 + 32 : (v - 32) * 5 / 9;
  const rounded = Math.round(result * 100) / 100;
  return { result: rounded, formula: rounded };
}
export function celsiusToKelvin(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v + 273.15 : v - 273.15;
  const rounded = Math.round(result * 100) / 100;
  return { result: rounded, formula: rounded };
}
export function fahrenheitToKelvin(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? (v - 32) * 5 / 9 + 273.15 : (v - 273.15) * 9 / 5 + 32;
  const rounded = Math.round(result * 100) / 100;
  return { result: rounded, formula: rounded };
}
export function celsiusToRankine(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? (v + 273.15) * 9 / 5 : v * 5 / 9 - 273.15;
  const rounded = Math.round(result * 100) / 100;
  return { result: rounded, formula: rounded };
}
export function fahrenheitToCelsius(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? (v - 32) * 5 / 9 : v * 9 / 5 + 32;
  const rounded = Math.round(result * 100) / 100;
  return { result: rounded, formula: rounded };
}
export function reaumurToCelsius(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 5 / 4 : v * 4 / 5;
  const rounded = Math.round(result * 100) / 100;
  return { result: rounded, formula: rounded };
}

// Area
export function sqmToSqft(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 10.7639 : v / 10.7639;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function hectareToAcre(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 2.47105 : v / 2.47105;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function tsuboToSqm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 3.30579 : v / 3.30579;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function joToSqm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 1.62 : v / 1.62;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function tsuboToJo(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 2.04 : v / 2.04;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function sqmToAcre(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 4046.86 : v * 4046.86;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function sqkmToSqmi(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 2.58999 : v * 2.58999;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function aarToSqm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 100 : v / 100;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function seToSqm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 99.1736 : v / 99.1736;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function tanToSqm(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 991.736 : v / 991.736;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}

// Volume
export function literToGallon(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 3.78541 : v * 3.78541;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function mlToFloz(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 29.5735 : v * 29.5735;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function literToCup(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 0.2 : v * 0.2;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function ccToMl(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  return { result: v, formula: v };
}
export function literToM3(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 1000 : v * 1000;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function tbspToMl(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 15 : v / 15;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function tspToMl(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 5 : v / 5;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function goToMl(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 180.39 : v / 180.39;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function pintToMl(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 473.176 : v / 473.176;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}
export function shoToLiter(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 1.80391 : v / 1.80391;
  const rounded = Math.round(result * 1000000) / 1000000;
  return { result: rounded, formula: rounded };
}

// Speed
export function kmhToMph(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v / 1.60934 : v * 1.60934;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function msToKmh(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 3.6 : v / 3.6;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function knotToKmh(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 1.852 : v / 1.852;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function machToKmh(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 1225.044 : v / 1225.044;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function fpsToMs(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 0.3048 : v / 0.3048;
  const rounded = Math.round(result * 10000) / 10000;
  return { result: rounded, formula: rounded };
}
export function lightSpeedToMs(inputs: Record<string, number | string>): Record<string, number> {
  const v = inputs.value as number;
  const d = inputs.direction as string;
  const result = d === 'a_to_b' ? v * 299792458 : v / 299792458;
  return { result: result, formula: result };
}

// Calculator function registry
const calculatorFunctions: Record<string, (inputs: Record<string, number | string>) => Record<string, number | string>> = {
  adRoas,
  advancePayment,
  ageCalculator,
  airConditionerCost,
  alcoholBreakdown,
  alcoholCalorie,
  alcoholTobaccoTax,
  anniversary,
  annualIncome,
  annualLeave,
  areaConvert,
  assetAllocation,
  autoTax,
  average,
  babyGrowth,
  basalMetabolism,
  baseConvert,
  birthdayCountdown,
  bloodAlcohol,
  blueReturn,
  bmi,
  bmiChild,
  bmiDetailed,
  bmiPet,
  bodyFat,
  bodyFatPercentage,
  bondYield,
  bonusTax,
  breakEven,
  businessDays,
  caffeine,
  calculateCryptoProfit,
  calculateForexProfit,
  calculateFurusatoNozei,
  calculateIdecoSimulation,
  calculateNisaSimulation,
  calorieBurn,
  caloriesBmr,
  capitalGainsTax,
  carCostTotal,
  carInsurance,
  carLease,
  carLoan,
  carTax,
  carbonFootprint,
  carpetCalculator,
  cashFlow,
  catAge,
  certificationCost,
  childCost,
  childcareBenefit,
  chineseZodiac,
  churnRate,
  circle,
  cityPlanningTax,
  clothingSize,
  commuteCost,
  compoundInterestDetail,
  concreteCalculator,
  condoMonthly,
  cone,
  consumptionTax,
  consumptionTaxCalc,
  corporatePension,
  corporateTax,
  correlation,
  countdown,
  creditCardInterest,
  cryptoTax,
  currencyConvert,
  cyclingCalorie,
  cylinder,
  dailyCalorie,
  dataSize,
  dataSizeConvert,
  daysBetween,
  debtRepayment,
  dependentDeduction,
  depreciation,
  disabilityInsurance,
  disabilityPension,
  discount,
  dividendYield,
  dogAge,
  dollarCostAveraging,
  dollarCostAvg,
  downloadTime,
  dueDate,
  earthquakeInsurance,
  educationCostSim,
  educationLoan,
  elapsedDays,
  electricityBill,
  electricityCost,
  ellipse,
  emailMarketing,
  emergencyFund,
  energyConvert,
  englishScore,
  etfCost,
  evCostComparison,
  examScore,
  exerciseCalorie,
  fabricCalculator,
  fireCalculation,
  fireInsurance,
  fixedAssetTax,
  fraction,
  fractionCalculator,
  freelanceRate,
  freelanceTax,
  fuelCost,
  furusatoDetail,
  gardenSoil,
  gasCost,
  gcdLcm,
  giftTax,
  goldInvestment,
  gpa,
  gpaCalculator,
  gradeCalculator,
  grossMargin,
  hearingLevel,
  hensachi,
  hexagon,
  highCostMedical,
  hourlyWage,
  housingDeduction,
  idealWeight,
  incomeTax,
  individualEnterpriseTax,
  inflationCalculator,
  inheritanceTax,
  inheritanceTaxSimulation,
  initialCost,
  internetCost,
  inventoryTurnover,
  investmentReturn,
  invoiceTax,
  japaneseEra,
  joggingPace,
  laborCost,
  landPrice,
  lengthConvert,
  lifeInsurance,
  loanRepayment,
  logarithm,
  ltv,
  mansionCost,
  marginTrading,
  maternityBenefit,
  maternityLeave,
  matrix,
  mealCalorie,
  medianMode,
  medicalDeduction,
  medicalExpense,
  medicineDose,
  meetingCost,
  menstrualCycle,
  mileage,
  minimumWage,
  mortgageComparison,
  movingCost,
  movingEstimate,
  nationalHealthInsurance,
  normalDistribution,
  overtimeIncome,
  overtimePay,
  ovulationCalc,
  ovulationDay,
  packingList,
  paintArea,
  paintCalculator,
  paperSize,
  partTimeIncome,
  partyFood,
  paybackPeriod,
  pensionContribution,
  pensionEstimate,
  perPbr,
  perUnitPrice,
  percentage,
  percentageCalculator,
  personalLoan,
  petAge,
  petInsurance,
  photoPrint,
  pointValue,
  polygonArea,
  postalRate,
  power,
  powerConsumption,
  pregnancyWeek,
  pressureConvert,
  pricingMarkup,
  primeFactorization,
  probability,
  profitMargin,
  propertyYield,
  proteinNeed,
  pythagorean,
  quadratic,
  raiseImpact,
  randomNumber,
  ratio,
  readingSpeed,
  realEstateAcquisitionTax,
  rebalance,
  recipeScale,
  rectangle,
  refinance,
  registrationTax,
  reitYield,
  renovationCost,
  rentBudget,
  rentCalculator,
  rentVsBuy,
  repaymentPlan,
  residentTax,
  retirementPay,
  roi,
  roiCalculator,
  roomBrightness,
  rule72,
  runningPace,
  salaryAfterTax,
  salaryComparison,
  savingsGoal,
  savingsSimulation,
  scholarship,
  scholarshipRepayment,
  schoolCommute,
  schoolSupplies,
  screenSize,
  severanceTax,
  shoeSize,
  sideJobTax,
  sleepCalculator,
  sleepCycle,
  socialInsuranceCalc,
  speedConvert,
  sphere,
  splitBill,
  spouseDeduction,
  squareRoot,
  stampDuty,
  standardDeviation,
  stepsToDistance,
  stockProfit,
  stretchTimer,
  studyPlan,
  studyTime,
  subscriptionCost,
  survivorPension,
  swimmingCalorie,
  takeHomePay,
  targetHeartRate,
  taxIncluded,
  temperatureConvert,
  tileCalculator,
  timeConvert,
  timeZone,
  timezoneCalc,
  tipCalculator,
  trapezoid,
  travelInsurance,
  triangle,
  trigonometry,
  tsuboM2,
  tsuboSqm,
  tuitionCost,
  typingSpeed,
  unemploymentBenefit,
  unemploymentInsurance,
  unitPrice,
  visionTest,
  vocabSize,
  volumeConvert,
  waistHipRatio,
  walkingCalorie,
  wallpaperCalculator,
  waterCost,
  waterIntake,
  weddingCost,
  weekday,
  weightConvert,
  wifiSpeed,
  workDays,
  workersComp,
  workingCapital,
  yearEndAdjustment,
  yieldComparison,
  zodiac,
  calcCompoundInterest: compoundInterest,
  // Unit conversion category - Length
  cmToInch,
  mToFeet,
  kmToMile,
  mmToInch,
  mToYard,
  cmToFeet,
  mToKm,
  inchToFeet,
  shakuToCm,
  sunToMm,
  riToKm,
  nauticalMileToKm,
  micronToMm,
  nmToMm,
  kenToM,
  // Unit conversion category - Weight
  kgToLb,
  gToOz,
  kgToStone,
  tonToKg,
  mgToG,
  kanToKg,
  monmeToG,
  caratToG,
  lbToOz,
  grainToMg,
  // Unit conversion category - Temperature
  celsiusToFahrenheit,
  celsiusToKelvin,
  fahrenheitToKelvin,
  celsiusToRankine,
  fahrenheitToCelsius,
  reaumurToCelsius,
  // Unit conversion category - Area
  sqmToSqft,
  hectareToAcre,
  tsuboToSqm,
  joToSqm,
  tsuboToJo,
  sqmToAcre,
  sqkmToSqmi,
  aarToSqm,
  seToSqm,
  tanToSqm,
  // Unit conversion category - Volume
  literToGallon,
  mlToFloz,
  literToCup,
  ccToMl,
  literToM3,
  tbspToMl,
  tspToMl,
  goToMl,
  pintToMl,
  shoToLiter,
  // Unit conversion category - Speed
  kmhToMph,
  msToKmh,
  knotToKmh,
  machToKmh,
  fpsToMs,
  lightSpeedToMs,
};

export function getCalculatorFunction(
  name: string
): ((inputs: Record<string, number | string>) => Record<string, number | string>) | undefined {
  return calculatorFunctions[name];
}
