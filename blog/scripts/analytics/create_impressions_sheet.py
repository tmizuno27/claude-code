"""
日別インプレッション管理シートをSearch Console APIから自動取得してスプレッドシートに書き込む
- --init: シートを初期化（全記事の行+日付列を作成）
- --update: Search Console APIから最新データを取得して既存シートに書き込み（デフォルト）

毎朝5時にTask Schedulerから --update で実行される想定
"""
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account as sa_module
from googleapiclient.discovery import build
import csv
import os
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# パス設定
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR / '..' / '..'
CONFIG_DIR = PROJECT_ROOT / 'config'
SHEETS_CRED_PATH = PROJECT_ROOT / '..' / 'tools' / 'sheets-sync' / 'credentials' / 'service-account.json'
GSC_CRED_PATH = CONFIG_DIR / 'gsc-credentials.json'
CSV_PATH = PROJECT_ROOT / 'outputs' / 'article-management.csv'
SETTINGS_PATH = CONFIG_DIR / 'settings.json'

SHEET_ID = os.environ.get('ARTICLE_SHEET_ID', '1rWFxYNCxyeIoW0QKXx4RsPbYfeJLp7j0bwKw8a6x6n8')
TAB_NAME = '日別インプレッション'

SHEETS_SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
GSC_SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

# 開始日（最初の記事公開日）
START_DATE = datetime(2026, 3, 5)
NUM_DAYS = 90


def read_csv():
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        return list(csv.reader(f))


def load_settings():
    with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def connect_sheets():
    creds = Credentials.from_service_account_file(str(SHEETS_CRED_PATH), scopes=SHEETS_SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SHEET_ID)


def connect_gsc(settings):
    """Search Console APIに接続"""
    sc_config = settings.get("search_console", {})
    site_url = sc_config.get("site_url", "https://nambei-oyaji.com")
    cred_path = sc_config.get("credentials_file", "gsc-credentials.json")

    cred_file = PROJECT_ROOT / cred_path if "/" in cred_path else CONFIG_DIR / cred_path
    if not cred_file.exists():
        cred_file = GSC_CRED_PATH

    credentials = sa_module.Credentials.from_service_account_file(
        str(cred_file), scopes=GSC_SCOPES
    )
    service = build("searchconsole", "v1", credentials=credentials)
    return service, site_url


def fetch_daily_impressions(service, site_url, start_date, end_date):
    """Search Console APIからページ別・日別インプレッションを取得"""
    print(f"Search Console APIからデータ取得中: {start_date} 〜 {end_date}")

    response = service.searchanalytics().query(
        siteUrl=site_url,
        body={
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": ["page", "date"],
            "rowLimit": 25000,
            "type": "web",
        },
    ).execute()

    # {page_url: {date_str: impressions}} の辞書に変換
    data = {}
    for row in response.get("rows", []):
        page = row["keys"][0]
        date = row["keys"][1]
        impressions = row.get("impressions", 0)
        if page not in data:
            data[page] = {}
        data[page][date] = impressions

    total_rows = len(response.get("rows", []))
    total_pages = len(data)
    print(f"  取得完了: {total_rows}行, {total_pages}ページ分")
    return data


def date_to_col_index(date_str):
    """日付文字列(YYYY-MM-DD)をシートの列インデックス(0始まり)に変換"""
    d = datetime.strptime(date_str, "%Y-%m-%d")
    delta = (d - START_DATE).days
    if 0 <= delta < NUM_DAYS:
        return delta + 2  # A=0, B=1, C=2(最初の日付列)
    return None


def permalink_to_url(permalink, site_url):
    """パーマリンクからフルURLを構築"""
    if not permalink:
        return ""
    return f"{site_url}/{permalink}/"


def init_sheet(sh, rows):
    """シートを初期化: 全記事の行+日付列を作成"""
    data_rows = rows[1:]
    settings = load_settings()
    site_url = settings.get("search_console", {}).get("site_url", "https://nambei-oyaji.com")

    # ヘッダー行
    header = ['記事タイトル', '合計']
    for i in range(NUM_DAYS):
        d = START_DATE + timedelta(days=i)
        header.append(f'{d.month}/{d.day}')

    sheet_data = [header]

    # 2行目: 全記事合計行（各列の合計をSUM関数で算出）
    num_articles = len(data_rows)
    first_article_row = 3  # 記事データは3行目から
    last_article_row = first_article_row + num_articles - 1
    last_col_num = NUM_DAYS + 2
    total_b = f'=SUM(B{first_article_row}:B{last_article_row})'
    total_row = ['【全記事合計】', total_b]
    for col in range(NUM_DAYS):
        col_letter_num = col + 3  # C列=3
        total_row.append(f'=SUM(INDIRECT(ADDRESS({first_article_row},{col_letter_num},4)&":"&ADDRESS({last_article_row},{col_letter_num},4)))')
    sheet_data.append(total_row)

    for idx, row in enumerate(data_rows):
        title = row[6] if len(row) > 6 else ''
        permalink = row[14] if len(row) > 14 else ''
        url = permalink_to_url(permalink, site_url)

        # ハイパーリンク付きタイトル
        if url:
            safe_title = title.replace('"', '""')
            cell_a = f'=HYPERLINK("{url}", "{safe_title}")'
        else:
            cell_a = title

        # SUM関数（3行目以降）
        row_num = idx + 3  # 1=ヘッダー, 2=合計行, 3〜=記事
        cell_b = f'=SUM(INDIRECT("C{row_num}:"&ADDRESS({row_num},{last_col_num},4)))'

        sheet_data.append([cell_a, cell_b] + [''] * NUM_DAYS)

    # シート作成
    try:
        ws = sh.worksheet(TAB_NAME)
        sh.del_worksheet(ws)
    except gspread.exceptions.WorksheetNotFound:
        pass

    num_rows = len(sheet_data) + 5
    num_cols = NUM_DAYS + 2
    ws = sh.add_worksheet(title=TAB_NAME, rows=num_rows, cols=num_cols)

    print(f"データ書き込み中...（{len(sheet_data)-1}記事, {NUM_DAYS}日分）")
    ws.update(sheet_data, value_input_option='USER_ENTERED')

    # フォーマット設定
    requests = [
        # ヘッダー書式
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': num_cols},
            'cell': {'userEnteredFormat': {
                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.7},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'fontSize': 10},
                'horizontalAlignment': 'CENTER',
            }},
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }},
        # 2行目（合計行）の書式: 太字+薄い青背景
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 1, 'endRowIndex': 2, 'startColumnIndex': 0, 'endColumnIndex': num_cols},
            'cell': {'userEnteredFormat': {
                'backgroundColor': {'red': 0.85, 'green': 0.92, 'blue': 1.0},
                'textFormat': {'bold': True, 'fontSize': 10},
                'horizontalAlignment': 'CENTER',
            }},
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }},
        # A列幅
        {'updateDimensionProperties': {
            'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 500}, 'fields': 'pixelSize'
        }},
        # B列幅
        {'updateDimensionProperties': {
            'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2},
            'properties': {'pixelSize': 80}, 'fields': 'pixelSize'
        }},
        # 日付列幅
        {'updateDimensionProperties': {
            'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': num_cols},
            'properties': {'pixelSize': 55}, 'fields': 'pixelSize'
        }},
        # 行列固定
        {'updateSheetProperties': {
            'properties': {'sheetId': ws.id, 'gridProperties': {'frozenRowCount': 1, 'frozenColumnCount': 2}},
            'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'
        }},
        # B列背景色
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 1, 'endRowIndex': len(sheet_data), 'startColumnIndex': 1, 'endColumnIndex': 2},
            'cell': {'userEnteredFormat': {
                'backgroundColor': {'red': 1.0, 'green': 0.98, 'blue': 0.8},
                'textFormat': {'bold': True}, 'horizontalAlignment': 'CENTER',
            }},
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }},
        # 日付列中央揃え
        {'repeatCell': {
            'range': {'sheetId': ws.id, 'startRowIndex': 1, 'endRowIndex': len(sheet_data), 'startColumnIndex': 2, 'endColumnIndex': num_cols},
            'cell': {'userEnteredFormat': {'horizontalAlignment': 'CENTER', 'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0'}}},
            'fields': 'userEnteredFormat(horizontalAlignment,numberFormat)'
        }},
        # 罫線
        {'updateBorders': {
            'range': {'sheetId': ws.id, 'startRowIndex': 0, 'endRowIndex': len(sheet_data), 'startColumnIndex': 0, 'endColumnIndex': num_cols},
            'top': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'bottom': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'left': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'right': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'innerHorizontal': {'style': 'SOLID', 'color': {'red': 0.9, 'green': 0.9, 'blue': 0.9}},
            'innerVertical': {'style': 'SOLID', 'color': {'red': 0.9, 'green': 0.9, 'blue': 0.9}},
        }},
    ]
    sh.batch_update({'requests': requests})
    print(f"シート「{TAB_NAME}」初期化完了")
    return ws


def update_sheet(sh, rows):
    """Search Console APIからデータを取得して既存シートに差分書き込み"""
    settings = load_settings()
    service, site_url = connect_gsc(settings)

    # GSCデータは3日遅れ → 3日前までのデータを取得
    today = datetime.now()
    end_date = (today - timedelta(days=3)).strftime("%Y-%m-%d")
    start_date = START_DATE.strftime("%Y-%m-%d")

    # 開始日が未来の場合はスキップ
    if start_date > end_date:
        print("開始日がまだ到来していないためスキップ")
        return

    gsc_data = fetch_daily_impressions(service, site_url, start_date, end_date)

    # シートを取得
    try:
        ws = sh.worksheet(TAB_NAME)
    except gspread.exceptions.WorksheetNotFound:
        print(f"シート「{TAB_NAME}」が見つかりません。--init で初期化してください")
        return

    # CSVからパーマリンク→行番号のマッピング構築
    data_rows = rows[1:]
    permalink_to_row = {}
    for idx, row in enumerate(data_rows):
        permalink = row[14] if len(row) > 14 else ''
        if permalink:
            full_url = permalink_to_url(permalink, site_url)
            permalink_to_row[full_url] = idx + 3  # シートの行番号（1=ヘッダー, 2=合計行, 3〜=記事）

            # URLの末尾スラッシュあり/なし両対応
            full_url_no_slash = full_url.rstrip('/')
            permalink_to_row[full_url_no_slash] = idx + 2

    # セル更新データを構築
    cells_to_update = []
    matched_pages = 0
    for page_url, date_data in gsc_data.items():
        # URLの正規化（末尾スラッシュなしでも照合）
        row_num = permalink_to_row.get(page_url)
        if not row_num:
            row_num = permalink_to_row.get(page_url.rstrip('/'))
        if not row_num:
            row_num = permalink_to_row.get(page_url + '/')
        if not row_num:
            continue

        matched_pages += 1
        for date_str, impressions in date_data.items():
            col_idx = date_to_col_index(date_str)
            if col_idx is None:
                continue
            cells_to_update.append(gspread.Cell(row_num, col_idx + 1, impressions))  # gspread.Cellは1始まり

    if cells_to_update:
        print(f"シート更新中: {matched_pages}ページ, {len(cells_to_update)}セル")
        # バッチ更新（API呼び出し最小化）
        ws.update_cells(cells_to_update, value_input_option='USER_ENTERED')
        print("更新完了")
    else:
        print("更新するデータがありません")

    # 未マッチのページを表示（デバッグ用）
    unmatched = [url for url in gsc_data.keys() if
                 url not in permalink_to_row and
                 url.rstrip('/') not in permalink_to_row and
                 (url + '/') not in permalink_to_row]
    if unmatched:
        print(f"\n注意: 以下の{len(unmatched)}ページはCSVに対応する記事がありません:")
        for url in unmatched[:5]:
            print(f"  - {url}")


def main():
    mode = '--update'
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    print("認証中...")
    sh = connect_sheets()
    print(f"スプレッドシート: {sh.title}")

    rows = read_csv()

    if mode == '--init':
        init_sheet(sh, rows)
    else:
        update_sheet(sh, rows)

    print(f"\n完了! URL: {sh.url}")


if __name__ == '__main__':
    main()
