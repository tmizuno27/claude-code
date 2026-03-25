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
  const adSpend = inputs.adSpend as number;
  const revenue = inputs.revenue as number;
  const conversions = inputs.conversions as number;
  const roas = adSpend > 0 ? Math.round(revenue / adSpend * 100) : 0;
  return { roas, profit: revenue - adSpend };
}

export function advancePayment(inputs: Record<string, number | string>): Record<string, number | string> {
  const loanBalance = inputs.loanBalance as number;
  const rate = inputs.rate as number;
  const remainingYears = inputs.remainingYears as number;
  const advanceAmount = inputs.advanceAmount as number;
  const type = inputs.type as string;
  const current10k = currentBalance * 10000;
  const advance10k = advanceAmount * 10000;
  const remaining = current10k - advance10k;
  const savedInterest = Math.round(advance10k * rate / 100 * remainingYears);
  return { remaining, savedInterest, newBalance: Math.max(remaining, 0) };
}

export function airConditionerCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const capacity = inputs.capacity as number;
  const hoursPerDay = inputs.hoursPerDay as number;
  const days = inputs.days as number;
  const pricePerKwh = inputs.pricePerKwh as number;
  const wattMap: Record<number, number> = { 4: 300, 6: 450, 8: 630, 10: 830, 12: 1050, 14: 1300, 16: 1500, 18: 1700, 20: 2000, 22: 2200, 24: 2500, 26: 2800, 28: 3000, 30: 3300 };
  const watt = wattMap[capacity] || capacity * 100;
  const kwh = watt / 1000 * hoursPerDay * days;
  const cost = Math.round(kwh * pricePerKwh);
  return { monthlyCost: cost, dailyCost: Math.round(cost / days), seasonCost: Math.round(cost * 3) };
}

export function alcoholCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const drinkType = inputs.drinkType as string;
  const amount = inputs.amount as number;
  const alcoholPercent: Record<string, number> = { beer: 5, wine: 12, sake: 15, shochu: 25, whisky: 40, chuhai: 7 };
  const pct = alcoholPercent[drinkType] || 5;
  const pureAlcohol = amount * pct / 100 * 0.8;
  const calories = Math.round(pureAlcohol * 7.1);
  return { calories, pureAlcohol: Math.round(pureAlcohol * 10) / 10 };
}

export function alcoholTobaccoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const product = inputs.product as string;
  const price = inputs.price as number;
  const qty = quantity as number;
  const taxRates: Record<string, number> = { beer: 77, wine: 47, sake: 38, whisky: 67, tobacco: 16.7 };
  const rate = taxRates[productType] || 50;
  const tax = Math.round(qty * rate);
  return { tax, unitTax: rate, totalWithTax: Math.round(qty * rate * 1.1) };
}

export function anniversary(inputs: Record<string, number | string>): Record<string, number | string> {
  const startDate = inputs.startDate as number;
  const startDate = new Date(startYear, startMonth - 1, startDay);
  const now = new Date();
  const diffMs = now.getTime() - startDate.getTime();
  const days = Math.floor(diffMs / 86400000);
  const next100 = Math.ceil(days / 100) * 100;
  return { days, months: Math.floor(days / 30), years: Math.round(days / 365 * 10) / 10, nextMilestone: next100 };
}

export function assetAllocation(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = inputs.age as number;
  const riskTolerance = inputs.riskTolerance as string;
  const totalAsset = inputs.totalAsset as number;
  const total = stocks + bonds + realEstate + cash;
  if (total === 0) return { stocksRatio: 0, bondsRatio: 0, realEstateRatio: 0, cashRatio: 0, total: 0 };
  return { stocksRatio: Math.round(stocks/total*100), bondsRatio: Math.round(bonds/total*100), realEstateRatio: Math.round(realEstate/total*100), cashRatio: Math.round(cash/total*100), total };
}

export function autoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const displacement = inputs.displacement as string;
  const years = inputs.years as number;
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
  const ecoDiscount = typeof inputs.ecoDiscount === 'number' ? inputs.ecoDiscount : 0;
  const finalTax = Math.round(tax * (1 - ecoDiscount / 100));
  return { tax: finalTax, baseTax: tax, annualCost: finalTax };
}

export function babyGrowth(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthsAge = inputs.monthsAge as number;
  const gender = inputs.gender as string;
  const weight = inputs.weight as number;
  const height = inputs.height as number;
  const weekNum = week as number;
  const estimatedWeight = weekNum < 20 ? Math.round(weekNum * 15) : Math.round(weekNum * weekNum * 1.5 - 20 * weekNum);
  const estimatedLength = Math.round(weekNum * 1.2);
  return { estimatedWeight, estimatedLength };
}

export function baseConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const num = number as number;
  return { decimal: num, binary: parseInt(num.toString(2)) || 0, octal: parseInt(num.toString(8)) || 0, hex: num.toString(16).toUpperCase() } as any;
}

export function bloodAlcohol(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const gender = inputs.gender as string;
  const pureAlcohol = inputs.pureAlcohol as number;
  const hours = inputs.hours as number;
  const pureAlcohol = drinks * 14;
  const bodyWater = weight * (gender === 'male' ? 0.68 : 0.55);
  const bac = Math.round((pureAlcohol / (bodyWater * 10) - 0.015 * hours) * 1000) / 1000;
  return { bac: Math.max(bac, 0), status: bac > 0.08 ? '飲酒運転基準超' : bac > 0 ? '微量' : '検出なし' } as any;
}

export function blueReturn(inputs: Record<string, number | string>): Record<string, number | string> {
  const businessIncome = inputs.businessIncome as number;
  const deductionType = inputs.deductionType as string;
  const income10k = income * 10000;
  const blueDeduction = 650000;
  const taxable = Math.max(income10k - blueDeduction - 480000, 0);
  const taxSaving = Math.round(blueDeduction * 0.2);
  return { blueDeduction, taxable, taxSaving };
}

export function bmiChild(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = inputs.age as number;
  const height = inputs.height as number;
  const weight = inputs.weight as number;
  const gender = inputs.gender as string;
  const bmiVal = Math.round(weight / Math.pow(height / 100, 2) * 10) / 10;
  return { bmi: bmiVal };
}

export function bmiDetailed(inputs: Record<string, number | string>): Record<string, number | string> {
  const height = inputs.height as number;
  const weight = inputs.weight as number;
  const bmiVal = Math.round(weight / Math.pow(height / 100, 2) * 10) / 10;
  const idealWt = Math.round(Math.pow(height / 100, 2) * 22 * 10) / 10;
  const cat = bmiVal < 18.5 ? '低体重' : bmiVal < 25 ? '普通体重' : bmiVal < 30 ? '肥満1度' : bmiVal < 35 ? '肥満2度' : '肥満3度以上';
  return { bmi: bmiVal, category: cat, idealWeight: idealWt, weightDiff: Math.round((weight - idealWt) * 10) / 10 } as any;
}

export function bmiPet(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const idealWeight = inputs.idealWeight as number;
  const bcs = Math.round(weight / idealWeight * 5);
  const diff = Math.round((weight - idealWeight) * 10) / 10;
  return { bcs: Math.min(Math.max(bcs, 1), 9), weightDiff: diff };
}

export function bodyFatPercentage(inputs: Record<string, number | string>): Record<string, number | string> {
  const height = inputs.height as number;
  const weight = inputs.weight as number;
  const age = inputs.age as number;
  const gender = inputs.gender as string;
  const bmiVal = weight / Math.pow(height / 100, 2);
  const isMale = gender === 'male';
  const bf = isMale ? 1.2 * bmiVal + 0.23 * age - 16.2 : 1.2 * bmiVal + 0.23 * age - 5.4;
  const category = isMale ? (bf < 10 ? '低い' : bf < 20 ? '標準' : bf < 25 ? 'やや高い' : '高い') : (bf < 20 ? '低い' : bf < 30 ? '標準' : bf < 35 ? 'やや高い' : '高い');
  return { bodyFat: Math.round(bf * 10) / 10, bmi: Math.round(bmiVal * 10) / 10, category } as any;
}

export function bondYield(inputs: Record<string, number | string>): Record<string, number | string> {
  const faceValue = inputs.faceValue as number;
  const purchasePrice = inputs.purchasePrice as number;
  const couponRate = inputs.couponRate as number;
  const yearsToMaturity = inputs.yearsToMaturity as number;
  const faceValue10k = faceValue * 10000;
  const purchasePrice10k = purchasePrice * 10000;
  const annualCoupon = Math.round(faceValue10k * couponRate / 100);
  const currentYield = purchasePrice10k > 0 ? Math.round(annualCoupon / purchasePrice10k * 10000) / 100 : 0;
  const totalReturn = annualCoupon * yearsToMaturity + (faceValue10k - purchasePrice10k);
  return { annualCoupon, currentYield, totalReturn };
}

export function businessDays(inputs: Record<string, number | string>): Record<string, number | string> {
  const startDate = inputs.startDate as number;
  const days = inputs.days as number;
  const totalDays = daysCount as number;
  const weekends = Math.floor(totalDays / 7) * 2;
  const bd = totalDays - weekends;
  return { businessDays: bd, weekendDays: weekends };
}

export function caffeine(inputs: Record<string, number | string>): Record<string, number | string> {
  const coffee = inputs.coffee as number;
  const tea = inputs.tea as number;
  const greenTea = inputs.greenTea as number;
  const energyDrink = inputs.energyDrink as number;
  const caffeinePerCup: Record<string, number> = { coffee: 95, tea: 47, energy: 80, cola: 34 };
  const mg = (caffeinePerCup[drinkType] || 95) * cups;
  const safe = mg <= 400;
  return { totalCaffeine: mg, safe: safe ? 1 : 0, halfLifeHours: 5 };
}

export function capitalGainsTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const salePrice = inputs.salePrice as number;
  const purchasePrice = inputs.purchasePrice as number;
  const expenses = inputs.expenses as number;
  const assetType = inputs.assetType as string;
  const gain10k = gain * 10000;
  const shortTermRate = 0.3942;
  const longTermRate = 0.2042;
  const rate = holdingPeriod === 'short' ? shortTermRate : longTermRate;
  const tax = Math.round(gain10k * rate);
  return { tax, effectiveRate: Math.round(rate * 10000) / 100, afterTax: gain10k - tax };
}

export function carCostTotal(inputs: Record<string, number | string>): Record<string, number | string> {
  const carType = inputs.carType as string;
  const annualMileage = inputs.annualMileage as number;
  const fuelEfficiency = inputs.fuelEfficiency as number;
  const fuelPrice = inputs.fuelPrice as number;
  const annual = (insurance + tax + maintenance + fuel) * 10000;
  return { annual, monthly: Math.round(annual / 12), daily: Math.round(annual / 365) };
}

export function carLease(inputs: Record<string, number | string>): Record<string, number | string> {
  const carPrice = inputs.carPrice as number;
  const leaseMonthly = inputs.leaseMonthly as number;
  const leaseYears = inputs.leaseYears as number;
  const residualRate = inputs.residualRate as number;
  const price10k = vehiclePrice * 10000;
  const residual10k = Math.round(price10k * residualRate / 100);
  const leaseBase = price10k - residual10k;
  const months = leaseYears * 12;
  const monthlyPayment = Math.round(leaseBase / months);
  return { monthlyPayment, totalPayment: monthlyPayment * months, residualValue: residual10k };
}

export function carbonFootprint(inputs: Record<string, number | string>): Record<string, number | string> {
  const carKm = inputs.carKm as number;
  const electricityKwh = inputs.electricityKwh as number;
  const gasM3 = inputs.gasM3 as number;
  const electricity = electricityKwh * 0.423;
  const gas = gasM3 * 2.21;
  const car = carKm * 0.23;
  const total = Math.round((electricity + gas + car) * 10) / 10;
  return { total, electricity: Math.round(electricity * 10) / 10, gas: Math.round(gas * 10) / 10, car: Math.round(car * 10) / 10 };
}

export function carpetCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = inputs.width as number;
  const depth = inputs.depth as number;
  const a = width * depth;
  const tatami = Math.round(a / 1.62 * 10) / 10;
  return { area: Math.round(a * 100) / 100, tatami, cost: Math.round(a * 3000) };
}

export function certificationCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const cert = inputs.cert as string;
  const studyMethod = inputs.studyMethod as string;
  const total = examFee + textbookCost + courseFee;
  return { total, monthlyIfSave: Math.round(total / monthsToSave) };
}

export function childCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const childAge = inputs.childAge as number;
  const schoolType = inputs.schoolType as string;
  const university = inputs.university as string;
  const annual = (education + food + clothing + medical) * 10000;
  return { annual, monthly: Math.round(annual / 12), total18years: annual * 18 };
}

export function childcareBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = inputs.monthlySalary as number;
  const salary10k = monthlySalary * 10000;
  const first6months = Math.round(salary10k * 0.67);
  const after6months = Math.round(salary10k * 0.50);
  const total = first6months * 6 + after6months * 6;
  return { first6months, after6months, annualTotal: total };
}

export function chineseZodiac(inputs: Record<string, number | string>): Record<string, number | string> {
  const year = inputs.year as number;
  const animals = ['子(ねずみ)', '丑(うし)', '寅(とら)', '卯(うさぎ)', '辰(たつ)', '巳(へび)', '午(うま)', '未(ひつじ)', '申(さる)', '酉(とり)', '戌(いぬ)', '亥(いのしし)'];
  const idx = (year - 4) % 12;
  return { zodiac: animals[idx >= 0 ? idx : idx + 12], year } as any;
}

export function churnRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const startCustomers = inputs.startCustomers as number;
  const churned = inputs.churned as number;
  const period = inputs.period as number;
  const rate = totalCustomers > 0 ? Math.round(lostCustomers / totalCustomers * 10000) / 100 : 0;
  const retentionRate = 100 - rate;
  return { churnRate: rate, retentionRate, avgLifespan: rate > 0 ? Math.round(100 / rate * 10) / 10 : 0 };
}

export function cityPlanningTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const landValue = inputs.landValue as number;
  const buildingValue = inputs.buildingValue as number;
  const assessed10k = assessedValue * 10000;
  const rate = taxRate / 100;
  const tax = Math.round(assessed10k * rate);
  return { tax, monthlyTax: Math.round(tax / 12) };
}

export function clothingSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const jpSize = inputs.jpSize as string;
  const gender = inputs.gender as string;
  const h = height as number; const w = weight as number;
  const bmi = w / Math.pow(h / 100, 2);
  const size = bmi < 18.5 ? 'S' : bmi < 23 ? 'M' : bmi < 25 ? 'L' : bmi < 28 ? 'XL' : 'XXL';
  return { size, bmi: Math.round(bmi * 10) / 10 } as any;
}

export function commuteCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const method = inputs.method as string;
  const monthlyCost = inputs.monthlyCost as number;
  const distance = inputs.distance as number;
  const monthly = monthlyCost as number;
  const workDaysPerMonth = workDays as number;
  const annual = monthly * 12;
  const daily = Math.round(monthly / workDaysPerMonth);
  const taxFree = Math.min(annual, 150000);
  return { annual, daily, taxFree, taxable: Math.max(annual - 150000, 0) };
}

export function compoundInterestDetail(inputs: Record<string, number | string>): Record<string, number | string> {
  const principal = inputs.principal as number;
  const rate = inputs.rate as number;
  const years = inputs.years as number;
  const monthly = inputs.monthly as number;
  const p = principal * 10000;
  const r = rate / 100;
  const m = monthly * 10000;
  let fv = p * Math.pow(1 + r, years);
  if (m > 0) fv += m * ((Math.pow(1 + r/12, years*12) - 1) / (r/12));
  const totalDeposit = p + m * years * 12;
  const interest = Math.round(fv - totalDeposit);
  return { futureValue: Math.round(fv), totalDeposit: Math.round(totalDeposit), interest, returnRate: totalDeposit > 0 ? Math.round(interest / totalDeposit * 100) : 0 };
}

export function concreteCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = inputs.width as number;
  const depth = inputs.depth as number;
  const thickness = inputs.thickness as number;
  const vol = width * depth * thickness / 100;
  const wt = Math.round(vol * 2300);
  return { volume: Math.round(vol * 100) / 100, weight: wt, bags: Math.ceil(vol / 0.012) };
}

export function consumptionTaxCalc(inputs: Record<string, number | string>): Record<string, number | string> {
  const price = inputs.price as number;
  const direction = inputs.direction as string;
  const rate = inputs.rate as string;
  const r = rate === '8' ? 0.08 : 0.10;
  if (direction === 'excl_to_incl') {
    const taxAmount = Math.round(price * r);
    return { result: price + taxAmount, taxAmount };
  } else {
    const exclPrice = Math.round(price / (1 + r));
    return { result: exclPrice, taxAmount: price - exclPrice };
  }
}

export function corporatePension(inputs: Record<string, number | string>): Record<string, number | string> {
  const years = inputs.years as number;
  const avgSalary = inputs.avgSalary as number;
  const type = inputs.type as string;
  const dcContribution = inputs.dcContribution as number;
  const monthly10k = monthlyContribution * 10000;
  const r = expectedReturn / 100 / 12;
  const months = years * 12;
  const total = monthly10k * months;
  const fv = r > 0 ? Math.round(monthly10k * ((Math.pow(1+r,months)-1)/r)) : total;
  return { futureValue: fv, totalContribution: total, investmentReturn: fv - total };
}

export function corporateTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const taxableIncome = inputs.taxableIncome as number;
  const isSmall = inputs.isSmall as string;
  const income10k = income * 10000;
  let rate: number;
  if (income10k <= 8000000) rate = 0.15;
  else rate = 0.234;
  const tax = Math.round(income10k * rate);
  const effectiveRate = Math.round(rate * 10000) / 100;
  const localTax = Math.round(tax * 0.174);
  return { corporateTax: tax, effectiveRate, localTax, totalTax: tax + localTax };
}

export function correlation(inputs: Record<string, number | string>): Record<string, number | string> {
  const dataX = inputs.dataX as number;
  const dataY = inputs.dataY as number;
  // Simplified: return placeholder for correlation coefficient
  const xMean = (x1 + x2 + x3) / 3;
  const yMean = (y1 + y2 + y3) / 3;
  const num = (x1-xMean)*(y1-yMean) + (x2-xMean)*(y2-yMean) + (x3-xMean)*(y3-yMean);
  const denX = Math.sqrt(Math.pow(x1-xMean,2) + Math.pow(x2-xMean,2) + Math.pow(x3-xMean,2));
  const denY = Math.sqrt(Math.pow(y1-yMean,2) + Math.pow(y2-yMean,2) + Math.pow(y3-yMean,2));
  const r = denX*denY > 0 ? Math.round(num / (denX * denY) * 10000) / 10000 : 0;
  return { correlation: r, strength: Math.abs(r) > 0.7 ? '強い' : Math.abs(r) > 0.4 ? '中程度' : '弱い' } as any;
}

export function cryptoTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const profit = inputs.profit as number;
  const otherIncome = inputs.otherIncome as number;
  const profit10k = profit * 10000;
  const otherIncome10k = otherIncome * 10000;
  const totalIncome = profit10k + otherIncome10k;
  let rate: number;
  if (totalIncome <= 1950000) rate = 0.15;
  else if (totalIncome <= 3300000) rate = 0.20;
  else if (totalIncome <= 6950000) rate = 0.30;
  else if (totalIncome <= 9000000) rate = 0.33;
  else rate = 0.43;
  const tax = Math.round(profit10k * rate);
  return { tax, effectiveRate: Math.round(rate * 100), afterTax: profit10k - tax };
}

export function currencyConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = inputs.amount as number;
  const rate = inputs.rate as number;
  const direction = inputs.direction as string;
  const result = Math.round(amount * exchangeRate * 100) / 100;
  return { result, rate: exchangeRate };
}

export function cyclingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const minutes = inputs.minutes as number;
  const intensity = inputs.intensity as string;
  const metsMap: Record<string, number> = { light: 4, moderate: 6, vigorous: 10 };
  const m = metsMap[intensity] || 6;
  const cal = Math.round(m * weight * (minutes / 60) * 1.05);
  const speedMap: Record<string, number> = { light: 10, moderate: 16, vigorous: 25 };
  const dist = Math.round((speedMap[intensity] || 16) * minutes / 60 * 100) / 100;
  return { calories: cal, distance: dist, fatBurn: Math.round(cal / 7.2 * 10) / 10 };
}

export function dataSizeConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const fromUnit = inputs.fromUnit as string;
  const multipliers: Record<string, number> = { B: 1, KB: 1024, MB: 1048576, GB: 1073741824, TB: 1099511627776 };
  const bytes = value * (multipliers[fromUnit] || 1);
  return { B: bytes, KB: Math.round(bytes / 1024 * 1000) / 1000, MB: Math.round(bytes / 1048576 * 1000) / 1000, GB: Math.round(bytes / 1073741824 * 10000) / 10000, TB: Math.round(bytes / 1099511627776 * 100000) / 100000 };
}

export function debtRepayment(inputs: Record<string, number | string>): Record<string, number | string> {
  const balance = inputs.balance as number;
  const rate = inputs.rate as number;
  const monthlyPayment = inputs.monthlyPayment as number;
  const debt10k = totalDebt * 10000;
  const payment10k = monthlyPayment * 10000;
  const r = interestRate / 100 / 12;
  let balance = debt10k; let months = 0; let totalInterest = 0;
  while (balance > 0 && months < 600) { const interest = Math.round(balance * r); totalInterest += interest; balance = balance + interest - payment10k; months++; }
  return { months, years: Math.round(months / 12 * 10) / 10, totalInterest, totalPaid: debt10k + totalInterest };
}

export function disabilityInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlyIncome = inputs.monthlyIncome as number;
  const monthlyExpense = inputs.monthlyExpense as number;
  const publicBenefit = inputs.publicBenefit as number;
  const monthly10k = monthlyIncome * 10000;
  const coverage = Math.round(monthly10k * coverageRate / 100);
  const premium = Math.round(coverage * 0.02);
  return { coverage, premium, annualPremium: premium * 12 };
}

export function dollarCostAveraging(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlyAmount = inputs.monthlyAmount as number;
  const years = inputs.years as number;
  const expectedReturn = inputs.expectedReturn as number;
  const m = monthlyAmount * 10000;
  const totalMonths = years * 12;
  const totalInvested = m * totalMonths;
  const r = expectedReturn / 100 / 12;
  const fv = r > 0 ? Math.round(m * ((Math.pow(1+r, totalMonths)-1)/r)) : totalInvested;
  const profit = fv - totalInvested;
  return { totalInvested, futureValue: fv, profit, profitRate: totalInvested > 0 ? Math.round(profit/totalInvested*100) : 0 };
}

export function downloadTime(inputs: Record<string, number | string>): Record<string, number | string> {
  const fileSize = inputs.fileSize as number;
  const speed = inputs.speed as number;
  const sizeMB = fileSize as number;
  const speedMbps = connectionSpeed as number;
  const seconds = Math.round(sizeMB * 8 / speedMbps);
  return { seconds, minutes: Math.round(seconds / 60 * 10) / 10 };
}

export function electricityBill(inputs: Record<string, number | string>): Record<string, number | string> {
  const watt = inputs.watt as number;
  const hoursPerDay = inputs.hoursPerDay as number;
  const days = inputs.days as number;
  const pricePerKwh = inputs.pricePerKwh as number;
  const kwhUsed = watt / 1000 * hoursPerDay * days;
  const cost = Math.round(kwhUsed * pricePerKwh);
  return { monthlyCost: cost, kwhUsed: Math.round(kwhUsed * 10) / 10, dailyCost: Math.round(cost / days) };
}

export function ellipse(inputs: Record<string, number | string>): Record<string, number | string> {
  const a = inputs.a as number;
  const b = inputs.b as number;
  const a = semiMajor as number; const b = semiMinor as number;
  const area = Math.round(Math.PI * a * b * 100) / 100;
  const perimeter = Math.round(Math.PI * (3*(a+b) - Math.sqrt((3*a+b)*(a+3*b))) * 100) / 100;
  return { area, perimeter };
}

export function emailMarketing(inputs: Record<string, number | string>): Record<string, number | string> {
  const subscribers = inputs.subscribers as number;
  const openRate = inputs.openRate as number;
  const clickRate = inputs.clickRate as number;
  const cvr = inputs.cvr as number;
  const avgOrderValue = inputs.avgOrderValue as number;
  const opens = Math.round(sent * openRate / 100);
  const clicks = Math.round(opens * clickRate / 100);
  return { opens, clicks, conversionEstimate: Math.round(clicks * 0.02) };
}

export function emergencyFund(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlyExpense = inputs.monthlyExpense as number;
  const employmentType = inputs.employmentType as string;
  const monthly = monthlyExpenses * 10000;
  const fund3 = monthly * 3;
  const fund6 = monthly * 6;
  const fund12 = monthly * 12;
  return { fund3, fund6, fund12 };
}

export function energyConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const fromUnit = inputs.fromUnit as string;
  const cal = value as number;
  return { kcal: cal, kJ: Math.round(cal * 4.184 * 100) / 100, wh: Math.round(cal * 1.163 * 100) / 100 };
}

export function englishScore(inputs: Record<string, number | string>): Record<string, number | string> {
  const toeicScore = inputs.toeicScore as number;
  const toeic = score as number;
  const ielts = Math.round((toeic / 990 * 9) * 10) / 10;
  const toefl = Math.round(toeic / 990 * 120);
  return { toeic, ielts: Math.min(ielts, 9), toefl: Math.min(toefl, 120) };
}

export function etfCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const investAmount = inputs.investAmount as number;
  const expenseRatio = inputs.expenseRatio as number;
  const years = inputs.years as number;
  const annualReturn = inputs.annualReturn as number;
  const investment10k = investment * 10000;
  const annualCost = Math.round(investment10k * expenseRatio / 100);
  const cost10yr = annualCost * 10;
  return { annualCost, cost10yr, dailyCost: Math.round(annualCost / 365) };
}

export function evCostComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const annualMileage = inputs.annualMileage as number;
  const evEfficiency = inputs.evEfficiency as number;
  const electricityPrice = inputs.electricityPrice as number;
  const gasEfficiency = inputs.gasEfficiency as number;
  const gasPrice = inputs.gasPrice as number;
  const evAnnual = Math.round(annualKm / evEfficiency * electricityRate);
  const gasAnnual = Math.round(annualKm / gasFuelEfficiency * gasPrice);
  return { evAnnual, gasAnnual, savings: gasAnnual - evAnnual };
}

export function exerciseCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const minutes = inputs.minutes as number;
  const exercise = inputs.exercise as string;
  const metsMap: Record<string, number> = { jogging: 7, cycling: 6, swimming: 8, yoga: 3, tennis: 7, dancing: 5 };
  const m = metsMap[exercise] || 5;
  const cal = Math.round(m * weight * (minutes / 60) * 1.05);
  return { calories: cal, fatBurn: Math.round(cal / 7.2 * 10) / 10 };
}

export function fabricCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = inputs.width as number;
  const height = inputs.height as number;
  const fabricWidth = inputs.fabricWidth as number;
  const seam = inputs.seam as number;
  const totalArea = width * length / 10000;
  const fabricWidth = fabricWidthCm / 100;
  const fabricLength = Math.ceil(totalArea / fabricWidth * 100) / 100;
  return { fabricLength: Math.round(fabricLength * 100) / 100, totalArea: Math.round(totalArea * 100) / 100 };
}

export function fireInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const buildingType = inputs.buildingType as string;
  const area = inputs.area as number;
  const coverage = inputs.coverage as number;
  const base = buildingValue * 10000;
  const rateMap: Record<string, number> = { wooden: 0.001, fireproof: 0.0005 };
  const r = rateMap[structure] || 0.001;
  const annual = Math.round(base * r);
  return { annual, fiveYear: annual * 5, tenYear: annual * 10 };
}

export function fractionCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const num1 = inputs.num1 as number;
  const den1 = inputs.den1 as number;
  const operator = inputs.operator as string;
  const num2 = inputs.num2 as number;
  const den2 = inputs.den2 as number;
  function gcd(a: number, b: number): number { return b === 0 ? a : gcd(b, a % b); }
  let rn: number, rd: number;
  if (operator === 'add') { rn = num1*den2 + num2*den1; rd = den1*den2; }
  else if (operator === 'sub') { rn = num1*den2 - num2*den1; rd = den1*den2; }
  else if (operator === 'mul') { rn = num1*num2; rd = den1*den2; }
  else { rn = num1*den2; rd = den1*num2; }
  const g = gcd(Math.abs(rn), Math.abs(rd));
  return { resultNum: rn/g, resultDen: rd/g, decimal: Math.round(rn/rd * 10000) / 10000 };
}

export function freelanceRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const targetIncome = inputs.targetIncome as number;
  const workDays = inputs.workDays as number;
  const workHours = inputs.workHours as number;
  const expenseRate = inputs.expenseRate as number;
  const annual10k = targetIncome * 10000;
  const totalCost = annual10k + expenses * 10000 + annual10k * 0.3;
  const hourly = Math.round(totalCost / (workHoursPerMonth * 12));
  return { hourlyRate: hourly, dailyRate: hourly * 8, monthlyRate: hourly * workHoursPerMonth };
}

export function gardenSoil(inputs: Record<string, number | string>): Record<string, number | string> {
  const area = inputs.area as number;
  const depth = inputs.depth as number;
  const pricePerBag = inputs.pricePerBag as number;
  const bagVolume = inputs.bagVolume as number;
  const volume = width * depth * soilDepth / 100;
  const bags = Math.ceil(volume / 14);
  return { volume: Math.round(volume * 100) / 100, bags };
}

export function goldInvestment(inputs: Record<string, number | string>): Record<string, number | string> {
  const purchasePrice = inputs.purchasePrice as number;
  const currentPrice = inputs.currentPrice as number;
  const grams = inputs.grams as number;
  const totalCost = Math.round(goldPrice * weight);
  return { totalCost, perGram: goldPrice, weight };
}

export function gpaCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const subjects = inputs.subjects as number;
  const s1 = inputs.s1 as number;
  const s2 = inputs.s2 as number;
  const s3 = inputs.s3 as number;
  const s4 = inputs.s4 as number;
  const s5 = inputs.s5 as number;
  const c1 = inputs.c1 as number;
  const c2 = inputs.c2 as number;
  const c3 = inputs.c3 as number;
  const c4 = inputs.c4 as number;
  const c5 = inputs.c5 as number;
  const scores = [s1, s2, s3, s4, s5];
  const credits = [c1, c2, c3, c4, c5];
  const count = subjects as number;
  let totalPoints = 0; let totalCredits = 0;
  for (let i = 0; i < count; i++) { totalPoints += (scores[i] as number) * (credits[i] as number); totalCredits += credits[i] as number; }
  return { gpa: totalCredits > 0 ? Math.round(totalPoints / totalCredits * 100) / 100 : 0, totalCredits, totalPoints };
}

export function gradeCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const subject1 = inputs.subject1 as number;
  const subject2 = inputs.subject2 as number;
  const subject3 = inputs.subject3 as number;
  const subject4 = inputs.subject4 as number;
  const subject5 = inputs.subject5 as number;
  const total = score1 + score2 + score3;
  const avg = Math.round(total / 3 * 10) / 10;
  const grade = avg >= 90 ? 'A' : avg >= 80 ? 'B' : avg >= 70 ? 'C' : avg >= 60 ? 'D' : 'F';
  return { average: avg, grade, total } as any;
}

export function grossMargin(inputs: Record<string, number | string>): Record<string, number | string> {
  const revenue = inputs.revenue as number;
  const cogs = inputs.cogs as number;
  const revenue10k = revenue * 10000;
  const cogs10k = cogs * 10000;
  const grossProfit = revenue10k - cogs10k;
  const margin = revenue10k > 0 ? Math.round(grossProfit / revenue10k * 10000) / 100 : 0;
  return { grossProfit, margin };
}

export function hearingLevel(inputs: Record<string, number | string>): Record<string, number | string> {
  const decibel = inputs.decibel as number;
  const avg = Math.round((freq500 + freq1000 + freq2000 + freq4000) / 4);
  const level = avg < 25 ? '正常' : avg < 40 ? '軽度難聴' : avg < 70 ? '中等度難聴' : '高度難聴';
  return { average: avg, level } as any;
}

export function hensachi(inputs: Record<string, number | string>): Record<string, number | string> {
  const score = inputs.score as number;
  const average = inputs.average as number;
  const sd = inputs.sd as number;
  const dev = stdDeviation > 0 ? Math.round((score - average) / stdDeviation * 10 + 50) : 50;
  return { hensachi: dev };
}

export function hexagon(inputs: Record<string, number | string>): Record<string, number | string> {
  const side = inputs.side as number;
  const s = sideLength as number;
  return { area: Math.round(3 * Math.sqrt(3) / 2 * s * s * 100) / 100, perimeter: Math.round(6 * s * 100) / 100 };
}

export function housingDeduction(inputs: Record<string, number | string>): Record<string, number | string> {
  const loanBalance = inputs.loanBalance as number;
  const houseType = inputs.houseType as string;
  const moveInYear = inputs.moveInYear as number;
  const loanBalance10k = loanBalance * 10000;
  const deduction = Math.min(Math.round(loanBalance10k * 0.007), 210000);
  const total13yr = deduction * 13;
  return { annualDeduction: deduction, total13yr };
}

export function individualEnterpriseTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = inputs.income as number;
  const industry = inputs.industry as string;
  const income10k = income * 10000;
  const deduction = 2900000;
  const taxable = Math.max(income10k - deduction, 0);
  const tax = Math.round(taxable * 0.05);
  return { tax, taxable, deduction };
}

export function inflationCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = inputs.amount as number;
  const inflationRate = inputs.inflationRate as number;
  const years = inputs.years as number;
  const r = inflationRate / 100;
  const futureNominal = Math.round(amount * 10000 * Math.pow(1 + r, years));
  const realValue = Math.round(amount * 10000 / Math.pow(1 + r, years));
  const loss = Math.round((1 - 1 / Math.pow(1 + r, years)) * 100);
  return { futureNominal, realValue, purchasingPowerLoss: loss };
}

export function inheritanceTaxSimulation(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalAssets = inputs.totalAssets as number;
  const heirs = inputs.heirs as number;
  const spouse = inputs.spouse as string;
  const assets10k = assets * 10000;
  const basicDeduction = 30000000 + 6000000 * heirs;
  const taxable = Math.max(assets10k - basicDeduction, 0);
  let rate = 0.10; let ded = 0;
  if (taxable > 600000000) { rate = 0.55; ded = 72000000; }
  else if (taxable > 300000000) { rate = 0.50; ded = 42000000; }
  else if (taxable > 200000000) { rate = 0.45; ded = 27000000; }
  else if (taxable > 100000000) { rate = 0.40; ded = 17000000; }
  else if (taxable > 50000000) { rate = 0.30; ded = 7000000; }
  else if (taxable > 30000000) { rate = 0.20; ded = 2000000; }
  else if (taxable > 10000000) { rate = 0.15; ded = 500000; }
  const tax = Math.round(taxable * rate - ded);
  return { tax: Math.max(tax, 0), basicDeduction, taxable };
}

export function initialCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const rent = inputs.rent as number;
  const deposit = inputs.deposit as number;
  const keyMoney = inputs.keyMoney as number;
  const agentFee = inputs.agentFee as number;
  const price10k = price * 10000;
  const agentFee = Math.round(price10k * 0.03 + 60000) * 1.1;
  const regTax = Math.round(price10k * 0.02);
  const acqTax = Math.round(price10k * 0.03);
  const total = Math.round(agentFee + regTax + acqTax);
  return { agentFee: Math.round(agentFee), registrationTax: regTax, acquisitionTax: acqTax, total };
}

export function investmentReturn(inputs: Record<string, number | string>): Record<string, number | string> {
  const initialAmount = inputs.initialAmount as number;
  const monthlyAmount = inputs.monthlyAmount as number;
  const annualReturn = inputs.annualReturn as number;
  const years = inputs.years as number;
  const initial10k = initialAmount * 10000;
  const final10k = finalAmount * 10000;
  const profit = final10k - initial10k;
  const returnRate = Math.round(profit / initial10k * 10000) / 100;
  const annualReturn = Math.round((Math.pow(final10k / initial10k, 1 / years) - 1) * 10000) / 100;
  return { profit, returnRate, annualReturn };
}

export function japaneseEra(inputs: Record<string, number | string>): Record<string, number | string> {
  const year = inputs.year as number;
  const y = year as number;
  let era = ''; let eraYear = 0;
  if (y >= 2019) { era = '令和'; eraYear = y - 2018; }
  else if (y >= 1989) { era = '平成'; eraYear = y - 1988; }
  else if (y >= 1926) { era = '昭和'; eraYear = y - 1925; }
  else if (y >= 1912) { era = '大正'; eraYear = y - 1911; }
  else { era = '明治'; eraYear = y - 1867; }
  return { era, eraYear, fullText: `${era}${eraYear}年` } as any;
}

export function joggingPace(inputs: Record<string, number | string>): Record<string, number | string> {
  const distance = inputs.distance as number;
  const minutes = inputs.minutes as number;
  const pace = Math.round(minutes / distance * 100) / 100;
  const speedKmh = Math.round(distance / (minutes / 60) * 10) / 10;
  const cal = Math.round(7 * 65 * (minutes / 60) * 1.05);
  return { pace, speed: speedKmh, calories: cal };
}

export function laborCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = inputs.monthlySalary as number;
  const bonusMonths = inputs.bonusMonths as number;
  const salary10k = salary * 10000;
  const socialIns = Math.round(salary10k * 0.15);
  const totalCost = salary10k + socialIns;
  const laborCostRatio = revenue > 0 ? Math.round(totalCost / (revenue * 10000) * 100) : 0;
  return { totalCost, socialInsurance: socialIns, laborCostRatio };
}

export function landPrice(inputs: Record<string, number | string>): Record<string, number | string> {
  const pricePerTsubo = inputs.pricePerTsubo as number;
  const areaTsubo = inputs.areaTsubo as number;
  const pricePerSqm10k = pricePerSqm * 10000;
  const totalPrice = Math.round(pricePerSqm10k * area);
  const tsubo = Math.round(area / 3.30579 * 100) / 100;
  const pricePerTsubo = Math.round(totalPrice / tsubo);
  return { totalPrice, tsubo, pricePerTsubo };
}

export function logarithm(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const base = inputs.base as number;
  const val = value as number;
  const b = base as number;
  const result = Math.log(val) / Math.log(b);
  return { result: Math.round(result * 10000) / 10000, ln: Math.round(Math.log(val) * 10000) / 10000, log10: Math.round(Math.log10(val) * 10000) / 10000 };
}

export function ltv(inputs: Record<string, number | string>): Record<string, number | string> {
  const avgOrderValue = inputs.avgOrderValue as number;
  const purchaseFrequency = inputs.purchaseFrequency as number;
  const customerLifespan = inputs.customerLifespan as number;
  const grossMarginRate = inputs.grossMarginRate as number;
  const value = avgPurchase * purchaseFrequency * customerLifespan;
  return { ltv: Math.round(value), annualValue: Math.round(avgPurchase * purchaseFrequency) };
}

export function mansionCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const managementFee = inputs.managementFee as number;
  const repairReserve = inputs.repairReserve as number;
  const parkingFee = inputs.parkingFee as number;
  const ownershipYears = inputs.ownershipYears as number;
  const price10k = price * 10000;
  const management10k = management * 10000;
  const repair10k = repair * 10000;
  const monthlyCost = management10k + repair10k;
  const annualCost = monthlyCost * 12;
  return { monthlyCost, annualCost, totalCost30yr: annualCost * 30 + price10k };
}

export function marginTrading(inputs: Record<string, number | string>): Record<string, number | string> {
  const stockPrice = inputs.stockPrice as number;
  const shares = inputs.shares as number;
  const marginRate = inputs.marginRate as number;
  const priceChange = inputs.priceChange as number;
  const deposit10k = deposit * 10000;
  const totalPosition = Math.round(deposit10k * leverage);
  const profitLoss = Math.round(totalPosition * priceChange / 100);
  return { totalPosition, profitLoss, returnOnDeposit: Math.round(profitLoss / deposit10k * 100) };
}

export function maternityBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = inputs.monthlySalary as number;
  const dailyWage = Math.round(monthlySalary * 10000 / 30);
  const benefit = Math.round(dailyWage * 2 / 3);
  const totalDays = 98;
  const totalBenefit = benefit * totalDays;
  return { dailyBenefit: benefit, totalBenefit, totalDays };
}

export function matrix(inputs: Record<string, number | string>): Record<string, number | string> {
  const a11 = inputs.a11 as number;
  const a12 = inputs.a12 as number;
  const a21 = inputs.a21 as number;
  const a22 = inputs.a22 as number;
  const det = a11 * a22 - a12 * a21;
  return { determinant: det, trace: a11 + a22 };
}

export function mealCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const rice = inputs.rice as number;
  const meat = inputs.meat as number;
  const fish = inputs.fish as number;
  const vegetables = inputs.vegetables as number;
  const oil = inputs.oil as number;
  const total = rice + mainDish + sideDish + soup;
  return { total, perMeal: total };
}

export function medianMode(inputs: Record<string, number | string>): Record<string, number | string> {
  const data = inputs.data as number;
  const values = [v1, v2, v3, v4, v5].filter((v): v is number => typeof v === 'number').slice(0, n as number).sort((a, b) => a - b);
  const len = values.length;
  const median = len % 2 === 0 ? (values[len/2-1] + values[len/2]) / 2 : values[Math.floor(len/2)];
  const mean = values.reduce((s, v) => s + v, 0) / len;
  return { median, mean: Math.round(mean * 100) / 100 };
}

export function medicineDose(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const dosePerKg = inputs.dosePerKg as number;
  const timesPerDay = inputs.timesPerDay as number;
  const adultDose = standardDose as number;
  const childDose = Math.round(adultDose * childWeight / 50 * 10) / 10;
  return { childDose, ratio: Math.round(childWeight / 50 * 100) };
}

export function meetingCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const participants = inputs.participants as number;
  const avgHourlyRate = inputs.avgHourlyRate as number;
  const durationMinutes = inputs.durationMinutes as number;
  const hourlyRate = averageSalary * 10000 / 12 / 160;
  const cost = Math.round(hourlyRate * participants * durationMinutes / 60);
  return { cost, perMinute: Math.round(cost / durationMinutes) };
}

export function menstrualCycle(inputs: Record<string, number | string>): Record<string, number | string> {
  const lastPeriod = inputs.lastPeriod as number;
  const cycleLength = inputs.cycleLength as number;
  const periodLength = inputs.periodLength as number;
  const nextPeriod = cycleLength;
  const ovulationDay = cycleLength - 14;
  const fertileStart = ovulationDay - 5;
  return { nextPeriod, ovulationDay, fertileStart: Math.max(fertileStart, 1), fertileEnd: ovulationDay + 1 };
}

export function minimumWage(inputs: Record<string, number | string>): Record<string, number | string> {
  const hourlyWage = inputs.hourlyWage as number;
  const region = inputs.region as string;
  const hourly = minimumWageAmount as number;
  const monthly = Math.round(hourly * hoursPerDay * daysPerMonth);
  const annual = monthly * 12;
  return { monthly, annual, hourly };
}

export function nationalHealthInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = inputs.income as number;
  const members = inputs.members as number;
  const age = inputs.age as number;
  const income10k = income * 10000;
  const taxable = Math.max(income10k - 430000, 0);
  const medical = Math.min(Math.round(taxable * 0.0789 + 22200 * family), 650000);
  const support = Math.min(Math.round(taxable * 0.0266 + 7500 * family), 220000);
  const care = age >= 40 && age < 65 ? Math.min(Math.round(taxable * 0.0222 + 6200 * family), 170000) : 0;
  const total = medical + support + care;
  return { total, monthly: Math.round(total / 12), medical, support, care };
}

export function normalDistribution(inputs: Record<string, number | string>): Record<string, number | string> {
  const mean = inputs.mean as number;
  const stddev = inputs.stddev as number;
  const x = inputs.x as number;
  const z = (x - mean) / stdDev;
  return { zScore: Math.round(z * 10000) / 10000 };
}

export function ovulationDay(inputs: Record<string, number | string>): Record<string, number | string> {
  const lastPeriod = inputs.lastPeriod as number;
  const cycleLength = inputs.cycleLength as number;
  const ovDay = cycleLength - 14;
  const fertileStart = ovDay - 5;
  const fertileEnd = ovDay + 1;
  return { ovulationDay: ovDay, fertileStart: Math.max(fertileStart, 1), fertileEnd };
}

export function packingList(inputs: Record<string, number | string>): Record<string, number | string> {
  const days = inputs.days as number;
  const season = inputs.season as string;
  const laundry = inputs.laundry as string;
  const base = 5;
  const clothingSets = days;
  const totalItems = base + clothingSets + (days > 3 ? 3 : 0);
  return { totalItems, clothingSets, luggageWeight: Math.round(totalItems * 0.3 * 10) / 10 };
}

export function paintArea(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = inputs.width as number;
  const depth = inputs.depth as number;
  const height = inputs.height as number;
  const windows = inputs.windows as number;
  const doors = inputs.doors as number;
  const wallArea = 2 * (width + depth) * height - windows * 1.5 - doors * 1.8;
  const ceilArea = width * depth;
  const total = Math.round((wallArea + ceilArea) * 100) / 100;
  return { wallArea: Math.round(wallArea * 100) / 100, ceilingArea: Math.round(ceilArea * 100) / 100, totalArea: total, paintLiters: Math.round(total / 6 * 10) / 10 };
}

export function paintCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const wallArea = inputs.wallArea as number;
  const coats = inputs.coats as number;
  const coveragePerLiter = inputs.coveragePerLiter as number;
  const canSize = inputs.canSize as number;
  const totalArea = wallArea as number;
  const coats = numberOfCoats as number;
  const liters = Math.ceil(totalArea * coats / 6 * 10) / 10;
  return { liters, cans: Math.ceil(liters / 4) };
}

export function paperSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const size = inputs.size as string;
  const sizes: Record<string, number[]> = { A0:[841,1189], A1:[594,841], A2:[420,594], A3:[297,420], A4:[210,297], A5:[148,210], A6:[105,148], B0:[1000,1414], B1:[707,1000], B2:[500,707], B3:[353,500], B4:[250,353], B5:[176,250] };
  const s = sizes[size] || sizes['A4'];
  return { width: s[0], height: s[1], area: s[0] * s[1] };
}

export function partyFood(inputs: Record<string, number | string>): Record<string, number | string> {
  const guests = inputs.guests as number;
  const duration = inputs.duration as number;
  const style = inputs.style as string;
  const foodPerPerson = 300;
  const drinkPerPerson = 500;
  const totalFood = guests * foodPerPerson * hours / 2;
  const totalDrink = guests * drinkPerPerson * hours / 2;
  return { totalFoodG: Math.round(totalFood), totalDrinkMl: Math.round(totalDrink) };
}

export function paybackPeriod(inputs: Record<string, number | string>): Record<string, number | string> {
  const investment = inputs.investment as number;
  const annualReturn = inputs.annualReturn as number;
  const annualCost = inputs.annualCost as number;
  const invest10k = investment * 10000;
  const annual10k = annualCashflow * 10000;
  const period = annual10k > 0 ? Math.round(invest10k / annual10k * 10) / 10 : 0;
  return { period, monthlyReturn: Math.round(annual10k / 12) };
}

export function perPbr(inputs: Record<string, number | string>): Record<string, number | string> {
  const stockPrice = inputs.stockPrice as number;
  const eps = inputs.eps as number;
  const bps = inputs.bps as number;
  const per = stockPrice / eps;
  const pbr = stockPrice / bps;
  return { per: Math.round(per * 100) / 100, pbr: Math.round(pbr * 100) / 100, earningsYield: Math.round(1/per * 10000) / 100 };
}

export function percentageCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const valueA = inputs.valueA as number;
  const valueB = inputs.valueB as number;
  const calcType = inputs.calcType as string;
  if (calcType === 'of') return { result: Math.round(valueB * valueA / 100 * 100) / 100, explanation: `${valueB}の${valueA}%` } as any;
  if (calcType === 'is') return { result: valueB > 0 ? Math.round(valueA / valueB * 10000) / 100 : 0, explanation: `${valueA}は${valueB}の何%` } as any;
  return { result: valueA > 0 ? Math.round((valueB - valueA) / valueA * 10000) / 100 : 0, explanation: `${valueA}→${valueB}の変化率` } as any;
}

export function personalLoan(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = inputs.amount as number;
  const rate = inputs.rate as number;
  const years = inputs.years as number;
  const amt10k = amount * 10000;
  const r = rate / 100 / 12;
  const months = years * 12;
  const payment = r > 0 ? Math.round(amt10k * r / (1 - Math.pow(1+r, -months))) : Math.round(amt10k / months);
  return { monthlyPayment: payment, totalPayment: payment * months, totalInterest: payment * months - amt10k };
}

export function petAge(inputs: Record<string, number | string>): Record<string, number | string> {
  const petType = inputs.petType as string;
  const age = inputs.age as number;
  const petYears = age as number;
  const isdog = petType === 'dog';
  const humanAge = isdog ? (petYears <= 2 ? petYears * 12 : 24 + (petYears - 2) * 4) : (petYears <= 2 ? petYears * 12.5 : 25 + (petYears - 2) * 4);
  return { humanAge: Math.round(humanAge) };
}

export function petInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const petType = inputs.petType as string;
  const age = inputs.age as number;
  const coverage = inputs.coverage as string;
  const base = petAge < 3 ? 2000 : petAge < 7 ? 3000 : 5000;
  const typeMultiplier = petType === 'dog' ? 1.2 : 1.0;
  const monthly = Math.round(base * typeMultiplier * coverageRate / 100);
  return { monthly, annual: monthly * 12 };
}

export function photoPrint(inputs: Record<string, number | string>): Record<string, number | string> {
  const widthPx = inputs.widthPx as number;
  const heightPx = inputs.heightPx as number;
  const dpi = inputs.dpi as number;
  const dpiNeeded = 300;
  const widthPixels = Math.round(printWidth * 2.54 * dpiNeeded);
  const heightPixels = Math.round(printHeight * 2.54 * dpiNeeded);
  const megapixels = Math.round(widthPixels * heightPixels / 1000000 * 10) / 10;
  return { widthPixels, heightPixels, megapixels };
}

export function pointValue(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = inputs.amount as number;
  const rate = inputs.rate as number;
  const monthlySpend = inputs.monthlySpend as number;
  const pointRate = rate as number;
  const totalPoints = points as number;
  const value = Math.round(totalPoints * pointRate / 100);
  return { value, effectiveDiscount: pointRate };
}

export function polygonArea(inputs: Record<string, number | string>): Record<string, number | string> {
  const sides = inputs.sides as number;
  const sideLength = inputs.sideLength as number;
  const n = sides as number; const s = sideLength as number;
  const area = Math.round(n * s * s / (4 * Math.tan(Math.PI / n)) * 100) / 100;
  return { area, perimeter: Math.round(n * s * 100) / 100 };
}

export function postalRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const type = inputs.type as string;
  const weight = inputs.weight as number;
  const w = weightGram as number;
  let rate: number;
  if (mailType === 'letter') { rate = w <= 25 ? 84 : w <= 50 ? 94 : 140; }
  else if (mailType === 'postcard') { rate = 63; }
  else { rate = w <= 150 ? 180 : w <= 250 ? 215 : w <= 500 ? 310 : w <= 1000 ? 360 : 510; }
  return { rate };
}

export function powerConsumption(inputs: Record<string, number | string>): Record<string, number | string> {
  const watt1 = inputs.watt1 as number;
  const watt2 = inputs.watt2 as number;
  const hoursPerDay = inputs.hoursPerDay as number;
  const pricePerKwh = inputs.pricePerKwh as number;
  const kwh1 = watt1 / 1000 * hoursPerDay * 365;
  const kwh2 = watt2 / 1000 * hoursPerDay * 365;
  const cost1 = Math.round(kwh1 * pricePerKwh);
  const cost2 = Math.round(kwh2 * pricePerKwh);
  return { annualCost1: cost1, annualCost2: cost2, annualSaving: cost1 - cost2, tenYearSaving: (cost1 - cost2) * 10 };
}

export function pressureConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const fromUnit = inputs.fromUnit as string;
  const hpa = value as number;
  return { hPa: hpa, atm: Math.round(hpa / 1013.25 * 10000) / 10000, mmHg: Math.round(hpa * 0.75006 * 100) / 100, psi: Math.round(hpa * 0.014504 * 10000) / 10000 };
}

export function pricingMarkup(inputs: Record<string, number | string>): Record<string, number | string> {
  const cost = inputs.cost as number;
  const price = inputs.price as number;
  const cost10k = cost * 10000;
  const price = Math.round(cost10k * (1 + markupRate / 100));
  const profit = price - cost10k;
  const margin = price > 0 ? Math.round(profit / price * 100) : 0;
  return { price, profit, margin };
}

export function primeFactorization(inputs: Record<string, number | string>): Record<string, number | string> {
  const number = inputs.number as number;
  let n = number as number;
  const factors: number[] = [];
  for (let d = 2; d * d <= n; d++) { while (n % d === 0) { factors.push(d); n /= d; } }
  if (n > 1) factors.push(n);
  return { factors: factors.length, result: factors.join(' × '), isPrime: factors.length <= 1 ? 1 : 0 } as any;
}

export function probability(inputs: Record<string, number | string>): Record<string, number | string> {
  const n = inputs.n as number;
  const r = inputs.r as number;
  const favorable = favorableOutcomes as number;
  const total = totalOutcomes as number;
  const p = total > 0 ? favorable / total : 0;
  return { probability: Math.round(p * 10000) / 10000, percentage: Math.round(p * 10000) / 100, odds: `${favorable}:${total - favorable}` } as any;
}

export function proteinNeed(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const activity = inputs.activity as string;
  const multiplier: Record<string, number> = { sedentary: 0.8, moderate: 1.2, athlete: 1.6, bodybuilder: 2.0 };
  const m = multiplier[activityLevel] || 0.8;
  const daily = Math.round(weight * m);
  return { dailyProtein: daily, perMeal: Math.round(daily / 3) };
}

export function pythagorean(inputs: Record<string, number | string>): Record<string, number | string> {
  const sideA = inputs.sideA as number;
  const sideB = inputs.sideB as number;
  const a = sideA as number; const b = sideB as number;
  const c = Math.sqrt(a*a + b*b);
  return { hypotenuse: Math.round(c * 10000) / 10000, area: Math.round(a * b / 2 * 100) / 100 };
}

export function quadratic(inputs: Record<string, number | string>): Record<string, number | string> {
  const a = inputs.a as number;
  const b = inputs.b as number;
  const c_val = inputs.c_val as number;
  const discriminant = b * b - 4 * a * c;
  if (discriminant < 0) return { discriminant, realRoots: 0 } as any;
  const x1 = Math.round((-b + Math.sqrt(discriminant)) / (2 * a) * 10000) / 10000;
  const x2 = Math.round((-b - Math.sqrt(discriminant)) / (2 * a) * 10000) / 10000;
  return { x1, x2, discriminant, realRoots: discriminant === 0 ? 1 : 2 };
}

export function randomNumber(inputs: Record<string, number | string>): Record<string, number | string> {
  const min = inputs.min as number;
  const max = inputs.max as number;
  const count = inputs.count as number;
  const min = minValue as number;
  const max = maxValue as number;
  const result = Math.floor(Math.random() * (max - min + 1)) + min;
  return { result, min, max };
}

export function realEstateAcquisitionTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const landValue = inputs.landValue as number;
  const buildingValue = inputs.buildingValue as number;
  const isResidential = inputs.isResidential as string;
  const assessment10k = assessment * 10000;
  const landTax = Math.round(assessment10k * 0.5 * 0.03);
  const buildingTax = Math.round(assessment10k * 0.03);
  return { landTax, buildingTax, totalTax: landTax + buildingTax };
}

export function rebalance(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalAsset = inputs.totalAsset as number;
  const currentStock = inputs.currentStock as number;
  const currentBond = inputs.currentBond as number;
  const targetStock = inputs.targetStock as number;
  const targetBond = inputs.targetBond as number;
  const total = stocksCurrent + bondsCurrent + cashCurrent;
  if (total === 0) return { stocksAdj: 0, bondsAdj: 0, cashAdj: 0 };
  const stocksTarget = Math.round(total * stocksTargetPct / 100);
  const bondsTarget = Math.round(total * bondsTargetPct / 100);
  const cashTarget = total - stocksTarget - bondsTarget;
  return { stocksAdj: stocksTarget - stocksCurrent, bondsAdj: bondsTarget - bondsCurrent, cashAdj: cashTarget - cashCurrent };
}

export function recipeScale(inputs: Record<string, number | string>): Record<string, number | string> {
  const originalServings = inputs.originalServings as number;
  const newServings = inputs.newServings as number;
  const ingredientAmount = inputs.ingredientAmount as number;
  const ratio = targetServings / originalServings;
  return { ratio: Math.round(ratio * 100) / 100, scaledAmount: Math.round(ingredientAmount * ratio * 10) / 10 };
}

export function refinance(inputs: Record<string, number | string>): Record<string, number | string> {
  const remainingBalance = inputs.remainingBalance as number;
  const currentRate = inputs.currentRate as number;
  const newRate = inputs.newRate as number;
  const remainingYears = inputs.remainingYears as number;
  const refinanceCost = inputs.refinanceCost as number;
  const bal10k = balance * 10000;
  const oldRate = currentRate / 100 / 12;
  const newRate = newInterestRate / 100 / 12;
  const months = remainingYears * 12;
  const oldPayment = oldRate > 0 ? Math.round(bal10k * oldRate / (1 - Math.pow(1+oldRate, -months))) : Math.round(bal10k / months);
  const newPayment = newRate > 0 ? Math.round(bal10k * newRate / (1 - Math.pow(1+newRate, -months))) : Math.round(bal10k / months);
  const savings = (oldPayment - newPayment) * months;
  return { oldPayment, newPayment, monthlySavings: oldPayment - newPayment, totalSavings: savings };
}

export function registrationTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const propertyValue = inputs.propertyValue as number;
  const regType = inputs.regType as string;
  const loanAmount = inputs.loanAmount as number;
  const value10k = value * 10000;
  const rateMap: Record<string, number> = { ownership: 0.02, mortgage: 0.004, transfer: 0.02 };
  const rate = rateMap[type] || 0.02;
  const tax = Math.round(value10k * rate);
  return { tax, rate: rate * 100 };
}

export function reitYield(inputs: Record<string, number | string>): Record<string, number | string> {
  const price = inputs.price as number;
  const annualDistribution = inputs.annualDistribution as number;
  const units = inputs.units as number;
  const annualDiv = dividend * 12;
  const yld = price > 0 ? Math.round(annualDiv / price * 10000) / 100 : 0;
  return { annualDividend: annualDiv, yield: yld, afterTax: Math.round(annualDiv * 0.79685) };
}

export function rentCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = inputs.income as number;
  const familySize = inputs.familySize as number;
  const rent10k = rent * 10000;
  const annualRent = rent10k * 12;
  const deposit10k = deposit * rent10k;
  const key10k = keyMoney * rent10k;
  const initialCost = deposit10k + key10k + rent10k;
  return { annualRent, initialCost, monthlyCost: rent10k };
}

export function roomBrightness(inputs: Record<string, number | string>): Record<string, number | string> {
  const area = inputs.area as number;
  const roomType = inputs.roomType as string;
  const lumensPerJo: Record<string, number> = { living: 400, bedroom: 200, study: 500, kitchen: 300 };
  const lm = (lumensPerJo[roomType] || 400) * area;
  return { lumens: lm, ledWatt: Math.round(lm / 100), fixtures: Math.ceil(area / 8) };
}

export function rule72(inputs: Record<string, number | string>): Record<string, number | string> {
  const rate = inputs.rate as number;
  const years = Math.round(72 / rate * 10) / 10;
  const actualYears = Math.round(Math.log(2) / Math.log(1 + rate / 100) * 10) / 10;
  return { years, actualYears, rate };
}

export function runningPace(inputs: Record<string, number | string>): Record<string, number | string> {
  const distance = inputs.distance as number;
  const hours = inputs.hours as number;
  const minutes = inputs.minutes as number;
  const paceMin = Math.round(time / distance * 100) / 100;
  const speed = Math.round(distance / (time / 60) * 10) / 10;
  return { pace: paceMin, speed, estimatedMarathon: Math.round(paceMin * 42.195) };
}

export function salaryAfterTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const income = inputs.income as number;
  const dependents = inputs.dependents as number;
  const inc = income * 10000;
  const si = Math.round(inc * 0.15);
  const employmentDed = inc <= 1625000 ? 550000 : inc <= 1800000 ? Math.round(inc * 0.4 - 100000) : inc <= 3600000 ? Math.round(inc * 0.3 + 80000) : inc <= 6600000 ? Math.round(inc * 0.2 + 440000) : Math.round(inc * 0.1 + 1100000);
  const taxableInc = Math.max(inc - employmentDed - si - 480000 - dependents * 380000, 0);
  let taxRate = 0.05; let ded = 0;
  if (taxableInc > 40000000) { taxRate = 0.45; ded = 4796000; }
  else if (taxableInc > 18000000) { taxRate = 0.40; ded = 2796000; }
  else if (taxableInc > 9000000) { taxRate = 0.33; ded = 1536000; }
  else if (taxableInc > 6950000) { taxRate = 0.23; ded = 636000; }
  else if (taxableInc > 3300000) { taxRate = 0.20; ded = 427500; }
  else if (taxableInc > 1950000) { taxRate = 0.10; ded = 97500; }
  const incomeTax = Math.round(taxableInc * taxRate - ded);
  const residentTax = Math.round(taxableInc * 0.10);
  const totalTax = incomeTax + residentTax;
  const takeHome = inc - si - totalTax;
  return { takeHome, monthlyTakeHome: Math.round(takeHome / 12), totalTax, socialInsurance: si, ratio: Math.round(takeHome / inc * 100) };
}

export function salaryComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const monthlySalary = inputs.monthlySalary as number;
  const bonusMonths = inputs.bonusMonths as number;
  const salaryA10k = salaryA * 10000;
  const salaryB10k = salaryB * 10000;
  const diff = salaryA10k - salaryB10k;
  const ratio = salaryB10k > 0 ? Math.round(salaryA10k / salaryB10k * 100) : 0;
  return { diff, ratio, monthlyDiff: Math.round(diff / 12) };
}

export function scholarship(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalBorrowed = inputs.totalBorrowed as number;
  const rate = inputs.rate as number;
  const years = inputs.years as number;
  const total = monthlyAmount * 10000 * 12 * years;
  return { total, monthly: monthlyAmount * 10000, annual: monthlyAmount * 10000 * 12 };
}

export function schoolCommute(inputs: Record<string, number | string>): Record<string, number | string> {
  const distance = inputs.distance as number;
  const method = inputs.method as string;
  const monthlyCost = inputs.monthlyCost as number;
  const monthlyPass = monthlyCost as number;
  const annual = monthlyPass * 12;
  const fourYears = annual * 4;
  return { annual, fourYears, daily: Math.round(monthlyPass / 20) };
}

export function schoolSupplies(inputs: Record<string, number | string>): Record<string, number | string> {
  const schoolType = inputs.schoolType as string;
  const total = notebooks * 200 + pens * 150 + textbooks * 1500;
  return { total, perItem: Math.round(total / (notebooks + pens + textbooks)) };
}

export function screenSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const inches = inputs.inches as number;
  const ratio = inputs.ratio as string;
  const diagonal = diagonalInch as number;
  const ratio = aspectRatio === '16:9' ? 16/9 : aspectRatio === '16:10' ? 16/10 : aspectRatio === '4:3' ? 4/3 : 16/9;
  const widthInch = diagonal / Math.sqrt(1 + 1/(ratio*ratio));
  const heightInch = widthInch / ratio;
  return { widthCm: Math.round(widthInch * 2.54 * 10) / 10, heightCm: Math.round(heightInch * 2.54 * 10) / 10, areaSqCm: Math.round(widthInch * heightInch * 2.54 * 2.54) };
}

export function severanceTax(inputs: Record<string, number | string>): Record<string, number | string> {
  const severance = inputs.severance as number;
  const years = inputs.years as number;
  const severance10k = severance * 10000;
  const deduction = yearsWorked <= 20 ? yearsWorked * 400000 : 8000000 + (yearsWorked - 20) * 700000;
  const taxable = Math.max(Math.round((severance10k - deduction) / 2), 0);
  let rate: number; let ded = 0;
  if (taxable <= 1950000) rate = 0.05;
  else if (taxable <= 3300000) { rate = 0.10; ded = 97500; }
  else if (taxable <= 6950000) { rate = 0.20; ded = 427500; }
  else { rate = 0.23; ded = 636000; }
  const incomeTax = Math.round(taxable * rate - ded);
  const residentTax = Math.round(taxable * 0.10);
  return { incomeTax: Math.max(incomeTax, 0), residentTax, deduction, taxable, afterTax: severance10k - Math.max(incomeTax, 0) - residentTax };
}

export function shoeSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const jpSize = inputs.jpSize as number;
  const gender = inputs.gender as string;
  const footLength = footLengthCm as number;
  const jp = Math.round(footLength * 2) / 2;
  const us = Math.round((footLength - 18) / 0.667 * 10) / 10;
  const eu = Math.round((footLength + 1.5) * 1.5 * 10) / 10;
  return { jp, us: Math.max(us, 1), eu };
}

export function sleepCycle(inputs: Record<string, number | string>): Record<string, number | string> {
  const wakeUpHour = inputs.wakeUpHour as number;
  const wakeUpMinute = inputs.wakeUpMinute as number;
  const cycles = [4, 5, 6];
  const results: Record<string, number> = {};
  for (const c of cycles) { results[`bedtime${c}`] = c * 90 + 15; }
  return results;
}

export function squareRoot(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const num = number as number;
  return { result: Math.round(Math.sqrt(num) * 10000) / 10000, squared: num, isInteger: Number.isInteger(Math.sqrt(num)) ? 1 : 0 };
}

export function stampDuty(inputs: Record<string, number | string>): Record<string, number | string> {
  const amount = inputs.amount as number;
  const docType = inputs.docType as string;
  const amount10k = amount * 10000;
  let stampDuty: number;
  if (amount10k <= 10000) stampDuty = 200;
  else if (amount10k <= 1000000) stampDuty = 400;
  else if (amount10k <= 2000000) stampDuty = 600;
  else if (amount10k <= 3000000) stampDuty = 1000;
  else if (amount10k <= 5000000) stampDuty = 2000;
  else if (amount10k <= 10000000) stampDuty = 10000;
  else if (amount10k <= 50000000) stampDuty = 20000;
  else if (amount10k <= 100000000) stampDuty = 60000;
  else stampDuty = 100000;
  return { stampDuty, contractAmount: amount10k };
}

export function stretchTimer(inputs: Record<string, number | string>): Record<string, number | string> {
  const deskHours = inputs.deskHours as number;
  const mins = Math.round(deskHours * 3);
  return { stretchMinutes: mins, exercises: Math.round(mins / 3), breakInterval: 60 };
}

export function studyPlan(inputs: Record<string, number | string>): Record<string, number | string> {
  const totalHours = inputs.totalHours as number;
  const daysUntilExam = inputs.daysUntilExam as number;
  const availableDays = inputs.availableDays as number;
  const totalHours = targetHours as number;
  const daysAvail = daysAvailable as number;
  const dailyHours = Math.round(totalHours / daysAvail * 10) / 10;
  return { dailyHours, weeklyHours: Math.round(dailyHours * 7 * 10) / 10 };
}

export function subscriptionCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const sub1 = inputs.sub1 as number;
  const sub2 = inputs.sub2 as number;
  const sub3 = inputs.sub3 as number;
  const sub4 = inputs.sub4 as number;
  const sub5 = inputs.sub5 as number;
  const total = sub1 + sub2 + sub3 + sub4 + sub5;
  return { monthlyTotal: total, annualTotal: total * 12, dailyCost: Math.round(total / 30) };
}

export function swimmingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const minutes = inputs.minutes as number;
  const stroke = inputs.stroke as string;
  const metsMap: Record<string, number> = { crawl: 8, breaststroke: 6, backstroke: 5, butterfly: 10, water_walk: 4 };
  const m = metsMap[stroke] || 6;
  const cal = Math.round(m * weight * (minutes / 60) * 1.05);
  return { calories: cal, fatBurn: Math.round(cal / 7.2 * 10) / 10 };
}

export function targetHeartRate(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = inputs.age as number;
  const restingHR = inputs.restingHR as number;
  const maxHR = 220 - age;
  const lower = Math.round(maxHR * 0.6);
  const upper = Math.round(maxHR * 0.8);
  const fatBurn = Math.round(maxHR * 0.65);
  return { maxHR, lower, upper, fatBurn };
}

export function tileCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const areaWidth = inputs.areaWidth as number;
  const areaDepth = inputs.areaDepth as number;
  const tileSize = inputs.tileSize as number;
  const lossRate = inputs.lossRate as number;
  const area = areaWidth * areaDepth;
  const tileArea = (tileSize / 100) * (tileSize / 100);
  const tilesRaw = area / tileArea;
  const tiles = Math.ceil(tilesRaw * (1 + lossRate / 100));
  return { tilesNeeded: tiles, area: Math.round(area * 100) / 100, boxes: Math.ceil(tiles / 10) };
}

export function timeConvert(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const fromUnit = inputs.fromUnit as string;
  const totalSeconds = hours * 3600 + minutes * 60 + seconds;
  return { totalSeconds, totalMinutes: Math.round(totalSeconds / 60 * 100) / 100, totalHours: Math.round(totalSeconds / 3600 * 1000) / 1000, days: Math.round(totalSeconds / 86400 * 1000) / 1000 };
}

export function timeZone(inputs: Record<string, number | string>): Record<string, number | string> {
  const fromOffset = inputs.fromOffset as number;
  const toOffset = inputs.toOffset as number;
  const hour = inputs.hour as number;
  const diff = toOffset - fromOffset;
  let h = hour + diff;
  let dayShift = 0;
  if (h >= 24) { h -= 24; dayShift = 1; } else if (h < 0) { h += 24; dayShift = -1; }
  return { convertedHour: h, dayShift, timeDiff: diff } as any;
}

export function tipCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const billAmount = inputs.billAmount as number;
  const tipRate = inputs.tipRate as number;
  const people = inputs.people as number;
  const tip = Math.round(billAmount * tipRate / 100);
  const total = billAmount + tip;
  const perPerson = people > 0 ? Math.round(total / people) : total;
  return { tip, total, perPerson };
}

export function trapezoid(inputs: Record<string, number | string>): Record<string, number | string> {
  const topBase = inputs.topBase as number;
  const bottomBase = inputs.bottomBase as number;
  const height = inputs.height as number;
  const a = topBase as number; const b = bottomBase as number; const h = trapHeight as number;
  return { area: Math.round((a + b) * h / 2 * 100) / 100, perimeter: Math.round((a + b + 2 * Math.sqrt(Math.pow((b-a)/2, 2) + h*h)) * 100) / 100 };
}

export function travelInsurance(inputs: Record<string, number | string>): Record<string, number | string> {
  const destination = inputs.destination as string;
  const days = inputs.days as number;
  const plan = inputs.plan as string;
  const base = days <= 3 ? 500 : days <= 7 ? 1000 : days <= 14 ? 2000 : 3000;
  const regionMultiplier = destination === 'asia' ? 1.0 : destination === 'europe' ? 1.5 : destination === 'americas' ? 1.5 : 1.2;
  const premium = Math.round(base * regionMultiplier * people);
  return { premium, perPerson: Math.round(premium / people) };
}

export function trigonometry(inputs: Record<string, number | string>): Record<string, number | string> {
  const angle = inputs.angle as number;
  const rad = angle * Math.PI / 180;
  return { sin: Math.round(Math.sin(rad) * 10000) / 10000, cos: Math.round(Math.cos(rad) * 10000) / 10000, tan: Math.round(Math.tan(rad) * 10000) / 10000 };
}

export function tsuboM2(inputs: Record<string, number | string>): Record<string, number | string> {
  const value = inputs.value as number;
  const fromUnit = inputs.fromUnit as string;
  const sqm = tsubo * 3.30579;
  return { sqm: Math.round(sqm * 100) / 100, tsubo, jo: Math.round(tsubo * 2 * 100) / 100 };
}

export function typingSpeed(inputs: Record<string, number | string>): Record<string, number | string> {
  const characters = inputs.characters as number;
  const minutes = inputs.minutes as number;
  const wpm = Math.round(characters / minutes * 60 / 5);
  const cpm = Math.round(characters / minutes);
  return { wpm, cpm };
}

export function unemploymentBenefit(inputs: Record<string, number | string>): Record<string, number | string> {
  const age = inputs.age as number;
  const monthlySalary = inputs.monthlySalary as number;
  const yearsWorked = inputs.yearsWorked as number;
  const reason = inputs.reason as string;
  const dailyWage = Math.round(monthlySalary * 10000 / 30);
  const rate = dailyWage < 5110 ? 0.8 : dailyWage < 12580 ? 0.65 : 0.5;
  const dailyBenefit = Math.round(dailyWage * rate);
  const totalDays = yearsWorked < 5 ? 90 : yearsWorked < 10 ? 120 : 150;
  return { dailyBenefit, totalDays, totalBenefit: dailyBenefit * totalDays };
}

export function unitPrice(inputs: Record<string, number | string>): Record<string, number | string> {
  const price1 = inputs.price1 as number;
  const amount1 = inputs.amount1 as number;
  const price2 = inputs.price2 as number;
  const amount2 = inputs.amount2 as number;
  const upA = price1 / amount1 * 100;
  const upB = price2 / amount2 * 100;
  const verdict = upA < upB ? '商品Aがお得' : upA > upB ? '商品Bがお得' : '同じ';
  return { unitPriceA: Math.round(upA * 10) / 10, unitPriceB: Math.round(upB * 10) / 10, savings: Math.round(Math.abs(upA - upB) * 10) / 10, verdict } as any;
}

export function visionTest(inputs: Record<string, number | string>): Record<string, number | string> {
  const decimalVision = inputs.decimalVision as number;
  const corrected = uncorrectedVision * correctionFactor;
  return { corrected: Math.round(corrected * 10) / 10, diopter: Math.round(-1 / corrected * 100) / 100 };
}

export function vocabSize(inputs: Record<string, number | string>): Record<string, number | string> {
  const words = inputs.words as number;
  const est = knownWords * totalWords / sampleSize;
  return { estimatedVocab: Math.round(est), knownRate: Math.round(knownWords / sampleSize * 100) };
}

export function waistHipRatio(inputs: Record<string, number | string>): Record<string, number | string> {
  const waist = inputs.waist as number;
  const hip = inputs.hip as number;
  const gender = inputs.gender as string;
  const ratio = Math.round(waist / hip * 100) / 100;
  const risk = typeof gender === 'string' ? ((gender === 'male' && ratio > 0.9) || (gender === 'female' && ratio > 0.85) ? 'リスクあり' : '正常') : (ratio > 0.9 ? 'リスクあり' : '正常');
  return { ratio, risk } as any;
}

export function walkingCalorie(inputs: Record<string, number | string>): Record<string, number | string> {
  const weight = inputs.weight as number;
  const minutes = inputs.minutes as number;
  const speed = inputs.speed as string;
  const mets: Record<string, number> = { slow: 2.5, normal: 3.5, fast: 5.0 };
  const m = mets[speed] || 3.5;
  const cal = Math.round(m * weight * (minutes / 60) * 1.05);
  const speedKm: Record<string, number> = { slow: 3, normal: 4, fast: 6 };
  const dist = Math.round((speedKm[speed] || 4) * minutes / 60 * 100) / 100;
  const steps = Math.round(dist * 1000 / 0.7);
  return { calories: cal, distance: dist, steps };
}

export function wallpaperCalculator(inputs: Record<string, number | string>): Record<string, number | string> {
  const width = inputs.width as number;
  const depth = inputs.depth as number;
  const height = inputs.height as number;
  const rollWidth = inputs.rollWidth as number;
  const perimeter = 2 * (width + depth);
  const wallArea = perimeter * height;
  const rollW = rollWidth / 100;
  const strips = Math.ceil(perimeter / rollW);
  const totalLength = Math.round(strips * height * 100) / 100;
  return { totalLength, rolls: Math.ceil(totalLength / 10), wallArea: Math.round(wallArea * 100) / 100 };
}

export function weddingCost(inputs: Record<string, number | string>): Record<string, number | string> {
  const guests = inputs.guests as number;
  const style = inputs.style as string;
  const giftPerPerson = inputs.giftPerPerson as number;
  const venue = venueCost * 10000;
  const food = foodCost * guests * 10000;
  const total = venue + food;
  const perGuest = guests > 0 ? Math.round(total / guests) : 0;
  return { total, perGuest };
}

export function workersComp(inputs: Record<string, number | string>): Record<string, number | string> {
  const avgDailyWage = inputs.avgDailyWage as number;
  const dailyWage = Math.round(monthlySalary * 10000 / 30);
  const benefit = Math.round(dailyWage * 0.8);
  const total = benefit * days;
  return { dailyBenefit: benefit, totalBenefit: total };
}

export function workingCapital(inputs: Record<string, number | string>): Record<string, number | string> {
  const receivables = inputs.receivables as number;
  const inventory = inputs.inventory as number;
  const payables = inputs.payables as number;
  const ar10k = receivables * 10000;
  const inv10k = inventory * 10000;
  const ap10k = payables * 10000;
  const wc = ar10k + inv10k - ap10k;
  return { workingCapital: wc, ratio: ap10k > 0 ? Math.round((ar10k + inv10k) / ap10k * 100) / 100 : 0 };
}

export function yieldComparison(inputs: Record<string, number | string>): Record<string, number | string> {
  const propertyPrice = inputs.propertyPrice as number;
  const monthlyRent = inputs.monthlyRent as number;
  const annualExpense = inputs.annualExpense as number;
  const vacancy = inputs.vacancy as number;
  const priceA10k = priceA * 10000;
  const priceB10k = priceB * 10000;
  const rentA10k = rentA * 10000;
  const rentB10k = rentB * 10000;
  const yieldA = priceA10k > 0 ? Math.round(rentA10k * 12 / priceA10k * 10000) / 100 : 0;
  const yieldB = priceB10k > 0 ? Math.round(rentB10k * 12 / priceB10k * 10000) / 100 : 0;
  return { yieldA, yieldB, difference: Math.round((yieldA - yieldB) * 100) / 100 };
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
  electricityCost,
  gasCost,
  waterCost,
  internetCost,
  stepsToDistance,
  sleepCalculator,
  alcoholBreakdown,
  dogAge,
  catAge,
  timezoneCalc,
  birthdayCountdown,
  ovulationCalc,
  maternityLeave,
  unemploymentInsurance,
  movingEstimate,
  rentBudget,
  condoMonthly,
  furusatoDetail,
  spouseDeduction,
  dependentDeduction,
  educationCostSim,
  scholarshipRepayment,
  wifiSpeed,
  tsuboSqm,
  adRoas,
  advancePayment,
  airConditionerCost,
  alcoholCalorie,
  alcoholTobaccoTax,
  anniversary,
  assetAllocation,
  autoTax,
  babyGrowth,
  baseConvert,
  bloodAlcohol,
  blueReturn,
  bmiChild,
  bmiDetailed,
  bmiPet,
  bodyFatPercentage,
  bondYield,
  businessDays,
  caffeine,
  capitalGainsTax,
  carCostTotal,
  carLease,
  carbonFootprint,
  carpetCalculator,
  certificationCost,
  childCost,
  childcareBenefit,
  chineseZodiac,
  churnRate,
  cityPlanningTax,
  clothingSize,
  commuteCost,
  compoundInterestDetail,
  concreteCalculator,
  consumptionTaxCalc,
  corporatePension,
  corporateTax,
  correlation,
  cryptoTax,
  currencyConvert,
  cyclingCalorie,
  dataSizeConvert,
  debtRepayment,
  disabilityInsurance,
  dollarCostAveraging,
  downloadTime,
  electricityBill,
  ellipse,
  emailMarketing,
  emergencyFund,
  energyConvert,
  englishScore,
  etfCost,
  evCostComparison,
  exerciseCalorie,
  fabricCalculator,
  fireInsurance,
  fractionCalculator,
  freelanceRate,
  gardenSoil,
  goldInvestment,
  gpaCalculator,
  gradeCalculator,
  grossMargin,
  hearingLevel,
  hensachi,
  hexagon,
  housingDeduction,
  individualEnterpriseTax,
  inflationCalculator,
  inheritanceTaxSimulation,
  initialCost,
  investmentReturn,
  japaneseEra,
  joggingPace,
  laborCost,
  landPrice,
  logarithm,
  ltv,
  mansionCost,
  marginTrading,
  maternityBenefit,
  matrix,
  mealCalorie,
  medianMode,
  medicineDose,
  meetingCost,
  menstrualCycle,
  minimumWage,
  nationalHealthInsurance,
  normalDistribution,
  ovulationDay,
  packingList,
  paintArea,
  paintCalculator,
  paperSize,
  partyFood,
  paybackPeriod,
  perPbr,
  percentageCalculator,
  personalLoan,
  petAge,
  petInsurance,
  photoPrint,
  pointValue,
  polygonArea,
  postalRate,
  powerConsumption,
  pressureConvert,
  pricingMarkup,
  primeFactorization,
  probability,
  proteinNeed,
  pythagorean,
  quadratic,
  randomNumber,
  realEstateAcquisitionTax,
  rebalance,
  recipeScale,
  refinance,
  registrationTax,
  reitYield,
  rentCalculator,
  roomBrightness,
  rule72,
  runningPace,
  salaryAfterTax,
  salaryComparison,
  scholarship,
  schoolCommute,
  schoolSupplies,
  screenSize,
  severanceTax,
  shoeSize,
  sleepCycle,
  squareRoot,
  stampDuty,
  stretchTimer,
  studyPlan,
  subscriptionCost,
  swimmingCalorie,
  targetHeartRate,
  tileCalculator,
  timeConvert,
  timeZone,
  tipCalculator,
  trapezoid,
  travelInsurance,
  trigonometry,
  tsuboM2,
  typingSpeed,
  unemploymentBenefit,
  unitPrice,
  visionTest,
  vocabSize,
  waistHipRatio,
  walkingCalorie,
  wallpaperCalculator,
  weddingCost,
  workersComp,
  workingCapital,
  yieldComparison,
};

export function getCalculatorFunction(
  name: string
): ((inputs: Record<string, number | string>) => Record<string, number | string>) | undefined {
  return calculatorFunctions[name];
}
