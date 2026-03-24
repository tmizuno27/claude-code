const input = document.getElementById("input");
const tabs = document.querySelectorAll(".tab");
const tabContents = document.querySelectorAll(".tab-content");
const copyBtns = document.querySelectorAll(".copy-btn");

// Tab switching
tabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    tabs.forEach((t) => t.classList.remove("active"));
    tabContents.forEach((c) => c.classList.remove("active"));
    tab.classList.add("active");
    document.querySelector(`.tab-content[data-tab="${tab.dataset.tab}"]`).classList.add("active");
  });
});

// Copy buttons
copyBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const val = btn.parentElement.querySelector(".value");
    const text = val.textContent;
    if (!text || text === "\u2014") return;
    navigator.clipboard.writeText(text).then(() => {
      btn.textContent = "Done";
      btn.classList.add("copied");
      setTimeout(() => {
        btn.textContent = "Copy";
        btn.classList.remove("copied");
      }, 1200);
    });
  });
});

// MD5 (pure JS, no Web Crypto support for MD5)
function md5(str) {
  function h(a, b) { var c, d, e, f, g; e = a & 2147483648; f = b & 2147483648; c = a & 1073741824; d = b & 1073741824; g = (a & 1073741823) + (b & 1073741823); if (c & d) return g ^ 2147483648 ^ e ^ f; if (c | d) { if (g & 1073741824) return g ^ 3221225472 ^ e ^ f; else return g ^ 1073741824 ^ e ^ f; } else return g ^ e ^ f; }
  function k(a, b, c, d, e, f, g) { a = h(a, h(h(b & c | ~b & d, e), g)); return h(a << f | a >>> (32 - f), b); }
  function l(a, b, c, d, e, f, g) { a = h(a, h(h(b & d | c & ~d, e), g)); return h(a << f | a >>> (32 - f), b); }
  function m(a, b, c, d, e, f, g) { a = h(a, h(h(b ^ c ^ d, e), g)); return h(a << f | a >>> (32 - f), b); }
  function n(a, b, c, d, e, f, g) { a = h(a, h(h(c ^ (b | ~d), e), g)); return h(a << f | a >>> (32 - f), b); }
  function o(a) {
    var b = "", c, d;
    for (d = 0; d <= 3; d++) { c = a >>> d * 8 & 255; b += ("0" + c.toString(16)).slice(-2); }
    return b;
  }
  var p = [], q, r, s, t, a, b, c, d;
  var u = function(str) {
    var enc = new TextEncoder();
    var bytes = enc.encode(str);
    var arr = [];
    for (var i = 0; i < bytes.length; i++) arr.push(bytes[i]);
    return arr;
  };
  var bytes = u(str);
  var len = bytes.length;
  // padding
  bytes.push(128);
  while (bytes.length % 64 !== 56) bytes.push(0);
  var bitLen = len * 8;
  bytes.push(bitLen & 0xff, (bitLen >> 8) & 0xff, (bitLen >> 16) & 0xff, (bitLen >> 24) & 0xff, 0, 0, 0, 0);
  // words
  for (var i = 0; i < bytes.length; i += 4) {
    p.push(bytes[i] | (bytes[i + 1] << 8) | (bytes[i + 2] << 16) | (bytes[i + 3] << 24));
  }
  a = 1732584193; b = 4023233417; c = 2562383102; d = 271733878;
  for (var i = 0; i < p.length; i += 16) {
    q = a; r = b; s = c; t = d;
    a=k(a,b,c,d,p[i],7,3614090360);d=k(d,a,b,c,p[i+1],12,3905402710);c=k(c,d,a,b,p[i+2],17,606105819);b=k(b,c,d,a,p[i+3],22,3250441966);
    a=k(a,b,c,d,p[i+4],7,4118548399);d=k(d,a,b,c,p[i+5],12,1200080426);c=k(c,d,a,b,p[i+6],17,2821735955);b=k(b,c,d,a,p[i+7],22,4249261313);
    a=k(a,b,c,d,p[i+8],7,1770035416);d=k(d,a,b,c,p[i+9],12,2336552879);c=k(c,d,a,b,p[i+10],17,4294925233);b=k(b,c,d,a,p[i+11],22,2304563134);
    a=k(a,b,c,d,p[i+12],7,1804603682);d=k(d,a,b,c,p[i+13],12,4254626195);c=k(c,d,a,b,p[i+14],17,2792965006);b=k(b,c,d,a,p[i+15],22,1236535329);
    a=l(a,b,c,d,p[i+1],5,4129170786);d=l(d,a,b,c,p[i+6],9,3225465664);c=l(c,d,a,b,p[i+11],14,643717713);b=l(b,c,d,a,p[i],20,3921069994);
    a=l(a,b,c,d,p[i+5],5,3593408605);d=l(d,a,b,c,p[i+10],9,38016083);c=l(c,d,a,b,p[i+15],14,3634488961);b=l(b,c,d,a,p[i+4],20,3889429448);
    a=l(a,b,c,d,p[i+9],5,568446438);d=l(d,a,b,c,p[i+14],9,3275163606);c=l(c,d,a,b,p[i+3],14,4107603335);b=l(b,c,d,a,p[i+8],20,1163531501);
    a=l(a,b,c,d,p[i+13],5,2850285829);d=l(d,a,b,c,p[i+2],9,4243563512);c=l(c,d,a,b,p[i+7],14,1735328473);b=l(b,c,d,a,p[i+12],20,2368359562);
    a=m(a,b,c,d,p[i+5],4,4294588738);d=m(d,a,b,c,p[i+8],11,2272392833);c=m(c,d,a,b,p[i+11],16,1839030562);b=m(b,c,d,a,p[i+14],23,4259657740);
    a=m(a,b,c,d,p[i+1],4,2763975236);d=m(d,a,b,c,p[i+4],11,1272893353);c=m(c,d,a,b,p[i+7],16,4139469664);b=m(b,c,d,a,p[i+10],23,3200236656);
    a=m(a,b,c,d,p[i+13],4,681279174);d=m(d,a,b,c,p[i],11,3936430074);c=m(c,d,a,b,p[i+3],16,3572445317);b=m(b,c,d,a,p[i+6],23,76029189);
    a=m(a,b,c,d,p[i+9],4,3654602809);d=m(d,a,b,c,p[i+12],11,3873151461);c=m(c,d,a,b,p[i+15],16,530742520);b=m(b,c,d,a,p[i+2],23,3299628645);
    a=n(a,b,c,d,p[i],6,4096336452);d=n(d,a,b,c,p[i+7],10,1126891415);c=n(c,d,a,b,p[i+14],15,2878612391);b=n(b,c,d,a,p[i+5],21,4237533241);
    a=n(a,b,c,d,p[i+12],6,1700485571);d=n(d,a,b,c,p[i+3],10,2399980690);c=n(c,d,a,b,p[i+10],15,4293915773);b=n(b,c,d,a,p[i+1],21,2240044497);
    a=n(a,b,c,d,p[i+8],6,1873313359);d=n(d,a,b,c,p[i+15],10,4264355552);c=n(c,d,a,b,p[i+6],15,2734768916);b=n(b,c,d,a,p[i+3],21,1309151649);
    a=n(a,b,c,d,p[i+0],6,4149444226);d=n(d,a,b,c,p[i+7],10,3174756917);c=n(c,d,a,b,p[i+14],15,718787259);b=n(b,c,d,a,p[i+9],21,3951481745);
    a=h(a,q);b=h(b,r);c=h(c,s);d=h(d,t);
  }
  return o(a) + o(b) + o(c) + o(d);
}

// SHA hashes via Web Crypto
async function sha(algo, text) {
  const data = new TextEncoder().encode(text);
  const buf = await crypto.subtle.digest(algo, data);
  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

// Encode helpers
function base64Encode(s) {
  return btoa(unescape(encodeURIComponent(s)));
}
function base64Decode(s) {
  return decodeURIComponent(escape(atob(s)));
}
function htmlEncode(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
}
function htmlDecode(s) {
  const el = document.createElement("textarea");
  el.innerHTML = s;
  return el.value;
}
function jwtDecode(s) {
  const parts = s.split(".");
  if (parts.length !== 3) throw new Error("Invalid JWT");
  const fix = (b) => b.replace(/-/g, "+").replace(/_/g, "/");
  const header = JSON.parse(base64Decode(fix(parts[0])));
  const payload = JSON.parse(base64Decode(fix(parts[1])));
  return JSON.stringify({ header, payload }, null, 2);
}

function setVal(id, text, isError) {
  const el = document.getElementById(id);
  el.textContent = text;
  el.classList.toggle("error", !!isError);
}

function tryOr(fn, id) {
  try {
    setVal(id, fn());
  } catch {
    setVal(id, "Invalid input", true);
  }
}

async function processInput() {
  const text = input.value;
  if (!text) {
    document.querySelectorAll(".value").forEach((v) => { v.textContent = "\u2014"; v.classList.remove("error"); });
    return;
  }

  // Hashes
  setVal("out-md5", md5(text));
  sha("SHA-1", text).then((h) => setVal("out-sha1", h));
  sha("SHA-256", text).then((h) => setVal("out-sha256", h));
  sha("SHA-512", text).then((h) => setVal("out-sha512", h));

  // Encode
  tryOr(() => base64Encode(text), "out-base64enc");
  tryOr(() => encodeURIComponent(text), "out-urlenc");
  tryOr(() => htmlEncode(text), "out-htmlenc");

  // Decode
  tryOr(() => base64Decode(text), "out-base64dec");
  tryOr(() => decodeURIComponent(text), "out-urldec");
  tryOr(() => htmlDecode(text), "out-htmldec");
  tryOr(() => jwtDecode(text), "out-jwt");
}

input.addEventListener("input", processInput);

// Load selected text from context menu
document.addEventListener("DOMContentLoaded", () => {
  if (chrome.storage && chrome.storage.local) {
    chrome.storage.local.get("selectedText", (data) => {
      if (chrome.runtime.lastError) return;
      if (data && data.selectedText) {
        input.value = data.selectedText;
        chrome.storage.local.remove("selectedText");
        processInput();
      }
    });
  }
});
