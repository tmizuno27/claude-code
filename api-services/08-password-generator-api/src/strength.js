const COMMON_PASSWORDS = new Set([
  'password', '123456', '12345678', 'qwerty', 'abc123', 'monkey', 'master',
  'dragon', '111111', 'baseball', 'iloveyou', 'trustno1', 'sunshine',
  'princess', 'football', 'charlie', 'shadow', 'michael', 'login',
  'letmein', 'superman', 'hello', 'admin', 'welcome', 'password1',
  '123456789', '1234567890', '000000', 'passw0rd', 'p@ssword', 'qwerty123',
]);

const KEYBOARD_PATTERNS = [
  'qwerty', 'asdfgh', 'zxcvbn', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
  '1234567890', '0987654321', 'qazwsx', 'edcrfv',
];

export function checkStrength(password) {
  if (!password) {
    return { score: 0, level: 'none', crack_time_estimate: 'instant', suggestions: ['Provide a password to check.'] };
  }

  let score = 0;
  const suggestions = [];
  const len = password.length;

  // Length scoring (up to 30 points)
  if (len >= 16) score += 30;
  else if (len >= 12) score += 22;
  else if (len >= 10) score += 16;
  else if (len >= 8) score += 10;
  else if (len >= 6) score += 5;
  else score += 2;

  if (len < 8) suggestions.push('Use at least 8 characters.');
  if (len < 12) suggestions.push('Consider using 12+ characters for better security.');

  // Character variety (up to 30 points)
  const hasLower = /[a-z]/.test(password);
  const hasUpper = /[A-Z]/.test(password);
  const hasDigit = /[0-9]/.test(password);
  const hasSymbol = /[^a-zA-Z0-9]/.test(password);
  const variety = [hasLower, hasUpper, hasDigit, hasSymbol].filter(Boolean).length;

  score += variety * 7.5;
  if (!hasUpper) suggestions.push('Add uppercase letters.');
  if (!hasLower) suggestions.push('Add lowercase letters.');
  if (!hasDigit) suggestions.push('Add numbers.');
  if (!hasSymbol) suggestions.push('Add special characters (!@#$%^&*).');

  // Entropy bonus (up to 20 points)
  const uniqueChars = new Set(password).size;
  const uniqueRatio = uniqueChars / len;
  score += Math.min(20, uniqueRatio * 20);

  if (uniqueRatio < 0.5) suggestions.push('Avoid repeating characters too much.');

  // Penalties
  // Common password check
  if (COMMON_PASSWORDS.has(password.toLowerCase())) {
    score = Math.min(score, 5);
    suggestions.unshift('This is a commonly used password. Choose something unique.');
  }

  // Keyboard pattern check
  const lowerPw = password.toLowerCase();
  for (const pattern of KEYBOARD_PATTERNS) {
    if (lowerPw.includes(pattern)) {
      score -= 10;
      suggestions.push('Avoid keyboard patterns like "' + pattern + '".');
      break;
    }
  }

  // Sequential characters
  let sequential = 0;
  for (let i = 1; i < password.length; i++) {
    if (password.charCodeAt(i) - password.charCodeAt(i - 1) === 1) sequential++;
  }
  if (sequential >= 3) {
    score -= 10;
    suggestions.push('Avoid sequential characters (abc, 123).');
  }

  // Repeated characters (e.g., aaa, 111)
  if (/(.)\1{2,}/.test(password)) {
    score -= 10;
    suggestions.push('Avoid repeating the same character 3+ times in a row.');
  }

  // All same case
  if (password === password.toLowerCase() || password === password.toUpperCase()) {
    if (/[a-zA-Z]/.test(password)) score -= 5;
  }

  score = Math.max(0, Math.min(100, Math.round(score)));

  // Crack time estimate
  let poolSize = 0;
  if (hasLower) poolSize += 26;
  if (hasUpper) poolSize += 26;
  if (hasDigit) poolSize += 10;
  if (hasSymbol) poolSize += 33;
  if (poolSize === 0) poolSize = 26;

  const combinations = Math.pow(poolSize, len);
  // Assume 10 billion guesses/sec (modern GPU cluster)
  const seconds = combinations / 1e10 / 2;
  const crackTime = formatTime(seconds);

  let level;
  if (score >= 80) level = 'very_strong';
  else if (score >= 60) level = 'strong';
  else if (score >= 40) level = 'moderate';
  else if (score >= 20) level = 'weak';
  else level = 'very_weak';

  if (suggestions.length === 0) suggestions.push('Great password!');

  return { score, level, crack_time_estimate: crackTime, suggestions };
}

function formatTime(seconds) {
  if (seconds < 0.001) return 'instant';
  if (seconds < 1) return 'less than a second';
  if (seconds < 60) return Math.round(seconds) + ' seconds';
  if (seconds < 3600) return Math.round(seconds / 60) + ' minutes';
  if (seconds < 86400) return Math.round(seconds / 3600) + ' hours';
  if (seconds < 86400 * 365) return Math.round(seconds / 86400) + ' days';
  if (seconds < 86400 * 365 * 1000) return Math.round(seconds / (86400 * 365)) + ' years';
  if (seconds < 86400 * 365 * 1e6) return Math.round(seconds / (86400 * 365 * 1000)) + ' thousand years';
  if (seconds < 86400 * 365 * 1e9) return Math.round(seconds / (86400 * 365 * 1e6)) + ' million years';
  if (seconds < 86400 * 365 * 1e12) return Math.round(seconds / (86400 * 365 * 1e9)) + ' billion years';
  return 'centuries';
}
