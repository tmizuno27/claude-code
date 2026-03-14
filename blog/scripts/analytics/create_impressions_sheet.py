"""
日別インプレッション管理シートを既存スプレッドシートに追加するスクリプト
- A列: 記事タイトル（ハイパーリンク付き）
- B列: 合計インプレッション（SUM関数）
- C列以降: 日別インプレッション（3/14, 3/15, ...）
"""
import gspread
from google.oauth2.service_account import Credentials
import csv
import os
from datetime import datetime, timedelta

# 設定
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'outputs', 'article-management.csv')
SHEET_ID = os.environ.get('ARTICLE_SHEET_ID', '1rWFxYNCxyeIoW0QKXx4RsPbYfeJLp7j0bwKw8a6x6n8')
SITE_URL = 'https://nambei-oyaji.com'

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# 開始日と日数
START_DATE = datetime(2026, 3, 14)
NUM_DAYS = 90  # 約3ヶ月分の列を用意


def read_csv():
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        return list(csv.reader(f))


def connect():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SHEET_ID)


def build_impressions_sheet(rows):
    """インプレッション管理用のデータを構築"""
    data_rows = rows[1:]  # ヘッダー除外

    # ヘッダー行: A=記事タイトル, B=合計, C以降=日付
    header_fixed = ['記事タイトル', '合計']
    for i in range(NUM_DAYS):
        d = START_DATE + timedelta(days=i)
        header_fixed.append(f'{d.month}/{d.day}')

    # データ行
    sheet_data = [header_fixed]
    for idx, row in enumerate(data_rows):
        title = row[6] if len(row) > 6 else ''
        permalink = row[14] if len(row) > 14 else ''
        status = row[7] if len(row) > 7 else ''

        # 公開済み記事のみ対象にする場合はここでフィルタ（今は全記事）
        url = f'{SITE_URL}/{permalink}/' if permalink else ''

        # A列: ハイパーリンク付きタイトル
        if url:
            cell_a = f'=HYPERLINK("{url}", "{title}")'
        else:
            cell_a = title

        # B列: SUM関数（C列〜最終列）
        row_num = idx + 2  # ヘッダーが1行目
        cell_b = f'=SUM(C{row_num}:{chr(ord("A") + NUM_DAYS + 1)}{row_num})'
        # 列数が多い場合はINDIRECT使用
        last_col_num = NUM_DAYS + 2  # C列が3列目なので
        cell_b = f'=SUM(INDIRECT("C{row_num}:"&ADDRESS({row_num},{last_col_num},4)))'

        article_row = [cell_a, cell_b] + [''] * NUM_DAYS
        sheet_data.append(article_row)

    return sheet_data


def write_impressions(sh, sheet_data):
    """インプレッションシートを書き込み"""
    tab_name = '日別インプレッション'

    # 既存シートがあれば削除
    try:
        ws = sh.worksheet(tab_name)
        sh.del_worksheet(ws)
    except gspread.exceptions.WorksheetNotFound:
        pass

    num_rows = len(sheet_data) + 5
    num_cols = NUM_DAYS + 2  # A(タイトル) + B(合計) + 日数分
    ws = sh.add_worksheet(title=tab_name, rows=num_rows, cols=num_cols)

    print(f"データ書き込み中...（{len(sheet_data)-1}記事, {NUM_DAYS}日分）")
    ws.update(sheet_data, value_input_option='USER_ENTERED')

    # フォーマット設定
    requests = []

    # ヘッダー行の書式
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': ws.id,
                'startRowIndex': 0, 'endRowIndex': 1,
                'startColumnIndex': 0, 'endColumnIndex': num_cols
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.7},
                    'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'fontSize': 10},
                    'horizontalAlignment': 'CENTER',
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }
    })

    # A列幅（タイトル）
    requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 500}, 'fields': 'pixelSize'
        }
    })

    # B列幅（合計）
    requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2},
            'properties': {'pixelSize': 80}, 'fields': 'pixelSize'
        }
    })

    # 日付列幅
    requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': num_cols},
            'properties': {'pixelSize': 55}, 'fields': 'pixelSize'
        }
    })

    # ヘッダー固定（1行目 + A列）
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': ws.id,
                'gridProperties': {'frozenRowCount': 1, 'frozenColumnCount': 2}
            },
            'fields': 'gridProperties.frozenRowCount,gridProperties.frozenColumnCount'
        }
    })

    # B列（合計）の背景色を薄い黄色に
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': ws.id,
                'startRowIndex': 1, 'endRowIndex': len(sheet_data),
                'startColumnIndex': 1, 'endColumnIndex': 2
            },
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': {'red': 1.0, 'green': 0.98, 'blue': 0.8},
                    'textFormat': {'bold': True},
                    'horizontalAlignment': 'CENTER',
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }
    })

    # 日付列の中央揃え
    requests.append({
        'repeatCell': {
            'range': {
                'sheetId': ws.id,
                'startRowIndex': 1, 'endRowIndex': len(sheet_data),
                'startColumnIndex': 2, 'endColumnIndex': num_cols
            },
            'cell': {
                'userEnteredFormat': {
                    'horizontalAlignment': 'CENTER',
                    'numberFormat': {'type': 'NUMBER', 'pattern': '#,##0'}
                }
            },
            'fields': 'userEnteredFormat(horizontalAlignment,numberFormat)'
        }
    })

    # 罫線（グリッド全体）
    requests.append({
        'updateBorders': {
            'range': {
                'sheetId': ws.id,
                'startRowIndex': 0, 'endRowIndex': len(sheet_data),
                'startColumnIndex': 0, 'endColumnIndex': num_cols
            },
            'top': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'bottom': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'left': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'right': {'style': 'SOLID', 'color': {'red': 0.8, 'green': 0.8, 'blue': 0.8}},
            'innerHorizontal': {'style': 'SOLID', 'color': {'red': 0.9, 'green': 0.9, 'blue': 0.9}},
            'innerVertical': {'style': 'SOLID', 'color': {'red': 0.9, 'green': 0.9, 'blue': 0.9}},
        }
    })

    sh.batch_update({'requests': requests})

    print(f"シート「{tab_name}」作成完了")
    return ws


def main():
    print("認証中...")
    sh = connect()
    print(f"スプレッドシート: {sh.title}")

    rows = read_csv()
    sheet_data = build_impressions_sheet(rows)
    write_impressions(sh, sheet_data)

    print(f"\n完了!")
    print(f"URL: {sh.url}")
    return sh.url


if __name__ == '__main__':
    main()
