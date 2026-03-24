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

// Calculator function registry
const calculatorFunctions: Record<string, (inputs: Record<string, number | string>) => Record<string, number | string>> = {
  loanRepayment,
  incomeTax,
  takeHomePay,
  bmi,
  daysBetween,
  compoundInterest,
  calcCompoundInterest: compoundInterest,
};

export function getCalculatorFunction(
  name: string
): ((inputs: Record<string, number | string>) => Record<string, number | string>) | undefined {
  return calculatorFunctions[name];
}
