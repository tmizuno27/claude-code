import 'package:flutter/foundation.dart';
import '../models/currency.dart';
import '../services/exchange_rate_service.dart';

class CalculatorProvider extends ChangeNotifier {
  final ExchangeRateService _rateService = ExchangeRateService();

  Currency _selectedCurrency = Currency.usd;
  String _inputValue = '0';
  Map<String, double> _rates = {'USD': 1.0, 'JPY': 150.0, 'PYG': 7500.0};
  DateTime? _lastUpdate;
  bool _isLoading = true;

  Currency get selectedCurrency => _selectedCurrency;
  String get inputValue => _inputValue;
  Map<String, double> get rates => _rates;
  DateTime? get lastUpdate => _lastUpdate;
  bool get isLoading => _isLoading;

  CalculatorProvider() {
    _loadRates();
  }

  Future<void> _loadRates() async {
    _isLoading = true;
    notifyListeners();

    _rates = await _rateService.getRates();
    _lastUpdate = await _rateService.getLastUpdateTime();

    _isLoading = false;
    notifyListeners();
  }

  Future<void> refreshRates() async {
    // キャッシュをクリアして強制更新
    await _loadRates();
  }

  void selectCurrency(Currency currency) {
    if (_selectedCurrency == currency) return;

    // 現在の換算値を新しい通貨の入力値にする
    final currentAmount = _getAmountForCurrency(currency);
    _selectedCurrency = currency;
    if (currentAmount == 0) {
      _inputValue = '0';
    } else {
      _inputValue = _formatForInput(currentAmount, currency);
    }
    notifyListeners();
  }

  void onKeyPressed(String key) {
    switch (key) {
      case 'C':
        _inputValue = '0';
        break;
      case '⌫':
        if (_inputValue.length > 1) {
          _inputValue = _inputValue.substring(0, _inputValue.length - 1);
        } else {
          _inputValue = '0';
        }
        break;
      case '.':
        if (!_inputValue.contains('.')) {
          _inputValue = '$_inputValue.';
        }
        break;
      case '00':
        if (_inputValue != '0') {
          _inputValue = '${_inputValue}00';
        }
        break;
      default:
        // 数字キー
        if (_inputValue == '0' && key != '.') {
          _inputValue = key;
        } else {
          // 入力制限（最大15桁）
          final digits = _inputValue.replaceAll('.', '');
          if (digits.length < 15) {
            _inputValue = '$_inputValue$key';
          }
        }
        break;
    }
    notifyListeners();
  }

  /// 指定通貨の換算金額を取得
  double getConvertedAmount(Currency currency) {
    final inputAmount = double.tryParse(_inputValue) ?? 0;
    if (inputAmount == 0) return 0;

    // 入力通貨のUSDレート
    final fromRate = _rates[_selectedCurrency.code] ?? 1.0;
    // 出力通貨のUSDレート
    final toRate = _rates[currency.code] ?? 1.0;

    // USD経由で換算: 入力額 / fromRate * toRate
    return inputAmount / fromRate * toRate;
  }

  double _getAmountForCurrency(Currency currency) {
    return getConvertedAmount(currency);
  }

  String _formatForInput(double amount, Currency currency) {
    if (currency.decimalPlaces == 0) {
      return amount.round().toString();
    }
    // 小数点以下の不要なゼロを除去
    final str = amount.toStringAsFixed(currency.decimalPlaces);
    if (str.contains('.')) {
      final trimmed = str.replaceAll(RegExp(r'0+$'), '').replaceAll(RegExp(r'\.$'), '');
      return trimmed.isEmpty ? '0' : trimmed;
    }
    return str;
  }
}
