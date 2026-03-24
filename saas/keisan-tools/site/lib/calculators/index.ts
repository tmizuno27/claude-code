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

// Calculator function registry
const calculatorFunctions: Record<string, (inputs: Record<string, number | string>) => Record<string, number | string>> = {
  loanRepayment,
  incomeTax,
  takeHomePay,
  bmi,
  daysBetween,
  compoundInterest,
  calcCompoundInterest: compoundInterest,
  carLoan,
  educationLoan,
  mortgageComparison,
  inheritanceTax,
  giftTax,
  consumptionTax,
  fixedAssetTax,
  bonusTax,
  hourlyWage,
  pensionEstimate,
  pensionContribution,
  stockProfit,
  dividendYield,
  lifeInsurance,
  rentVsBuy,
  calculateNisaSimulation,
  calculateIdecoSimulation,
  calculateForexProfit,
  calculateCryptoProfit,
  calculateFurusatoNozei,
  savingsSimulation,
  caloriesBmr,
  ageCalculator,
  roiCalculator,
  idealWeight,
  bodyFat,
  basalMetabolism,
  calorieBurn,
  dailyCalorie,
  dueDate,
  pregnancyWeek,
  medicalExpense,
  highCostMedical,
  waterIntake,
  ageCalculator,
  countdown,
  weekday,
  zodiac,
  elapsedDays,
  workDays,
  lengthConvert,
  weightConvert,
  temperatureConvert,
  areaConvert,
  volumeConvert,
  speedConvert,
  discount,
  taxIncluded,
  splitBill,
  perUnitPrice,
  dataSize,
  fuelCost,
  carTax,
  mileage,
  breakEven,
  profitMargin,
  roi,
  roiCalculator,
  cashFlow,
  inventoryTurnover,
  depreciation,
  overtimePay,
  annualLeave,
  retirementPay,
  socialInsuranceCalc,
  invoiceTax,
  freelanceTax,
  percentage,
  ratio,
  fraction,
  power,
  gcdLcm,
  circle,
  triangle,
  rectangle,
  sphere,
  cylinder,
  cone,
  average,
  standardDeviation,
  gpa,
  examScore,
  tuitionCost,
  studyTime,
  readingSpeed,
  medicalDeduction,
  sideJobTax,
  propertyYield,
  movingCost,
  carInsurance,
  annualIncome,
  repaymentPlan,
  savingsGoal,
  savingsSimulation,
  fireCalculation,
  residentTax,
  partTimeIncome,
  overtimeIncome,
  survivorPension,
  disabilityPension,
  earthquakeInsurance,
  renovationCost,
  dollarCostAvg,
  yearEndAdjustment,
  raiseImpact,
  creditCardInterest,
};

export function getCalculatorFunction(
  name: string
): ((inputs: Record<string, number | string>) => Record<string, number | string>) | undefined {
  return calculatorFunctions[name];
}
