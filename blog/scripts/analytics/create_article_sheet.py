"""
記事管理表をGoogleスプレッドシートに書き込むスクリプト
- full: 全データを再構築（記事一覧 + サマリー）
- add:  CSVに1行追加してシートを更新
サマリーはCSVデータから毎回自動集計する
"""
import gspread
from google.oauth2.service_account import Credentials
import csv
import os
from collections import Counter, OrderedDict

# 設定
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools', 'sheets-sync', 'credentials', 'service-account.json')
CSV_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'outputs', 'article-management.csv')
SHEET_ID = os.environ.get('ARTICLE_SHEET_ID', '1rWFxYNCxyeIoW0QKXx4RsPbYfeJLp7j0bwKw8a6x6n8')

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

TYPE_COLORS = {
    '集客記事': {'red': 0.93, 'green': 0.98, 'blue': 0.93},
    '収益記事': {'red': 0.93, 'green': 0.95, 'blue': 1.0},
    'キラー記事': {'red': 1.0, 'green': 0.96, 'blue': 0.92},
    '実験記事': {'red': 0.97, 'green': 0.93, 'blue': 0.98},
}

TYPE_ROLES = {
    '集客記事': 'PV獲得・ドメインパワー強化',
    '収益記事': 'アフィリエイト成約',
    'キラー記事': '高単価アフィリ集中',
    '実験記事': 'ファン獲得・信頼構築',
}


def read_csv():
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        return list(csv.reader(f))


def build_summary(rows):
    """CSVデータからサマリーを自動集計"""
    data = rows[1:]  # ヘッダー除外
    total = len(data)

    # ステータス集計（列7）
    statuses = Counter(r[7] if len(r) > 7 else '' for r in data)
    draft_count = statuses.get('ドラフト', 0)
    published_count = statuses.get('公開済み', 0)

    # 柱別集計（列2）
    pillars = Counter(r[2] if len(r) > 2 else '' for r in data)
    paraguay_count = pillars.get('パラグアイ', 0)
    ai_count = pillars.get('AI副業', 0)

    # 記事タイプ別集計（列3）
    types = Counter(r[3] if len(r) > 3 else '' for r in data)

    # 週別集計（列1）
    week_order = ['W1-2', 'W3-4', 'W5-6', 'W7-8', 'W9-10', 'W11-12']
    weeks = Counter(r[1] if len(r) > 1 else '' for r in data)
    week_statuses = {}
    for w in week_order:
        week_rows = [r for r in data if len(r) > 1 and r[1] == w]
        if not week_rows:
            continue
        ws = Counter(r[7] if len(r) > 7 else '' for r in week_rows)
        if ws.get('公開済み', 0) == len(week_rows):
            week_statuses[w] = '全て公開済み'
        elif ws.get('ドラフト', 0) == len(week_rows):
            week_statuses[w] = '全てドラフト'
        else:
            parts = []
            if ws.get('公開済み', 0):
                parts.append(f"公開{ws['公開済み']}")
            if ws.get('ドラフト', 0):
                parts.append(f"ドラフト{ws['ドラフト']}")
            week_statuses[w] = '・'.join(parts)

    summary = [
        ['南米おやじのAI実践ラボ 記事管理サマリー'],
        [''],
        ['■ 全体'],
        ['総記事数', total],
        ['ドラフト', draft_count],
        ['公開済み', published_count],
        [''],
        ['■ 柱別', '記事数'],
        ['パラグアイ系（集客）', paraguay_count],
        ['AI副業系（収益化）', ai_count],
        [''],
        ['■ 記事タイプ別', '記事数', '役割'],
    ]
    for t in ['集客記事', '収益記事', 'キラー記事', '実験記事']:
        summary.append([t, types.get(t, 0), TYPE_ROLES.get(t, '')])
    summary.append([''])
    summary.append(['■ 週別進捗', '記事数', 'ステータス'])
    for w in week_order:
        if weeks.get(w, 0) > 0:
            summary.append([w, weeks[w], week_statuses.get(w, '')])
    summary.append([''])
    summary.append(['■ 色凡例'])
    summary.append(['集客記事 = 緑系'])
    summary.append(['収益記事 = 青系'])
    summary.append(['キラー記事 = オレンジ系'])
    summary.append(['実験記事 = 紫系'])

    return summary


def connect():
    creds = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(SHEET_ID)


def write_article_list(sh, rows):
    """記事一覧シートを再構築"""
    try:
        ws = sh.worksheet('記事一覧')
        sh.del_worksheet(ws)
    except gspread.exceptions.WorksheetNotFound:
        pass
    ws = sh.add_worksheet(title='記事一覧', rows=max(len(rows) + 5, 30), cols=18)

    print(f"データ書き込み中...（{len(rows)-1}記事）")
    ws.update(rows, value_input_option='USER_ENTERED')

    # ヘッダーフォーマット
    ws.format('A1:R1', {
        'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.7},
        'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 'fontSize': 10},
        'horizontalAlignment': 'CENTER',
    })

    # 記事タイプ別の色分け + ステータス列
    print("書式設定中...")
    for i, row in enumerate(rows[1:], start=2):
        atype = row[3] if len(row) > 3 else ''
        color = TYPE_COLORS.get(atype, {'red': 1, 'green': 1, 'blue': 1})
        ws.format(f'A{i}:R{i}', {'backgroundColor': color})
        status = row[7] if len(row) > 7 else ''
        if status == 'ドラフト':
            ws.format(f'H{i}', {
                'backgroundColor': {'red': 1.0, 'green': 0.95, 'blue': 0.7},
                'textFormat': {'bold': True}
            })

    # フィルター
    ws.set_basic_filter(f'A1:Q{len(rows)}')

    # 列幅・ヘッダー固定
    sh.batch_update({'requests': [
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 40}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2}, 'properties': {'pixelSize': 65}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3}, 'properties': {'pixelSize': 90}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4}, 'properties': {'pixelSize': 90}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5}, 'properties': {'pixelSize': 110}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6}, 'properties': {'pixelSize': 200}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 6, 'endIndex': 7}, 'properties': {'pixelSize': 450}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 7, 'endIndex': 8}, 'properties': {'pixelSize': 85}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 8, 'endIndex': 9}, 'properties': {'pixelSize': 70}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 9, 'endIndex': 13}, 'properties': {'pixelSize': 80}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 13, 'endIndex': 14}, 'properties': {'pixelSize': 280}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 14, 'endIndex': 16}, 'properties': {'pixelSize': 95}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': ws.id, 'dimension': 'COLUMNS', 'startIndex': 16, 'endIndex': 17}, 'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}},
        {'updateSheetProperties': {'properties': {'sheetId': ws.id, 'gridProperties': {'frozenRowCount': 1}}, 'fields': 'gridProperties.frozenRowCount'}},
    ]})

    # 記事一覧シートを先頭に移動
    sh.batch_update({'requests': [
        {'updateSheetProperties': {
            'properties': {'sheetId': ws.id, 'index': 0},
            'fields': 'index'
        }}
    ]})
    return ws


def write_summary(sh, rows):
    """サマリーシートをCSVデータから自動集計して書き込み"""
    summary = build_summary(rows)

    try:
        ws2 = sh.worksheet('サマリー')
        ws2.clear()
    except gspread.exceptions.WorksheetNotFound:
        ws2 = sh.add_worksheet(title='サマリー', rows=max(len(summary) + 5, 35), cols=5)

    ws2.update(summary, value_input_option='USER_ENTERED')

    # バッチフォーマットで一括更新（API呼び出し回数を最小化）
    formats = [{'range': 'A1', 'format': {'textFormat': {'bold': True, 'fontSize': 14}}}]

    # セクションヘッダーの太字化（■で始まる行）
    for i, row in enumerate(summary, start=1):
        if row and isinstance(row[0], str) and row[0].startswith('■'):
            formats.append({'range': f'A{i}', 'format': {'textFormat': {'bold': True, 'fontSize': 11}}})

    # 色凡例の背景色（末尾4行）
    legend_labels = {'集客記事': '集客記事 = 緑系', '収益記事': '収益記事 = 青系',
                     'キラー記事': 'キラー記事 = オレンジ系', '実験記事': '実験記事 = 紫系'}
    for i, row in enumerate(summary, start=1):
        if row and isinstance(row[0], str):
            for tname, label in legend_labels.items():
                if row[0] == label:
                    formats.append({'range': f'A{i}', 'format': {'backgroundColor': TYPE_COLORS[tname]}})

    ws2.batch_format(formats)
    return ws2


def main():
    """全データを再構築"""
    print("認証中...")
    sh = connect()
    print(f"タイトル: {sh.title}")

    rows = read_csv()
    write_article_list(sh, rows)
    write_summary(sh, rows)

    print(f"\n完了!")
    print(f"URL: {sh.url}")
    return sh.url


if __name__ == '__main__':
    main()
