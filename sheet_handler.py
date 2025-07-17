from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SHEET_RANGE = 'A:D'  # 回答列（例：タイムスタンプ, 学籍番号, 名前, その他）

def get_sheet_values(sheet_id: str):
    creds = service_account.Credentials.from_service_account_file(
        'service_account.json', scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=SHEET_RANGE).execute()
    values = result.get('values', [])

    # タイトル行を除いて、当日の回答だけを抽出
    today = datetime.datetime.now().strftime('%Y/%m/%d')
    entries = []

    for row in values[1:]:
        if len(row) >= 3 and today in row[0]:
            student_id = row[1].strip()
            name = row[2].strip()
            entries.append(f"・{student_id} {name}")

    return entries
