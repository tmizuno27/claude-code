#!/usr/bin/env python3
"""Rebuild all pages with Apple-inspired premium design."""

import requests
import time
from base64 import b64encode

URL = 'https://nambei-oyaji.com/wp-json/wp/v2'
CREDS = b64encode(
    't.mizuno27@gmail.com:agNg 2624 4lL4 QoT9 EOOZ OEZr'.encode()
).decode()
HEADERS = {
    'Authorization': f'Basic {CREDS}',
    'Content-Type': 'application/json',
}

IMG = {
    'logo_w': 'https://nambei-oyaji.com/wp-content/uploads/2026/03/logo-white.png',
    'logotype_w': 'https://nambei-oyaji.com/wp-content/uploads/2026/03/logotype-white.png',
    'profile': 'https://nambei-oyaji.com/wp-content/uploads/2026/03/profile-avatar.png',
    'banner': 'https://nambei-oyaji.com/wp-content/uploads/2026/03/hero-banner.png',
    'family': 'https://nambei-oyaji.com/wp-content/uploads/2026/03/family-illustration.png',
}

# Will be replaced after CSS deploy
CSS_BLOCK_IDS = [360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376]
REFS = ''.join(
    [f'<!-- wp:block {{"ref":{bid}}} /-->\n' for bid in CSS_BLOCK_IDS]
)


def m_header(active='home'):
    """Mobile sticky header with logo + nav links."""
    links = {
        'home': ('/', '\u30db\u30fc\u30e0'),
        'articles': ('/category/ai/', '\u8a18\u4e8b'),
        'about': ('/about/', 'About'),
        'contact': ('/contact/', '\u304a\u554f\u3044\u5408\u308f\u305b'),
    }
    nav = ''
    for key, (url, label) in links.items():
        if key == active:
            continue
        nav += f'<a href="{url}">{label}</a>'
    return f'''<div class="nao-m-header">
    <a href="/"><img src="{IMG['logotype_w']}" alt="\u5357\u7c73\u304a\u3084\u3058"></a>
    <nav class="nao-m-header-nav">{nav}</nav>
  </div>'''


def m_bottom(primary_url, primary_label, ghost_url, ghost_label):
    """Mobile floating bottom CTA bar."""
    return f'''<div class="nao-m-bottom">
    <a href="{primary_url}" class="nao-m-btn-primary">{primary_label}</a>
    <a href="{ghost_url}" class="nao-m-btn-ghost">{ghost_label}</a>
  </div>'''


def home_html():
    return f'''<!-- wp:html -->
<div class="nao-home">

  {m_header('home')}

  <section class="nao-hero nao-full">
    <div class="nao-hero-content">
      <div class="nao-hero-eyebrow">\ud83c\uddf5\ud83c\uddfe \u30d1\u30e9\u30b0\u30a2\u30a4\u304b\u3089\u767a\u4fe1\u4e2d</div>
      <h1>\u5357\u7c73\u304a\u3084\u3058\u306e<br><em>AI\u5b9f\u8df5\u30e9\u30dc</em></h1>
      <p class="nao-hero-sub">\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f\u306e\u65e5\u672c\u4eba\u304c\u3001AI\u3092\u6b66\u5668\u306b\u526f\u696d\u3067\u3069\u3053\u307e\u3067\u7a3c\u3052\u308b\u304b\u3002\u5168\u904e\u7a0b\u3092\u516c\u958b\u3057\u307e\u3059\u3002</p>
      <div class="nao-hero-buttons">
        <a href="/category/ai/" class="nao-btn nao-btn-primary">\u8a18\u4e8b\u3092\u8aad\u3080</a>
        <a href="/about/" class="nao-btn nao-btn-ghost">\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb</a>
      </div>
      <div class="nao-hero-visual">
        <img src="{IMG['banner']}" alt="\u5357\u7c73\u304a\u3084\u3058 \u5bb6\u65cf4\u4eba\u3067\u5357\u7c73\u79fb\u4f4f">
      </div>
    </div>
  </section>

  <section class="nao-section-dark nao-full">
    <div class="nao-section-inner">
      <div class="nao-stats">
        <div class="nao-stat"><span class="nao-stat-num">\ud83c\uddf5\ud83c\uddfe</span><span class="nao-stat-label">\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f10\u5e74</span></div>
        <div class="nao-stat"><span class="nao-stat-num">AI</span><span class="nao-stat-label">\u6bce\u65e5\u30d5\u30eb\u6d3b\u7528</span></div>
        <div class="nao-stat"><span class="nao-stat-num">\u00a50\u2192</span><span class="nao-stat-label">\u30bc\u30ed\u304b\u3089\u7acb\u3061\u4e0a\u3052\u4e2d</span></div>
      </div>
    </div>
  </section>

  <section class="nao-section-light nao-full">
    <div class="nao-section-inner">
      <span class="nao-eyebrow">What We Cover</span>
      <h2 class="nao-headline">\u30ea\u30a2\u30eb\u3092\u3001<em>\u305d\u306e\u307e\u307e</em>\u3002</h2>
      <p class="nao-subhead">\u58f2\u4e0a\u3082\u5931\u6557\u3082PV\u3082\u5168\u90e8\u898b\u305b\u307e\u3059\u3002\u6d77\u5916\u00d7AI\u00d7\u526f\u696d\u306e\u30ea\u30a2\u30eb\u3092\u3001\u7f8e\u5316\u305b\u305a\u304a\u5c4a\u3051\u3057\u307e\u3059\u3002</p>
      <div class="nao-tiles">
        <div class="nao-tile"><span class="nao-tile-icon">\ud83d\udcca</span><h3>\u6570\u5b57\u3067\u5168\u516c\u958b</h3><p>\u58f2\u4e0a\u30fbPV\u30fb\u53ce\u76ca\u3092\u3059\u3079\u3066\u516c\u958b\u3002\u4e0d\u90fd\u5408\u306a\u6570\u5b57\u3082\u96a0\u3057\u307e\u305b\u3093\u3002</p></div>
        <div class="nao-tile"><span class="nao-tile-icon">\ud83e\udd16</span><h3>AI\u30d5\u30eb\u6d3b\u7528</h3><p>ChatGPT\u3001Claude\u3001\u753b\u50cf\u751f\u6210AI\u2026\u6700\u65b0\u30c4\u30fc\u30eb\u3092\u5b9f\u969b\u306b\u8a66\u3057\u3066\u30ec\u30dd\u30fc\u30c8\u3002</p></div>
        <div class="nao-tile"><span class="nao-tile-icon">\ud83c\udf0e</span><h3>\u6d77\u5916\u306e\u8996\u70b9</h3><p>\u5357\u7c73\u304b\u3089\u3053\u305d\u898b\u3048\u308b\u4e16\u754c\u3002\u8a00\u8a9e\u30fb\u6587\u5316\u30fb\u751f\u6d3b\u306e\u58c1\u3092\u8d85\u3048\u305f\u4ed5\u4e8b\u8853\u3002</p></div>
      </div>
    </div>
  </section>

  <section class="nao-section-dark nao-full">
    <div class="nao-section-inner">
      <span class="nao-eyebrow">Two Pillars</span>
      <h2 class="nao-headline">2\u3064\u306e\u30c6\u30fc\u30de\u3067\u3001<br><em>\u6df1\u304f\u5c4a\u3051\u308b</em>\u3002</h2>
      <p class="nao-subhead">\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u751f\u6d3b\u60c5\u5831\u3068\u3001AI\u526f\u696d\u306e\u5b9f\u8df5\u8a18\u9332\u3002\u3053\u306e2\u672c\u67f1\u3067\u304a\u5c4a\u3051\u3057\u307e\u3059\u3002</p>
      <div class="nao-showcase">
        <div class="nao-showcase-card --warm">
          <span class="nao-showcase-emoji">\ud83c\uddf5\ud83c\uddfe</span>
          <h3>\u30d1\u30e9\u30b0\u30a2\u30a4<br>\u751f\u6d3b\u30ac\u30a4\u30c9</h3>
          <p>\u79fb\u4f4f10\u5e74\u76ee\u306e\u7d4c\u9a13\u3092\u3082\u3068\u306b\u3001\u30cd\u30c3\u30c8\u306b\u51fa\u3066\u3053\u306a\u3044\u30ea\u30a2\u30eb\u306a\u60c5\u5831\u3092\u767a\u4fe1\u3002</p>
          <ul class="nao-showcase-list">
            <li>\u79fb\u4f4f\u306e\u8cbb\u7528\u3068\u30ea\u30a2\u30eb\u306a\u624b\u7d9a\u304d</li>
            <li>\u73fe\u5730\u306e\u751f\u6d3b\u4e8b\u60c5\u30fb\u7269\u4fa1</li>
            <li>\u6c38\u4f4f\u6a29\u53d6\u5f97\u5b8c\u5168\u30ac\u30a4\u30c9</li>
            <li>\u65e5\u672c\u4eba\u30b3\u30df\u30e5\u30cb\u30c6\u30a3\u3068\u73fe\u5730\u306e\u66ae\u3089\u3057</li>
          </ul>
        </div>
        <div class="nao-showcase-card --dark">
          <span class="nao-showcase-emoji">\ud83d\ude80</span>
          <h3>AI\u526f\u696d<br>\u30c1\u30e3\u30ec\u30f3\u30b8</h3>
          <p>AI\u30c4\u30fc\u30eb\u3092\u30d5\u30eb\u6d3b\u7528\u3057\u3066\u3001\u6d77\u5916\u304b\u3089\u65e5\u672c\u5186\u3067\u7a3c\u3050\u65b9\u6cd5\u3092\u691c\u8a3c\u3002</p>
          <ul class="nao-showcase-list">
            <li>AI\u00d7\u30d6\u30ed\u30b0\u3067\u67085\u4e07\u5186\u3092\u76ee\u6307\u3059</li>
            <li>\u6d77\u5916\u5728\u4f4f\u8005\u5411\u3051\u526f\u696d\u6bd4\u8f03</li>
            <li>\u4f7f\u3063\u3066\u5206\u304b\u3063\u305fAI\u30c4\u30fc\u30eb\u30ec\u30d3\u30e5\u30fc</li>
            <li>\u30c7\u30b8\u30bf\u30eb\u5546\u54c1\u306e\u4f5c\u308a\u65b9\u3068\u8ca9\u58f2\u6cd5</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="nao-section-warm nao-full">
    <div class="nao-section-inner">
      <span class="nao-eyebrow">Experiment Log</span>
      <h2 class="nao-headline">\u5b9f\u9a13\u30ed\u30b0\u3002</h2>
      <p class="nao-subhead">\u3053\u306e\u30b5\u30a4\u30c8\u81ea\u4f53\u304c\u5b9f\u9a13\u3002\u7acb\u3061\u4e0a\u3052\u304b\u3089\u53ce\u76ca\u5316\u307e\u3067\u306e\u5168\u5de5\u7a0b\u3092\u8a18\u9332\u3057\u307e\u3059\u3002</p>
      <div class="nao-log-timeline">
        <div class="nao-log-item"><div class="nao-log-date">2026.01</div><h4>\u30d6\u30ed\u30b0\u69cb\u60f3\u30fb\u30c9\u30e1\u30a4\u30f3\u53d6\u5f97</h4><p>\u300c\u5357\u7c73\u304a\u3084\u3058\u300d\u3092\u7acb\u3061\u4e0a\u3052\u3002WordPress\u30bb\u30c3\u30c8\u30a2\u30c3\u30d7\u3001\u30b3\u30f3\u30bb\u30d7\u30c8\u8a2d\u8a08\u3002</p></div>
        <div class="nao-log-item"><div class="nao-log-date">2026.02</div><h4>AI\u30c4\u30fc\u30eb\u691c\u8a3c\u958b\u59cb</h4><p>Claude\u3001ChatGPT\u3001Midjourney\u306a\u3069\u5404\u7a2eAI\u30c4\u30fc\u30eb\u3092\u5c0e\u5165\u3002\u52b9\u7387\u5316\u691c\u8a3c\u4e2d\u3002</p></div>
        <div class="nao-log-item"><div class="nao-log-date">2026.03</div><h4>\u30b3\u30f3\u30c6\u30f3\u30c4\u62e1\u5145\u30fb\u53ce\u76ca\u5316\u6311\u6226</h4><p>\u30a2\u30d5\u30a3\u30ea\u30a8\u30a4\u30c8\u8a18\u4e8b\u3092\u672c\u683c\u7a3c\u52d5\u3002\u521d\u53ce\u76ca\u3092\u76ee\u6307\u3057\u3066\u91cf\u7523\u4f53\u5236\u3092\u69cb\u7bc9\u4e2d\u3002</p></div>
      </div>
    </div>
  </section>

  <section class="nao-section-white nao-full">
    <div class="nao-section-inner">
      <div class="nao-about-inner">
        <div class="nao-about-avatar">
          <img src="{IMG['profile']}" alt="\u5357\u7c73\u304a\u3084\u3058" class="nao-avatar-img">
        </div>
        <div class="nao-about-text">
          <h2>\u5357\u7c73\u304a\u3084\u3058\u3068\u306f\u3002</h2>
          <p>\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f10\u5e74\u76ee\u3002\u5bb6\u65cf4\u4eba\u3067\u5357\u7c73\u79fb\u4f4f\u3057\u305f\u65e5\u672c\u4eba\u304c\u3001AI\u3092\u6b66\u5668\u306b\u526f\u696d\u306b\u6311\u6226\u4e2d\u3002\u5168\u3066\u306e\u904e\u7a0b\u3092\u30ea\u30a2\u30eb\u306b\u516c\u958b\u3057\u307e\u3059\u3002</p>
          <div class="nao-about-tags">
            <span class="nao-about-tag">\ud83c\uddf5\ud83c\uddfe \u30d1\u30e9\u30b0\u30a2\u30a4</span>
            <span class="nao-about-tag">\ud83e\udd16 AI\u6d3b\u7528</span>
            <span class="nao-about-tag">\ud83d\udc68\u200d\ud83d\udc69\u200d\ud83d\udc67\u200d\ud83d\udc66 \u5bb6\u65cf4\u4eba</span>
          </div>
          <div style="margin-top:32px">
            <a href="/about/" class="nao-link">\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb\u3092\u898b\u308b</a>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="nao-cta nao-full">
    <div class="nao-cta-inner">
      <img src="{IMG['logotype_w']}" alt="\u5357\u7c73\u304a\u3084\u3058" class="nao-cta-logo">
      <h2>\u4e00\u7dd2\u306b\u5b9f\u9a13\u3057\u307e\u305b\u3093\u304b\u3002</h2>
      <p>AI\u00d7\u6d77\u5916\u751f\u6d3b\u306e\u30ea\u30a2\u30eb\u3092\u767a\u4fe1\u4e2d\u3002</p>
      <div class="nao-cta-buttons">
        <a href="/category/ai/" class="nao-btn nao-btn-primary">\u8a18\u4e8b\u4e00\u89a7\u3078</a>
        <a href="/contact/" class="nao-btn nao-btn-ghost">\u304a\u554f\u3044\u5408\u308f\u305b</a>
      </div>
    </div>
  </section>

  {m_bottom('/category/ai/', '\u8a18\u4e8b\u3092\u8aad\u3080', '/about/', '\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb')}

</div>
<!-- /wp:html -->'''


def about_html():
    return f'''<!-- wp:html -->
<div class="nao-page">

  {m_header('about')}

  <section class="nao-profile-hero nao-full">
    <div class="nao-profile-avatar">
      <img src="{IMG['profile']}" alt="\u5357\u7c73\u304a\u3084\u3058" class="nao-avatar-img">
    </div>
    <h1>\u5357\u7c73\u304a\u3084\u3058</h1>
    <p class="nao-subtitle">\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f\u30fb\u6c34\u91ce \u9054\u4e5f</p>
    <div class="nao-profile-tags">
      <span class="nao-profile-tag">\ud83c\uddf5\ud83c\uddfe \u30d1\u30e9\u30b0\u30a2\u30a4\u30fb\u30e9\u30f3\u30d0\u30ec</span>
      <span class="nao-profile-tag">\ud83e\udd16 AI\u6d3b\u7528\u6b741\u5e74</span>
      <span class="nao-profile-tag">\ud83d\udcb0 \u526f\u696d\u53ce\u76ca\u516c\u958b\u4e2d</span>
    </div>
  </section>

  <section class="nao-family-banner nao-full">
    <img src="{IMG['family']}" alt="\u5bb6\u65cf4\u4eba\u3067\u5357\u7c73\u79fb\u4f4f" class="nao-family-img">
  </section>

  <section class="nao-bio nao-full"><div class="nao-bio-inner">
    <h2>\u306f\u3058\u3081\u307e\u3057\u3066\u3002</h2>
    <p>\u30d1\u30e9\u30b0\u30a2\u30a4\u5728\u4f4f\u306e\u65e5\u672c\u4eba\u3001\u6c34\u91ce\u9054\u4e5f\u3068\u7533\u3057\u307e\u3059\u3002\u3053\u306e\u30b5\u30a4\u30c8\u300c\u5357\u7c73\u304a\u3084\u3058\u306eAI\u5b9f\u8df5\u30e9\u30dc\u300d\u3092\u904b\u55b6\u3057\u3066\u3044\u307e\u3059\u3002</p>
    <p>\u5357\u7c73\u30d1\u30e9\u30b0\u30a2\u30a4\u306b\u79fb\u4f4f\u3057\u306610\u5e74\u4ee5\u4e0a\u3002\u73fe\u5730\u3067\u3044\u304f\u3064\u304b\u306e\u30d3\u30b8\u30cd\u30b9\u3092\u7d4c\u9a13\u3057\u30012026\u5e74\u304b\u3089\u672c\u683c\u7684\u306bAI\u3092\u6d3b\u7528\u3057\u305f\u526f\u696d\u5b9f\u9a13\u3092\u30b9\u30bf\u30fc\u30c8\u3057\u307e\u3057\u305f\u3002</p>
    <h2>\u306a\u305c\u3053\u306e\u30b5\u30a4\u30c8\u3092\u3002</h2>
    <p>\u300c\u6d77\u5916\u306b\u4f4f\u3093\u3067\u308b\u304a\u3063\u3055\u3093\u304c\u3001AI\u306e\u529b\u3092\u501f\u308a\u3066\u3069\u3053\u307e\u3067\u7a3c\u3052\u308b\u306e\u304b\uff1f\u300d</p>
    <p>\u3053\u306e\u7d20\u6734\u306a\u7591\u554f\u304c\u3001\u3059\u3079\u3066\u306e\u59cb\u307e\u308a\u3067\u3057\u305f\u3002\u305f\u3060\u306e\u60c5\u5831\u30b5\u30a4\u30c8\u3067\u306f\u306a\u304f\u3001<strong>\u5b9f\u9a13\u30ed\u30b0</strong>\u3068\u3057\u3066\u30ea\u30a2\u30eb\u306a\u6570\u5b57\u3068\u904e\u7a0b\u3092\u5168\u90e8\u516c\u958b\u3057\u307e\u3059\u3002</p>
    <h2>\u5f97\u3089\u308c\u308b\u3053\u3068\u3002</h2>
    <p>\u2714 AI\u3092\u4f7f\u3063\u305f\u526f\u696d\u306e\u30ea\u30a2\u30eb\u306a\u5b9f\u8df5\u8a18\u9332<br>\u2714 \u6d77\u5916\u5728\u4f4f\u8005\u76ee\u7dda\u306e\u751f\u6d3b\u60c5\u5831<br>\u2714 \u8a66\u884c\u932f\u8aa4\u306e\u904e\u7a0b\u3068\u5177\u4f53\u7684\u306a\u6570\u5b57<br>\u2714 \u4f7f\u3063\u3066\u672c\u5f53\u306b\u826f\u304b\u3063\u305fAI\u30c4\u30fc\u30eb\u60c5\u5831</p>
  </div></section>

  <section class="nao-career nao-full"><div class="nao-career-inner">
    <h2>\u7d4c\u6b74\u3002</h2>
    <div class="nao-career-item"><div class="nao-career-year">2014\u2013</div><div><h3>\u30b5\u30c3\u30ab\u30fc\u30af\u30e9\u30d6\u8a2d\u7acb</h3><p>\u500b\u4eba\u4e8b\u696d\u4e3b\u3068\u3057\u3066\u30b5\u30c3\u30ab\u30fc\u30af\u30e9\u30d6\u3092\u904b\u55b6</p></div></div>
    <div class="nao-career-item"><div class="nao-career-year">2015\u20132019</div><div><h3>\u30d1\u30fc\u30bd\u30ca\u30eb\u30b8\u30e0 \u5e97\u8217\u8cac\u4efb\u8005</h3><p>\u30c8\u30a5\u30a8\u30f3\u30c6\u30a3\u30fc\u30d5\u30a9\u30fc\u30bb\u30d6\u30f3\u793e\u3067\u5e97\u8217\u30de\u30cd\u30b8\u30e1\u30f3\u30c8</p></div></div>
    <div class="nao-career-item"><div class="nao-career-year">2020\u20132021</div><div><h3>\u30ea\u30e6\u30fc\u30b9\u8cbf\u6613 \u62e0\u70b9\u8cac\u4efb\u8005</h3><p>\u4e09\u6d0b\u74b0\u5883\u793e\u3067\u30ea\u30e6\u30fc\u30b9\u8cbf\u6613\u62e0\u70b9\u3092\u7d71\u62ec</p></div></div>
    <div class="nao-career-item"><div class="nao-career-year">2021\u20132023</div><div><h3>\u500b\u5225\u6307\u5c0e\u587e \u6559\u5ba4\u9577</h3><p>D-ai\u793e\u306b\u3066\u6559\u5ba4\u904b\u55b6\u30fb\u751f\u5f92\u6307\u5c0e</p></div></div>
    <div class="nao-career-item"><div class="nao-career-year">2023\u20132025</div><div><h3>Amazon QA + Team Manager</h3><p>Sutherland Global Services\u3067QA\u30fb\u30c1\u30fc\u30e0\u30de\u30cd\u30b8\u30e1\u30f3\u30c8</p></div></div>
    <div class="nao-career-item"><div class="nao-career-year">2025\u2013</div><div><h3>\u30d5\u30ea\u30fc\u30e9\u30f3\u30b9 / \u30d6\u30ed\u30ac\u30fc</h3><p>\u30aa\u30f3\u30e9\u30a4\u30f3\u30bb\u30fc\u30eb\u30b9\uff0bAI\u526f\u696d\u5b9f\u9a13\u3092\u5168\u516c\u958b</p></div></div>
  </div></section>

  <section class="nao-site-info nao-full"><div class="nao-site-info-inner">
    <h2>\u30b5\u30a4\u30c8\u60c5\u5831\u3002</h2>
    <div class="nao-info-grid">
      <div class="nao-info-card"><span class="icon">\ud83c\udf10</span><h3>\u30b5\u30a4\u30c8\u540d</h3><p>\u5357\u7c73\u304a\u3084\u3058\u306eAI\u5b9f\u8df5\u30e9\u30dc</p></div>
      <div class="nao-info-card"><span class="icon">\ud83d\udcc5</span><h3>\u958b\u8a2d</h3><p>2026\u5e741\u6708</p></div>
      <div class="nao-info-card"><span class="icon">\ud83d\udcdd</span><h3>\u30c6\u30fc\u30de</h3><p>AI\u526f\u696d\u5b9f\u9a13 / \u30d1\u30e9\u30b0\u30a2\u30a4\u751f\u6d3b</p></div>
      <div class="nao-info-card"><span class="icon">\u2709\ufe0f</span><h3>\u304a\u554f\u3044\u5408\u308f\u305b</h3><p><a href="/contact/">\u304a\u554f\u3044\u5408\u308f\u305b\u30d5\u30a9\u30fc\u30e0</a></p></div>
    </div>
  </div></section>

  <section class="nao-about-cta nao-full">
    <h2>\u4e00\u7dd2\u306b\u5b9f\u9a13\u3057\u307e\u305b\u3093\u304b\u3002</h2>
    <p>AI\u00d7\u6d77\u5916\u751f\u6d3b\u306e\u30ea\u30a2\u30eb\u3092\u767a\u4fe1\u4e2d</p>
    <a href="/" class="nao-btn nao-btn-primary">\u30c8\u30c3\u30d7\u30da\u30fc\u30b8\u3078</a>
  </section>

  {m_bottom('/', '\u30c8\u30c3\u30d7\u3078', '/contact/', '\u304a\u554f\u3044\u5408\u308f\u305b')}

</div>
<!-- /wp:html -->'''


def contact_html():
    return f'''<!-- wp:html -->
<div class="nao-page">
  {m_header('contact')}
<div class="nao-contact">
  <h2>\u304a\u554f\u3044\u5408\u308f\u305b\u3002</h2>
  <p>\u3054\u8cea\u554f\u30fb\u3054\u610f\u898b\u30fb\u304a\u4ed5\u4e8b\u306e\u3054\u76f8\u8ac7\u306a\u3069\u3001\u304a\u6c17\u8efd\u306b\u3069\u3046\u305e\u3002</p>
  <div class="nao-cf">
    <div class="nao-fg"><label>\u304a\u540d\u524d<span class="req">\u5fc5\u9808</span></label><input type="text" placeholder="\u4f8b\uff09\u5c71\u7530 \u592a\u90ce"></div>
    <div class="nao-fg"><label>\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9<span class="req">\u5fc5\u9808</span></label><input type="email" placeholder="example@mail.com"></div>
    <div class="nao-fg"><label>\u4ef6\u540d</label><input type="text" placeholder="\u4f8b\uff09\u30d6\u30ed\u30b0\u306b\u3064\u3044\u3066"></div>
    <div class="nao-fg"><label>\u30e1\u30c3\u30bb\u30fc\u30b8<span class="req">\u5fc5\u9808</span></label><textarea placeholder="\u304a\u6c17\u8efd\u306b\u304a\u66f8\u304d\u304f\u3060\u3055\u3044"></textarea></div>
    <button class="nao-fs" type="button">\u9001\u4fe1\u3059\u308b</button>
    <div class="nao-cn"><h3>\u500b\u4eba\u60c5\u5831\u306e\u304a\u53d6\u308a\u6271\u3044</h3><p>\u3054\u5165\u529b\u3044\u305f\u3060\u3044\u305f\u500b\u4eba\u60c5\u5831\u306f\u3001\u304a\u554f\u3044\u5408\u308f\u305b\u3078\u306e\u8fd4\u4fe1\u306e\u307f\u306b\u4f7f\u7528\u3044\u305f\u3057\u307e\u3059\u3002<br>\u8a73\u3057\u304f\u306f<a href="/privacy-policy/">\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30dd\u30ea\u30b7\u30fc</a>\u3092\u3054\u89a7\u304f\u3060\u3055\u3044\u3002</p></div>
  </div>
</div>
  {m_bottom('/', '\u30c8\u30c3\u30d7\u3078', '/category/ai/', '\u8a18\u4e8b\u4e00\u89a7')}
</div>
<!-- /wp:html -->'''


def privacy_html():
    return f'''<!-- wp:html -->
<div class="nao-page">
  {m_header('other')}
<div class="nao-legal">
  <h1>\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30dd\u30ea\u30b7\u30fc</h1>
  <span class="updated">\u6700\u7d42\u66f4\u65b0\uff1a2026\u5e743\u6708</span>
  <h2>\u500b\u4eba\u60c5\u5831\u306e\u53ce\u96c6</h2>
  <p>\u5f53\u30b5\u30a4\u30c8\u3067\u306f\u3001\u304a\u554f\u3044\u5408\u308f\u305b\u30d5\u30a9\u30fc\u30e0\u3084\u30b3\u30e1\u30f3\u30c8\u6b04\u3092\u901a\u3058\u3066\u3001\u304a\u540d\u524d\u30fb\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9\u7b49\u306e\u500b\u4eba\u60c5\u5831\u3092\u53ce\u96c6\u3059\u308b\u5834\u5408\u304c\u3042\u308a\u307e\u3059\u3002</p>
  <h2>\u5229\u7528\u76ee\u7684</h2>
  <ul><li>\u304a\u554f\u3044\u5408\u308f\u305b\u3078\u306e\u8fd4\u4fe1</li><li>\u30b5\u30a4\u30c8\u306e\u6539\u5584\u30fb\u904b\u55b6\u306e\u305f\u3081\u306e\u7d71\u8a08\u60c5\u5831\u306e\u53d6\u5f97</li><li>\u65b0\u3057\u3044\u30b3\u30f3\u30c6\u30f3\u30c4\u306e\u304a\u77e5\u3089\u305b</li></ul>
  <h2>\u7b2c\u4e09\u8005\u3078\u306e\u63d0\u4f9b</h2>
  <p>\u53ce\u96c6\u3057\u305f\u500b\u4eba\u60c5\u5831\u306f\u3001\u6cd5\u4ee4\u306b\u57fa\u3065\u304f\u5834\u5408\u3092\u9664\u304d\u3001\u672c\u4eba\u306e\u540c\u610f\u306a\u304f\u7b2c\u4e09\u8005\u306b\u63d0\u4f9b\u3059\u308b\u3053\u3068\u306f\u3042\u308a\u307e\u305b\u3093\u3002</p>
  <h2>\u30a2\u30af\u30bb\u30b9\u89e3\u6790\u30c4\u30fc\u30eb</h2>
  <p>\u5f53\u30b5\u30a4\u30c8\u3067\u306fGoogle Analytics\u7b49\u306e\u30a2\u30af\u30bb\u30b9\u89e3\u6790\u30c4\u30fc\u30eb\u3092\u4f7f\u7528\u3059\u308b\u5834\u5408\u304c\u3042\u308a\u307e\u3059\u3002</p>
  <h2>\u5e83\u544a\u306b\u3064\u3044\u3066</h2>
  <p>\u5f53\u30b5\u30a4\u30c8\u306f\u7b2c\u4e09\u8005\u914d\u4fe1\u306e\u5e83\u544a\u30b5\u30fc\u30d3\u30b9\uff08Google AdSense\u3001A8.net\u7b49\uff09\u3092\u5229\u7528\u3059\u308b\u5834\u5408\u304c\u3042\u308a\u307e\u3059\u3002</p>
  <h2>\u514d\u8cac\u4e8b\u9805</h2>
  <p>\u5f53\u30b5\u30a4\u30c8\u306e\u60c5\u5831\u306f\u53ef\u80fd\u306a\u9650\u308a\u6b63\u78ba\u306a\u60c5\u5831\u3092\u63b2\u8f09\u3059\u308b\u3088\u3046\u52aa\u3081\u3066\u304a\u308a\u307e\u3059\u304c\u3001\u6b63\u78ba\u6027\u3084\u5b89\u5168\u6027\u3092\u4fdd\u8a3c\u3059\u308b\u3082\u306e\u3067\u306f\u3042\u308a\u307e\u305b\u3093\u3002</p>
  <h2>\u304a\u554f\u3044\u5408\u308f\u305b</h2>
  <p>\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30dd\u30ea\u30b7\u30fc\u306b\u95a2\u3059\u308b\u304a\u554f\u3044\u5408\u308f\u305b\u306f\u3001<a href="/contact/">\u304a\u554f\u3044\u5408\u308f\u305b\u30da\u30fc\u30b8</a>\u3088\u308a\u304a\u9858\u3044\u3044\u305f\u3057\u307e\u3059\u3002</p>
</div>
  {m_bottom('/', '\u30c8\u30c3\u30d7\u3078', '/contact/', '\u304a\u554f\u3044\u5408\u308f\u305b')}
</div>
<!-- /wp:html -->'''


def sitemap_html():
    return f'''<!-- wp:html -->
<div class="nao-page">
  {m_header('other')}
<div class="nao-sitemap">
  <h1>\u30b5\u30a4\u30c8\u30de\u30c3\u30d7</h1>
  <div class="nao-sitemap-section">
    <h2>\u30e1\u30a4\u30f3\u30da\u30fc\u30b8</h2>
    <ul>
      <li><a href="/">\u30c8\u30c3\u30d7\u30da\u30fc\u30b8</a><span class="desc">\u30b5\u30a4\u30c8\u306e\u30c8\u30c3\u30d7</span></li>
      <li><a href="/about/">\u30d7\u30ed\u30d5\u30a3\u30fc\u30eb</a><span class="desc">\u5357\u7c73\u304a\u3084\u3058\u306b\u3064\u3044\u3066</span></li>
      <li><a href="/contact/">\u304a\u554f\u3044\u5408\u308f\u305b</a><span class="desc">\u304a\u6c17\u8efd\u306b\u3054\u9023\u7d61\u304f\u3060\u3055\u3044</span></li>
      <li><a href="/privacy-policy/">\u30d7\u30e9\u30a4\u30d0\u30b7\u30fc\u30dd\u30ea\u30b7\u30fc</a><span class="desc">\u500b\u4eba\u60c5\u5831\u306e\u53d6\u308a\u6271\u3044</span></li>
    </ul>
  </div>
  <div class="nao-sitemap-section">
    <h2>\u30ab\u30c6\u30b4\u30ea\u30fc</h2>
    <ul>
      <li><a href="/category/ai/">AI\u6d3b\u7528</a><span class="desc">AI\u30c4\u30fc\u30eb\u306e\u5b9f\u8df5\u30ec\u30d3\u30e5\u30fc</span></li>
      <li><a href="/category/paraguay/">\u30d1\u30e9\u30b0\u30a2\u30a4\u751f\u6d3b</a><span class="desc">\u73fe\u5730\u306e\u30ea\u30a2\u30eb\u306a\u751f\u6d3b\u60c5\u5831</span></li>
      <li><a href="/category/side-hustle/">\u526f\u696d\u30fb\u7a3c\u304e\u65b9</a><span class="desc">\u53ce\u76ca\u5316\u306e\u904e\u7a0b\u3092\u516c\u958b</span></li>
      <li><a href="/category/tools/">\u30c4\u30fc\u30eb\u6bd4\u8f03</a><span class="desc">\u5b9f\u969b\u306b\u4f7f\u3063\u305f\u30c4\u30fc\u30eb\u306e\u6bd4\u8f03</span></li>
      <li><a href="/category/experiment/">\u5b9f\u9a13\u30ec\u30dd\u30fc\u30c8</a><span class="desc">\u691c\u8a3c\u7d50\u679c\u306e\u8a73\u7d30\u30ec\u30dd\u30fc\u30c8</span></li>
    </ul>
  </div>
</div>
  {m_bottom('/', '\u30c8\u30c3\u30d7\u3078', '/category/ai/', '\u8a18\u4e8b\u4e00\u89a7')}
</div>
<!-- /wp:html -->'''


PAGES = {
    47: ('home', home_html),
    48: ('about', about_html),
    49: ('contact', contact_html),
    50: ('privacy-policy', privacy_html),
    51: ('sitemap', sitemap_html),
}


def main():
    print('=== Apple-inspired Page Rebuild ===\n')

    for pid, (slug, html_fn) in PAGES.items():
        html = html_fn()
        content = REFS + html
        r = requests.post(
            f'{URL}/pages/{pid}',
            headers=HEADERS,
            json={'content': content},
            timeout=30,
        )
        if r.status_code == 200:
            print(f'  {slug}: OK')
        else:
            print(f'  {slug}: FAILED {r.status_code}')
        time.sleep(0.5)

    print('\n=== Done! ===')


if __name__ == '__main__':
    main()
