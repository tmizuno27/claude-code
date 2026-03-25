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
export function giftTax(inputs: Record<string, number | string>): Record<string, number> {
  const amount = (inputs.amount as number) * 10000;
  const taxable = Math.max(0, amount - 1_100_000);
  let tax: number;
  if (taxable <= 2_000_000) tax = taxable * 0.10;
  else if (taxable <= 3_000_000) tax = taxable * 0.15 - 100_000;
  else if (taxable <= 4_000_000) tax = taxable * 0.20 - 250_000;
  else if (taxable <= 6_000_000) tax = taxable * 0.30 - 650_000;
  else if (taxable <= 10_000_000) tax = taxable * 0.40 - 1_250_000;
  else if (taxable <= 15_000_000) tax = taxable * 0.45 - 1_750_000;
  else if (taxable <= 30_000_000) tax = taxable * 0.50 - 2_500_000;
  else tax = taxable * 0.55 - 4_000_000;
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
  const basicPensionFull = 816_000; // 2026 base
  const basicPension = Math.round(basicPensionFull * Math.min(years, 40) / 40);
  const welfareMultiplier = 0.005481;
  const welfarePension = Math.round(avgSalary * welfareMultiplier * years);
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
  // Tax on retirement pay
  const deduction = years <= 20 ? 400000 * years : 8000000 + 700000 * (years - 20);
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
  const si = income * 0.15;
  const basicDeduction = 430000;
  const dependents = (inputs.dependents as number || 0) * 330000;
  const taxableIncome = Math.max(0, empIncome - si - basicDeduction - dependents);
  const prefectureTax = Math.round(taxableIncome * 0.04);
  const cityTax = Math.round(taxableIncome * 0.06);
  const equalRate = 5000;
  const total = prefectureTax + cityTax + equalRate;
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
  let deduction: number;
  if (familyType === 'single') deduction = 0;
  else if (familyType === 'couple') deduction = 380000;
  else deduction = 760000;
  const taxableIncome = Math.max(annualIncome - annualIncome * 0.2 - deduction - 480000, 0);
  let taxRate: number;
  if (taxableIncome <= 1950000) taxRate = 0.05;
  else if (taxableIncome <= 3300000) taxRate = 0.1;
  else if (taxableIncome <= 6950000) taxRate = 0.2;
  else if (taxableIncome <= 9000000) taxRate = 0.23;
  else taxRate = 0.33;
  const residentTaxRate = 0.1;
  const limit = Math.round(taxableIncome * residentTaxRate * 0.2 / (1 - taxRate - residentTaxRate) + 2000);
  return { limit: Math.max(limit, 2000), taxableIncome: Math.round(taxableIncome), taxRate: Math.round(taxRate * 100) };
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
  const _adSpend = Number(inputs.adSpend ?? 0);
  const _revenue = Number(inputs.revenue ?? 0);
  const _conversions = Number(inputs.conversions ?? 0);
  return{roas:_adSpend>0?Math.round(_revenue/_adSpend*100):0,profit:_revenue-_adSpend};
}

export function advancePayment(inputs: Record<string, number | string>): Record<string, number | string> {
  const _loanBalance = Number(inputs.loanBalance ?? 0);
  const _rate = Number(inputs.rate ?? 0);
  const _remainingYears = Number(inputs.remainingYears ?? 0);
  const _advanceAmount = Number(inputs.advanceAmount ?? 0);
  const _type = String(inputs.type ?? '');
  const c=_currentBalance*10000;
  const a=_advanceAmount*10000;
  return{remaining:Math.max(c-a,0),savedInterest:Math.round(a*_rate/100*_remainingYears),newBalance:Math.max(c-a,0)};
}

export function airConditionerCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _capacity = Number(inputs.capacity ?? 0);
  const _hoursPerDay = Number(inputs.hoursPerDay ?? 0);
  const _days = Number(inputs.days ?? 0);
  const _pricePerKwh = Number(inputs.pricePerKwh ?? 0);
  const wm:Record<number,number>={4:300,6:450,8:630,10:830,12:1050,14:1300};
  const w=wm[_capacity]||_capacity*100;
  const kwh=w/1000*_hoursPerDay*_days;
  const cost=Math.round(kwh*_pricePerKwh);
  return{monthlyCost:cost,dailyCost:Math.round(cost/_days),seasonCost:cost*3};
}

export function alcoholCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const _drinkType = String(inputs.drinkType ?? '');
  const _amount = Number(inputs.amount ?? 0);
  const pcts: Record<string, number> = { beer: 5, wine: 12, sake: 15, shochu: 25, whisky: 40, chuhai: 7 };
  const pct = pcts[_drinkType] || 5;
  const pa = _amount * pct / 100 * 0.8;
  return { calories: Math.round(pa * 7.1), pureAlcohol: Math.round(pa * 10) / 10 };
}

export function alcoholTobaccoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _product = String(inputs.product ?? '');
  const _price = Number(inputs.price ?? 0);
  const rates: Record<string, number> = { beer: 77, wine: 47, sake: 38, whisky: 67, tobacco: 16.7 };
  const r = rates[_productType] || 50;
  const tax = Math.round(_quantity * r);
  return { tax, unitTax: r, totalWithTax: Math.round(_quantity * r * 1.1) };
}

export function anniversary(inputs: Record<string, number | string>): Record<string, number | string> {
  const _startDate = Number(inputs.startDate ?? 0);
  const start = new Date(_startYear, _startMonth - 1, _startDay);
  const now = new Date();
  const days = Math.floor((now.getTime() - start.getTime()) / 86400000);
  return { days, months: Math.floor(days/30), years: Math.round(days/365*10)/10, nextMilestone: Math.ceil(days/100)*100 };
}

export function assetAllocation(inputs: Record<string, number | string>): Record<string, number | string> {
  const _age = Number(inputs.age ?? 0);
  const _riskTolerance = String(inputs.riskTolerance ?? '');
  const _totalAsset = Number(inputs.totalAsset ?? 0);
  const total = _stocks + _bonds + _realEstate + _cash;
  if (total === 0) return { stocksRatio: 0, bondsRatio: 0, realEstateRatio: 0, cashRatio: 0, total: 0 };
  return { stocksRatio: Math.round(_stocks/total*100), bondsRatio: Math.round(_bonds/total*100), realEstateRatio: Math.round(_realEstate/total*100), cashRatio: Math.round(_cash/total*100), total };
}

export function autoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _displacement = String(inputs.displacement ?? '');
  const _years = Number(inputs.years ?? 0);
  const d = _displacement;
  let tax = d <= 1000 ? 29500 : d <= 1500 ? 34500 : d <= 2000 ? 39500 : d <= 2500 ? 45000 : d <= 3000 ? 51000 : d <= 3500 ? 58000 : d <= 4000 ? 66500 : d <= 4500 ? 76500 : d <= 6000 ? 88000 : 111000;
  return { tax, baseTax: tax, annualCost: tax };
}

export function babyGrowth(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthsAge = Number(inputs.monthsAge ?? 0);
  const _gender = String(inputs.gender ?? '');
  const _weight = Number(inputs.weight ?? 0);
  const _height = Number(inputs.height ?? 0);
  const w = _week;
  return { estimatedWeight: w < 20 ? Math.round(w * 15) : Math.round(w*w*1.5 - 20*w), estimatedLength: Math.round(w * 1.2) };
}

export function baseConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  const n = Math.round(_number);
  return { decimal: n, binary: parseInt(n.toString(2)) || 0, octal: parseInt(n.toString(8)) || 0, hex: n.toString(16).toUpperCase() } as any;
}

export function bloodAlcohol(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _gender = String(inputs.gender ?? '');
  const _pureAlcohol = Number(inputs.pureAlcohol ?? 0);
  const _hours = Number(inputs.hours ?? 0);
  const pa = _drinks * 14;
  const bw = _weight * (_gender === 'male' ? 0.68 : 0.55);
  const bac = Math.max(Math.round((pa / (bw * 10) - 0.015 * _hours) * 1000) / 1000, 0);
  return { bac, status: bac > 0.08 ? '飲酒運転基準超' : bac > 0 ? '微量' : '検出なし' } as any;
}

export function blueReturn(inputs: Record<string, number | string>): Record<string, number | string> {
  const _businessIncome = Number(inputs.businessIncome ?? 0);
  const _deductionType = String(inputs.deductionType ?? '');
  const inc = _income * 10000;
  const taxable = Math.max(inc - 650000 - 480000, 0);
  return { blueDeduction: 650000, taxable, taxSaving: Math.round(650000 * 0.2) };
}

export function bmiChild(inputs: Record<string, number | string>): Record<string, number | string> {
  const _age = Number(inputs.age ?? 0);
  const _height = Number(inputs.height ?? 0);
  const _weight = Number(inputs.weight ?? 0);
  const _gender = String(inputs.gender ?? '');
  return{bmi:Math.round(_weight/Math.pow(_height/100,2)*10)/10};
}

export function bmiDetailed(inputs: Record<string, number | string>): Record<string, number | string> {
  const _height = Number(inputs.height ?? 0);
  const _weight = Number(inputs.weight ?? 0);
  const bmi=Math.round(_weight/Math.pow(_height/100,2)*10)/10;
  const iw=Math.round(Math.pow(_height/100,2)*22*10)/10;
  const c=bmi<18.5?'低体重':bmi<25?'普通体重':bmi<30?'肥満1度':bmi<35?'肥満2度':'肥満3度以上';
  return{bmi,category:c,idealWeight:iw,weightDiff:Math.round((_weight-iw)*10)/10} as any;
}

export function bmiPet(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _idealWeight = Number(inputs.idealWeight ?? 0);
  const diff=Math.round((_weight-_idealWeight)*10)/10;
  return{bcs:Math.min(Math.max(Math.round(_weight/_idealWeight*5),1),9),weightDiff:diff};
}

export function bodyFatPercentage(inputs: Record<string, number | string>): Record<string, number | string> {
  const _height = Number(inputs.height ?? 0);
  const _weight = Number(inputs.weight ?? 0);
  const _age = Number(inputs.age ?? 0);
  const _gender = String(inputs.gender ?? '');
  const bmi = _weight / Math.pow(_height / 100, 2);
  const isMale = _gender === 'male';
  const bf = isMale ? 1.2*bmi + 0.23*_age - 16.2 : 1.2*bmi + 0.23*_age - 5.4;
  const cat = isMale ? (bf<10?'低い':bf<20?'標準':bf<25?'やや高い':'高い') : (bf<20?'低い':bf<30?'標準':bf<35?'やや高い':'高い');
  return { bodyFat: Math.round(bf*10)/10, bmi: Math.round(bmi*10)/10, category: cat } as any;
}

export function bondYield(inputs: Record<string, number | string>): Record<string, number | string> {
  const _faceValue = Number(inputs.faceValue ?? 0);
  const _purchasePrice = Number(inputs.purchasePrice ?? 0);
  const _couponRate = Number(inputs.couponRate ?? 0);
  const _yearsToMaturity = Number(inputs.yearsToMaturity ?? 0);
  const fv = _faceValue * 10000;
  const pp = _purchasePrice * 10000;
  const coupon = Math.round(fv * _couponRate / 100);
  return { annualCoupon: coupon, currentYield: pp > 0 ? Math.round(coupon/pp*10000)/100 : 0, totalReturn: coupon * _yearsToMaturity + (fv - pp) };
}

export function businessDays(inputs: Record<string, number | string>): Record<string, number | string> {
  const _startDate = Number(inputs.startDate ?? 0);
  const _days = Number(inputs.days ?? 0);
  const w=Math.floor(_daysCount/7)*2;
  return{businessDays:_daysCount-w,weekendDays:w};
}

export function caffeine(inputs: Record<string, number | string>): Record<string, number | string> {
  const _coffee = Number(inputs.coffee ?? 0);
  const _tea = Number(inputs.tea ?? 0);
  const _greenTea = Number(inputs.greenTea ?? 0);
  const _energyDrink = Number(inputs.energyDrink ?? 0);
  const mg:Record<string,number>={coffee:95,tea:47,energy:80,cola:34};
  return{totalCaffeine:(mg[_drinkType]||95)*_cups,safe:(mg[_drinkType]||95)*_cups<=400?1:0,halfLifeHours:5};
}

export function capitalGainsTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _salePrice = Number(inputs.salePrice ?? 0);
  const _purchasePrice = Number(inputs.purchasePrice ?? 0);
  const _expenses = Number(inputs.expenses ?? 0);
  const _assetType = String(inputs.assetType ?? '');
  const g = _gain * 10000;
  const r = _holdingPeriod === 'short' ? 0.3942 : 0.2042;
  const tax = Math.round(g * r);
  return { tax, effectiveRate: Math.round(r * 10000) / 100, afterTax: g - tax };
}

export function carCostTotal(inputs: Record<string, number | string>): Record<string, number | string> {
  const _carType = String(inputs.carType ?? '');
  const _annualMileage = Number(inputs.annualMileage ?? 0);
  const _fuelEfficiency = Number(inputs.fuelEfficiency ?? 0);
  const _fuelPrice = Number(inputs.fuelPrice ?? 0);
  const annual = (_insurance + _tax + _maintenance + _fuel) * 10000;
  return { annual, monthly: Math.round(annual/12), daily: Math.round(annual/365) };
}

export function carLease(inputs: Record<string, number | string>): Record<string, number | string> {
  const _carPrice = Number(inputs.carPrice ?? 0);
  const _leaseMonthly = Number(inputs.leaseMonthly ?? 0);
  const _leaseYears = Number(inputs.leaseYears ?? 0);
  const _residualRate = Number(inputs.residualRate ?? 0);
  const p=_vehiclePrice*10000;
  const rv=Math.round(p*_residualRate/100);
  const m=_leaseYears*12;
  const mp=Math.round((p-rv)/m);
  return{monthlyPayment:mp,totalPayment:mp*m,residualValue:rv};
}

export function carbonFootprint(inputs: Record<string, number | string>): Record<string, number | string> {
  const _carKm = Number(inputs.carKm ?? 0);
  const _electricityKwh = Number(inputs.electricityKwh ?? 0);
  const _gasM3 = Number(inputs.gasM3 ?? 0);
  const e=_electricityKwh*0.423;
  const g=_gasM3*2.21;
  const c=_carKm*0.23;
  return{total:Math.round((e+g+c)*10)/10,electricity:Math.round(e*10)/10,gas:Math.round(g*10)/10,car:Math.round(c*10)/10};
}

export function carpetCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _width = Number(inputs.width ?? 0);
  const _depth = Number(inputs.depth ?? 0);
  const a=_width*_depth;
  return{area:Math.round(a*100)/100,tatami:Math.round(a/1.62*10)/10,cost:Math.round(a*3000)};
}

export function certificationCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _cert = String(inputs.cert ?? '');
  const _studyMethod = String(inputs.studyMethod ?? '');
  const t=_examFee+_textbookCost+_courseFee;
  return{total:t,monthlyIfSave:_monthsToSave>0?Math.round(t/_monthsToSave):0};
}

export function childCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _childAge = Number(inputs.childAge ?? 0);
  const _schoolType = String(inputs.schoolType ?? '');
  const _university = String(inputs.university ?? '');
  const a=(_education+_food+_clothing+_medical)*10000;
  return{annual:a,monthly:Math.round(a/12),total18years:a*18};
}

export function childcareBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthlySalary = Number(inputs.monthlySalary ?? 0);
  const s = _monthlySalary * 10000;
  const f6 = Math.round(s * 0.67);
  const a6 = Math.round(s * 0.50);
  return { first6months: f6, after6months: a6, annualTotal: f6 * 6 + a6 * 6 };
}

export function chineseZodiac(inputs: Record<string, number | string>): Record<string, number | string> {
  const _year = Number(inputs.year ?? 0);
  const a=['子(ねずみ)','丑(うし)','寅(とら)','卯(うさぎ)','辰(たつ)','巳(へび)','午(うま)','未(ひつじ)','申(さる)','酉(とり)','戌(いぬ)','亥(いのしし)'];
  const idx=(_year-4)%12;
  return{zodiac:a[idx>=0?idx:idx+12],year:_year} as any;
}

export function churnRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const _startCustomers = Number(inputs.startCustomers ?? 0);
  const _churned = Number(inputs.churned ?? 0);
  const _period = Number(inputs.period ?? 0);
  const r=_totalCustomers>0?Math.round(_lostCustomers/_totalCustomers*10000)/100:0;
  return{churnRate:r,retentionRate:100-r,avgLifespan:r>0?Math.round(100/r*10)/10:0};
}

export function cityPlanningTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _landValue = Number(inputs.landValue ?? 0);
  const _buildingValue = Number(inputs.buildingValue ?? 0);
  const a = _assessedValue * 10000;
  const tax = Math.round(a * _taxRate / 100);
  return { tax, monthlyTax: Math.round(tax / 12) };
}

export function clothingSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const _jpSize = String(inputs.jpSize ?? '');
  const _gender = String(inputs.gender ?? '');
  const bmi=_weight/Math.pow(_height/100,2);
  return{size:bmi<18.5?'S':bmi<23?'M':bmi<25?'L':bmi<28?'XL':'XXL',bmi:Math.round(bmi*10)/10} as any;
}

export function commuteCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _method = String(inputs.method ?? '');
  const _monthlyCost = Number(inputs.monthlyCost ?? 0);
  const _distance = Number(inputs.distance ?? 0);
  const annual = _monthlyCost * 12;
  return { annual, daily: Math.round(_monthlyCost / _workDays), taxFree: Math.min(annual, 150000), taxable: Math.max(annual - 150000, 0) };
}

export function compoundInterestDetail(inputs: Record<string, number | string>): Record<string, number | string> {
  const _principal = Number(inputs.principal ?? 0);
  const _rate = Number(inputs.rate ?? 0);
  const _years = Number(inputs.years ?? 0);
  const _monthly = Number(inputs.monthly ?? 0);
  const p = _principal * 10000;
  const r = _rate / 100;
  const m = _monthly * 10000;
  let fv = p * Math.pow(1 + r, _years);
  if (m > 0 && r > 0) fv += m * ((Math.pow(1 + r/12, _years*12) - 1) / (r/12));
  else if (m > 0) fv += m * _years * 12;
  const td = p + m * _years * 12;
  return { futureValue: Math.round(fv), totalDeposit: Math.round(td), interest: Math.round(fv - td), returnRate: td > 0 ? Math.round((fv-td)/td*100) : 0 };
}

export function concreteCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _width = Number(inputs.width ?? 0);
  const _depth = Number(inputs.depth ?? 0);
  const _thickness = Number(inputs.thickness ?? 0);
  const v=_width*_depth*_thickness/100;
  return{volume:Math.round(v*100)/100,weight:Math.round(v*2300),bags:Math.ceil(v/0.012)};
}

export function consumptionTaxCalc(inputs: Record<string, number | string>): Record<string, number | string> {
  const _price = Number(inputs.price ?? 0);
  const _direction = String(inputs.direction ?? '');
  const _rate = String(inputs.rate ?? '');
  const r = _rate === '8' ? 0.08 : 0.10;
  if (_direction === 'excl_to_incl') { const t = Math.round(_price * r);
  return { result: _price + t, taxAmount: t };
  }
  const ex = Math.round(_price / (1 + r));
  return { result: ex, taxAmount: _price - ex };
}

export function corporatePension(inputs: Record<string, number | string>): Record<string, number | string> {
  const _years = Number(inputs.years ?? 0);
  const _avgSalary = Number(inputs.avgSalary ?? 0);
  const _type = String(inputs.type ?? '');
  const _dcContribution = Number(inputs.dcContribution ?? 0);
  const m = _monthlyContribution * 10000;
  const months = _years * 12;
  const r = _expectedReturn / 100 / 12;
  const tc = m * months;
  const fv = r > 0 ? Math.round(m * ((Math.pow(1+r,months)-1)/r)) : tc;
  return { futureValue: fv, totalContribution: tc, investmentReturn: fv - tc };
}

export function corporateTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _taxableIncome = Number(inputs.taxableIncome ?? 0);
  const _isSmall = String(inputs.isSmall ?? '');
  const inc = _income * 10000;
  const rate = inc <= 8000000 ? 0.15 : 0.234;
  const tax = Math.round(inc * rate);
  const localTax = Math.round(tax * 0.174);
  return { corporateTax: tax, effectiveRate: Math.round(rate * 10000) / 100, localTax, totalTax: tax + localTax };
}

export function correlation(inputs: Record<string, number | string>): Record<string, number | string> {
  const _dataX = Number(inputs.dataX ?? 0);
  const _dataY = Number(inputs.dataY ?? 0);
  const xm = (_x1+_x2+_x3)/3;
  const ym = (_y1+_y2+_y3)/3;
  const num = (_x1-xm)*(_y1-ym)+(_x2-xm)*(_y2-ym)+(_x3-xm)*(_y3-ym);
  const dx = Math.sqrt((_x1-xm)**2+(_x2-xm)**2+(_x3-xm)**2);
  const dy = Math.sqrt((_y1-ym)**2+(_y2-ym)**2+(_y3-ym)**2);
  const r = dx*dy>0 ? Math.round(num/(dx*dy)*10000)/10000 : 0;
  return { correlation: r, strength: Math.abs(r)>0.7?'強い':Math.abs(r)>0.4?'中程度':'弱い' } as any;
}

export function cryptoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _profit = Number(inputs.profit ?? 0);
  const _otherIncome = Number(inputs.otherIncome ?? 0);
  const p = _profit * 10000;
  const o = _otherIncome * 10000;
  const total = p + o;
  const r = total <= 1950000 ? 0.15 : total <= 3300000 ? 0.20 : total <= 6950000 ? 0.30 : total <= 9000000 ? 0.33 : 0.43;
  return { tax: Math.round(p * r), effectiveRate: Math.round(r * 100), afterTax: p - Math.round(p * r) };
}

export function currencyConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const _amount = Number(inputs.amount ?? 0);
  const _rate = Number(inputs.rate ?? 0);
  const _direction = String(inputs.direction ?? '');
  return{result:Math.round(_amount*_exchangeRate*100)/100,rate:_exchangeRate};
}

export function cyclingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _minutes = Number(inputs.minutes ?? 0);
  const _intensity = String(inputs.intensity ?? '');
  const mets: Record<string, number> = { light: 4, moderate: 6, vigorous: 10 };
  const m = mets[_intensity] || 6;
  const cal = Math.round(m * _weight * (_minutes / 60) * 1.05);
  const speeds: Record<string, number> = { light: 10, moderate: 16, vigorous: 25 };
  return { calories: cal, distance: Math.round((speeds[_intensity]||16)*_minutes/60*100)/100, fatBurn: Math.round(cal/7.2*10)/10 };
}

export function dataSizeConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  const _fromUnit = String(inputs.fromUnit ?? '');
  const mult:Record<string,number>={B:1,KB:1024,MB:1048576,GB:1073741824,TB:1099511627776};
  const bytes=_value*(mult[_fromUnit]||1);
  return{B:bytes,KB:Math.round(bytes/1024*1000)/1000,MB:Math.round(bytes/1048576*1000)/1000,GB:Math.round(bytes/1073741824*10000)/10000,TB:Math.round(bytes/1099511627776*100000)/100000};
}

export function debtRepayment(inputs: Record<string, number | string>): Record<string, number | string> {
  const _balance = Number(inputs.balance ?? 0);
  const _rate = Number(inputs.rate ?? 0);
  const _monthlyPayment = Number(inputs.monthlyPayment ?? 0);
  const d = _totalDebt * 10000;
  const p = _monthlyPayment * 10000;
  const r = _interestRate / 100 / 12;
  let bal = d;
  let months = 0;
  let ti = 0;
  while (bal > 0 && months < 600) { const interest = Math.round(bal * r);
  ti += interest;
  bal = bal + interest - p;
  months++;
  }
  return { months, years: Math.round(months / 12 * 10) / 10, totalInterest: ti, totalPaid: d + ti };
}

export function disabilityInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthlyIncome = Number(inputs.monthlyIncome ?? 0);
  const _monthlyExpense = Number(inputs.monthlyExpense ?? 0);
  const _publicBenefit = Number(inputs.publicBenefit ?? 0);
  const cov=Math.round(_monthlyIncome*10000*_coverageRate/100);
  return{coverage:cov,premium:Math.round(cov*0.02),annualPremium:Math.round(cov*0.02)*12};
}

export function dollarCostAveraging(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthlyAmount = Number(inputs.monthlyAmount ?? 0);
  const _years = Number(inputs.years ?? 0);
  const _expectedReturn = Number(inputs.expectedReturn ?? 0);
  const m = _monthlyAmount * 10000;
  const months = _years * 12;
  const r = _expectedReturn / 100 / 12;
  const ti = m * months;
  const fv = r > 0 ? Math.round(m * ((Math.pow(1+r, months)-1)/r)) : ti;
  return { totalInvested: ti, futureValue: fv, profit: fv - ti, profitRate: ti > 0 ? Math.round((fv-ti)/ti*100) : 0 };
}

export function downloadTime(inputs: Record<string, number | string>): Record<string, number | string> {
  const _fileSize = Number(inputs.fileSize ?? 0);
  const _speed = Number(inputs.speed ?? 0);
  const sec=Math.round(_fileSize*8/_connectionSpeed);
  return{seconds:sec,minutes:Math.round(sec/60*10)/10};
}

export function electricityBill(inputs: Record<string, number | string>): Record<string, number | string> {
  const _watt = Number(inputs.watt ?? 0);
  const _hoursPerDay = Number(inputs.hoursPerDay ?? 0);
  const _days = Number(inputs.days ?? 0);
  const _pricePerKwh = Number(inputs.pricePerKwh ?? 0);
  const kwh=_watt/1000*_hoursPerDay*_days;
  const cost=Math.round(kwh*_pricePerKwh);
  return{monthlyCost:cost,kwhUsed:Math.round(kwh*10)/10,dailyCost:Math.round(cost/_days)};
}

export function ellipse(inputs: Record<string, number | string>): Record<string, number | string> {
  const _a = Number(inputs.a ?? 0);
  const _b = Number(inputs.b ?? 0);
  return { area: Math.round(Math.PI*_semiMajor*_semiMinor*100)/100, perimeter: Math.round(Math.PI*(3*(_semiMajor+_semiMinor)-Math.sqrt((3*_semiMajor+_semiMinor)*(_semiMajor+3*_semiMinor)))*100)/100 };
}

export function emailMarketing(inputs: Record<string, number | string>): Record<string, number | string> {
  const _subscribers = Number(inputs.subscribers ?? 0);
  const _openRate = Number(inputs.openRate ?? 0);
  const _clickRate = Number(inputs.clickRate ?? 0);
  const _cvr = Number(inputs.cvr ?? 0);
  const _avgOrderValue = Number(inputs.avgOrderValue ?? 0);
  const opens=Math.round(_sent*_openRate/100);
  const clicks=Math.round(opens*_clickRate/100);
  return{opens,clicks,conversionEstimate:Math.round(clicks*0.02)};
}

export function emergencyFund(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthlyExpense = Number(inputs.monthlyExpense ?? 0);
  const _employmentType = String(inputs.employmentType ?? '');
  const m = _monthlyExpenses * 10000;
  return { fund3: m * 3, fund6: m * 6, fund12: m * 12 };
}

export function energyConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  const _fromUnit = String(inputs.fromUnit ?? '');
  return { kcal: _value, kJ: Math.round(_value*4.184*100)/100, wh: Math.round(_value*1.163*100)/100 };
}

export function englishScore(inputs: Record<string, number | string>): Record<string, number | string> {
  const _toeicScore = Number(inputs.toeicScore ?? 0);
  return{toeic:_score,ielts:Math.min(Math.round(_score/990*9*10)/10,9),toefl:Math.min(Math.round(_score/990*120),120)};
}

export function etfCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _investAmount = Number(inputs.investAmount ?? 0);
  const _expenseRatio = Number(inputs.expenseRatio ?? 0);
  const _years = Number(inputs.years ?? 0);
  const _annualReturn = Number(inputs.annualReturn ?? 0);
  const inv = _investment * 10000;
  const annual = Math.round(inv * _expenseRatio / 100);
  return { annualCost: annual, cost10yr: annual * 10, dailyCost: Math.round(annual / 365) };
}

export function evCostComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const _annualMileage = Number(inputs.annualMileage ?? 0);
  const _evEfficiency = Number(inputs.evEfficiency ?? 0);
  const _electricityPrice = Number(inputs.electricityPrice ?? 0);
  const _gasEfficiency = Number(inputs.gasEfficiency ?? 0);
  const _gasPrice = Number(inputs.gasPrice ?? 0);
  const ev = Math.round(_annualKm / _evEfficiency * _electricityRate);
  const gas = Math.round(_annualKm / _gasFuelEfficiency * _gasPrice);
  return { evAnnual: ev, gasAnnual: gas, savings: gas - ev };
}

export function exerciseCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _minutes = Number(inputs.minutes ?? 0);
  const _exercise = String(inputs.exercise ?? '');
  const mets: Record<string, number> = { jogging: 7, cycling: 6, swimming: 8, yoga: 3, tennis: 7, dancing: 5 };
  const m = mets[_exercise] || 5;
  const cal = Math.round(m * _weight * (_minutes / 60) * 1.05);
  return { calories: cal, fatBurn: Math.round(cal / 7.2 * 10) / 10 };
}

export function fabricCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _width = Number(inputs.width ?? 0);
  const _height = Number(inputs.height ?? 0);
  const _fabricWidth = Number(inputs.fabricWidth ?? 0);
  const _seam = Number(inputs.seam ?? 0);
  const area=_width*_length/10000;
  const fw=_fabricWidthCm/100;
  return{fabricLength:fw>0?Math.round(area/fw*100)/100:0,totalArea:Math.round(area*100)/100};
}

export function fireInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const _buildingType = String(inputs.buildingType ?? '');
  const _area = Number(inputs.area ?? 0);
  const _coverage = Number(inputs.coverage ?? 0);
  const base = _buildingValue * 10000;
  const rates: Record<string, number> = { wooden: 0.001, fireproof: 0.0005 };
  const r = rates[_structure] || 0.001;
  const annual = Math.round(base * r);
  return { annual, fiveYear: annual * 5, tenYear: annual * 10 };
}

export function fractionCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _num1 = Number(inputs.num1 ?? 0);
  const _den1 = Number(inputs.den1 ?? 0);
  const _operator = String(inputs.operator ?? '');
  const _num2 = Number(inputs.num2 ?? 0);
  const _den2 = Number(inputs.den2 ?? 0);
  function gcd(a:number,b:number):number{return b===0?a:gcd(b,a%b)}let rn:number,rd:number;
  if(_operator==='add'){rn=_num1*_den2+_num2*_den1;
  rd=_den1*_den2}else if(_operator==='sub'){rn=_num1*_den2-_num2*_den1;
  rd=_den1*_den2}else if(_operator==='mul'){rn=_num1*_num2;
  rd=_den1*_den2}else{rn=_num1*_den2;
  rd=_den1*_num2}const g=gcd(Math.abs(rn),Math.abs(rd));
  return{resultNum:rn/g,resultDen:rd/g,decimal:Math.round(rn/rd*10000)/10000};
}

export function freelanceRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const _targetIncome = Number(inputs.targetIncome ?? 0);
  const _workDays = Number(inputs.workDays ?? 0);
  const _workHours = Number(inputs.workHours ?? 0);
  const _expenseRate = Number(inputs.expenseRate ?? 0);
  const annual = _targetIncome * 10000;
  const total = annual + _expenses * 10000 + annual * 0.3;
  const hourly = Math.round(total / (_workHoursPerMonth * 12));
  return { hourlyRate: hourly, dailyRate: hourly * 8, monthlyRate: hourly * _workHoursPerMonth };
}

export function gardenSoil(inputs: Record<string, number | string>): Record<string, number | string> {
  const _area = Number(inputs.area ?? 0);
  const _depth = Number(inputs.depth ?? 0);
  const _pricePerBag = Number(inputs.pricePerBag ?? 0);
  const _bagVolume = Number(inputs.bagVolume ?? 0);
  const v=_width*_depth*_soilDepth/100;
  return{volume:Math.round(v*100)/100,bags:Math.ceil(v/14)};
}

export function goldInvestment(inputs: Record<string, number | string>): Record<string, number | string> {
  const _purchasePrice = Number(inputs.purchasePrice ?? 0);
  const _currentPrice = Number(inputs.currentPrice ?? 0);
  const _grams = Number(inputs.grams ?? 0);
  return { totalCost: Math.round(_goldPrice * _weight), perGram: _goldPrice, weight: _weight };
}

export function gpaCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _subjects = Number(inputs.subjects ?? 0);
  const _s1 = Number(inputs.s1 ?? 0);
  const _s2 = Number(inputs.s2 ?? 0);
  const _s3 = Number(inputs.s3 ?? 0);
  const _s4 = Number(inputs.s4 ?? 0);
  const _s5 = Number(inputs.s5 ?? 0);
  const _c1 = Number(inputs.c1 ?? 0);
  const _c2 = Number(inputs.c2 ?? 0);
  const _c3 = Number(inputs.c3 ?? 0);
  const _c4 = Number(inputs.c4 ?? 0);
  const _c5 = Number(inputs.c5 ?? 0);
  const scores=[_s1,_s2,_s3,_s4,_s5];
  const credits=[_c1,_c2,_c3,_c4,_c5];
  let tp=0,tc=0;
  for(let i=0;
  i<_subjects;
  i++){tp+=scores[i]*credits[i];
  tc+=credits[i]}return{gpa:tc>0?Math.round(tp/tc*100)/100:0,totalCredits:tc,totalPoints:tp};
}

export function gradeCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _subject1 = Number(inputs.subject1 ?? 0);
  const _subject2 = Number(inputs.subject2 ?? 0);
  const _subject3 = Number(inputs.subject3 ?? 0);
  const _subject4 = Number(inputs.subject4 ?? 0);
  const _subject5 = Number(inputs.subject5 ?? 0);
  const total = _score1 + _score2 + _score3;
  const avg = Math.round(total/3*10)/10;
  return { average: avg, grade: avg>=90?'A':avg>=80?'B':avg>=70?'C':avg>=60?'D':'F', total } as any;
}

export function grossMargin(inputs: Record<string, number | string>): Record<string, number | string> {
  const _revenue = Number(inputs.revenue ?? 0);
  const _cogs = Number(inputs.cogs ?? 0);
  const rev = _revenue * 10000;
  const c = _cogs * 10000;
  const gp = rev - c;
  return { grossProfit: gp, margin: rev > 0 ? Math.round(gp/rev*10000)/100 : 0 };
}

export function hearingLevel(inputs: Record<string, number | string>): Record<string, number | string> {
  const _decibel = Number(inputs.decibel ?? 0);
  const avg=Math.round((_freq500+_freq1000+_freq2000+_freq4000)/4);
  return{average:avg,level:avg<25?'正常':avg<40?'軽度難聴':avg<70?'中等度難聴':'高度難聴'} as any;
}

export function hensachi(inputs: Record<string, number | string>): Record<string, number | string> {
  const _score = Number(inputs.score ?? 0);
  const _average = Number(inputs.average ?? 0);
  const _sd = Number(inputs.sd ?? 0);
  return { hensachi: _stdDeviation > 0 ? Math.round((_score-_average)/_stdDeviation*10+50) : 50 };
}

export function hexagon(inputs: Record<string, number | string>): Record<string, number | string> {
  const _side = Number(inputs.side ?? 0);
  return { area: Math.round(3*Math.sqrt(3)/2*_sideLength*_sideLength*100)/100, perimeter: Math.round(6*_sideLength*100)/100 };
}

export function housingDeduction(inputs: Record<string, number | string>): Record<string, number | string> {
  const _loanBalance = Number(inputs.loanBalance ?? 0);
  const _houseType = String(inputs.houseType ?? '');
  const _moveInYear = Number(inputs.moveInYear ?? 0);
  const lb=_loanBalance*10000;
  const d=Math.min(Math.round(lb*0.007),210000);
  return{annualDeduction:d,total13yr:d*13};
}

export function individualEnterpriseTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _income = Number(inputs.income ?? 0);
  const _industry = String(inputs.industry ?? '');
  const inc = _income * 10000;
  const taxable = Math.max(inc - 2900000, 0);
  return { tax: Math.round(taxable * 0.05), taxable, deduction: 2900000 };
}

export function inflationCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _amount = Number(inputs.amount ?? 0);
  const _inflationRate = Number(inputs.inflationRate ?? 0);
  const _years = Number(inputs.years ?? 0);
  const r = _inflationRate / 100;
  const a = _amount * 10000;
  return { futureNominal: Math.round(a * Math.pow(1+r, _years)), realValue: Math.round(a / Math.pow(1+r, _years)), purchasingPowerLoss: Math.round((1 - 1/Math.pow(1+r, _years)) * 100) };
}

export function inheritanceTaxSimulation(inputs: Record<string, number | string>): Record<string, number | string> {
  const _totalAssets = Number(inputs.totalAssets ?? 0);
  const _heirs = Number(inputs.heirs ?? 0);
  const _spouse = String(inputs.spouse ?? '');
  const a=_assets*10000;
  const bd=30000000+6000000*_heirs;
  const t=Math.max(a-bd,0);
  let r=0.10,d=0;
  if(t>600000000){r=0.55;
  d=72000000}else if(t>300000000){r=0.50;
  d=42000000}else if(t>200000000){r=0.45;
  d=27000000}else if(t>100000000){r=0.40;
  d=17000000}else if(t>50000000){r=0.30;
  d=7000000}else if(t>30000000){r=0.20;
  d=2000000}else if(t>10000000){r=0.15;
  d=500000}return{tax:Math.max(Math.round(t*r-d),0),basicDeduction:bd,taxable:t};
}

export function initialCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _rent = Number(inputs.rent ?? 0);
  const _deposit = Number(inputs.deposit ?? 0);
  const _keyMoney = Number(inputs.keyMoney ?? 0);
  const _agentFee = Number(inputs.agentFee ?? 0);
  const p=_price*10000;
  const af=Math.round((p*0.03+60000)*1.1);
  const rt=Math.round(p*0.02);
  const at=Math.round(p*0.03);
  return{agentFee:af,registrationTax:rt,acquisitionTax:at,total:af+rt+at};
}

export function investmentReturn(inputs: Record<string, number | string>): Record<string, number | string> {
  const _initialAmount = Number(inputs.initialAmount ?? 0);
  const _monthlyAmount = Number(inputs.monthlyAmount ?? 0);
  const _annualReturn = Number(inputs.annualReturn ?? 0);
  const _years = Number(inputs.years ?? 0);
  const i = _initialAmount * 10000;
  const f = _finalAmount * 10000;
  const profit = f - i;
  return { profit, returnRate: i > 0 ? Math.round(profit / i * 10000) / 100 : 0, annualReturn: i > 0 ? Math.round((Math.pow(f / i, 1 / _years) - 1) * 10000) / 100 : 0 };
}

export function japaneseEra(inputs: Record<string, number | string>): Record<string, number | string> {
  const _year = Number(inputs.year ?? 0);
  const y = _year;
  let era = '', ey = 0;
  if (y>=2019){era='令和';
  ey=y-2018}else if(y>=1989){era='平成';
  ey=y-1988}else if(y>=1926){era='昭和';
  ey=y-1925}else if(y>=1912){era='大正';
  ey=y-1911}else{era='明治';
  ey=y-1867}
  return { era, eraYear: ey, fullText: `${era}${ey}年` } as any;
}

export function joggingPace(inputs: Record<string, number | string>): Record<string, number | string> {
  const _distance = Number(inputs.distance ?? 0);
  const _minutes = Number(inputs.minutes ?? 0);
  return{pace:_distance>0?Math.round(_minutes/_distance*100)/100:0,speed:_minutes>0?Math.round(_distance/(_minutes/60)*10)/10:0,calories:Math.round(7*65*(_minutes/60)*1.05)};
}

export function laborCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthlySalary = Number(inputs.monthlySalary ?? 0);
  const _bonusMonths = Number(inputs.bonusMonths ?? 0);
  const s = _salary * 10000;
  const si = Math.round(s * 0.15);
  return { totalCost: s+si, socialInsurance: si, laborCostRatio: _revenue > 0 ? Math.round((s+si)/(_revenue*10000)*100) : 0 };
}

export function landPrice(inputs: Record<string, number | string>): Record<string, number | string> {
  const _pricePerTsubo = Number(inputs.pricePerTsubo ?? 0);
  const _areaTsubo = Number(inputs.areaTsubo ?? 0);
  const tp=Math.round(_pricePerSqm*10000*_area);
  const tb=Math.round(_area/3.30579*100)/100;
  return{totalPrice:tp,tsubo:tb,pricePerTsubo:tb>0?Math.round(tp/tb):0};
}

export function logarithm(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  const _base = Number(inputs.base ?? 0);
  return { result: Math.round(Math.log(_value)/Math.log(_base)*10000)/10000, ln: Math.round(Math.log(_value)*10000)/10000, log10: Math.round(Math.log10(_value)*10000)/10000 };
}

export function ltv(inputs: Record<string, number | string>): Record<string, number | string> {
  const _avgOrderValue = Number(inputs.avgOrderValue ?? 0);
  const _purchaseFrequency = Number(inputs.purchaseFrequency ?? 0);
  const _customerLifespan = Number(inputs.customerLifespan ?? 0);
  const _grossMarginRate = Number(inputs.grossMarginRate ?? 0);
  return{ltv:Math.round(_avgPurchase*_purchaseFrequency*_customerLifespan),annualValue:Math.round(_avgPurchase*_purchaseFrequency)};
}

export function mansionCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _managementFee = Number(inputs.managementFee ?? 0);
  const _repairReserve = Number(inputs.repairReserve ?? 0);
  const _parkingFee = Number(inputs.parkingFee ?? 0);
  const _ownershipYears = Number(inputs.ownershipYears ?? 0);
  const p = _price * 10000;
  const mg = _management * 10000;
  const rp = _repair * 10000;
  const mc = mg + rp;
  return { monthlyCost: mc, annualCost: mc * 12, totalCost30yr: mc * 12 * 30 + p };
}

export function marginTrading(inputs: Record<string, number | string>): Record<string, number | string> {
  const _stockPrice = Number(inputs.stockPrice ?? 0);
  const _shares = Number(inputs.shares ?? 0);
  const _marginRate = Number(inputs.marginRate ?? 0);
  const _priceChange = Number(inputs.priceChange ?? 0);
  const dep = _deposit * 10000;
  const pos = Math.round(dep * _leverage);
  const pl = Math.round(pos * _priceChange / 100);
  return { totalPosition: pos, profitLoss: pl, returnOnDeposit: dep > 0 ? Math.round(pl/dep*100) : 0 };
}

export function maternityBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthlySalary = Number(inputs.monthlySalary ?? 0);
  const daily = Math.round(_monthlySalary * 10000 / 30);
  const benefit = Math.round(daily * 2 / 3);
  return { dailyBenefit: benefit, totalBenefit: benefit * 98, totalDays: 98 };
}

export function matrix(inputs: Record<string, number | string>): Record<string, number | string> {
  const _a11 = Number(inputs.a11 ?? 0);
  const _a12 = Number(inputs.a12 ?? 0);
  const _a21 = Number(inputs.a21 ?? 0);
  const _a22 = Number(inputs.a22 ?? 0);
  return{determinant:_a11*_a22-_a12*_a21,trace:_a11+_a22};
}

export function mealCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const _rice = Number(inputs.rice ?? 0);
  const _meat = Number(inputs.meat ?? 0);
  const _fish = Number(inputs.fish ?? 0);
  const _vegetables = Number(inputs.vegetables ?? 0);
  const _oil = Number(inputs.oil ?? 0);
  const total = _rice + _mainDish + _sideDish + _soup;
  return { total, perMeal: total };
}

export function medianMode(inputs: Record<string, number | string>): Record<string, number | string> {
  const _data = Number(inputs.data ?? 0);
  const vals=[_v1,_v2,_v3,_v4,_v5].slice(0,_n).sort((a:any,b:any)=>a-b);
  const len=vals.length;
  const median=len%2===0?(vals[len/2-1]+vals[len/2])/2:vals[Math.floor(len/2)];
  const mean=vals.reduce((s:number,v:any)=>s+Number(v),0)/len;
  return{median,mean:Math.round(mean*100)/100};
}

export function medicineDose(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _dosePerKg = Number(inputs.dosePerKg ?? 0);
  const _timesPerDay = Number(inputs.timesPerDay ?? 0);
  const child = Math.round(_standardDose * _childWeight / 50 * 10) / 10;
  return { childDose: child, ratio: Math.round(_childWeight / 50 * 100) };
}

export function meetingCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _participants = Number(inputs.participants ?? 0);
  const _avgHourlyRate = Number(inputs.avgHourlyRate ?? 0);
  const _durationMinutes = Number(inputs.durationMinutes ?? 0);
  const hr=_averageSalary*10000/12/160;
  const cost=Math.round(hr*_participants*_durationMinutes/60);
  return{cost,perMinute:Math.round(cost/_durationMinutes)};
}

export function menstrualCycle(inputs: Record<string, number | string>): Record<string, number | string> {
  const _lastPeriod = Number(inputs.lastPeriod ?? 0);
  const _cycleLength = Number(inputs.cycleLength ?? 0);
  const _periodLength = Number(inputs.periodLength ?? 0);
  const ov=_cycleLength-14;
  return{nextPeriod:_cycleLength,ovulationDay:ov,fertileStart:Math.max(ov-5,1),fertileEnd:ov+1};
}

export function minimumWage(inputs: Record<string, number | string>): Record<string, number | string> {
  const _hourlyWage = Number(inputs.hourlyWage ?? 0);
  const _region = String(inputs.region ?? '');
  const monthly = Math.round(_minimumWageAmount * _hoursPerDay * _daysPerMonth);
  return { monthly, annual: monthly * 12, hourly: _minimumWageAmount };
}

export function nationalHealthInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const _income = Number(inputs.income ?? 0);
  const _members = Number(inputs.members ?? 0);
  const _age = Number(inputs.age ?? 0);
  const inc = _income * 10000;
  const taxable = Math.max(inc - 430000, 0);
  const medical = Math.min(Math.round(taxable * 0.0789 + 22200 * _family), 650000);
  const support = Math.min(Math.round(taxable * 0.0266 + 7500 * _family), 220000);
  const care = _age >= 40 && _age < 65 ? Math.min(Math.round(taxable * 0.0222 + 6200 * _family), 170000) : 0;
  const total = medical + support + care;
  return { total, monthly: Math.round(total / 12), medical, support, care };
}

export function normalDistribution(inputs: Record<string, number | string>): Record<string, number | string> {
  const _mean = Number(inputs.mean ?? 0);
  const _stddev = Number(inputs.stddev ?? 0);
  const _x = Number(inputs.x ?? 0);
  return{zScore:Math.round((_x-_mean)/_stdDev*10000)/10000};
}

export function ovulationDay(inputs: Record<string, number | string>): Record<string, number | string> {
  const _lastPeriod = Number(inputs.lastPeriod ?? 0);
  const _cycleLength = Number(inputs.cycleLength ?? 0);
  const ov = _cycleLength - 14;
  return { ovulationDay: ov, fertileStart: Math.max(ov - 5, 1), fertileEnd: ov + 1 };
}

export function packingList(inputs: Record<string, number | string>): Record<string, number | string> {
  const _days = Number(inputs.days ?? 0);
  const _season = String(inputs.season ?? '');
  const _laundry = String(inputs.laundry ?? '');
  return{totalItems:5+_days+(_days>3?3:0),clothingSets:_days,luggageWeight:Math.round((5+_days)*0.3*10)/10};
}

export function paintArea(inputs: Record<string, number | string>): Record<string, number | string> {
  const _width = Number(inputs.width ?? 0);
  const _depth = Number(inputs.depth ?? 0);
  const _height = Number(inputs.height ?? 0);
  const _windows = Number(inputs.windows ?? 0);
  const _doors = Number(inputs.doors ?? 0);
  const wa=2*(_width+_depth)*_height-_windows*1.5-_doors*1.8;
  const ca=_width*_depth;
  return{wallArea:Math.round(wa*100)/100,ceilingArea:Math.round(ca*100)/100,totalArea:Math.round((wa+ca)*100)/100,paintLiters:Math.round((wa+ca)/6*10)/10};
}

export function paintCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _wallArea = Number(inputs.wallArea ?? 0);
  const _coats = Number(inputs.coats ?? 0);
  const _coveragePerLiter = Number(inputs.coveragePerLiter ?? 0);
  const _canSize = Number(inputs.canSize ?? 0);
  const liters=Math.ceil(_wallArea*_numberOfCoats/6*10)/10;
  return{liters,cans:Math.ceil(liters/4)};
}

export function paperSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const _size = String(inputs.size ?? '');
  const s:Record<string,number[]>={A0:[841,1189],A1:[594,841],A2:[420,594],A3:[297,420],A4:[210,297],A5:[148,210],A6:[105,148],B4:[250,353],B5:[176,250]};
  const sz=s[_size]||s['A4'];
  return{width:sz[0],height:sz[1],area:sz[0]*sz[1]};
}

export function partyFood(inputs: Record<string, number | string>): Record<string, number | string> {
  const _guests = Number(inputs.guests ?? 0);
  const _duration = Number(inputs.duration ?? 0);
  const _style = String(inputs.style ?? '');
  return{totalFoodG:Math.round(_guests*300*_hours/2),totalDrinkMl:Math.round(_guests*500*_hours/2)};
}

export function paybackPeriod(inputs: Record<string, number | string>): Record<string, number | string> {
  const _investment = Number(inputs.investment ?? 0);
  const _annualReturn = Number(inputs.annualReturn ?? 0);
  const _annualCost = Number(inputs.annualCost ?? 0);
  const inv=_investment*10000;
  const cf=_annualCashflow*10000;
  return{period:cf>0?Math.round(inv/cf*10)/10:0,monthlyReturn:Math.round(cf/12)};
}

export function perPbr(inputs: Record<string, number | string>): Record<string, number | string> {
  const _stockPrice = Number(inputs.stockPrice ?? 0);
  const _eps = Number(inputs.eps ?? 0);
  const _bps = Number(inputs.bps ?? 0);
  const per = _eps > 0 ? Math.round(_stockPrice / _eps * 100) / 100 : 0;
  const pbr = _bps > 0 ? Math.round(_stockPrice / _bps * 100) / 100 : 0;
  return { per, pbr, earningsYield: per > 0 ? Math.round(1/per * 10000) / 100 : 0 };
}

export function percentageCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _valueA = Number(inputs.valueA ?? 0);
  const _valueB = Number(inputs.valueB ?? 0);
  const _calcType = String(inputs.calcType ?? '');
  if(_calcType==='of')return{result:Math.round(_valueB*_valueA/100*100)/100,explanation:`${_valueB}の${_valueA}%`} as any;
  if(_calcType==='is')return{result:_valueB>0?Math.round(_valueA/_valueB*10000)/100:0,explanation:`${_valueA}は${_valueB}の何%`} as any;
  return{result:_valueA>0?Math.round((_valueB-_valueA)/_valueA*10000)/100:0,explanation:`${_valueA}→${_valueB}の変化率`} as any;
}

export function personalLoan(inputs: Record<string, number | string>): Record<string, number | string> {
  const _amount = Number(inputs.amount ?? 0);
  const _rate = Number(inputs.rate ?? 0);
  const _years = Number(inputs.years ?? 0);
  const a=_amount*10000;
  const r=_rate/100/12;
  const m=_years*12;
  const p=r>0?Math.round(a*r/(1-Math.pow(1+r,-m))):Math.round(a/m);
  return{monthlyPayment:p,totalPayment:p*m,totalInterest:p*m-a};
}

export function petAge(inputs: Record<string, number | string>): Record<string, number | string> {
  const _petType = String(inputs.petType ?? '');
  const _age = Number(inputs.age ?? 0);
  const isD=_petType==='dog';
  const ha=isD?(_age<=2?_age*12:24+(_age-2)*4):(_age<=2?_age*12.5:25+(_age-2)*4);
  return{humanAge:Math.round(ha)};
}

export function petInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const _petType = String(inputs.petType ?? '');
  const _age = Number(inputs.age ?? 0);
  const _coverage = String(inputs.coverage ?? '');
  const base=_petAge<3?2000:_petAge<7?3000:5000;
  const m=_petType==='dog'?1.2:1.0;
  const monthly=Math.round(base*m*_coverageRate/100);
  return{monthly,annual:monthly*12};
}

export function photoPrint(inputs: Record<string, number | string>): Record<string, number | string> {
  const _widthPx = Number(inputs.widthPx ?? 0);
  const _heightPx = Number(inputs.heightPx ?? 0);
  const _dpi = Number(inputs.dpi ?? 0);
  const w=Math.round(_printWidth*2.54*300);
  const h=Math.round(_printHeight*2.54*300);
  return{widthPixels:w,heightPixels:h,megapixels:Math.round(w*h/1000000*10)/10};
}

export function pointValue(inputs: Record<string, number | string>): Record<string, number | string> {
  const _amount = Number(inputs.amount ?? 0);
  const _rate = Number(inputs.rate ?? 0);
  const _monthlySpend = Number(inputs.monthlySpend ?? 0);
  return { value: Math.round(_points * _rate / 100), effectiveDiscount: _rate };
}

export function polygonArea(inputs: Record<string, number | string>): Record<string, number | string> {
  const _sides = Number(inputs.sides ?? 0);
  const _sideLength = Number(inputs.sideLength ?? 0);
  const area=Math.round(_sides*_sideLength*_sideLength/(4*Math.tan(Math.PI/_sides))*100)/100;
  return{area,perimeter:Math.round(_sides*_sideLength*100)/100};
}

export function postalRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const _type = String(inputs.type ?? '');
  const _weight = Number(inputs.weight ?? 0);
  let rate:number;
  if(_mailType==='letter'){rate=_weightGram<=25?84:_weightGram<=50?94:140}else if(_mailType==='postcard'){rate=63}else{rate=_weightGram<=150?180:_weightGram<=250?215:_weightGram<=500?310:_weightGram<=1000?360:510}return{rate};
}

export function powerConsumption(inputs: Record<string, number | string>): Record<string, number | string> {
  const _watt1 = Number(inputs.watt1 ?? 0);
  const _watt2 = Number(inputs.watt2 ?? 0);
  const _hoursPerDay = Number(inputs.hoursPerDay ?? 0);
  const _pricePerKwh = Number(inputs.pricePerKwh ?? 0);
  const c1=Math.round(_watt1/1000*_hoursPerDay*365*_pricePerKwh);
  const c2=Math.round(_watt2/1000*_hoursPerDay*365*_pricePerKwh);
  return{annualCost1:c1,annualCost2:c2,annualSaving:c1-c2,tenYearSaving:(c1-c2)*10};
}

export function pressureConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  const _fromUnit = String(inputs.fromUnit ?? '');
  return { hPa: _value, atm: Math.round(_value/1013.25*10000)/10000, mmHg: Math.round(_value*0.75006*100)/100, psi: Math.round(_value*0.014504*10000)/10000 };
}

export function pricingMarkup(inputs: Record<string, number | string>): Record<string, number | string> {
  const _cost = Number(inputs.cost ?? 0);
  const _price = Number(inputs.price ?? 0);
  const c=_cost*10000;
  const p=Math.round(c*(1+_markupRate/100));
  return{price:p,profit:p-c,margin:p>0?Math.round((p-c)/p*100):0};
}

export function primeFactorization(inputs: Record<string, number | string>): Record<string, number | string> {
  const _number = Number(inputs.number ?? 0);
  let n = Math.round(_number);
  const factors: number[] = [];
  for (let d = 2;
  d * d <= n;
  d++) { while (n % d === 0) { factors.push(d);
  n /= d;
  } }
  if (n > 1) factors.push(n);
  return { factors: factors.length, result: factors.join(' × '), isPrime: factors.length <= 1 ? 1 : 0 } as any;
}

export function probability(inputs: Record<string, number | string>): Record<string, number | string> {
  const _n = Number(inputs.n ?? 0);
  const _r = Number(inputs.r ?? 0);
  const p = _totalOutcomes > 0 ? _favorableOutcomes/_totalOutcomes : 0;
  return { probability: Math.round(p*10000)/10000, percentage: Math.round(p*10000)/100, odds: `${_favorableOutcomes}:${_totalOutcomes-_favorableOutcomes}` } as any;
}

export function proteinNeed(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _activity = String(inputs.activity ?? '');
  const m:Record<string,number>={sedentary:0.8,moderate:1.2,athlete:1.6,bodybuilder:2.0};
  const d=Math.round(_weight*(m[_activityLevel]||0.8));
  return{dailyProtein:d,perMeal:Math.round(d/3)};
}

export function pythagorean(inputs: Record<string, number | string>): Record<string, number | string> {
  const _sideA = Number(inputs.sideA ?? 0);
  const _sideB = Number(inputs.sideB ?? 0);
  return { hypotenuse: Math.round(Math.sqrt(_sideA*_sideA+_sideB*_sideB)*10000)/10000, area: Math.round(_sideA*_sideB/2*100)/100 };
}

export function quadratic(inputs: Record<string, number | string>): Record<string, number | string> {
  const _a = Number(inputs.a ?? 0);
  const _b = Number(inputs.b ?? 0);
  const _c_val = Number(inputs.c_val ?? 0);
  const disc=_b*_b-4*_a*_c;
  if(disc<0)return{discriminant:disc,realRoots:0};
  const x1=Math.round((-_b+Math.sqrt(disc))/(2*_a)*10000)/10000;
  const x2=Math.round((-_b-Math.sqrt(disc))/(2*_a)*10000)/10000;
  return{x1,x2,discriminant:disc,realRoots:disc===0?1:2};
}

export function randomNumber(inputs: Record<string, number | string>): Record<string, number | string> {
  const _min = Number(inputs.min ?? 0);
  const _max = Number(inputs.max ?? 0);
  const _count = Number(inputs.count ?? 0);
  return{result:Math.floor(Math.random()*(_maxValue-_minValue+1))+_minValue,min:_minValue,max:_maxValue};
}

export function realEstateAcquisitionTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _landValue = Number(inputs.landValue ?? 0);
  const _buildingValue = Number(inputs.buildingValue ?? 0);
  const _isResidential = String(inputs.isResidential ?? '');
  const a = _assessment * 10000;
  const landTax = Math.round(a * 0.5 * 0.03);
  const buildingTax = Math.round(a * 0.03);
  return { landTax, buildingTax, totalTax: landTax + buildingTax };
}

export function rebalance(inputs: Record<string, number | string>): Record<string, number | string> {
  const _totalAsset = Number(inputs.totalAsset ?? 0);
  const _currentStock = Number(inputs.currentStock ?? 0);
  const _currentBond = Number(inputs.currentBond ?? 0);
  const _targetStock = Number(inputs.targetStock ?? 0);
  const _targetBond = Number(inputs.targetBond ?? 0);
  const t=_stocksCurrent+_bondsCurrent+_cashCurrent;
  if(t===0)return{stocksAdj:0,bondsAdj:0,cashAdj:0};
  const st=Math.round(t*_stocksTargetPct/100);
  const bt=Math.round(t*_bondsTargetPct/100);
  return{stocksAdj:st-_stocksCurrent,bondsAdj:bt-_bondsCurrent,cashAdj:(t-st-bt)-_cashCurrent};
}

export function recipeScale(inputs: Record<string, number | string>): Record<string, number | string> {
  const _originalServings = Number(inputs.originalServings ?? 0);
  const _newServings = Number(inputs.newServings ?? 0);
  const _ingredientAmount = Number(inputs.ingredientAmount ?? 0);
  const r=_targetServings/_originalServings;
  return{ratio:Math.round(r*100)/100,scaledAmount:Math.round(_ingredientAmount*r*10)/10};
}

export function refinance(inputs: Record<string, number | string>): Record<string, number | string> {
  const _remainingBalance = Number(inputs.remainingBalance ?? 0);
  const _currentRate = Number(inputs.currentRate ?? 0);
  const _newRate = Number(inputs.newRate ?? 0);
  const _remainingYears = Number(inputs.remainingYears ?? 0);
  const _refinanceCost = Number(inputs.refinanceCost ?? 0);
  const b = _balance * 10000;
  const m = _remainingYears * 12;
  const r1 = _currentRate / 100 / 12;
  const r2 = _newInterestRate / 100 / 12;
  const p1 = r1 > 0 ? Math.round(b * r1 / (1 - Math.pow(1+r1, -m))) : Math.round(b / m);
  const p2 = r2 > 0 ? Math.round(b * r2 / (1 - Math.pow(1+r2, -m))) : Math.round(b / m);
  return { oldPayment: p1, newPayment: p2, monthlySavings: p1 - p2, totalSavings: (p1 - p2) * m };
}

export function registrationTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _propertyValue = Number(inputs.propertyValue ?? 0);
  const _regType = String(inputs.regType ?? '');
  const _loanAmount = Number(inputs.loanAmount ?? 0);
  const v = _value * 10000;
  const rates: Record<string, number> = { ownership: 0.02, mortgage: 0.004, transfer: 0.02 };
  const r = rates[_type] || 0.02;
  return { tax: Math.round(v * r), rate: r * 100 };
}

export function reitYield(inputs: Record<string, number | string>): Record<string, number | string> {
  const _price = Number(inputs.price ?? 0);
  const _annualDistribution = Number(inputs.annualDistribution ?? 0);
  const _units = Number(inputs.units ?? 0);
  const ann = _dividend * 12;
  return { annualDividend: ann, yield: _price > 0 ? Math.round(ann/_price*10000)/100 : 0, afterTax: Math.round(ann * 0.79685) };
}

export function rentCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _income = Number(inputs.income ?? 0);
  const _familySize = Number(inputs.familySize ?? 0);
  const r = _rent * 10000;
  return { annualRent: r * 12, initialCost: r * (_deposit + _keyMoney + 1), monthlyCost: r };
}

export function roomBrightness(inputs: Record<string, number | string>): Record<string, number | string> {
  const _area = Number(inputs.area ?? 0);
  const _roomType = String(inputs.roomType ?? '');
  const lm:Record<string,number>={living:400,bedroom:200,study:500,kitchen:300};
  const l=(lm[_roomType]||400)*_area;
  return{lumens:l,ledWatt:Math.round(l/100),fixtures:Math.ceil(_area/8)};
}

export function rule72(inputs: Record<string, number | string>): Record<string, number | string> {
  const _rate = Number(inputs.rate ?? 0);
  return { years: Math.round(72 / _rate * 10) / 10, actualYears: Math.round(Math.log(2) / Math.log(1 + _rate / 100) * 10) / 10, rate: _rate };
}

export function runningPace(inputs: Record<string, number | string>): Record<string, number | string> {
  const _distance = Number(inputs.distance ?? 0);
  const _hours = Number(inputs.hours ?? 0);
  const _minutes = Number(inputs.minutes ?? 0);
  return{pace:_distance>0?Math.round(_time/_distance*100)/100:0,speed:_time>0?Math.round(_distance/(_time/60)*10)/10:0,estimatedMarathon:_distance>0?Math.round(_time/_distance*42.195):0};
}

export function salaryAfterTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _income = Number(inputs.income ?? 0);
  const _dependents = Number(inputs.dependents ?? 0);
  const inc=_income*10000;
  const si=Math.round(inc*0.15);
  const ed=inc<=1625000?550000:inc<=1800000?Math.round(inc*0.4-100000):inc<=3600000?Math.round(inc*0.3+80000):inc<=6600000?Math.round(inc*0.2+440000):Math.round(inc*0.1+1100000);
  const ti=Math.max(inc-ed-si-480000-_dependents*380000,0);
  let tr=0.05,d=0;
  if(ti>40000000){tr=0.45;
  d=4796000}else if(ti>18000000){tr=0.40;
  d=2796000}else if(ti>9000000){tr=0.33;
  d=1536000}else if(ti>6950000){tr=0.23;
  d=636000}else if(ti>3300000){tr=0.20;
  d=427500}else if(ti>1950000){tr=0.10;
  d=97500}const it=Math.round(ti*tr-d);
  const rt=Math.round(ti*0.10);
  const th=inc-si-it-rt;
  return{takeHome:th,monthlyTakeHome:Math.round(th/12),totalTax:it+rt,socialInsurance:si,ratio:inc>0?Math.round(th/inc*100):0};
}

export function salaryComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const _monthlySalary = Number(inputs.monthlySalary ?? 0);
  const _bonusMonths = Number(inputs.bonusMonths ?? 0);
  const a = _salaryA * 10000;
  const b = _salaryB * 10000;
  return { diff: a - b, ratio: b > 0 ? Math.round(a / b * 100) : 0, monthlyDiff: Math.round((a - b) / 12) };
}

export function scholarship(inputs: Record<string, number | string>): Record<string, number | string> {
  const _totalBorrowed = Number(inputs.totalBorrowed ?? 0);
  const _rate = Number(inputs.rate ?? 0);
  const _years = Number(inputs.years ?? 0);
  const total = _monthlyAmount * 10000 * 12 * _years;
  return { total, monthly: _monthlyAmount * 10000, annual: _monthlyAmount * 10000 * 12 };
}

export function schoolCommute(inputs: Record<string, number | string>): Record<string, number | string> {
  const _distance = Number(inputs.distance ?? 0);
  const _method = String(inputs.method ?? '');
  const _monthlyCost = Number(inputs.monthlyCost ?? 0);
  const a=_monthlyCost*12;
  return{annual:a,fourYears:a*4,daily:Math.round(_monthlyCost/20)};
}

export function schoolSupplies(inputs: Record<string, number | string>): Record<string, number | string> {
  const _schoolType = String(inputs.schoolType ?? '');
  const t=_notebooks*200+_pens*150+_textbooks*1500;
  return{total:t,perItem:(_notebooks+_pens+_textbooks)>0?Math.round(t/(_notebooks+_pens+_textbooks)):0};
}

export function screenSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const _inches = Number(inputs.inches ?? 0);
  const _ratio = String(inputs.ratio ?? '');
  const r=_aspectRatio==='16:9'?16/9:_aspectRatio==='16:10'?16/10:_aspectRatio==='4:3'?4/3:16/9;
  const w=_diagonalInch/Math.sqrt(1+1/(r*r));
  const h=w/r;
  return{widthCm:Math.round(w*2.54*10)/10,heightCm:Math.round(h*2.54*10)/10,areaSqCm:Math.round(w*h*2.54*2.54)};
}

export function severanceTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const _severance = Number(inputs.severance ?? 0);
  const _years = Number(inputs.years ?? 0);
  const s = _severance * 10000;
  const ded = _yearsWorked <= 20 ? _yearsWorked * 400000 : 8000000 + (_yearsWorked - 20) * 700000;
  const taxable = Math.max(Math.round((s - ded) / 2), 0);
  const rate = taxable <= 1950000 ? 0.05 : taxable <= 3300000 ? 0.10 : taxable <= 6950000 ? 0.20 : 0.23;
  const d2 = taxable <= 1950000 ? 0 : taxable <= 3300000 ? 97500 : taxable <= 6950000 ? 427500 : 636000;
  const it = Math.max(Math.round(taxable * rate - d2), 0);
  const rt = Math.round(taxable * 0.10);
  return { incomeTax: it, residentTax: rt, deduction: ded, taxable, afterTax: s - it - rt };
}

export function shoeSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const _jpSize = Number(inputs.jpSize ?? 0);
  const _gender = String(inputs.gender ?? '');
  const jp=Math.round(_footLengthCm*2)/2;
  return{jp,us:Math.max(Math.round((_footLengthCm-18)/0.667*10)/10,1),eu:Math.round((_footLengthCm+1.5)*1.5*10)/10};
}

export function sleepCycle(inputs: Record<string, number | string>): Record<string, number | string> {
  const _wakeUpHour = Number(inputs.wakeUpHour ?? 0);
  const _wakeUpMinute = Number(inputs.wakeUpMinute ?? 0);
  return{bedtime4:4*90+15,bedtime5:5*90+15,bedtime6:6*90+15};
}

export function squareRoot(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  return{result:Math.round(Math.sqrt(_number)*10000)/10000,squared:_number,isInteger:Number.isInteger(Math.sqrt(_number))?1:0};
}

export function stampDuty(inputs: Record<string, number | string>): Record<string, number | string> {
  const _amount = Number(inputs.amount ?? 0);
  const _docType = String(inputs.docType ?? '');
  const a = _amount * 10000;
  const sd = a <= 10000 ? 200 : a <= 1000000 ? 400 : a <= 2000000 ? 600 : a <= 3000000 ? 1000 : a <= 5000000 ? 2000 : a <= 10000000 ? 10000 : a <= 50000000 ? 20000 : a <= 100000000 ? 60000 : 100000;
  return { stampDuty: sd, contractAmount: a };
}

export function stretchTimer(inputs: Record<string, number | string>): Record<string, number | string> {
  const _deskHours = Number(inputs.deskHours ?? 0);
  return{stretchMinutes:Math.round(_deskHours*3),exercises:Math.round(_deskHours),breakInterval:60};
}

export function studyPlan(inputs: Record<string, number | string>): Record<string, number | string> {
  const _totalHours = Number(inputs.totalHours ?? 0);
  const _daysUntilExam = Number(inputs.daysUntilExam ?? 0);
  const _availableDays = Number(inputs.availableDays ?? 0);
  return{dailyHours:_daysAvailable>0?Math.round(_targetHours/_daysAvailable*10)/10:0,weeklyHours:_daysAvailable>0?Math.round(_targetHours/_daysAvailable*7*10)/10:0};
}

export function subscriptionCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _sub1 = Number(inputs.sub1 ?? 0);
  const _sub2 = Number(inputs.sub2 ?? 0);
  const _sub3 = Number(inputs.sub3 ?? 0);
  const _sub4 = Number(inputs.sub4 ?? 0);
  const _sub5 = Number(inputs.sub5 ?? 0);
  const t=_sub1+_sub2+_sub3+_sub4+_sub5;
  return{monthlyTotal:t,annualTotal:t*12,dailyCost:Math.round(t/30)};
}

export function swimmingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _minutes = Number(inputs.minutes ?? 0);
  const _stroke = String(inputs.stroke ?? '');
  const mets: Record<string, number> = { crawl: 8, breaststroke: 6, backstroke: 5, butterfly: 10, water_walk: 4 };
  const m = mets[_stroke] || 6;
  const cal = Math.round(m * _weight * (_minutes / 60) * 1.05);
  return { calories: cal, fatBurn: Math.round(cal / 7.2 * 10) / 10 };
}

export function targetHeartRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const _age = Number(inputs.age ?? 0);
  const _restingHR = Number(inputs.restingHR ?? 0);
  const max = 220 - _age;
  return { maxHR: max, lower: Math.round(max*0.6), upper: Math.round(max*0.8), fatBurn: Math.round(max*0.65) };
}

export function tileCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _areaWidth = Number(inputs.areaWidth ?? 0);
  const _areaDepth = Number(inputs.areaDepth ?? 0);
  const _tileSize = Number(inputs.tileSize ?? 0);
  const _lossRate = Number(inputs.lossRate ?? 0);
  const a=_areaWidth*_areaDepth;
  const ta=(_tileSize/100)*(_tileSize/100);
  const tiles=Math.ceil(a/ta*(1+_lossRate/100));
  return{tilesNeeded:tiles,area:Math.round(a*100)/100,boxes:Math.ceil(tiles/10)};
}

export function timeConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  const _fromUnit = String(inputs.fromUnit ?? '');
  const ts = _hours * 3600 + _minutes * 60 + _seconds;
  return { totalSeconds: ts, totalMinutes: Math.round(ts/60*100)/100, totalHours: Math.round(ts/3600*1000)/1000, days: Math.round(ts/86400*1000)/1000 };
}

export function timeZone(inputs: Record<string, number | string>): Record<string, number | string> {
  const _fromOffset = Number(inputs.fromOffset ?? 0);
  const _toOffset = Number(inputs.toOffset ?? 0);
  const _hour = Number(inputs.hour ?? 0);
  const diff = _toOffset - _fromOffset;
  let h = _hour + diff;
  let ds = 0;
  if (h >= 24) { h -= 24;
  ds = 1;
  } else if (h < 0) { h += 24;
  ds = -1;
  }
  return { convertedHour: h, dayShift: ds, timeDiff: diff };
}

export function tipCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _billAmount = Number(inputs.billAmount ?? 0);
  const _tipRate = Number(inputs.tipRate ?? 0);
  const _people = Number(inputs.people ?? 0);
  const tip = Math.round(_billAmount * _tipRate / 100);
  return { tip, total: _billAmount + tip, perPerson: _people > 0 ? Math.round((_billAmount+tip)/_people) : _billAmount+tip };
}

export function trapezoid(inputs: Record<string, number | string>): Record<string, number | string> {
  const _topBase = Number(inputs.topBase ?? 0);
  const _bottomBase = Number(inputs.bottomBase ?? 0);
  const _height = Number(inputs.height ?? 0);
  return { area: Math.round((_topBase+_bottomBase)*_trapHeight/2*100)/100, perimeter: Math.round((_topBase+_bottomBase+2*Math.sqrt(Math.pow((_bottomBase-_topBase)/2,2)+_trapHeight*_trapHeight))*100)/100 };
}

export function travelInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const _destination = String(inputs.destination ?? '');
  const _days = Number(inputs.days ?? 0);
  const _plan = String(inputs.plan ?? '');
  const base=_days<=3?500:_days<=7?1000:_days<=14?2000:3000;
  const rm:Record<string,number>={asia:1,europe:1.5,americas:1.5};
  const p=Math.round(base*(rm[_destination]||1.2)*_people);
  return{premium:p,perPerson:Math.round(p/_people)};
}

export function trigonometry(inputs: Record<string, number | string>): Record<string, number | string> {
  const _angle = Number(inputs.angle ?? 0);
  const rad=_angle*Math.PI/180;
  return{sin:Math.round(Math.sin(rad)*10000)/10000,cos:Math.round(Math.cos(rad)*10000)/10000,tan:Math.round(Math.tan(rad)*10000)/10000};
}

export function tsuboM2(inputs: Record<string, number | string>): Record<string, number | string> {
  const _value = Number(inputs.value ?? 0);
  const _fromUnit = String(inputs.fromUnit ?? '');
  return{sqm:Math.round(_tsubo*3.30579*100)/100,tsubo:_tsubo,jo:Math.round(_tsubo*2*100)/100};
}

export function typingSpeed(inputs: Record<string, number | string>): Record<string, number | string> {
  const _characters = Number(inputs.characters ?? 0);
  const _minutes = Number(inputs.minutes ?? 0);
  return { wpm: Math.round(_characters/_minutes*60/5), cpm: Math.round(_characters/_minutes) };
}

export function unemploymentBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const _age = Number(inputs.age ?? 0);
  const _monthlySalary = Number(inputs.monthlySalary ?? 0);
  const _yearsWorked = Number(inputs.yearsWorked ?? 0);
  const _reason = String(inputs.reason ?? '');
  const daily = Math.round(_monthlySalary * 10000 / 30);
  const r = daily < 5110 ? 0.8 : daily < 12580 ? 0.65 : 0.5;
  const benefit = Math.round(daily * r);
  const days = _yearsWorked < 5 ? 90 : _yearsWorked < 10 ? 120 : 150;
  return { dailyBenefit: benefit, totalDays: days, totalBenefit: benefit * days };
}

export function unitPrice(inputs: Record<string, number | string>): Record<string, number | string> {
  const _price1 = Number(inputs.price1 ?? 0);
  const _amount1 = Number(inputs.amount1 ?? 0);
  const _price2 = Number(inputs.price2 ?? 0);
  const _amount2 = Number(inputs.amount2 ?? 0);
  const a=_price1/_amount1*100;
  const b=_price2/_amount2*100;
  return{unitPriceA:Math.round(a*10)/10,unitPriceB:Math.round(b*10)/10,savings:Math.round(Math.abs(a-b)*10)/10,verdict:a<b?'商品Aがお得':a>b?'商品Bがお得':'同じ'} as any;
}

export function visionTest(inputs: Record<string, number | string>): Record<string, number | string> {
  const _decimalVision = Number(inputs.decimalVision ?? 0);
  const c=_uncorrectedVision*_correctionFactor;
  return{corrected:Math.round(c*10)/10,diopter:c>0?Math.round(-1/c*100)/100:0};
}

export function vocabSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const _words = Number(inputs.words ?? 0);
  return{estimatedVocab:_sampleSize>0?Math.round(_knownWords*_totalWords/_sampleSize):0,knownRate:_sampleSize>0?Math.round(_knownWords/_sampleSize*100):0};
}

export function waistHipRatio(inputs: Record<string, number | string>): Record<string, number | string> {
  const _waist = Number(inputs.waist ?? 0);
  const _hip = Number(inputs.hip ?? 0);
  const _gender = String(inputs.gender ?? '');
  const ratio = Math.round(_waist / _hip * 100) / 100;
  return { ratio, risk: ratio > 0.9 ? 'リスクあり' : '正常' } as any;
}

export function walkingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const _weight = Number(inputs.weight ?? 0);
  const _minutes = Number(inputs.minutes ?? 0);
  const _speed = String(inputs.speed ?? '');
  const mets: Record<string, number> = { slow: 2.5, normal: 3.5, fast: 5.0 };
  const m = mets[_speed] || 3.5;
  const cal = Math.round(m * _weight * (_minutes / 60) * 1.05);
  const speeds: Record<string, number> = { slow: 3, normal: 4, fast: 6 };
  const dist = Math.round((speeds[_speed]||4) * _minutes / 60 * 100) / 100;
  return { calories: cal, distance: dist, steps: Math.round(dist * 1000 / 0.7) };
}

export function wallpaperCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const _width = Number(inputs.width ?? 0);
  const _depth = Number(inputs.depth ?? 0);
  const _height = Number(inputs.height ?? 0);
  const _rollWidth = Number(inputs.rollWidth ?? 0);
  const p=2*(_width+_depth);
  const wa=p*_height;
  const rw=_rollWidth/100;
  const strips=Math.ceil(p/rw);
  const tl=Math.round(strips*_height*100)/100;
  return{totalLength:tl,rolls:Math.ceil(tl/10),wallArea:Math.round(wa*100)/100};
}

export function weddingCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const _guests = Number(inputs.guests ?? 0);
  const _style = String(inputs.style ?? '');
  const _giftPerPerson = Number(inputs.giftPerPerson ?? 0);
  const v=_venueCost*10000;
  const f=_foodCost*_guests*10000;
  return{total:v+f,perGuest:_guests>0?Math.round((v+f)/_guests):0};
}

export function workersComp(inputs: Record<string, number | string>): Record<string, number | string> {
  const _avgDailyWage = Number(inputs.avgDailyWage ?? 0);
  const daily = Math.round(_monthlySalary * 10000 / 30);
  const benefit = Math.round(daily * 0.8);
  return { dailyBenefit: benefit, totalBenefit: benefit * _days };
}

export function workingCapital(inputs: Record<string, number | string>): Record<string, number | string> {
  const _receivables = Number(inputs.receivables ?? 0);
  const _inventory = Number(inputs.inventory ?? 0);
  const _payables = Number(inputs.payables ?? 0);
  const ar = _receivables * 10000;
  const inv = _inventory * 10000;
  const ap = _payables * 10000;
  return { workingCapital: ar+inv-ap, ratio: ap > 0 ? Math.round((ar+inv)/ap*100)/100 : 0 };
}

export function yieldComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const _propertyPrice = Number(inputs.propertyPrice ?? 0);
  const _monthlyRent = Number(inputs.monthlyRent ?? 0);
  const _annualExpense = Number(inputs.annualExpense ?? 0);
  const _vacancy = Number(inputs.vacancy ?? 0);
  const yA=_priceA>0?Math.round(_rentA*10000*12/(_priceA*10000)*10000)/100:0;
  const yB=_priceB>0?Math.round(_rentB*10000*12/(_priceB*10000)*10000)/100:0;
  return{yieldA:yA,yieldB:yB,difference:Math.round((yA-yB)*100)/100};
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
};

export function getCalculatorFunction(
  name: string
): ((inputs: Record<string, number | string>) => Record<string, number | string>) | undefined {
  return calculatorFunctions[name];
}
