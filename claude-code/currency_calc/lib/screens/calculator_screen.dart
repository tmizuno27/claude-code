import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../models/currency.dart';
import '../providers/calculator_provider.dart';
import '../widgets/currency_display.dart';
import '../widgets/calculator_keypad.dart';

class CalculatorScreen extends StatelessWidget {
  const CalculatorScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      backgroundColor: colorScheme.surface,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        title: Text(
          'CurrencyCalc',
          style: TextStyle(
            color: colorScheme.onSurface,
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          Consumer<CalculatorProvider>(
            builder: (context, provider, _) {
              return IconButton(
                icon: provider.isLoading
                    ? SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: colorScheme.primary,
                        ),
                      )
                    : Icon(
                        Icons.refresh,
                        color: colorScheme.primary,
                      ),
                onPressed: provider.isLoading
                    ? null
                    : () => provider.refreshRates(),
                tooltip: 'レート更新',
              );
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // 通貨表示エリア
            Expanded(
              flex: 4,
              child: Consumer<CalculatorProvider>(
                builder: (context, provider, _) {
                  return Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: Currency.values.map((currency) {
                        final isSelected =
                            currency == provider.selectedCurrency;
                        return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 4),
                          child: CurrencyDisplay(
                            currency: currency,
                            amount: provider.getConvertedAmount(currency),
                            isSelected: isSelected,
                            isInput: isSelected,
                            inputText:
                                isSelected ? provider.inputValue : null,
                            onTap: () =>
                                provider.selectCurrency(currency),
                          ),
                        );
                      }).toList(),
                    ),
                  );
                },
              ),
            ),

            // 最終更新表示
            Consumer<CalculatorProvider>(
              builder: (context, provider, _) {
                final lastUpdate = provider.lastUpdate;
                String updateText;
                if (provider.isLoading) {
                  updateText = 'レート取得中...';
                } else if (lastUpdate != null) {
                  final formatter = DateFormat('yyyy/MM/dd HH:mm');
                  updateText = '最終更新: ${formatter.format(lastUpdate)}';
                } else {
                  updateText = 'デフォルトレート使用中';
                }

                // レート表示
                final rates = provider.rates;
                final jpyRate = rates['JPY']?.toStringAsFixed(2) ?? '-';
                final pygRate = rates['PYG']?.toStringAsFixed(0) ?? '-';

                return Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                  child: Column(
                    children: [
                      Text(
                        updateText,
                        style: TextStyle(
                          fontSize: 11,
                          color: colorScheme.onSurface.withValues(alpha: 0.5),
                        ),
                      ),
                      const SizedBox(height: 2),
                      Text(
                        '1 USD = ¥$jpyRate = ₲$pygRate',
                        style: TextStyle(
                          fontSize: 12,
                          color: colorScheme.onSurface.withValues(alpha: 0.4),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),

            // 区切り線
            Divider(
              height: 1,
              color: colorScheme.outlineVariant,
            ),

            // テンキーパッド
            Expanded(
              flex: 5,
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Consumer<CalculatorProvider>(
                  builder: (context, provider, _) {
                    return CalculatorKeypad(
                      onKeyPressed: (key) => provider.onKeyPressed(key),
                    );
                  },
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
