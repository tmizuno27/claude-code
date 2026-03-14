#!/usr/bin/env python3
"""Deploy all pages to WordPress using CSS block references."""

import requests
import time
from base64 import b64encode

URL = 'https://nambei-oyaji.com/wp-json/wp/v2'
CREDS = b64encode('t.mizuno27@gmail.com:agNg 2624 4lL4 QoT9 EOOZ OEZr'.encode()).decode()
HEADERS = {'Authorization': f'Basic {CREDS}', 'Content-Type': 'application/json'}

BLOCK_IDS = [360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376]
BLOCK_REFS = ''.join([f'<!-- wp:block {{"ref":{bid}}} /-->\n' for bid in BLOCK_IDS])


def create_page(title, slug, content):
    r = requests.post(URL + '/pages', headers=HEADERS, json={
        'title': title, 'slug': slug, 'content': content, 'status': 'publish'
    }, timeout=30)
    if r.status_code == 201:
        pid = r.json()['id']
        print(f"  OK: {title} (ID={pid}) -> https://nambei-oyaji.com/{slug}/")
        return pid
    else:
        print(f"  FAIL: {title} - {r.status_code} {r.text[:200]}")
        return None


def main():
    print("=== Deploying pages ===\n")

    # ABOUT PAGE
    about_html = BLOCK_REFS + '<!-- wp:html -->\n<div class="nao-page">\n'
    about_html += '  <section class="nao-profile-hero nao-full">\n'
    about_html += '    <div class="nao-profile-avatar">&#129492;</div>\n'
    about_html += '    <h1>&#21335;&#31859;&#12362;&#12420;&#12376;&#65288;&#27700;&#37326; &#36948;&#20063;&#65289;</h1>\n'
    about_html += '    <p class="nao-subtitle">&#12497;&#12521;&#12464;&#12450;&#12452;&#22312;&#20303; / AI&#21103;&#26989;&#23455;&#39443;&#23478; / &#12502;&#12525;&#12460;&#12540;</p>\n'
    about_html += '    <div class="nao-profile-tags">\n'
    about_html += '      <span class="nao-profile-tag">&#127477;&#127486; &#12497;&#12521;&#12464;&#12450;&#12452;&#12539;&#12521;&#12531;&#12496;&#12524;&#22312;&#20303;</span>\n'
    about_html += '      <span class="nao-profile-tag">&#129302; AI&#27963;&#29992;&#27508; 1&#24180;</span>\n'
    about_html += '      <span class="nao-profile-tag">&#128176; &#21103;&#26989;&#21454;&#30410;&#20844;&#38283;&#20013;</span>\n'
    about_html += '    </div>\n'
    about_html += '  </section>\n'
    about_html += '  <section class="nao-bio nao-full"><div class="nao-bio-inner">\n'
    about_html += '    <h2>&#12399;&#12376;&#12417;&#12414;&#12375;&#12390;</h2>\n'
    about_html += '    <p>&#12497;&#12521;&#12464;&#12450;&#12452;&#22312;&#20303;&#12398;&#26085;&#26412;&#20154;&#12289;&#27700;&#37326;&#36948;&#20063;&#12392;&#30003;&#12375;&#12414;&#12377;&#12290;&#12371;&#12398;&#12469;&#12452;&#12488;&#12300;&#21335;&#31859;&#12362;&#12420;&#12376;&#12398;AI&#23455;&#36341;&#12521;&#12508;&#12301;&#12434;&#36939;&#21942;&#12375;&#12390;&#12356;&#12414;&#12377;&#12290;</p>\n'
    about_html += '    <p>&#21335;&#31859;&#12497;&#12521;&#12464;&#12450;&#12452;&#12395;&#31227;&#20303;&#12375;&#12390;10&#24180;&#20197;&#19978;&#12290;&#29694;&#22320;&#12391;&#12356;&#12367;&#12388;&#12363;&#12398;&#12499;&#12472;&#12493;&#12473;&#12434;&#32076;&#39443;&#12375;&#12289;2026&#24180;&#12363;&#12425;&#26412;&#26684;&#30340;&#12395;AI&#12434;&#27963;&#29992;&#12375;&#12383;&#21103;&#26989;&#23455;&#39443;&#12434;&#12473;&#12479;&#12540;&#12488;&#12375;&#12414;&#12375;&#12383;&#12290;</p>\n'
    about_html += '    <h2>&#12394;&#12380;&#12371;&#12398;&#12469;&#12452;&#12488;&#12434;&#22987;&#12417;&#12383;&#12398;&#12363;</h2>\n'
    about_html += '    <p>&#12300;&#28023;&#22806;&#12395;&#20303;&#12435;&#12391;&#12427;&#12362;&#12387;&#12373;&#12435;&#12364;&#12289;AI&#12398;&#21147;&#12434;&#20511;&#12426;&#12390;&#12393;&#12371;&#12414;&#12391;&#31292;&#12370;&#12427;&#12398;&#12363;&#65311;&#12301;</p>\n'
    about_html += '    <p>&#12371;&#12398;&#32032;&#26420;&#12394;&#30097;&#21839;&#12364;&#12289;&#12377;&#12409;&#12390;&#12398;&#22987;&#12414;&#12426;&#12391;&#12375;&#12383;&#12290;&#12383;&#12384;&#12398;&#24773;&#22577;&#12469;&#12452;&#12488;&#12391;&#12399;&#12394;&#12367;&#12289;<strong>&#23455;&#39443;&#12525;&#12464;</strong>&#12392;&#12375;&#12390;&#12522;&#12450;&#12523;&#12394;&#25968;&#23383;&#12392;&#36942;&#31243;&#12434;&#20840;&#37096;&#20844;&#38283;&#12375;&#12414;&#12377;&#12290;</p>\n'
    about_html += '    <h2>&#12371;&#12398;&#12469;&#12452;&#12488;&#12391;&#24471;&#12425;&#12428;&#12427;&#12371;&#12392;</h2>\n'
    about_html += '    <p>&#10004; AI&#12434;&#20351;&#12387;&#12383;&#21103;&#26989;&#12398;&#12522;&#12450;&#12523;&#12394;&#23455;&#36341;&#35352;&#37682;<br>&#10004; &#28023;&#22806;&#22312;&#20303;&#32773;&#12394;&#12425;&#12391;&#12399;&#12398;&#21103;&#26989;&#12494;&#12454;&#12495;&#12454;<br>&#10004; &#12497;&#12521;&#12464;&#12450;&#12452;&#12398;&#29983;&#27963;&#12539;&#31227;&#20303;&#12395;&#38306;&#12377;&#12427;&#12522;&#12450;&#12523;&#12394;&#19968;&#27425;&#24773;&#22577;<br>&#10004; &#26412;&#24403;&#12395;&#20351;&#12360;&#12427;AI&#12484;&#12540;&#12523;&#12398;&#27491;&#30452;&#12524;&#12499;&#12517;&#12540;</p>\n'
    about_html += '  </div></section>\n'
    about_html += '  <section class="nao-career nao-full"><div class="nao-career-inner">\n'
    about_html += '    <h2>&#12371;&#12428;&#12414;&#12391;&#12398;&#32076;&#27508;</h2>\n'
    about_html += '    <div class="nao-career-item"><div class="nao-career-year">2014-2015</div><div><h3>&#12469;&#12483;&#12459;&#12540;&#12463;&#12521;&#12502;&#35373;&#31435;</h3><p>&#28716;&#35895;&#12452;&#12531;&#12479;&#12540;&#12490;&#12471;&#12519;&#12490;&#12523;FC&#12290;&#12476;&#12525;&#12363;&#12425;&#20107;&#26989;&#12434;&#31435;&#12385;&#19978;&#12370;&#12427;&#32076;&#39443;&#12434;&#31309;&#12416;&#12290;</p></div></div>\n'
    about_html += '    <div class="nao-career-item"><div class="nao-career-year">2015-2019</div><div><h3>&#12497;&#12540;&#12477;&#12490;&#12523;&#12472;&#12512; &#24215;&#33303;&#36012;&#20219;&#32773;</h3><p>&#12488;&#12453;&#12456;&#12531;&#12486;&#12451;&#12540;&#12501;&#12457;&#12540;&#12475;&#12502;&#12531;&#12290;&#24215;&#33303;&#36939;&#21942;&#12539;&#12510;&#12493;&#12472;&#12513;&#12531;&#12488;&#12434;&#32076;&#39443;&#12290;</p></div></div>\n'
    about_html += '    <div class="nao-career-item"><div class="nao-career-year">2020-2021</div><div><h3>&#12522;&#12518;&#12540;&#12473;&#36031;&#26131; &#25312;&#28857;&#36012;&#20219;&#32773;</h3><p>&#19977;&#27915;&#29872;&#22659;&#12290;&#28023;&#22806;&#36031;&#26131;&#12398;&#29694;&#22580;&#12391;&#22269;&#38555;&#12499;&#12472;&#12493;&#12473;&#12434;&#23398;&#12406;&#12290;</p></div></div>\n'
    about_html += '    <div class="nao-career-item"><div class="nao-career-year">2021-2023</div><div><h3>&#20491;&#21029;&#25351;&#23566;&#22654; &#25945;&#23460;&#38263;</h3><p>D-ai&#12290;&#25945;&#32946;&#20998;&#37326;&#12391;&#12398;&#12510;&#12493;&#12472;&#12513;&#12531;&#12488;&#32076;&#39443;&#12290;</p></div></div>\n'
    about_html += '    <div class="nao-career-item"><div class="nao-career-year">2023-2025</div><div><h3>Amazon QA + &#12481;&#12540;&#12512;&#12510;&#12493;&#12540;&#12472;&#12515;&#12540;</h3><p>Sutherland Global&#12290;&#12522;&#12514;&#12540;&#12488;&#12527;&#12540;&#12463;&#215;&#21697;&#36074;&#31649;&#29702;&#12290;</p></div></div>\n'
    about_html += '    <div class="nao-career-item"><div class="nao-career-year">2025-&#29694;&#22312;</div><div><h3>&#12501;&#12522;&#12540;&#12521;&#12531;&#12473; / AI&#21103;&#26989;&#23455;&#39443;&#23478;</h3><p>&#12458;&#12531;&#12521;&#12452;&#12531;&#12475;&#12540;&#12523;&#12473; + AI&#27963;&#29992;&#12398;&#12502;&#12525;&#12464;&#36939;&#21942;&#12290;</p></div></div>\n'
    about_html += '  </div></section>\n'
    about_html += '  <section class="nao-site-info nao-full"><div class="nao-site-info-inner">\n'
    about_html += '    <h2>&#12469;&#12452;&#12488;&#24773;&#22577;</h2>\n'
    about_html += '    <div class="nao-info-grid">\n'
    about_html += '      <div class="nao-info-card"><span class="icon">&#128187;</span><h3>&#36939;&#21942;&#29872;&#22659;</h3><p>WordPress + ConoHa WING<br>&#12486;&#12540;&#12510;: Cocoon / SEO: Rank Math</p></div>\n'
    about_html += '      <div class="nao-info-card"><span class="icon">&#129302;</span><h3>AI&#27963;&#29992;</h3><p>&#35352;&#20107;&#22519;&#31558;&#35036;&#21161;: Claude API<br>KW&#35519;&#26619;: &#33258;&#20316;&#12484;&#12540;&#12523;</p></div>\n'
    about_html += '      <div class="nao-info-card"><span class="icon">&#128200;</span><h3>&#36879;&#26126;&#24615;</h3><p>&#21454;&#30410;&#12539;PV&#12539;&#20316;&#26989;&#26178;&#38291;&#12434;<br>&#27598;&#26376;&#12524;&#12509;&#12540;&#12488;&#12391;&#20844;&#38283;</p></div>\n'
    about_html += '      <div class="nao-info-card"><span class="icon">&#128172;</span><h3>&#12362;&#21839;&#12356;&#21512;&#12431;&#12379;</h3><p><a href="/contact/" style="color:#2E7D32;font-weight:700">&#12362;&#21839;&#12356;&#21512;&#12431;&#12379;&#12501;&#12457;&#12540;&#12512;</a>&#12363;&#12425;</p></div>\n'
    about_html += '    </div>\n'
    about_html += '  </div></section>\n'
    about_html += '  <section class="nao-about-cta nao-full">\n'
    about_html += '    <h2>&#23455;&#39443;&#12398;&#34892;&#26041;&#12364;&#27671;&#12395;&#12394;&#12387;&#12383;&#12425;</h2>\n'
    about_html += '    <p>&#26368;&#26032;&#12398;&#35352;&#20107;&#12420;&#12524;&#12509;&#12540;&#12488;&#12434;&#12481;&#12455;&#12483;&#12463;&#12375;&#12390;&#12367;&#12384;&#12373;&#12356;</p>\n'
    about_html += '    <a href="/category/ai/" class="nao-btn nao-btn-primary">&#35352;&#20107;&#19968;&#35239;&#12434;&#35211;&#12427; &rarr;</a>\n'
    about_html += '  </section>\n'
    about_html += '</div>\n<!-- /wp:html -->'

    pid = create_page('プロフィール', 'about', about_html)
    time.sleep(1)

    # CONTACT PAGE
    contact_html = BLOCK_REFS + '<!-- wp:html -->\n<div class="nao-contact">\n'
    contact_html += '  <h2>お問い合わせ</h2>\n'
    contact_html += '  <p>ご質問・ご感想・お仕事のご依頼など、お気軽にどうぞ。<br>通常2-3営業日以内にご返信します。</p>\n'
    contact_html += '  <div class="nao-cf">\n'
    contact_html += '    <form method="POST">\n'
    contact_html += '      <div class="nao-fg"><label>お名前<span class="req">*必須</span></label><input type="text" name="name" required placeholder="例: 山田 太郎"></div>\n'
    contact_html += '      <div class="nao-fg"><label>メールアドレス<span class="req">*必須</span></label><input type="email" name="email" required placeholder="例: your@email.com"></div>\n'
    contact_html += '      <div class="nao-fg"><label>お問い合わせ種別</label><select name="type"><option value="question">ご質問・ご相談</option><option value="feedback">ご感想</option><option value="business">お仕事のご依頼</option><option value="other">その他</option></select></div>\n'
    contact_html += '      <div class="nao-fg"><label>メッセージ<span class="req">*必須</span></label><textarea name="message" required placeholder="お問い合わせ内容をご記入ください"></textarea></div>\n'
    contact_html += '      <button type="submit" class="nao-fs">送信する</button>\n'
    contact_html += '    </form>\n'
    contact_html += '  </div>\n'
    contact_html += '  <div class="nao-cn"><h3>ご注意</h3><p>いただいたメールアドレスは、ご返信の目的のみに使用します。パラグアイとの時差があるため、ご返信に少しお時間をいただく場合があります。</p></div>\n'
    contact_html += '</div>\n<!-- /wp:html -->'

    pid = create_page('お問い合わせ', 'contact', contact_html)
    time.sleep(1)

    # PRIVACY POLICY
    privacy_html = BLOCK_REFS + '<!-- wp:html -->\n<div class="nao-legal">\n'
    privacy_html += '  <h1>プライバシーポリシー</h1>\n'
    privacy_html += '  <span class="updated">最終更新日: 2026年3月3日</span>\n'
    privacy_html += '  <p>「南米おやじのAI実践ラボ」（URL: https://nambei-oyaji.com）では、ユーザーのプライバシーを尊重し、個人情報の保護に努めています。</p>\n'
    privacy_html += '  <h2>個人情報の収集</h2><p>お問い合わせフォームにて、お名前・メールアドレス・お問い合わせ内容を取得する場合があります。</p>\n'
    privacy_html += '  <h2>個人情報の利用目的</h2><p>取得した個人情報は、お問い合わせへのご返信の目的のみに利用します。</p>\n'
    privacy_html += '  <h2>個人情報の第三者提供</h2><p>法令に基づく場合を除き、ご本人の同意なく個人情報を第三者に提供しません。</p>\n'
    privacy_html += '  <h2>Cookieの使用</h2><p>当サイトではユーザー体験の向上や効果測定のためにCookieを使用しています。</p>\n'
    privacy_html += '  <h2>アクセス解析ツール</h2><p>Googleアナリティクス（GA4）を使用しています。データは匿名で収集され、個人を特定するものではありません。</p>\n'
    privacy_html += '  <h2>広告について</h2><p>第三者配信の広告サービス（Google AdSense、A8.net等）を利用しています。</p>\n'
    privacy_html += '  <h2>アフィリエイトプログラム</h2><p>A8.net、もしもアフィリエイトに参加しています。</p>\n'
    privacy_html += '  <h2>免責事項</h2><p>当サイトの情報の正確性や安全性を保証するものではありません。</p>\n'
    privacy_html += '  <h2>著作権</h2><p>当サイトのコンテンツの著作権は運営者に帰属します。無断転載・複製を禁じます。</p>\n'
    privacy_html += '  <h2>お問い合わせ</h2><p><a href="/contact/">お問い合わせページ</a>よりお願いいたします。</p>\n'
    privacy_html += '  <p style="margin-top:40px;padding-top:20px;border-top:1px solid #E0DED6;font-size:14px;color:#666">運営者: 南米おやじのAI実践ラボ / URL: https://nambei-oyaji.com</p>\n'
    privacy_html += '</div>\n<!-- /wp:html -->'

    pid = create_page('プライバシーポリシー', 'privacy-policy', privacy_html)
    time.sleep(1)

    # SITEMAP
    sitemap_html = BLOCK_REFS + '<!-- wp:html -->\n<div class="nao-sitemap">\n'
    sitemap_html += '  <h1>サイトマップ</h1>\n'
    sitemap_html += '  <div class="nao-sitemap-section"><h2>固定ページ</h2><ul>\n'
    sitemap_html += '    <li><a href="/">トップページ</a><span class="desc"> - サイトのホーム</span></li>\n'
    sitemap_html += '    <li><a href="/about/">プロフィール</a><span class="desc"> - 運営者について</span></li>\n'
    sitemap_html += '    <li><a href="/contact/">お問い合わせ</a><span class="desc"> - ご連絡はこちら</span></li>\n'
    sitemap_html += '    <li><a href="/privacy-policy/">プライバシーポリシー</a></li>\n'
    sitemap_html += '  </ul></div>\n'
    sitemap_html += '  <div class="nao-sitemap-section"><h2>カテゴリー</h2><ul>\n'
    sitemap_html += '    <li><a href="/category/ai/">AI活用</a><span class="desc"> - AI副業の実践記録</span></li>\n'
    sitemap_html += '    <li><a href="/category/paraguay/">パラグアイ生活</a><span class="desc"> - リアルな生活情報</span></li>\n'
    sitemap_html += '    <li><a href="/category/side-business/">副業・稼ぎ方</a><span class="desc"> - 収益化ノウハウ</span></li>\n'
    sitemap_html += '    <li><a href="/category/tools/">ツール比較</a><span class="desc"> - 正直レビュー</span></li>\n'
    sitemap_html += '    <li><a href="/category/report/">実験レポート</a><span class="desc"> - 月次報告</span></li>\n'
    sitemap_html += '  </ul></div>\n'
    sitemap_html += '</div>\n<!-- /wp:html -->'

    pid = create_page('サイトマップ', 'sitemap', sitemap_html)

    print("\n=== All pages deployed! ===")


if __name__ == '__main__':
    main()
