import requests, os
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate_sheets(api_key):
    return build('sheets', 'v4', developerKey=api_key).spreadsheets()

def get_values():
    sheets = authenticate_sheets(os.environ.get("SHEETS_API"))
    result = sheets.values().get(spreadsheetId=os.environ.get("SHEET_ID"), range="Connections!A2:B100000000").execute()
    values = result.get("values")

    return values

def update_values(values, row, col_ind):

    # col_ind == 0 means that values[0] is "FROM", otherwise, the whole of values is just "TO"

    sheets = authenticate_sheets(os.environ.get("SHEETS_API"))

    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    requests = [
        {
            'insertDimension': {
                'range': {
                    'sheetId': os.environ.get("CONNECTIONS_ID"),  # Assuming the first sheet, you can change it as needed
                    'dimension': 'ROWS',
                    'startIndex': row,
                    'endIndex': row
                },
                'inheritFromBefore': False
            }
        },
        {
            'updateCells': {
                'rows': [
                    {
                        'values': [
                            {'userEnteredValue': {'stringValue': value}} for value in values
                        ]
                    }
                ],
                'fields': 'userEnteredValue',
                'start': {
                    'sheetId': os.environ.get("CONNECTIONS_ID"),
                    'rowIndex': row,
                    'columnIndex': col_ind
                }
            }
        }
    ]

    body = { "requests": requests }

    try:
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=os.environ.get("SHEET_ID"),
            body=body
        ).execute()
        return {"status": f"Worked successfully: {response}"}
    except Exception as e:
        return {"status": f"Didn't work: {e}"}
