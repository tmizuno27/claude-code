"""Deploy Golden State design to otona-match.com WordPress."""
import requests
import json
import os

BASE = "https://otona-match.com/?rest_route=/wp/v2"
AUTH = ("t.mizuno27@gmail.com", "Yw4j OgFf wwzT o0mn wXQ9 TjYs")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
CSS_PATH = os.path.join(PROJECT_DIR, "theme", "css", "otona-global.css")

# Read CSS
with open(CSS_PATH, "r", encoding="utf-8") as f:
    css_content = f.read()

# Widget content = <style> + CSS + </style> + <script> for IntersectionObserver
widget_html = f"""<style>
{css_content}
</style>
<script>
document.addEventListener('DOMContentLoaded', function() {{
  var observer = new IntersectionObserver(function(entries) {{
    entries.forEach(function(entry) {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('otona-visible');
        observer.unobserve(entry.target);
      }}
    }});
  }}, {{ threshold: 0.1, rootMargin: '0px 0px -40px 0px' }});
  document.querySelectorAll('.otona-anim').forEach(function(el) {{
    observer.observe(el);
  }});
}});
</script>"""

# Top page HTML
top_page_html = """<div class="otona-hero">
  <div class="otona-hero-content">
    <span class="otona-hero-eyebrow">大人のマッチングナビ</span>
    <h1><span class="otona-gradient-text">30代からの出会い、<br>もっとスマートに。</span></h1>
    <p class="otona-hero-sub">100種類以上のマッチングアプリの中から、<br>あなたの年齢・目的にぴったりのアプリを見つけましょう。</p>
    <div class="otona-hero-buttons">
      <a href="/matching-app-ranking-2026/" class="otona-btn otona-btn-primary">おすすめランキングを見る</a>
      <a href="/category/matching-apps/" class="otona-btn otona-btn-secondary">カテゴリから探す</a>
    </div>
  </div>
  <div class="otona-scroll-indicator"><span></span></div>
</div>

<div class="otona-section otona-section--white otona-anim">
  <div class="otona-section-inner">
    <span class="otona-eyebrow">カテゴリ</span>
    <h2 class="otona-headline" style="border:none;background:none;padding:0;">6つのカテゴリから探す</h2>
    <p class="otona-subhead">目的に合わせて最適な情報をお届けします</p>
    <div class="otona-grid otona-grid--3">
      <a href="/category/matching-apps/" class="otona-tile">
        <span class="otona-tile-icon">📱</span>
        <h3>マッチングアプリ</h3>
        <p>Pairs・with・Omiaiなど<br>人気アプリを徹底比較</p>
      </a>
      <a href="/category/deaikei/" class="otona-tile">
        <span class="otona-tile-icon">🔍</span>
        <h3>出会い系サイト</h3>
        <p>ハッピーメール・PCMAXの<br>安全性と評判を調査</p>
      </a>
      <a href="/category/konkatsu/" class="otona-tile">
        <span class="otona-tile-icon">💍</span>
        <h3>婚活</h3>
        <p>婚活アプリ・結婚相談所<br>本気の婚活を全面サポート</p>
      </a>
      <a href="/category/renai-technique/" class="otona-tile">
        <span class="otona-tile-icon">💬</span>
        <h3>恋愛テクニック</h3>
        <p>プロフィール・メッセージ・<br>デートのコツを伝授</p>
      </a>
      <a href="/category/safety/" class="otona-tile">
        <span class="otona-tile-icon">🛡️</span>
        <h3>安全対策</h3>
        <p>サクラ・業者の見分け方<br>トラブル防止ガイド</p>
      </a>
      <a href="/category/reviews/" class="otona-tile">
        <span class="otona-tile-icon">📝</span>
        <h3>体験談・口コミ</h3>
        <p>実際に使った人の<br>リアルな声を紹介</p>
      </a>
    </div>
  </div>
</div>

<div class="otona-value-section otona-anim">
  <div class="otona-section-inner">
    <span class="otona-eyebrow" style="color:#2997ff;">大人のマッチングナビの特徴</span>
    <h2 class="otona-headline" style="color:#f5f5f7;border:none;background:none;padding:0;">信頼できる情報で、<br>最適な一歩を。</h2>
    <div class="otona-value-grid" style="margin-top:48px;">
      <div class="otona-value-card">
        <span class="otona-value-icon">🔬</span>
        <h3>徹底リサーチ</h3>
        <p>100以上のアプリを実際に利用・<br>調査した上で客観的に比較</p>
      </div>
      <div class="otona-value-card">
        <span class="otona-value-icon">🎯</span>
        <h3>30代・40代に特化</h3>
        <p>大人世代ならではの<br>悩み・ニーズに寄り添った情報</p>
      </div>
      <div class="otona-value-card">
        <span class="otona-value-icon">⚖️</span>
        <h3>公平な比較</h3>
        <p>料金・機能・安全性を<br>数字で客観的に評価</p>
      </div>
    </div>
  </div>
</div>

<div class="otona-stats-ribbon otona-anim">
  <div class="otona-stats-inner">
    <div class="otona-stat-item">
      <span class="otona-stat-number">20<span class="otona-stat-unit">本+</span></span>
      <span class="otona-stat-desc">レビュー記事</span>
    </div>
    <div class="otona-stat-item">
      <span class="otona-stat-number">6<span class="otona-stat-unit">カテゴリ</span></span>
      <span class="otona-stat-desc">専門カテゴリ</span>
    </div>
    <div class="otona-stat-item">
      <span class="otona-stat-number">100<span class="otona-stat-unit">+</span></span>
      <span class="otona-stat-desc">比較アプリ数</span>
    </div>
  </div>
</div>

<div class="otona-section otona-section--white otona-anim">
  <div class="otona-section-inner">
    <span class="otona-eyebrow">人気記事</span>
    <h2 class="otona-headline" style="border:none;background:none;padding:0;">よく読まれている記事</h2>
    <p class="otona-subhead">読者に人気の高い厳選記事をピックアップ</p>
    <div class="otona-articles-grid">
      <a href="/matching-app-ranking-2026/" class="otona-article-card">
        <div class="otona-article-thumb">📱</div>
        <div class="otona-article-body">
          <span class="otona-article-cat">マッチングアプリ</span>
          <h3>【2026年最新】マッチングアプリおすすめランキングTOP10</h3>
          <p class="otona-article-excerpt">目的・年齢別に人気アプリを厳選比較。初心者でも安心の1本が見つかる。</p>
        </div>
      </a>
      <a href="/matching-app-price-comparison/" class="otona-article-card">
        <div class="otona-article-thumb">💰</div>
        <div class="otona-article-body">
          <span class="otona-article-cat">マッチングアプリ</span>
          <h3>マッチングアプリの料金比較｜コスパ最強はどれ？</h3>
          <p class="otona-article-excerpt">主要10アプリの月額料金を一覧比較。Web版とアプリ版の料金差も解説。</p>
        </div>
      </a>
      <a href="/pairs-review/" class="otona-article-card">
        <div class="otona-article-thumb">💑</div>
        <div class="otona-article-body">
          <span class="otona-article-cat">マッチングアプリ</span>
          <h3>Pairs（ペアーズ）の評判・口コミを徹底調査</h3>
          <p class="otona-article-excerpt">累計2,500万人の最大級アプリ。メリット・デメリットを正直レビュー。</p>
        </div>
      </a>
      <a href="/konkatsu-app-osusume/" class="otona-article-card">
        <div class="otona-article-thumb">💍</div>
        <div class="otona-article-body">
          <span class="otona-article-cat">婚活</span>
          <h3>【2026年版】婚活アプリおすすめ5選</h3>
          <p class="otona-article-excerpt">本気で結婚したい30代・40代のための婚活アプリ完全ガイド。</p>
        </div>
      </a>
      <a href="/sakura-gyosha-miwakekata/" class="otona-article-card">
        <div class="otona-article-thumb">🛡️</div>
        <div class="otona-article-body">
          <span class="otona-article-cat">安全対策</span>
          <h3>サクラ・業者の見分け方｜騙されないための完全ガイド</h3>
          <p class="otona-article-excerpt">安全にアプリを使うために知っておくべき業者の特徴と対策。</p>
        </div>
      </a>
      <a href="/konkatsu-30dai/" class="otona-article-card">
        <div class="otona-article-thumb">✨</div>
        <div class="otona-article-body">
          <span class="otona-article-cat">婚活</span>
          <h3>30代からの婚活完全ガイド</h3>
          <p class="otona-article-excerpt">30代から始める婚活の現実と成功のコツを徹底解説。</p>
        </div>
      </a>
    </div>
  </div>
</div>

<div class="otona-cta-section otona-anim">
  <div class="otona-cta-inner">
    <h2>あなたにぴったりの<br>アプリを見つけよう</h2>
    <p>目的・年齢・予算から<br>最適なマッチングアプリを比較できます</p>
    <div class="otona-cta-buttons">
      <a href="/matching-app-ranking-2026/" class="otona-btn otona-btn-primary">おすすめランキングを見る</a>
      <a href="/category/matching-apps/" class="otona-btn otona-btn-secondary">アプリ一覧を見る</a>
    </div>
  </div>
</div>"""

# 1. Update widget
print("1. Updating CSS widget...")
r = requests.put(
    f"{BASE}/widgets/custom_html-2",
    auth=AUTH,
    json={
        "id": "custom_html-2",
        "sidebar": "sidebar",
        "instance": {
            "raw": {
                "title": "",
                "content": widget_html
            }
        }
    }
)
print(f"   Widget: {r.status_code}")
if r.status_code != 200:
    print(f"   Error: {r.text[:500]}")

# 2. Update top page
print("2. Updating top page (ID:80)...")
r2 = requests.post(
    f"{BASE}/pages/80",
    auth=AUTH,
    json={
        "content": top_page_html,
        "status": "publish"
    }
)
print(f"   Top page: {r2.status_code}")
if r2.status_code != 200:
    print(f"   Error: {r2.text[:500]}")

print("\nDone! Check https://otona-match.com/")
