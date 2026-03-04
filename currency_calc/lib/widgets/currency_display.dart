import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/currency.dart';

class CurrencyDisplay extends StatelessWidget {
  final Currency currency;
  final double amount;
  final bool isSelected;
  final bool isInput;
  final String? inputText;
  final VoidCallback onTap;

  const CurrencyDisplay({
    super.key,
    required this.currency,
    required this.amount,
    required this.isSelected,
    this.isInput = false,
    this.inputText,
    required this.onTap,
  });

  String _formatAmount() {
    if (isInput && inputText != null) {
      // 入力中: そのまま表示（カンマ付き）
      return _addCommas(inputText!);
    }
    if (amount == 0) return '0';

    if (currency.decimalPlaces == 0) {
      final formatter = NumberFormat('#,##0', 'ja');
      return formatter.format(amount.round());
    } else {
      final formatter = NumberFormat('#,##0.00', 'en');
      return formatter.format(amount);
    }
  }

  String _addCommas(String value) {
    if (value.contains('.')) {
      final parts = value.split('.');
      final intPart = _addCommasToInt(parts[0]);
      return '$intPart.${parts[1]}';
    }
    return _addCommasToInt(value);
  }

  String _addCommasToInt(String value) {
    if (value.isEmpty || value == '-') return value;
    final isNegative = value.startsWith('-');
    final digits = isNegative ? value.substring(1) : value;
    final buffer = StringBuffer();
    for (var i = 0; i < digits.length; i++) {
      if (i > 0 && (digits.length - i) % 3 == 0) {
        buffer.write(',');
      }
      buffer.write(digits[i]);
    }
    return isNegative ? '-${buffer.toString()}' : buffer.toString();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 16),
        decoration: BoxDecoration(
          color: isSelected
              ? colorScheme.primaryContainer
              : Colors.transparent,
          borderRadius: BorderRadius.circular(16),
          border: isSelected
              ? Border.all(color: colorScheme.primary, width: 2)
              : Border.all(color: Colors.transparent, width: 2),
        ),
        child: Row(
          children: [
            // 国旗と通貨コード
            Text(
              currency.flag,
              style: const TextStyle(fontSize: 28),
            ),
            const SizedBox(width: 12),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  currency.code,
                  style: TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: isSelected
                        ? colorScheme.onPrimaryContainer
                        : colorScheme.onSurface,
                  ),
                ),
                Text(
                  currency.name,
                  style: TextStyle(
                    fontSize: 11,
                    color: isSelected
                        ? colorScheme.onPrimaryContainer.withValues(alpha: 0.7)
                        : colorScheme.onSurface.withValues(alpha: 0.5),
                  ),
                ),
              ],
            ),
            const Spacer(),
            // 金額表示
            Flexible(
              child: Row(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.baseline,
                textBaseline: TextBaseline.alphabetic,
                children: [
                  Text(
                    currency.symbol,
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.w500,
                      color: isSelected
                          ? colorScheme.primary
                          : colorScheme.onSurface.withValues(alpha: 0.6),
                    ),
                  ),
                  const SizedBox(width: 4),
                  Flexible(
                    child: Text(
                      _formatAmount(),
                      style: TextStyle(
                        fontSize: isSelected ? 28 : 24,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
                        color: isSelected
                            ? colorScheme.onPrimaryContainer
                            : colorScheme.onSurface,
                      ),
                      textAlign: TextAlign.right,
                      overflow: TextOverflow.ellipsis,
                      maxLines: 1,
                    ),
                  ),
                  if (isSelected)
                    Container(
                      width: 2,
                      height: 32,
                      margin: const EdgeInsets.only(left: 2),
                      decoration: BoxDecoration(
                        color: colorScheme.primary,
                        borderRadius: BorderRadius.circular(1),
                      ),
                    ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
