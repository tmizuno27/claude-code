"""
3サイト統合スプレッドシート管理スクリプト
- 南米おやじ / 大人のマッチングナビ / SIM比較オンライン
- 各サイト3シート（記事一覧・日別インプレッション・サマリー）= 合計9シート
- 毎朝5時にTask Schedulerから実行

使い方:
  python update_all_sheets.py              # 全サイト更新（記事一覧+サマリー+インプレッション）
  python update_all_sheets.py --init       # 全サイトのインプレッションシートを初期化
  python update_all_sheets.py --site nambei # 特定サイトのみ
"""
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account as sa_module
from googleapiclient.discovery import build
import csv
import os
import sys
import json
import time
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# ==== パス設定 ====
TOOLS_DIR = Path(__file__).parent
REPO_ROOT = TOOLS_DIR.parent
CRED_PATH = TOOLS_DIR / 'sheets-sync' / 'credentials' / 'service-account.json'
SHEET_ID = os.environ.get('ARTICLE_SHEET_ID', '1rWFxYNCxyeIoW0QKXx4RsPbYfeJLp7j0bwKw8a6x6n8')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
GSC_SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

PYT = timezone(timedelta(hours=-3))
NUM_DAYS = 90

# ==== サイト定義 ====
SITES = {
    'nambei': {
        'label': '南米おやじ',
        'csv': REPO_ROOT / 'nambei-oyaji.com' / 'outputs' / 'article-management.csv',
        'site_url': 'https://nambei-oyaji.com',
        'gsc_cred': REPO_ROOT / 'nambei-oyaji.com' / 'config' / 'gsc-credentials.json',
        'start_date': datetime(2026, 3, 5),
        'header_color': {'red': 0.2, 'green': 0.4, 'blue': 0.7},
        # CSV列マッピング (0始まり)
        'col_title': 6,
        'col_status': 7,
        'col_type': 3,
        'col_pillar': 2,
        'col_permalink': 14,
        'col_publish_date': 17,
        'col_word_count': 8,
        'col_affiliate': 11,
        'col_internal': 12,
        'col_category': 4,
        'col_kw': 5,
        'col_notes': 18,
    },
    'otona': {
        'label': 'マッチングナビ',
        'csv': REPO_ROOT / 'otona-match.com' / 'outputs' / 'article-management.csv',
        'site_url': 'https://otona-match.com',
        'gsc_cred': REPO_ROOT / 'otona-match.com' / 'config' / 'gsc-credentials.json',
        'start_date': datetime(2026, 3, 15),
        'header_color': {'red': 0.6, 'green': 0.2, 'blue': 0.5},
        # CSV: id,slug,title,status,published_date,category,type,word_count,affiliate_count,internal_links,wp_url,notes
        'col_title': 2,
        'col_status': 3,
        'col_type': 6,
        'col_pillar': None,
        'col_permalink': None,  # wp_url(10)から抽出
        'col_wp_url': 10,
        'col_publish_date': 4,
        'col_word_count': 7,
        'col_affiliate': 8,
        'col_internal': 9,
        'col_category': 5,
        'col_kw': None,
        'col_notes': 11,
    },
    'sim': {
        'label': 'SIM比較',
        'csv': REPO_ROOT / 'sim-hikaku.online' / 'outputs' / 'article-management.csv',
        'site_url': 'https://sim-hikaku.online',
        'gsc_cred': REPO_ROOT / 'sim-hikaku.online' / 'config' / 'gsc-credentials.json',
        'start_date': datetime(2026, 3, 14),
        'header_color': {'red': 0.1, 'green': 0.5, 'blue': 0.4},
        # CSV: 公開順,タイトル,ステータス,公開日,柱,記事タイプ,カテゴリ,メインKW,文字数,アフィリ数,内部リンク数,ファイル名,WordPress ID,WordPress URL,備考
        'col_title': 1,
        'col_status': 2,
        'col_type': 5,
        'col_pillar': 4,
        'col_permalink': None,
        'col_wp_url': 13,
        'col_publish_date': 3,
        'col_word_count': 8,
        'col_affiliate': 9,
        'col_internal': 10,
        'col_category': 6,
        'col_kw': 7,
        'col_notes': 14,
    },
}

TYPE_COLORS = {
    '集客記事': {'red': 0.93, 'green': 0.98, 'blue': 0.93},
    '集客': {'red': 0.93, 'green': 0.98, 'blue': 0.93},
    '収益記事': {'red': 0.93, 'green': 0.95, 'blue': 1.0},
    '収益': {'red': 0.93, 'green': 0.95, 'blue': 1.0},
    'キラー記事': {'red': 1.0, 'green': 0.96, 'blue': 0.92},
    'キラー': {'red': 1.0, 'green': 0.96, 'blue': 0.92},
    '実験記事': {'red': 0.97, 'green': 0.93, 'blue': 0.98},
    'ピラー': {'red': 0.95, 'green': 0.95, 'blue': 0.85},
}


def read_csv(path):
    with open(path, 'r', encoding='utf-8') as f:
        return list(csv.reader(f))


def safe_get(row, idx, default=''):
    if idx is None or idx >= len(row):
        return default
    return row[idx] or default


def get_url(row, site_cfg):
    """記事URLを取得（サイトごとの違いを吸収）"""
    if site_cfg.get('col_permalink') is not None:
        permalink = safe_get(row, site_cfg['col_permalink'])
        if permalink:
            return f"{site_cfg['site_url']}/{permalink}/"
    if site_cfg.get('col_wp_url') is not None:
        return safe_get(row, site_cfg['col_wp_url'])
    return ''


def connect():
    creds = Credentials.from_service_account_file(str(CRED_PATH), scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SHEET_ID)


def get_or_create_worksheet(sh, name, rows=50, cols=20):
    """既存シートを取得 or 新規作成"""
    try:
        ws = sh.worksheet(name)
        sh.del_worksheet(ws)
    except gspread.exceptions.WorksheetNotFound:
        pass
    return sh.add_worksheet(title=name, rows=rows, cols=cols)


# ===================================================================
# 記事一覧シート
# ===================================================================
def write_article_list(sh, site_key, site_cfg, rows):
    tab_name = f"{site_cfg['label']}_記事一覧"
    data_rows = rows[1:]
    print(f"  [{tab_name}] {len(data_rows)}記事")

    # 統一ヘッダー
    header = ['#', 'タイトル', 'ステータス', '公開日', '記事タイプ', 'カテゴリ', 'メインKW',
              '文字数', 'アフィリ数', '内部リンク数', 'URL', '備考']
    num_cols = len(header)
    last_col = chr(ord('A') + num_cols - 1)

    sheet_data = [header]
    for i, row in enumerate(data_rows, 1):
        title = safe_get(row, site_cfg['col_title'])
        url = get_url(row, site_cfg)
        if url and title:
            safe_title = title.replace('"', '""')
            cell_title = f'=HYPERLINK("{url}", "{safe_title}")'
        else:
            cell_title = title

        sheet_data.append([
            i,
            cell_title,
            safe_get(row, site_cfg['col_status']),
            safe_get(row, site_cfg['col_publish_date']),
            safe_get(row, site_cfg['col_type']),
            safe_get(row, site_cfg['col_category']),
            safe_get(row, site_cfg.get('col_kw')),
            safe_get(row, site_cfg['col_word_count']),
            safe_get(row, site_cfg['col_affiliate']),
            safe_get(row, site_cfg['col_internal']),
            url,
            safe_get(row, site_cfg['col_notes']),
        ])

    ws = get_or_create_worksheet(sh, tab_name, rows=len(sheet_data) + 5, cols=num_cols)
    ws.update(sheet_data, value_input_option='USER_ENTERED')

    # 全フォーマットをbatch_updateで一括適用（API呼び出し最小化）
    hc = site_cfg['header_color']
    fmt_requests = [
        # ヘッダーフォーマット
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': num_cols},
            'cell': {'userEnteredFormat': {
                'backgroundColor': hc,
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'fontSize': 10},
                'horizontalAlignment': 'CENTER',
            }},
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }},
    ]

    # 記事タイプ別の色分け（タイプごとにまとめてrepeatCell）
    type_rows = {}  # {type_name: [row_indices]}
    for i, row in enumerate(sheet_data[1:], start=1):
        atype = row[4] if len(row) > 4 else ''
        if atype in TYPE_COLORS:
            type_rows.setdefault(atype, []).append(i)

    for atype, row_indices in type_rows.items():
        color = TYPE_COLORS[atype]
        for ri in row_indices:
            fmt_requests.append({'repeatCell': {
                'range': {'sheetId': ws.id, 'startRowIndex': ri, 'endRowIndex': ri + 1, 'startColumnIndex': 0, 'endColumnIndex': num_cols},
                'cell': {'userEnteredFormat': {'backgroundColor': color}},
                'fields': 'userEnteredFormat(backgroundColor)'
            }})

    # フィルター
    fmt_requests.append({'setBasicFilter': {
        'filter': {'range': {'sheetId': ws.id, 'startRowIndex': 0, 'endRowIndex': len(sheet_data), 'startColumnIndex': 0, 'endColumnIndex': num_cols}}
    }})

    # 列幅 + ヘッダー固定
    fmt_requests.extend([
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 40}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2}, 'properties': {'pixelSize': 450}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3}, 'properties': {'pixelSize': 85}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4}, 'properties': {'pixelSize': 95}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5}, 'properties': {'pixelSize': 90}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6}, 'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 6, 'endIndex': 7}, 'properties': {'pixelSize': 200}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 7, 'endIndex': 10}, 'properties': {'pixelSize': 70}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 10, 'endIndex': 11}, 'properties': {'pixelSize': 300}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 11, 'endIndex': 12}, 'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}},
        {'updateSheetProperties': {'properties': {'sheetId': ws.id, 'gridProperties': {'frozenRowCount': 1}}, 'fields': 'gridProperties.frozenRowCount'}},
    ])
    sh.batch_update({'requests': fmt_requests})
    return ws


# ===================================================================
# サマリーシート
# ===================================================================
def write_summary(sh, site_key, site_cfg, rows):
    tab_name = f"{site_cfg['label']}_サマリー"
    data = rows[1:]
    total = len(data)

    # ステータス集計
    statuses = Counter(safe_get(r, site_cfg['col_status']) for r in data)
    # 公開済みの表現揺れ対応
    published = 0
    draft = 0
    scheduled = 0
    for k, v in statuses.items():
        kl = k.lower().strip()
        if kl in ('公開済み', '公開済', 'publish', 'published'):
            published += v
        elif kl in ('ドラフト', 'draft', '下書き'):
            draft += v
        elif kl in ('予約済', '予約済み', 'scheduled'):
            scheduled += v

    # 記事タイプ集計
    types = Counter(safe_get(r, site_cfg['col_type']) for r in data)

    # カテゴリ集計
    categories = Counter(safe_get(r, site_cfg['col_category']) for r in data)

    summary = [
        [f"{site_cfg['label']} 記事管理サマリー"],
        [''],
        ['■ 全体'],
        ['総記事数', total],
        ['公開済み', published],
    ]
    if draft:
        summary.append(['ドラフト', draft])
    if scheduled:
        summary.append(['予約済み', scheduled])

    # 柱別（あるサイトのみ）
    if site_cfg.get('col_pillar') is not None:
        pillars = Counter(safe_get(r, site_cfg['col_pillar']) for r in data)
        summary.append([''])
        summary.append(['■ 柱別', '記事数'])
        for p, cnt in pillars.most_common():
            if p:
                summary.append([p, cnt])

    # 記事タイプ別
    summary.append([''])
    summary.append(['■ 記事タイプ別', '記事数'])
    for t, cnt in types.most_common():
        if t:
            summary.append([t, cnt])

    # カテゴリ別
    summary.append([''])
    summary.append(['■ カテゴリ別', '記事数'])
    for c, cnt in categories.most_common():
        if c:
            summary.append([c, cnt])

    now = datetime.now(PYT).strftime('%Y-%m-%d %H:%M PYT')
    summary.append([''])
    summary.append([f'最終更新: {now}'])

    ws = get_or_create_worksheet(sh, tab_name, rows=max(len(summary) + 5, 35), cols=5)
    ws.update(summary, value_input_option='USER_ENTERED')

    # フォーマット
    formats = [{'range': 'A1', 'format': {'textFormat': {'bold': True, 'fontSize': 14}}}]
    for i, row in enumerate(summary, start=1):
        if row and isinstance(row[0], str) and row[0].startswith('■'):
            formats.append({'range': f'A{i}', 'format': {'textFormat': {'bold': True, 'fontSize': 11}}})
    ws.batch_format(formats)
    return ws


# ===================================================================
# 日別インプレッションシート
# ===================================================================
def connect_gsc(cred_path, site_url):
    """Search Console APIに接続（認証ファイルがなければNone）"""
    if not Path(cred_path).exists():
        # 共通サービスアカウントで試行
        if CRED_PATH.exists():
            try:
                credentials = sa_module.Credentials.from_service_account_file(
                    str(CRED_PATH), scopes=GSC_SCOPES
                )
                service = build("searchconsole", "v1", credentials=credentials)
                # テストクエリ
                service.searchanalytics().query(
                    siteUrl=site_url,
                    body={"startDate": "2026-03-01", "endDate": "2026-03-01",
                          "dimensions": ["page"], "rowLimit": 1}
                ).execute()
                return service
            except Exception:
                pass
        return None
    try:
        credentials = sa_module.Credentials.from_service_account_file(
            str(cred_path), scopes=GSC_SCOPES
        )
        service = build("searchconsole", "v1", credentials=credentials)
        return service
    except Exception as e:
        print(f"    GSC接続エラー: {e}")
        return None


def init_impressions(sh, site_key, site_cfg, rows):
    """日別インプレッションシートを初期化（空マトリックス作成）"""
    tab_name = f"{site_cfg['label']}_日別インプレッション"
    data_rows = rows[1:]
    start_date = site_cfg['start_date']
    site_url = site_cfg['site_url']

    header = ['記事タイトル', '公開日', '合計']
    for i in range(NUM_DAYS):
        d = start_date + timedelta(days=i)
        header.append(f'{d.month}/{d.day}')

    sheet_data = [header]
    num_articles = len(data_rows)
    first_row = 3
    last_row = first_row + num_articles - 1
    last_col_num = NUM_DAYS + 3

    # 合計行
    total_c = f'=SUM(C{first_row}:C{last_row})'
    total_row = ['【全記事合計】', '', total_c]
    for col in range(NUM_DAYS):
        cn = col + 4
        total_row.append(f'=SUM(INDIRECT(ADDRESS({first_row},{cn},4)&":"&ADDRESS({last_row},{cn},4)))')
    sheet_data.append(total_row)

    for idx, row in enumerate(data_rows):
        title = safe_get(row, site_cfg['col_title'])
        url = get_url(row, site_cfg)
        pub_date = safe_get(row, site_cfg['col_publish_date'])

        if url and title:
            safe_title = title.replace('"', '""')
            cell_a = f'=HYPERLINK("{url}", "{safe_title}")'
        else:
            cell_a = title

        row_num = idx + 3
        cell_c = f'=SUM(INDIRECT("D{row_num}:"&ADDRESS({row_num},{last_col_num},4)))'
        sheet_data.append([cell_a, pub_date, cell_c] + [''] * NUM_DAYS)

    num_cols = NUM_DAYS + 3
    ws = get_or_create_worksheet(sh, tab_name, rows=len(sheet_data) + 5, cols=num_cols)
    ws.update(sheet_data, value_input_option='USER_ENTERED')

    hc = site_cfg['header_color']
    requests = [
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': num_cols},
            'cell': {'userEnteredFormat': {
                'backgroundColor': hc,
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'fontSize': 10},
                'horizontalAlignment': 'CENTER',
            }},
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }},
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': 0, 'endColumnIndex': num_cols},
            'cell': {'userEnteredFormat': {
                'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 1.0},
                'textFormat': {'bold': True, 'fontSize': 10},
                'horizontalAlignment': 'CENTER',
            }},
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 450}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2}, 'properties': {'pixelSize': 90}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3}, 'properties': {'pixelSize': 80}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': num_cols}, 'properties': {'pixelSize': 55}, 'fields': 'pixelSize'}},
        {'updateSheetProperties': {
            'properties': {'sheetId': ws.id, 'gridProperties': {'frozenRowCount': 1, 'frozenColumnCount': 3}},
            'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'
        }},
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 1, 'endRowIndex': len(sheet_data), 'startColumnIndex': 2, 'endColumnIndex': 3},
            'cell': {'userEnteredFormat': {
                'backgroundColor': {'red': 1.0, 'green': 0.98, 'blue': 0.8},
                'textFormat': {'bold': True}, 'horizontalAlignment': 'CENTER',
            }},
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }},
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 1, 'endRowIndex': len(sheet_data), 'startColumnIndex': 3, 'endColumnIndex': num_cols},
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0'}}},
            'fields': 'userEnteredFormat(horizontalAlignment,numberFormat)'
        }},
    ]
    sh.batch_update({'requests': requests})
    print(f"  [{tab_name}] 初期化完了（{num_articles}記事 × {NUM_DAYS}日）")
    return ws


def update_impressions(sh, site_key, site_cfg, rows):
    """GSCからデータ取得してインプレッションシート更新"""
    tab_name = f"{site_cfg['label']}_日別インプレッション"
    site_url = site_cfg['site_url']
    start_date = site_cfg['start_date']

    # シートが存在するか確認
    try:
        ws = sh.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        print(f"  [{tab_name}] シート未作成 → --init で初期化します")
        ws = init_impressions(sh, site_key, site_cfg, rows)

    # GSC接続
    service = connect_gsc(site_cfg['gsc_cred'], site_url)
    if not service:
        print(f"  [{tab_name}] GSC認証なし → スキップ")
        return

    today = datetime.now()
    end_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    sd = start_date.strftime("%Y-%m-%d")
    if sd > end_date:
        print(f"  [{tab_name}] 開始日が未到来 → スキップ")
        return

    try:
        response = service.searchanalytics().query(
            siteUrl=site_url,
            body={
                "startDate": sd,
                "endDate": end_date,
                "dimensions": ["page", "date"],
                "rowLimit": 25000,
                "type": "web",
            },
        ).execute()
    except Exception as e:
        print(f"  [{tab_name}] GSCクエリ失敗: {e}")
        return

    gsc_data = {}
    for row in response.get("rows", []):
        page = row["keys"][0]
        date = row["keys"][1]
        impressions = row.get("impressions", 0)
        gsc_data.setdefault(page, {})[date] = impressions

    # URL→行番号マッピング
    data_rows = rows[1:]
    url_to_row = {}
    for idx, row in enumerate(data_rows):
        url = get_url(row, site_cfg)
        if url:
            url_to_row[url] = idx + 3
            url_to_row[url.rstrip('/')] = idx + 3

    def date_to_col(date_str):
        d = datetime.strptime(date_str, "%Y-%m-%d")
        delta = (d - start_date).days
        if 0 <= delta < NUM_DAYS:
            return delta + 3 + 1  # gspread 1始まり, D列=4
        return None

    cells = []
    matched = 0
    for page_url, date_data in gsc_data.items():
        rn = url_to_row.get(page_url) or url_to_row.get(page_url.rstrip('/')) or url_to_row.get(page_url + '/')
        if not rn:
            continue
        matched += 1
        for ds, imp in date_data.items():
            ci = date_to_col(ds)
            if ci:
                cells.append(gspread.Cell(rn, ci, imp))

    if cells:
        ws.update_cells(cells, value_input_option='USER_ENTERED')
        print(f"  [{tab_name}] {matched}ページ, {len(cells)}セル更新")
    else:
        print(f"  [{tab_name}] 更新データなし")


# ===================================================================
# メイン
# ===================================================================
def reorder_sheets(sh):
    """シートを 南米おやじ→マッチングナビ→SIM比較 の順に並べ替え"""
    desired_order = []
    for site_cfg in SITES.values():
        label = site_cfg['label']
        for suffix in ['_記事一覧', '_サマリー', '_日別インプレッション']:
            desired_order.append(f"{label}{suffix}")

    existing = {ws.title: ws for ws in sh.worksheets()}
    requests = []
    idx = 0
    for name in desired_order:
        ws = existing.get(name)
        if ws:
            requests.append({
                'updateSheetProperties': {
                    'properties': {'sheetId': ws.id, 'index': idx},
                    'fields': 'index'
                }
            })
            idx += 1
    if requests:
        sh.batch_update({'requests': requests})


def main():
    args = sys.argv[1:]
    init_mode = '--init' in args
    target_site = None
    for i, a in enumerate(args):
        if a == '--site' and i + 1 < len(args):
            target_site = args[i + 1]

    print("認証中...")
    sh = connect()
    print(f"スプレッドシート: {sh.title}")

    for site_key, site_cfg in SITES.items():
        if target_site and site_key != target_site:
            continue

        print(f"\n=== {site_cfg['label']} ===")

        if not site_cfg['csv'].exists():
            print(f"  CSV未検出: {site_cfg['csv']}")
            continue

        rows = read_csv(site_cfg['csv'])
        if len(rows) < 2:
            print(f"  CSVデータなし")
            continue

        # 記事一覧
        write_article_list(sh, site_key, site_cfg, rows)
        time.sleep(1)  # API rate limit対策

        # サマリー
        write_summary(sh, site_key, site_cfg, rows)
        time.sleep(1)

        # 日別インプレッション
        if init_mode:
            init_impressions(sh, site_key, site_cfg, rows)
        else:
            update_impressions(sh, site_key, site_cfg, rows)
        time.sleep(1)

    # シート順序整理
    print("\nシート順序整理中...")
    reorder_sheets(sh)

    # 旧シート名の残りを削除（既存の「記事一覧」「サマリー」「日別インプレッション」）
    for old_name in ['記事一覧', 'サマリー', '日別インプレッション']:
        try:
            old_ws = sh.worksheet(old_name)
            # 安全のため: 旧シートのデータが南米おやじの新シートにコピー済みなので削除OK
            sh.del_worksheet(old_ws)
            print(f"  旧シート「{old_name}」を削除")
        except gspread.exceptions.WorksheetNotFound:
            pass

    print(f"\n完了! URL: {sh.url}")


if __name__ == '__main__':
    main()
