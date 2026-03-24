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
};

export function getCalculatorFunction(
  name: string
): ((inputs: Record<string, number | string>) => Record<string, number | string>) | undefined {
  return calculatorFunctions[name];
}
