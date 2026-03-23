const CURRENCIES = [
  { code: 'USD', name: 'US Dollar', flag: '🇺🇸' },
  { code: 'EUR', name: 'Euro', flag: '🇪🇺' },
  { code: 'JPY', name: 'Japanese Yen', flag: '🇯🇵' },
  { code: 'GBP', name: 'British Pound', flag: '🇬🇧' },
  { code: 'BRL', name: 'Brazilian Real', flag: '🇧🇷' },
  { code: 'PYG', name: 'Paraguayan Guarani', flag: '🇵🇾' },
  { code: 'ARS', name: 'Argentine Peso', flag: '🇦🇷' },
  { code: 'AUD', name: 'Australian Dollar', flag: '🇦🇺' },
  { code: 'CAD', name: 'Canadian Dollar', flag: '🇨🇦' },
  { code: 'CHF', name: 'Swiss Franc', flag: '🇨🇭' },
  { code: 'CNY', name: 'Chinese Yuan', flag: '🇨🇳' },
  { code: 'CLP', name: 'Chilean Peso', flag: '🇨🇱' },
  { code: 'COP', name: 'Colombian Peso', flag: '🇨🇴' },
  { code: 'CZK', name: 'Czech Koruna', flag: '🇨🇿' },
  { code: 'DKK', name: 'Danish Krone', flag: '🇩🇰' },
  { code: 'EGP', name: 'Egyptian Pound', flag: '🇪🇬' },
  { code: 'HKD', name: 'Hong Kong Dollar', flag: '🇭🇰' },
  { code: 'HUF', name: 'Hungarian Forint', flag: '🇭🇺' },
  { code: 'IDR', name: 'Indonesian Rupiah', flag: '🇮🇩' },
  { code: 'ILS', name: 'Israeli Shekel', flag: '🇮🇱' },
  { code: 'INR', name: 'Indian Rupee', flag: '🇮🇳' },
  { code: 'ISK', name: 'Icelandic Krona', flag: '🇮🇸' },
  { code: 'KRW', name: 'South Korean Won', flag: '🇰🇷' },
  { code: 'MXN', name: 'Mexican Peso', flag: '🇲🇽' },
  { code: 'MYR', name: 'Malaysian Ringgit', flag: '🇲🇾' },
  { code: 'NGN', name: 'Nigerian Naira', flag: '🇳🇬' },
  { code: 'NOK', name: 'Norwegian Krone', flag: '🇳🇴' },
  { code: 'NZD', name: 'New Zealand Dollar', flag: '🇳🇿' },
  { code: 'PEN', name: 'Peruvian Sol', flag: '🇵🇪' },
  { code: 'PHP', name: 'Philippine Peso', flag: '🇵🇭' },
  { code: 'PLN', name: 'Polish Zloty', flag: '🇵🇱' },
  { code: 'RON', name: 'Romanian Leu', flag: '🇷🇴' },
  { code: 'RUB', name: 'Russian Ruble', flag: '🇷🇺' },
  { code: 'SAR', name: 'Saudi Riyal', flag: '🇸🇦' },
  { code: 'SEK', name: 'Swedish Krona', flag: '🇸🇪' },
  { code: 'SGD', name: 'Singapore Dollar', flag: '🇸🇬' },
  { code: 'THB', name: 'Thai Baht', flag: '🇹🇭' },
  { code: 'TRY', name: 'Turkish Lira', flag: '🇹🇷' },
  { code: 'TWD', name: 'Taiwan Dollar', flag: '🇹🇼' },
  { code: 'UAH', name: 'Ukrainian Hryvnia', flag: '🇺🇦' },
  { code: 'UYU', name: 'Uruguayan Peso', flag: '🇺🇾' },
  { code: 'VND', name: 'Vietnamese Dong', flag: '🇻🇳' },
  { code: 'ZAR', name: 'South African Rand', flag: '🇿🇦' },
  { code: 'AED', name: 'UAE Dirham', flag: '🇦🇪' },
  { code: 'AFN', name: 'Afghan Afghani', flag: '🇦🇫' },
  { code: 'ALL', name: 'Albanian Lek', flag: '🇦🇱' },
  { code: 'AMD', name: 'Armenian Dram', flag: '🇦🇲' },
  { code: 'ANG', name: 'Netherlands Antillean Guilder', flag: '🇨🇼' },
  { code: 'AOA', name: 'Angolan Kwanza', flag: '🇦🇴' },
  { code: 'AWG', name: 'Aruban Florin', flag: '🇦🇼' },
  { code: 'AZN', name: 'Azerbaijani Manat', flag: '🇦🇿' },
  { code: 'BAM', name: 'Bosnia Mark', flag: '🇧🇦' },
  { code: 'BBD', name: 'Barbadian Dollar', flag: '🇧🇧' },
  { code: 'BDT', name: 'Bangladeshi Taka', flag: '🇧🇩' },
  { code: 'BGN', name: 'Bulgarian Lev', flag: '🇧🇬' },
  { code: 'BHD', name: 'Bahraini Dinar', flag: '🇧🇭' },
  { code: 'BIF', name: 'Burundian Franc', flag: '🇧🇮' },
  { code: 'BMD', name: 'Bermudian Dollar', flag: '🇧🇲' },
  { code: 'BND', name: 'Brunei Dollar', flag: '🇧🇳' },
  { code: 'BOB', name: 'Bolivian Boliviano', flag: '🇧🇴' },
  { code: 'BSD', name: 'Bahamian Dollar', flag: '🇧🇸' },
  { code: 'BTN', name: 'Bhutanese Ngultrum', flag: '🇧🇹' },
  { code: 'BWP', name: 'Botswana Pula', flag: '🇧🇼' },
  { code: 'BYN', name: 'Belarusian Ruble', flag: '🇧🇾' },
  { code: 'BZD', name: 'Belize Dollar', flag: '🇧🇿' },
  { code: 'CDF', name: 'Congolese Franc', flag: '🇨🇩' },
  { code: 'CRC', name: 'Costa Rican Colon', flag: '🇨🇷' },
  { code: 'CUP', name: 'Cuban Peso', flag: '🇨🇺' },
  { code: 'CVE', name: 'Cape Verdean Escudo', flag: '🇨🇻' },
  { code: 'DJF', name: 'Djiboutian Franc', flag: '🇩🇯' },
  { code: 'DOP', name: 'Dominican Peso', flag: '🇩🇴' },
  { code: 'DZD', name: 'Algerian Dinar', flag: '🇩🇿' },
  { code: 'ERN', name: 'Eritrean Nakfa', flag: '🇪🇷' },
  { code: 'ETB', name: 'Ethiopian Birr', flag: '🇪🇹' },
  { code: 'FJD', name: 'Fijian Dollar', flag: '🇫🇯' },
  { code: 'FKP', name: 'Falkland Pound', flag: '🇫🇰' },
  { code: 'GEL', name: 'Georgian Lari', flag: '🇬🇪' },
  { code: 'GHS', name: 'Ghanaian Cedi', flag: '🇬🇭' },
  { code: 'GIP', name: 'Gibraltar Pound', flag: '🇬🇮' },
  { code: 'GMD', name: 'Gambian Dalasi', flag: '🇬🇲' },
  { code: 'GNF', name: 'Guinean Franc', flag: '🇬🇳' },
  { code: 'GTQ', name: 'Guatemalan Quetzal', flag: '🇬🇹' },
  { code: 'GYD', name: 'Guyanese Dollar', flag: '🇬🇾' },
  { code: 'HNL', name: 'Honduran Lempira', flag: '🇭🇳' },
  { code: 'HRK', name: 'Croatian Kuna', flag: '🇭🇷' },
  { code: 'HTG', name: 'Haitian Gourde', flag: '🇭🇹' },
  { code: 'IQD', name: 'Iraqi Dinar', flag: '🇮🇶' },
  { code: 'IRR', name: 'Iranian Rial', flag: '🇮🇷' },
  { code: 'JMD', name: 'Jamaican Dollar', flag: '🇯🇲' },
  { code: 'JOD', name: 'Jordanian Dinar', flag: '🇯🇴' },
  { code: 'KES', name: 'Kenyan Shilling', flag: '🇰🇪' },
  { code: 'KGS', name: 'Kyrgyz Som', flag: '🇰🇬' },
  { code: 'KHR', name: 'Cambodian Riel', flag: '🇰🇭' },
  { code: 'KMF', name: 'Comorian Franc', flag: '🇰🇲' },
  { code: 'KWD', name: 'Kuwaiti Dinar', flag: '🇰🇼' },
  { code: 'KYD', name: 'Cayman Dollar', flag: '🇰🇾' },
  { code: 'KZT', name: 'Kazakh Tenge', flag: '🇰🇿' },
  { code: 'LAK', name: 'Lao Kip', flag: '🇱🇦' },
  { code: 'LBP', name: 'Lebanese Pound', flag: '🇱🇧' },
  { code: 'LKR', name: 'Sri Lankan Rupee', flag: '🇱🇰' },
  { code: 'LRD', name: 'Liberian Dollar', flag: '🇱🇷' },
  { code: 'LSL', name: 'Lesotho Loti', flag: '🇱🇸' },
  { code: 'LYD', name: 'Libyan Dinar', flag: '🇱🇾' },
  { code: 'MAD', name: 'Moroccan Dirham', flag: '🇲🇦' },
  { code: 'MDL', name: 'Moldovan Leu', flag: '🇲🇩' },
  { code: 'MGA', name: 'Malagasy Ariary', flag: '🇲🇬' },
  { code: 'MKD', name: 'Macedonian Denar', flag: '🇲🇰' },
  { code: 'MMK', name: 'Myanmar Kyat', flag: '🇲🇲' },
  { code: 'MNT', name: 'Mongolian Tugrik', flag: '🇲🇳' },
  { code: 'MOP', name: 'Macanese Pataca', flag: '🇲🇴' },
  { code: 'MRU', name: 'Mauritanian Ouguiya', flag: '🇲🇷' },
  { code: 'MUR', name: 'Mauritian Rupee', flag: '🇲🇺' },
  { code: 'MVR', name: 'Maldivian Rufiyaa', flag: '🇲🇻' },
  { code: 'MWK', name: 'Malawian Kwacha', flag: '🇲🇼' },
  { code: 'MZN', name: 'Mozambican Metical', flag: '🇲🇿' },
  { code: 'NAD', name: 'Namibian Dollar', flag: '🇳🇦' },
  { code: 'NIO', name: 'Nicaraguan Cordoba', flag: '🇳🇮' },
  { code: 'NPR', name: 'Nepalese Rupee', flag: '🇳🇵' },
  { code: 'OMR', name: 'Omani Rial', flag: '🇴🇲' },
  { code: 'PAB', name: 'Panamanian Balboa', flag: '🇵🇦' },
  { code: 'PGK', name: 'Papua New Guinean Kina', flag: '🇵🇬' },
  { code: 'PKR', name: 'Pakistani Rupee', flag: '🇵🇰' },
  { code: 'QAR', name: 'Qatari Riyal', flag: '🇶🇦' },
  { code: 'RSD', name: 'Serbian Dinar', flag: '🇷🇸' },
  { code: 'RWF', name: 'Rwandan Franc', flag: '🇷🇼' },
  { code: 'SBD', name: 'Solomon Islands Dollar', flag: '🇸🇧' },
  { code: 'SCR', name: 'Seychellois Rupee', flag: '🇸🇨' },
  { code: 'SDG', name: 'Sudanese Pound', flag: '🇸🇩' },
  { code: 'SHP', name: 'Saint Helena Pound', flag: '🇸🇭' },
  { code: 'SLE', name: 'Sierra Leonean Leone', flag: '🇸🇱' },
  { code: 'SOS', name: 'Somali Shilling', flag: '🇸🇴' },
  { code: 'SRD', name: 'Surinamese Dollar', flag: '🇸🇷' },
  { code: 'SSP', name: 'South Sudanese Pound', flag: '🇸🇸' },
  { code: 'STN', name: 'Sao Tome Dobra', flag: '🇸🇹' },
  { code: 'SYP', name: 'Syrian Pound', flag: '🇸🇾' },
  { code: 'SZL', name: 'Eswatini Lilangeni', flag: '🇸🇿' },
  { code: 'TJS', name: 'Tajikistani Somoni', flag: '🇹🇯' },
  { code: 'TMT', name: 'Turkmenistani Manat', flag: '🇹🇲' },
  { code: 'TND', name: 'Tunisian Dinar', flag: '🇹🇳' },
  { code: 'TOP', name: 'Tongan Paanga', flag: '🇹🇴' },
  { code: 'TTD', name: 'Trinidad Dollar', flag: '🇹🇹' },
  { code: 'TZS', name: 'Tanzanian Shilling', flag: '🇹🇿' },
  { code: 'UGX', name: 'Ugandan Shilling', flag: '🇺🇬' },
  { code: 'UZS', name: 'Uzbekistani Som', flag: '🇺🇿' },
  { code: 'VES', name: 'Venezuelan Bolivar', flag: '🇻🇪' },
  { code: 'VUV', name: 'Vanuatu Vatu', flag: '🇻🇺' },
  { code: 'WST', name: 'Samoan Tala', flag: '🇼🇸' },
  { code: 'XAF', name: 'Central African CFA', flag: '🌍' },
  { code: 'XCD', name: 'East Caribbean Dollar', flag: '🌎' },
  { code: 'XOF', name: 'West African CFA', flag: '🌍' },
  { code: 'XPF', name: 'CFP Franc', flag: '🌏' },
  { code: 'YER', name: 'Yemeni Rial', flag: '🇾🇪' },
  { code: 'ZMW', name: 'Zambian Kwacha', flag: '🇿🇲' },
  { code: 'ZWL', name: 'Zimbabwean Dollar', flag: '🇿🇼' },
];

const QUICK_CURRENCIES = ['USD', 'EUR', 'JPY', 'GBP', 'BRL', 'PYG', 'ARS', 'KRW'];
const currencyMap = Object.fromEntries(CURRENCIES.map(c => [c.code, c]));

let currentRates = null;

const $amount = document.getElementById('amount');
const $from = document.getElementById('fromCurrency');
const $to = document.getElementById('toCurrency');
const $result = document.getElementById('result');
const $rateInfo = document.getElementById('rateInfo');
const $quickRates = document.getElementById('quickRates');
const $favList = document.getElementById('favList');

function populateSelects() {
  CURRENCIES.forEach(c => {
    const opt = (sel) => {
      const o = document.createElement('option');
      o.value = c.code;
      o.textContent = `${c.flag} ${c.code}`;
      sel.appendChild(o);
    };
    opt($from);
    opt($to);
  });
}

async function loadSettings() {
  const { settings = { defaultFrom: 'USD', defaultTo: 'JPY' } } = await chrome.storage.local.get('settings');
  $from.value = settings.defaultFrom || 'USD';
  $to.value = settings.defaultTo || 'JPY';
}

async function saveSettings() {
  await chrome.storage.local.set({
    settings: { defaultFrom: $from.value, defaultTo: $to.value }
  });
}

async function convert() {
  const amount = parseFloat($amount.value);
  if (isNaN(amount)) { $result.value = ''; return; }

  const from = $from.value;
  const to = $to.value;

  const resp = await chrome.runtime.sendMessage({ type: 'getRate', from, to });
  if (resp?.rate) {
    const converted = amount * resp.rate;
    $result.value = formatNumber(converted, to);
    $rateInfo.textContent = `1 ${from} = ${formatNumber(resp.rate, to)} ${to}`;
  } else {
    $result.value = 'Error';
    $rateInfo.textContent = 'Failed to fetch rate';
  }
}

function formatNumber(n, currency) {
  const decimals = ['JPY','KRW','VND','PYG','CLP','IDR','UGX','RWF','GNF','KMF','BIF','VUV','XOF','XAF','XPF','DJF','MGA','CDF'].includes(currency) ? 0 : 2;
  return n.toLocaleString('en-US', { minimumFractionDigits: decimals, maximumFractionDigits: decimals });
}

async function loadQuickRates() {
  const from = $from.value;
  const resp = await chrome.runtime.sendMessage({ type: 'getRates', from });
  if (!resp?.rates) {
    $quickRates.innerHTML = '<div style="color:#475569;font-size:12px;grid-column:1/-1;text-align:center">Loading rates...</div>';
    return;
  }
  currentRates = resp.rates;
  $quickRates.innerHTML = '';
  QUICK_CURRENCIES.filter(c => c !== from).forEach(code => {
    const c = currencyMap[code];
    const rate = currentRates[code];
    if (!c || !rate) return;
    const div = document.createElement('div');
    div.className = 'quick-item';
    div.innerHTML = `<span class="currency-label">${c.flag} ${code}</span><span class="currency-value">${formatNumber(rate, code)}</span>`;
    div.addEventListener('click', () => {
      $to.value = code;
      saveSettings();
      convert();
    });
    $quickRates.appendChild(div);
  });
}

async function loadFavorites() {
  const { favorites = [] } = await chrome.storage.local.get('favorites');
  $favList.innerHTML = '';
  if (favorites.length === 0) {
    $favList.innerHTML = '<div class="fav-empty">No favorites yet. Click + to add.</div>';
    return;
  }
  for (const fav of favorites) {
    const resp = await chrome.runtime.sendMessage({ type: 'getRate', from: fav.from, to: fav.to });
    const fromC = currencyMap[fav.from];
    const toC = currencyMap[fav.to];
    const div = document.createElement('div');
    div.className = 'fav-item';
    div.innerHTML = `
      <span class="fav-pair">${fromC?.flag||''} ${fav.from} → ${toC?.flag||''} ${fav.to}</span>
      <span class="fav-rate">${resp?.rate ? formatNumber(resp.rate, fav.to) : '...'}</span>
      <button class="fav-remove" data-from="${fav.from}" data-to="${fav.to}">✕</button>
    `;
    div.querySelector('.fav-pair').addEventListener('click', () => {
      $from.value = fav.from;
      $to.value = fav.to;
      saveSettings();
      convert();
      loadQuickRates();
    });
    $favList.appendChild(div);
  }
  document.querySelectorAll('.fav-remove').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const { favorites = [] } = await chrome.storage.local.get('favorites');
      const updated = favorites.filter(f => !(f.from === btn.dataset.from && f.to === btn.dataset.to));
      await chrome.storage.local.set({ favorites: updated });
      loadFavorites();
    });
  });
}

document.getElementById('addFavBtn').addEventListener('click', async () => {
  const { favorites = [] } = await chrome.storage.local.get('favorites');
  const pair = { from: $from.value, to: $to.value };
  if (favorites.some(f => f.from === pair.from && f.to === pair.to)) return;
  favorites.push(pair);
  await chrome.storage.local.set({ favorites });
  loadFavorites();
});

document.getElementById('swapBtn').addEventListener('click', () => {
  const tmp = $from.value;
  $from.value = $to.value;
  $to.value = tmp;
  saveSettings();
  convert();
  loadQuickRates();
});

$amount.addEventListener('input', convert);
$from.addEventListener('change', () => { saveSettings(); convert(); loadQuickRates(); });
$to.addEventListener('change', () => { saveSettings(); convert(); });

// Init
populateSelects();
loadSettings().then(() => {
  convert();
  loadQuickRates();
  loadFavorites();
});
