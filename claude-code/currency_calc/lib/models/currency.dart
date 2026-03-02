enum Currency {
  jpy,
  usd,
  pyg,
}

extension CurrencyExtension on Currency {
  String get code {
    switch (this) {
      case Currency.jpy:
        return 'JPY';
      case Currency.usd:
        return 'USD';
      case Currency.pyg:
        return 'PYG';
    }
  }

  String get symbol {
    switch (this) {
      case Currency.jpy:
        return '¥';
      case Currency.usd:
        return '\$';
      case Currency.pyg:
        return '₲';
    }
  }

  String get flag {
    switch (this) {
      case Currency.jpy:
        return '🇯🇵';
      case Currency.usd:
        return '🇺🇸';
      case Currency.pyg:
        return '🇵🇾';
    }
  }

  String get name {
    switch (this) {
      case Currency.jpy:
        return '日本円';
      case Currency.usd:
        return '米ドル';
      case Currency.pyg:
        return 'グアラニー';
    }
  }

  int get decimalPlaces {
    switch (this) {
      case Currency.jpy:
        return 0;
      case Currency.usd:
        return 2;
      case Currency.pyg:
        return 0;
    }
  }
}
