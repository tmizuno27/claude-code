// Common domain typos mapped to correct domains
const TYPO_MAP = {
  // Gmail
  "gmial.com": "gmail.com",
  "gmai.com": "gmail.com",
  "gmal.com": "gmail.com",
  "gmali.com": "gmail.com",
  "gamil.com": "gmail.com",
  "gnail.com": "gmail.com",
  "gmaill.com": "gmail.com",
  "gmail.co": "gmail.com",
  "gmail.cm": "gmail.com",
  "gmail.om": "gmail.com",
  "gmail.con": "gmail.com",
  "gmail.cmo": "gmail.com",
  "gmail.vom": "gmail.com",
  "gmail.xom": "gmail.com",
  "gmail.comm": "gmail.com",
  "gmail.net": "gmail.com",
  "gmail.org": "gmail.com",
  "gmaul.com": "gmail.com",
  "gmeil.com": "gmail.com",
  "gmsil.com": "gmail.com",
  "gmqil.com": "gmail.com",
  "gimail.com": "gmail.com",
  "gemail.com": "gmail.com",
  "g]mail.com": "gmail.com",

  // Yahoo
  "yaho.com": "yahoo.com",
  "yahooo.com": "yahoo.com",
  "yhaoo.com": "yahoo.com",
  "yhoo.com": "yahoo.com",
  "yahoo.co": "yahoo.com",
  "yahoo.cm": "yahoo.com",
  "yahoo.con": "yahoo.com",
  "yahoo.om": "yahoo.com",
  "yahoo.comm": "yahoo.com",
  "yaoo.com": "yahoo.com",
  "tahoo.com": "yahoo.com",
  "uahoo.com": "yahoo.com",

  // Hotmail
  "hotmal.com": "hotmail.com",
  "hotmial.com": "hotmail.com",
  "hotmali.com": "hotmail.com",
  "hotamil.com": "hotmail.com",
  "hotmail.co": "hotmail.com",
  "hotmail.cm": "hotmail.com",
  "hotmail.con": "hotmail.com",
  "hotmail.om": "hotmail.com",
  "hotmaill.com": "hotmail.com",
  "hitmail.com": "hotmail.com",
  "htomail.com": "hotmail.com",
  "homail.com": "hotmail.com",
  "hotmai.com": "hotmail.com",

  // Outlook
  "outlok.com": "outlook.com",
  "outloo.com": "outlook.com",
  "outloook.com": "outlook.com",
  "outlool.com": "outlook.com",
  "outlook.co": "outlook.com",
  "outlook.cm": "outlook.com",
  "outlook.con": "outlook.com",
  "outlook.om": "outlook.com",
  "outllook.com": "outlook.com",
  "putlook.com": "outlook.com",
  "outtlook.com": "outlook.com",

  // Protonmail
  "protonmal.com": "protonmail.com",
  "protonmial.com": "protonmail.com",
  "protonmail.co": "protonmail.com",
  "protonmail.cm": "protonmail.com",
  "protonmail.con": "protonmail.com",
  "protonmali.com": "protonmail.com",
  "protomail.com": "protonmail.com",
  "protonmeil.com": "protonmail.com",

  // iCloud
  "icloud.co": "icloud.com",
  "icloud.cm": "icloud.com",
  "icloud.con": "icloud.com",
  "icloud.om": "icloud.com",
  "icolud.com": "icloud.com",
  "icoud.com": "icloud.com",
  "iclod.com": "icloud.com",

  // AOL
  "aol.co": "aol.com",
  "aol.cm": "aol.com",
  "aol.con": "aol.com",
  "aol.om": "aol.com",

  // Common TLD typos for any domain
  "live.co": "live.com",
  "live.cm": "live.com",
  "live.con": "live.com",
  "msn.co": "msn.com",
  "msn.cm": "msn.com",
  "msn.con": "msn.com",
  "mail.co": "mail.com",
  "mail.cm": "mail.com",
  "mail.con": "mail.com",
  "yandex.co": "yandex.com",
  "yandex.cm": "yandex.com",
  "zoho.co": "zoho.com",
  "zoho.cm": "zoho.com",
};

/**
 * Compute Levenshtein distance between two strings
 */
function levenshtein(a, b) {
  const m = a.length, n = b.length;
  if (m === 0) return n;
  if (n === 0) return m;
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1));
  for (let i = 0; i <= m; i++) dp[i][0] = i;
  for (let j = 0; j <= n; j++) dp[0][j] = j;
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = a[i - 1] === b[j - 1]
        ? dp[i - 1][j - 1]
        : 1 + Math.min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1]);
    }
  }
  return dp[m][n];
}

const COMMON_DOMAINS = [
  "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com",
  "icloud.com", "mail.com", "protonmail.com", "proton.me", "zoho.com",
  "yandex.com", "gmx.com", "live.com", "msn.com", "me.com",
  "yahoo.co.jp", "yahoo.co.uk", "hotmail.co.uk", "outlook.jp",
];

/**
 * Suggest a correction for a possibly mistyped domain.
 * Returns the suggested domain or null.
 */
export function suggestDomain(domain) {
  const d = domain.toLowerCase();
  // Direct typo map lookup
  if (TYPO_MAP[d]) return TYPO_MAP[d];
  // Levenshtein-based fuzzy match (distance <= 2)
  let best = null, bestDist = 3;
  for (const candidate of COMMON_DOMAINS) {
    if (candidate === d) return null; // exact match, no suggestion
    const dist = levenshtein(d, candidate);
    if (dist < bestDist) {
      bestDist = dist;
      best = candidate;
    }
  }
  return best;
}
