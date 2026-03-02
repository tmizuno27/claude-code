import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CalculatorKeypad extends StatelessWidget {
  final void Function(String key) onKeyPressed;

  const CalculatorKeypad({
    super.key,
    required this.onKeyPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildRow(context, ['7', '8', '9', '⌫']),
        const SizedBox(height: 8),
        _buildRow(context, ['4', '5', '6', 'C']),
        const SizedBox(height: 8),
        _buildRow(context, ['1', '2', '3', '00']),
        const SizedBox(height: 8),
        _buildRow(context, ['0', '.', '', '']),
      ],
    );
  }

  Widget _buildRow(BuildContext context, List<String> keys) {
    return Row(
      children: keys.map((key) {
        if (key.isEmpty) {
          return Expanded(child: Container());
        }
        return Expanded(
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 4),
            child: _KeyButton(
              label: key,
              onTap: () => onKeyPressed(key),
            ),
          ),
        );
      }).toList(),
    );
  }
}

class _KeyButton extends StatelessWidget {
  final String label;
  final VoidCallback onTap;

  const _KeyButton({
    required this.label,
    required this.onTap,
  });

  bool get _isAction => label == '⌫' || label == 'C';

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    Color backgroundColor;
    Color foregroundColor;

    if (label == 'C') {
      backgroundColor = colorScheme.errorContainer;
      foregroundColor = colorScheme.onErrorContainer;
    } else if (label == '⌫') {
      backgroundColor = colorScheme.tertiaryContainer;
      foregroundColor = colorScheme.onTertiaryContainer;
    } else {
      backgroundColor = colorScheme.surfaceContainerHighest;
      foregroundColor = colorScheme.onSurface;
    }

    return Material(
      color: backgroundColor,
      borderRadius: BorderRadius.circular(16),
      child: InkWell(
        onTap: () {
          HapticFeedback.lightImpact();
          onTap();
        },
        borderRadius: BorderRadius.circular(16),
        child: Container(
          height: 64,
          alignment: Alignment.center,
          child: _isAction
              ? Icon(
                  label == '⌫' ? Icons.backspace_outlined : Icons.clear,
                  color: foregroundColor,
                  size: 24,
                )
              : Text(
                  label,
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.w500,
                    color: foregroundColor,
                  ),
                ),
        ),
      ),
    );
  }
}
