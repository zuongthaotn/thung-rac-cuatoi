import os
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_service():
    """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.

        for guides on implementing OAuth2 for the application.
            """
    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    DATA_PATH = os.path.dirname(__file__)
    if os.path.exists(DATA_PATH + '/token.json'):
        creds = Credentials.from_authorized_user_file(DATA_PATH + '/token.json', SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service
    return None

def get_data(spreadsheet_id, range_name):
    service = get_service()
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        return pd.DataFrame(rows, columns=rows[0])

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def insert_row_data(spreadsheet_id, row_data):
    batch_update_spreadsheet_request_body = {
        "requests": [
            {
                "insertRange": {
                    "range": {
                        "sheetId": 0,
                        "startRowIndex": 0,
                        "endRowIndex": 1
                    },
                    "shiftDimension": "ROWS"
                }
            },
            {
                "pasteData": {
                    "data": row_data,
                    "type": "PASTE_NORMAL",
                    "delimiter": ",",
                    "coordinate": {
                        "sheetId": 0,
                        "rowIndex": 1
                    }
                }
            }
        ]
    }

    service = get_service()
    request = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=batch_update_spreadsheet_request_body)
    request.execute()