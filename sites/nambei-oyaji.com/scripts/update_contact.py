"""お問い合わせページにフォームを追加する"""
import requests
import json
import base64
import re

with open('config/wp-credentials.json', encoding='utf-8') as f:
    creds = json.load(f)

auth = base64.b64encode(f"{creds['username']}:{creds['app_password']}".encode()).decode()
headers = {
    'Authorization': f'Basic {auth}',
    'Content-Type': 'application/json'
}

# Get current content
r = requests.get(f"{creds['api_base']}/pages/1890?context=edit", headers=headers)
old_content = r.json()['content']['raw']

# Extract existing style/script blocks
style_blocks = re.findall(r'<script>.*?</script>|<style>.*?</style>', old_content, re.DOTALL)
header_css = '\n'.join(style_blocks)

form_css = """<style>
.nao-contact-form{max-width:600px;margin:0 auto 40px}
.nao-contact-form label{display:block;font-size:14px;font-weight:600;color:#1d1d1f;margin:0 0 6px;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif}
.nao-contact-form .required{color:#ff3b30;font-size:12px;margin-left:4px}
.nao-contact-form input[type=text],.nao-contact-form input[type=email],.nao-contact-form textarea{width:100%;padding:12px 16px;font-size:16px;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif;border:1px solid #d2d2d7;border-radius:8px;background:#fff;color:#1d1d1f;transition:border-color .2s;box-sizing:border-box;-webkit-appearance:none}
.nao-contact-form input:focus,.nao-contact-form textarea:focus{outline:none;border-color:#0071e3;box-shadow:0 0 0 3px rgba(0,113,227,.15)}
.nao-contact-form textarea{min-height:200px;resize:vertical;line-height:1.8}
.nao-contact-form .form-group{margin:0 0 24px}
.nao-contact-form button{display:inline-flex;align-items:center;justify-content:center;width:100%;padding:14px 32px;font-size:16px;font-weight:600;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN",sans-serif;color:#fff;background:#0071e3;border:none;border-radius:8px;cursor:pointer;transition:background .2s}
.nao-contact-form button:hover{background:#0077ED}
.nao-contact-privacy{font-size:13px;color:#86868b;text-align:center;margin:16px 0 0;line-height:1.8}
@media(max-width:734px){
.nao-contact-form{padding:0 4px}
.nao-contact-form input[type=text],.nao-contact-form input[type=email],.nao-contact-form textarea{font-size:16px}
}
</style>"""

form_html = """<p>当サイト「南米おやじの海外生活ラボ」へのお問い合わせは、下記フォームよりお気軽にご連絡ください。</p>

<h2>お問い合わせフォーム</h2>

<div class="nao-contact-form">
<form action="https://formsubmit.co/t.mizuno27@gmail.com" method="POST">
<input type="hidden" name="_subject" value="【南米おやじ】お問い合わせ">
<input type="hidden" name="_captcha" value="true">
<input type="hidden" name="_next" value="https://nambei-oyaji.com/contact/">
<input type="hidden" name="_template" value="table">
<input type="text" name="_honey" style="display:none">

<div class="form-group">
<label>お名前<span class="required">*必須</span></label>
<input type="text" name="name" placeholder="山田 太郎" required>
</div>

<div class="form-group">
<label>メールアドレス<span class="required">*必須</span></label>
<input type="email" name="email" placeholder="example@email.com" required>
</div>

<div class="form-group">
<label>お問い合わせの種類</label>
<input type="text" name="category" placeholder="例：移住相談 / 取材依頼 / 広告掲載 / その他">
</div>

<div class="form-group">
<label>お問い合わせ内容<span class="required">*必須</span></label>
<textarea name="message" placeholder="お問い合わせ内容をご記入ください" required></textarea>
</div>

<button type="submit">送信する</button>
<p class="nao-contact-privacy">※ 通常2〜3営業日以内にご返信いたします。<br>パラグアイはUTC-3（日本との時差12時間）のため、お時間をいただく場合があります。</p>
</form>
</div>

<h2>X（Twitter）でのお問い合わせ</h2>
<p>お急ぎの方はXのDMでもお受けしています。</p>
<p><strong>X アカウント</strong>: <a rel="noopener" href="https://x.com/nambei_oyaji" target="_blank">@nambei_oyaji</a></p>

<h2>お問い合わせの前に</h2>
<ul>
<li>パラグアイ移住に関するご質問は、まず<a href="https://nambei-oyaji.com/category/paraguay/">パラグアイ生活カテゴリ</a>の記事をご確認ください</li>
<li>海外からの仕事・副業については、<a href="https://nambei-oyaji.com/category/side-business/">海外からの稼ぎ方カテゴリ</a>をご覧ください</li>
<li>ビザ・永住権・送金などは、<a href="https://nambei-oyaji.com/category/ijuu-junbi/">お金と手続きカテゴリ</a>をチェックしてください</li>
</ul>

<h2>お仕事のご依頼</h2>
<p>以下のようなお仕事のご依頼も受け付けています。</p>
<ul>
<li>パラグアイ移住に関する取材・インタビュー</li>
<li>海外生活・移住関連の記事執筆・監修</li>
<li>広告掲載・タイアップ記事</li>
</ul>

<h2>注意事項</h2>
<ul>
<li>法律・税務・ビザに関する専門的なアドバイスは行っておりません。必ず専門家にご相談ください</li>
<li>営業目的のメッセージにはお返事しかねます</li>
</ul>"""

new_content = header_css + '\n' + form_css + '\n' + form_html

r = requests.post(
    f"{creds['api_base']}/pages/1890",
    headers=headers,
    json={'content': new_content, 'comment_status': 'closed'}
)
print(f'Status: {r.status_code}')
if r.status_code != 200:
    print(r.text[:500])
else:
    print('Contact page updated successfully')
