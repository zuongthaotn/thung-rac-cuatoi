from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_service():
    """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.

        for guides on implementing OAuth2 for the application.
            """
    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    DATA_PATH = os.path.abspath('../algo-stock/gsheet')
    if os.path.exists(DATA_PATH + '/token.json'):
        creds = Credentials.from_authorized_user_file(DATA_PATH + '/token.json', SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        return service
    return None

def get_values(spreadsheet_id, range_name):
    service = get_service()
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
def append_values(spreadsheet_id, range_name, value_input_option, _values):
    try:
        service = get_service()
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        body = {
            'values': _values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error
def prepend_values(spreadsheet_id, range_name, value_input_option, _values):
    try:
        service = get_service()
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        body = {
            'values': _values
        }
        result = service.spreadsheets().values().prepend(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{(result.get('updates').get('updatedCells'))} cells prepended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def update_values(spreadsheet_id, range_name, value_input_option,_values):

    try:

        service = get_service()
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        body = {
            'values': _values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error

def insert_row_data(spreadsheet_id):
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
                    "data": "sample11, sample21, sample31",
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
    response = request.execute()
if __name__ == '__main__':
    insert_row_data('1rmQO4H8v8Vrw32-qxoRyOusT7wjlD3ySl1WOmPbR-J0')

    import numpy as np
    # Pass: spreadsheet_id, and range_name
    # result = get_values("1roOZQvWo4g_M6uZj6t-3jriELM_pmkizt7b4k9Ni2VQ", "A1:L")
    # # print(type(result))
    # # print(result)
    # # arr = np.asarray(result)
    # # print(arr)
    # rows = result.get('values', [])
    # # print(rows[0])
    # import pandas as pd
    #
    # df = pd.DataFrame(rows, columns=rows[0])
    # print(df)
    # prepend_values
    # append_values("1roOZQvWo4g_M6uZj6t-3jriELM_pmkizt7b4k9Ni2VQ",
    #               "A2:C2", "USER_ENTERED",
    #               [
    #                   ['F0', 'B1', 'T3']
    #               ])
    # update_values("1roOZQvWo4g_M6uZj6t-3jriELM_pmkizt7b4k9Ni2VQ",
    #               "A1:C2", "USER_ENTERED",
    #               [
    #                   ['A', 'B' , 'B'],
    #                   ['C', 'D', 'B']
    #               ])