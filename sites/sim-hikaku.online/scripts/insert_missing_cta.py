import requests, base64, json, re, sys

DRY_RUN = '--dry-run' in sys.argv

creds = json.load(open('C:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/sim-hikaku.online/config/secrets.json', encoding='utf-8'))
links = json.load(open('C:/Users/tmizu/マイドライブ/GitHub/claude-code/sites/sim-hikaku.online/config/affiliate-links.json', encoding='utf-8'))

wp = creds['wordpress']
auth = base64.b64encode(f"{wp['username']}:{wp['app_password']}".encode()).decode()
headers = {'Authorization': f'Basic {auth}', 'Content-Type': 'application/json'}


def cta_html(heading, url, anchor, note):
    return (
        '<div class="affiliate-cta" style="background:#f0fff4;border:1px solid #c3e6cb;'
        'border-radius:8px;padding:20px;margin:30px 0;text-align:center;">'
        f'<p style="font-weight:bold;font-size:1.1em;margin-bottom:10px;">{heading}</p>'
        f'<p><a href="{url}" rel="nofollow" target="_blank" style="display:inline-block;'
        f'background:#28a745;color:#fff;padding:12px 30px;border-radius:5px;'
        f'text-decoration:none;font-weight:bold;">{anchor}</a></p>'
        f'<p style="font-size:0.85em;color:#666;margin-top:8px;">{note}</p>'
        '</div>'
    )


def fix_url(url):
    if url and url.startswith('//'):
        return 'https:' + url
    return url


L = links  # shorthand

cta_map = {
    # 用途別格安SIM選び方 -> 光回線 + WiMAX
    13: [
        cta_html(
            '自宅のWiFiもセットで節約！ドコモ光がお得',
            fix_url(L['wifi_wimax']['gmo-dokomo-hikari']['url']),
            'GMOとくとくBB ドコモ光を見る',
            '月額料金＋セット割でさらに安くなる！キャンペーン多数'
        ),
        cta_html(
            '工事不要・すぐ使えるWiMAXも人気',
            fix_url(L['wifi_wimax']['plaio-wimax']['url']),
            'PLAIO WiMAXの詳細を見る',
            'コンセントに挿すだけ。固定回線の代わりに使える'
        )
    ],
    # サブ回線 -> eSIM
    24: [
        cta_html(
            'サブ回線にぴったり！スマホにeSIMで即開通',
            fix_url(L['esim_services']['esim-san']['url']),
            'eSIM-sanを見る',
            '最短5分で開通。海外渡航にも使える万能eSIM'
        ),
        cta_html(
            '海外でも使えるeSIMサブ回線',
            fix_url(L['esim_services']['travesim']['url']),
            'TRAVeSIM（140カ国対応）を見る',
            '国内サブ回線＆海外旅行に両対応'
        )
    ],
    # 料金比較一覧 -> 光回線 + WiMAX
    27: [
        cta_html(
            '格安SIM＋光回線セットで毎月の通信費を最適化',
            fix_url(L['wifi_wimax']['gmo-dokomo-hikari']['url']),
            'GMOとくとくBB ドコモ光を確認する',
            'ドコモ回線ユーザーならセット割でさらにお得'
        ),
        cta_html(
            '工事不要のWiMAXで自宅WiFiもカバー',
            fix_url(L['wifi_wimax']['biglobe-wimax']['url']),
            'BIGLOBE WiMAX +5Gを見る',
            '5G対応・無制限プランで速度も安心'
        )
    ],
    # 通話放題格安SIM -> WiMAX + eSIM
    81: [
        cta_html(
            'データも通話も使い放題！WiMAXで自宅WiFiも解決',
            fix_url(L['wifi_wimax']['5g-connect']['url']),
            '5G CONNECTを見る',
            '5G対応・データ無制限でがっつり使いたい人向け'
        ),
        cta_html(
            'デュアルSIM構成にeSIMを追加するのもアリ',
            fix_url(L['esim_services']['esim-san']['url']),
            'eSIM-sanを確認する',
            'メイン回線＋eSIMサブ回線で最強の通話環境を'
        )
    ],
    # 楽天モバイル評判 -> eSIM + 光回線
    106: [
        cta_html(
            '楽天モバイルと迷ったら比較！海外もeSIMで対応',
            fix_url(L['esim_services']['voye-global']['url']),
            'Voye Global（海外eSIM）を見る',
            '楽天の海外ローミングより安い！各国最低2回線対応'
        ),
        cta_html(
            '自宅WiFiもセットで節約するなら光回線',
            fix_url(L['valuecommerce']['au-hikari-vc']['url']),
            'auひかりを確認する',
            '楽天モバイルとauひかりのセット割でさらにお得に'
        )
    ],
    # LINEMO評判 -> 光回線 + WiMAX
    108: [
        cta_html(
            'LINEMOとセット割でさらにお得！SoftBank光',
            fix_url(L['valuecommerce']['softbank-hikari-vc']['url']),
            'SoftBank光の詳細を見る',
            'LINEMOとSoftBank光のセット割で月最大1,100円割引'
        ),
        cta_html(
            '工事なしで使えるWiMAXも検討しよう',
            fix_url(L['wifi_wimax']['vision-wimax']['url']),
            'VisionWiMAXを確認する',
            'コンセントに挿すだけ。引越し後もすぐ使える'
        )
    ],
    # データ無制限格安SIM -> WiMAX 2本
    116: [
        cta_html(
            'データ無制限ならWiMAXが最強コスパ！',
            fix_url(L['wifi_wimax']['plaio-wimax']['url']),
            'PLAIO WiMAXを見る（月最大12,000円還元）',
            '高額キャッシュバック＋データ無制限でコスパ最高'
        ),
        cta_html(
            '5G対応・無制限WiMAXで速度も妥協しない',
            fix_url(L['wifi_wimax']['biglobe-wimax']['url']),
            'BIGLOBE WiMAX +5Gを確認する',
            '月6,205円還元キャンペーン実施中'
        )
    ],
    # 格安SIM全社レビューまとめ(ピラー) -> 光回線 + WiMAX
    122: [
        cta_html(
            '格安SIM＋自宅WiFiをセットで最適化しよう',
            fix_url(L['wifi_wimax']['gmo-dokomo-hikari']['url']),
            'GMOとくとくBB ドコモ光を見る',
            'ドコモ系格安SIMとの組み合わせで毎月の通信費を削減'
        ),
        cta_html(
            '引越し・工事なしで使えるWiMAXも人気',
            fix_url(L['wifi_wimax']['dinomo-wifi']['url']),
            'dinomoWiFiを確認する',
            '置くだけWiFi。工事不要で最短翌日利用可能'
        )
    ],
    # ワイモバイル評判 -> 光回線 + eSIM
    269: [
        cta_html(
            'ワイモバイル＋SoftBank光でセット割最大1,100円/月',
            fix_url(L['valuecommerce']['softbank-hikari-vc']['url']),
            'SoftBank光を確認する',
            'ワイモバイルユーザーなら光回線もセット割でお得'
        ),
        cta_html(
            'ワイモバイルと迷う人へ：格安eSIMも選択肢に',
            fix_url(L['esim_services']['japanconnect-esim']['url']),
            'JapanConnect eSIMを見る',
            '訪日外国人にも人気。日本国内で使えるeSIM'
        )
    ],
    # 子供・小学生格安SIM -> eSIM + 光回線
    346: [
        cta_html(
            '子どものスマホにeSIMで簡単開通',
            fix_url(L['esim_services']['esim-san']['url']),
            'eSIM-sanを見る',
            '最短5分開通。親子で別キャリアにしても管理しやすい'
        ),
        cta_html(
            '家族全員の通信費を光回線セットで節約',
            fix_url(L['wifi_wimax']['gmo-dokomo-hikari']['url']),
            'GMOとくとくBB ドコモ光を確認する',
            'ファミリーならセット割で月々の料金をまとめてお得に'
        )
    ]
}

# 記事取得
r = requests.get(f"{wp['api_url']}/posts", headers=headers, params={'per_page': 100, 'status': 'publish'})
posts = {p['id']: p for p in r.json()}

results = []
for post_id, ctas in cta_map.items():
    p = posts.get(post_id)
    if not p:
        print(f"ID:{post_id} NOT FOUND")
        continue

    content = p['content']['rendered']
    title = p['slug']

    # 挿入位置: まとめ系セクション直前
    insert_markers = ['まとめ', '総合評価', '結論', 'よくある質問', 'FAQ', 'Q&A']
    insert_pos = -1
    found_marker = None
    for marker in insert_markers:
        pattern = f'<h[23][^>]*>[^<]*{marker}[^<]*</h[23]>'
        m = re.search(pattern, content, re.I)
        if m:
            insert_pos = m.start()
            found_marker = marker
            break

    cta_block = '\n'.join(ctas)

    if insert_pos > 0:
        new_content = content[:insert_pos] + cta_block + '\n' + content[insert_pos:]
        insert_info = f"before '{found_marker}' section at pos {insert_pos}"
    else:
        new_content = content + '\n' + cta_block
        insert_info = "appended at end"

    print(f"[{'DRY-RUN' if DRY_RUN else 'LIVE'}] ID:{post_id} ({title})")
    print(f"  -> {insert_info}")

    if not DRY_RUN:
        update = requests.post(
            f"{wp['api_url']}/posts/{post_id}",
            headers=headers,
            json={'content': new_content}
        )
        if update.status_code == 200:
            print(f"  -> SUCCESS (HTTP 200)")
        else:
            print(f"  -> ERROR {update.status_code}: {update.text[:200]}")

    results.append({'id': post_id, 'slug': title, 'insert': insert_info, 'cta_count': len(ctas)})

print(f"\n{'=== DRY-RUN COMPLETE ===' if DRY_RUN else '=== LIVE UPDATE COMPLETE ==='}")
print(f"Processed {len(results)} articles, {sum(r['cta_count'] for r in results)} CTAs total")
