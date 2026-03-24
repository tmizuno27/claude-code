'use client';

import { useState, useCallback } from 'react';
import { getCalculatorFunction } from '@/lib/calculators';
import ResultDisplay from './ResultDisplay';

interface InputDef {
  id: string;
  label: string;
  type: 'number' | 'slider' | 'select' | 'date';
  unit?: string;
  default: number | string;
  min?: number;
  max?: number;
  step?: number;
  hint?: string;
  options?: { value: string; label: string }[];
}

interface OutputDef {
  id: string;
  label: string;
  format: string;
  primary?: boolean;
}

interface CalculatorClientProps {
  title: string;
  description: string;
  calculatorFunction: string;
  inputs: InputDef[];
  outputs: OutputDef[];
}

function getDefaultValue(input: InputDef): string {
  if (input.type === 'date') {
    if (input.default === 'today') {
      return new Date().toISOString().split('T')[0];
    }
    return String(input.default);
  }
  return String(input.default);
}

export default function CalculatorClient({
  title,
  description,
  calculatorFunction,
  inputs,
  outputs,
}: CalculatorClientProps) {
  const [values, setValues] = useState<Record<string, string>>(() => {
    const initial: Record<string, string> = {};
    for (const input of inputs) {
      initial[input.id] = getDefaultValue(input);
    }
    return initial;
  });

  const [results, setResults] = useState<Record<string, number | string> | null>(null);

  const handleChange = useCallback((id: string, value: string) => {
    setValues(prev => ({ ...prev, [id]: value }));
  }, []);

  const handleCalculate = useCallback(() => {
    const fn = getCalculatorFunction(calculatorFunction);
    if (!fn) return;

    const parsed: Record<string, number | string> = {};
    for (const input of inputs) {
      if (input.type === 'date' || input.type === 'select') {
        parsed[input.id] = values[input.id];
      } else {
        parsed[input.id] = parseFloat(values[input.id]) || 0;
      }
    }

    const result = fn(parsed);
    setResults(result);
  }, [calculatorFunction, inputs, values]);

  return (
    <>
      <div className="calc-form">
        <h1>{title}</h1>
        <p className="calc-form-description">{description}</p>

        {inputs.map(input => (
          <div className="calc-field" key={input.id}>
            <label htmlFor={input.id}>
              {input.label}
              {input.hint && <span className="calc-field-hint">({input.hint})</span>}
            </label>

            {input.type === 'number' && (
              <div className="calc-input-with-unit">
                <input
                  id={input.id}
                  type="number"
                  className="calc-input"
                  value={values[input.id]}
                  onChange={e => handleChange(input.id, e.target.value)}
                  min={input.min}
                  max={input.max}
                  step={input.step}
                />
                {input.unit && <span className="calc-input-unit">{input.unit}</span>}
              </div>
            )}

            {input.type === 'slider' && (
              <div className="calc-slider-row">
                <input
                  id={input.id}
                  type="range"
                  className="calc-slider"
                  value={values[input.id]}
                  onChange={e => handleChange(input.id, e.target.value)}
                  min={input.min}
                  max={input.max}
                  step={input.step}
                />
                <span className="calc-slider-value">
                  {values[input.id]}{input.unit}
                </span>
              </div>
            )}

            {input.type === 'select' && input.options && (
              <select
                id={input.id}
                className="calc-select"
                value={values[input.id]}
                onChange={e => handleChange(input.id, e.target.value)}
              >
                {input.options.map(opt => (
                  <option key={opt.value} value={opt.value}>
                    {opt.label}
                  </option>
                ))}
              </select>
            )}

            {input.type === 'date' && (
              <input
                id={input.id}
                type="date"
                className="calc-input"
                value={values[input.id]}
                onChange={e => handleChange(input.id, e.target.value)}
              />
            )}
          </div>
        ))}

        <button className="calc-btn" onClick={handleCalculate} type="button">
          計算する
        </button>
      </div>

      {results && <ResultDisplay outputs={outputs} results={results} />}
    </>
  );
}
