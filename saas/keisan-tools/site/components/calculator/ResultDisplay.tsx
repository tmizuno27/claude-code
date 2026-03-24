'use client';

import { useCallback } from 'react';
import { formatCurrencyExact, formatPercent, formatNumber } from '@/lib/utils/format';

interface OutputDef {
  id: string;
  label: string;
  format: string;
  primary?: boolean;
}

interface ResultDisplayProps {
  outputs: OutputDef[];
  results: Record<string, number | string>;
}

function formatValue(value: number | string, format: string): string {
  if (typeof value === 'string') return value;
  switch (format) {
    case 'currency':
      return formatCurrencyExact(value);
    case 'percent':
      return formatPercent(value);
    case 'number':
      return formatNumber(value);
    case 'weight':
      return `${value}kg`;
    case 'days':
      return `${value}日`;
    default:
      return String(value);
  }
}

export default function ResultDisplay({ outputs, results }: ResultDisplayProps) {
  const handleCopy = useCallback(() => {
    const text = outputs
      .map(o => `${o.label}: ${formatValue(results[o.id], o.format)}`)
      .join('\n');
    navigator.clipboard.writeText(text).catch(() => {
      // Fallback: ignore
    });
  }, [outputs, results]);

  return (
    <div className="calc-results">
      <h2>計算結果</h2>
      <table className="result-table">
        <tbody>
          {outputs.map(output => {
            const val = results[output.id];
            if (val === undefined) return null;
            const formatted = formatValue(val, output.format);
            const isNegative = typeof val === 'number' && val < 0;

            return (
              <tr key={output.id}>
                <td>{output.label}</td>
                <td
                  className={
                    output.primary
                      ? 'result-primary'
                      : isNegative
                      ? 'result-negative'
                      : ''
                  }
                >
                  {formatted}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
      <button className="copy-btn" onClick={handleCopy} type="button">
        結果をコピー
      </button>
    </div>
  );
}
