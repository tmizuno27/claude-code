export function formatCurrency(n: number): string {
  if (Math.abs(n) >= 100_000_000) {
    return `${(n / 100_000_000).toLocaleString('ja-JP', { maximumFractionDigits: 2 })}億円`;
  }
  if (Math.abs(n) >= 10_000) {
    return `${Math.round(n / 10_000).toLocaleString('ja-JP')}万円`;
  }
  return `¥${Math.round(n).toLocaleString('ja-JP')}`;
}

export function formatCurrencyExact(n: number): string {
  return `¥${Math.round(n).toLocaleString('ja-JP')}`;
}

export function formatPercent(n: number): string {
  return `${n.toFixed(1)}%`;
}

export function formatNumber(n: number): string {
  return n.toLocaleString('ja-JP');
}

export function formatDate(d: Date): string {
  return `${d.getFullYear()}年${d.getMonth() + 1}月${d.getDate()}日`;
}
