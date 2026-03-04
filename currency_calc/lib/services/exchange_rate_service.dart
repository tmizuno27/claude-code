import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ExchangeRateService {
  static const String _apiUrl = 'https://open.er-api.com/v6/latest/USD';
  static const String _cacheKey = 'cached_rates';
  static const String _cacheTimeKey = 'cached_rates_time';
  static const Duration _cacheDuration = Duration(hours: 6);

  /// USD基準のレートを取得（キャッシュ優先）
  Future<Map<String, double>> getRates() async {
    final prefs = await SharedPreferences.getInstance();

    // キャッシュが有効か確認
    final cachedTime = prefs.getInt(_cacheTimeKey) ?? 0;
    final now = DateTime.now().millisecondsSinceEpoch;
    if (now - cachedTime < _cacheDuration.inMilliseconds) {
      final cached = prefs.getString(_cacheKey);
      if (cached != null) {
        return _parseRates(cached);
      }
    }

    // APIから取得
    try {
      final response = await http
          .get(Uri.parse(_apiUrl))
          .timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        // キャッシュに保存
        await prefs.setString(_cacheKey, response.body);
        await prefs.setInt(_cacheTimeKey, now);
        return _parseRates(response.body);
      }
    } catch (_) {
      // ネットワークエラー時はキャッシュにフォールバック
    }

    // フォールバック: キャッシュから取得
    final cached = prefs.getString(_cacheKey);
    if (cached != null) {
      return _parseRates(cached);
    }

    // キャッシュもない場合はデフォルトレート
    return {'USD': 1.0, 'JPY': 150.0, 'PYG': 7500.0};
  }

  /// 最終更新日時を取得
  Future<DateTime?> getLastUpdateTime() async {
    final prefs = await SharedPreferences.getInstance();
    final cachedTime = prefs.getInt(_cacheTimeKey);
    if (cachedTime != null) {
      return DateTime.fromMillisecondsSinceEpoch(cachedTime);
    }
    return null;
  }

  Map<String, double> _parseRates(String body) {
    final json = jsonDecode(body) as Map<String, dynamic>;
    final rates = json['rates'] as Map<String, dynamic>;
    return {
      'USD': 1.0,
      'JPY': (rates['JPY'] as num).toDouble(),
      'PYG': (rates['PYG'] as num).toDouble(),
    };
  }
}
