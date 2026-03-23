import json, urllib.request, base64, sys
sys.stdout.reconfigure(encoding='utf-8')
creds = base64.b64encode(b't.mizuno27@gmail.com:WutS MaRq ukGx OcQ8 uhBj Ej0D').decode()

def api_call(endpoint, data=None, method='GET'):
    url = 'https://nambei-oyaji.com/wp-json/wp/v2/' + endpoint
    if data:
        payload = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(url, data=payload,
            headers={'Content-Type': 'application/json', 'Authorization': 'Basic ' + creds},
            method=method or 'POST')
    else:
        req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + creds})
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read().decode('utf-8'))

# Media IDs from upload
media = {
    'asuncion-aerial': 1101,
    'asuncion-city': 1102,
    'py-building': 1103,
    'py-nature': 1104,
    'asado': 1105,
    'bbq-cook': 1106,
    'latin-street': 1107,
    'passport1': 1108,
    'passport2': 1109,
    'air-wing': 1110,
    'rw-laptop': 1111,
    'desk-lp': 1112,
    'lp-coffee': 1113,
    'lp-silver': 1114,
    'classroom': 1115,
    'ch-desks': 1116,
    'fam-out': 1117,
    'fam-pic': 1118,
    'ch-play': 1119,
    'money-ex': 1120,
    'money-bn': 1121,
    'mob-bank': 1122,
    'cityview': 1123,
    'stars': 1124,
    'fam-park': 1125,
    'airplane-window': 1095,
    'airplane-city-view': 1096,
    'laptop-wooden-table': 1097,
    'school-children': 1098,
    'hero-landscape': 1099,
    'meat-grill': 1100,
}

# ============================================================
# Set featured images for posts
# ============================================================
post_featured = {
    1008: media['asuncion-aerial'],      # パラグアイの気候 -> アスンシオン空撮
    1065: media['passport1'],            # 移住の費用と手続き -> パスポート
    1066: media['latin-street'],         # 生活費 -> 南米の街並み
    1067: media['asuncion-city'],        # 治安 -> アスンシオンの街
    1068: media['classroom'],            # 子育て -> 教室
    1069: media['rw-laptop'],            # 海外の働き方 -> リモートワーク
    1070: media['money-ex'],             # 海外送金 -> 外貨
}

print('=== Setting featured images for posts ===')
for post_id, media_id in post_featured.items():
    try:
        result = api_call(f'posts/{post_id}', {'featured_media': media_id}, 'POST')
        print(f'OK: Post {post_id} -> Media {media_id} ({result["title"]["rendered"][:30]}...)')
    except Exception as e:
        print(f'FAIL: Post {post_id} -> {e}')

# ============================================================
# Update media titles and alt text (Japanese metadata)
# ============================================================
print('\n=== Updating media metadata ===')
media_meta = {
    1101: ('\u30a2\u30b9\u30f3\u30b7\u30aa\u30f3\u306e\u7a7a\u64ae\u5199\u771f', '\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u9996\u90fd\u30a2\u30b9\u30f3\u30b7\u30aa\u30f3\u306e\u7a7a\u304b\u3089\u306e\u5199\u771f'),
    1102: ('\u30a2\u30b9\u30f3\u30b7\u30aa\u30f3\u306e\u8857\u4e26\u307f', '\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u9996\u90fd\u30a2\u30b9\u30f3\u30b7\u30aa\u30f3\u306e\u590c\u666f'),
    1103: ('\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u5efa\u7269', '\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u767d\u3044\u5efa\u7269\u3068\u7dd1\u306e\u82d7\u5834'),
    1104: ('\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u81ea\u7136', '\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u6c34\u8fba\u3068\u7dd1\u306e\u98a8\u666f'),
    1105: ('\u30a2\u30b5\u30fc\u30c9BBQ', '\u5357\u7c73\u5f0f\u30d0\u30fc\u30d9\u30ad\u30e5\u30fc\u306e\u5199\u771f'),
    1106: ('\u30a2\u30b5\u30fc\u30c9\u8abf\u7406', '\u30b0\u30ea\u30eb\u3067\u8089\u3092\u713c\u3044\u3066\u3044\u308b\u5199\u771f'),
    1107: ('\u5357\u7c73\u306e\u8857\u4e26\u307f', '\u5357\u7c73\u306e\u6559\u4f1a\u3068\u7dd1\u306e\u6728\u3005'),
    1108: ('\u30d1\u30b9\u30dd\u30fc\u30c8\u3068\u6e21\u822a\u66f8\u985e', '\u30d1\u30b9\u30dd\u30fc\u30c8\u306e\u5199\u771f'),
    1109: ('\u30d1\u30b9\u30dd\u30fc\u30c8', '\u30d1\u30b9\u30dd\u30fc\u30c8\u30d6\u30c3\u30af'),
    1110: ('\u98db\u884c\u6a5f\u306e\u7ffc', '\u98db\u884c\u6a5f\u306e\u7ffc\u3068\u7a7a'),
    1111: ('\u30ea\u30e2\u30fc\u30c8\u30ef\u30fc\u30af', '\u30ea\u30e2\u30fc\u30c8\u30ef\u30fc\u30af\u7528\u306e\u30ce\u30fc\u30c8\u30d1\u30bd\u30b3\u30f3'),
    1112: ('\u30c7\u30b9\u30af\u30ef\u30fc\u30af', '\u30c7\u30b9\u30af\u3067\u30ce\u30fc\u30c8\u30d1\u30bd\u30b3\u30f3\u3092\u4f7f\u3046'),
    1113: ('\u30ce\u30fc\u30c8PC\u3068\u30b3\u30fc\u30d2\u30fc', '\u30ce\u30fc\u30c8\u30d1\u30bd\u30b3\u30f3\u3068\u30b3\u30fc\u30d2\u30fc'),
    1114: ('\u30b7\u30eb\u30d0\u30fc\u306e\u30ce\u30fc\u30c8PC', '\u30b7\u30eb\u30d0\u30fc\u306e\u30ce\u30fc\u30c8\u30d1\u30bd\u30b3\u30f3'),
    1115: ('\u6559\u5ba4\u306e\u98a8\u666f', '\u6559\u5ba4\u3067\u5b66\u3076\u5b50\u3069\u3082\u305f\u3061'),
    1116: ('\u6388\u696d\u4e2d\u306e\u5b50\u3069\u3082', '\u673a\u306b\u5ea7\u308b\u5b50\u3069\u3082\u305f\u3061'),
    1117: ('\u5bb6\u65cf\u304a\u51fa\u304b\u3051', '\u5c4b\u5916\u3067\u904a\u3076\u5b50\u3069\u3082\u305f\u3061'),
    1118: ('\u5b50\u3069\u3082\u305f\u3061\u306e\u81ea\u7136\u4f53\u9a13', '\u8349\u539f\u306e\u5b50\u3069\u3082\u305f\u3061'),
    1119: ('\u5b50\u3069\u3082\u306e\u904a\u3073\u5834', '\u5e83\u5834\u3067\u904a\u3076\u5b50\u3069\u3082\u305f\u3061'),
    1120: ('\u5916\u8ca8\u7d19\u5e63', '\u30c9\u30eb\u7d19\u5e63\u306e\u5199\u771f'),
    1121: ('\u5404\u56fd\u306e\u7d19\u5e63', '\u5404\u56fd\u306e\u7d19\u5e63\u306e\u5199\u771f'),
    1122: ('\u30e2\u30d0\u30a4\u30eb\u30d0\u30f3\u30ad\u30f3\u30b0', '\u7d19\u5e63\u306e\u30af\u30ed\u30fc\u30ba\u30a2\u30c3\u30d7'),
    1123: ('\u8857\u306e\u98a8\u666f', '\u9060\u304f\u304b\u3089\u898b\u305f\u8857\u306e\u98a8\u666f'),
    1124: ('\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u661f\u7a7a', '\u30d1\u30e9\u30b0\u30a2\u30a4\u306e\u7f8e\u3057\u3044\u661f\u7a7a'),
    1125: ('\u5b50\u3069\u3082\u306e\u904a\u3073', '\u5c4b\u5916\u3067\u904a\u3076\u5b50\u3069\u3082\u305f\u3061'),
    1095: ('\u98db\u884c\u6a5f\u306e\u7a93\u304b\u3089\u306e\u666f\u8272', '\u98db\u884c\u6a5f\u306e\u7a93\u304b\u3089\u898b\u305f\u96f2'),
    1096: ('\u98db\u884c\u6a5f\u304b\u3089\u306e\u8857\u306e\u666f\u8272', '\u98db\u884c\u6a5f\u306e\u7a93\u304b\u3089\u898b\u305f\u8857'),
    1097: ('\u30ce\u30fc\u30c8\u30d1\u30bd\u30b3\u30f3', '\u6728\u306e\u30c6\u30fc\u30d6\u30eb\u306e\u4e0a\u306e\u30ce\u30fc\u30c8\u30d1\u30bd\u30b3\u30f3'),
    1098: ('\u5b66\u6821\u306e\u5b50\u3069\u3082\u305f\u3061', '\u6559\u5ba4\u306e\u5b50\u3069\u3082\u305f\u3061'),
    1099: ('\u5c71\u306e\u98a8\u666f', '\u5c71\u306b\u5149\u304c\u5dee\u3059\u98a8\u666f'),
    1100: ('\u30b0\u30ea\u30eb\u8089', '\u30b0\u30ea\u30eb\u3067\u8089\u3092\u713c\u304f'),
}

for media_id, (title, alt_text) in media_meta.items():
    try:
        api_call(f'media/{media_id}', {'title': title, 'alt_text': alt_text}, 'POST')
        print(f'OK: Media {media_id} -> {title}')
    except Exception as e:
        print(f'FAIL: Media {media_id} -> {e}')

print('\nAll done!')
