from __future__ import print_function
from googleapiclient.discovery import build
from connectGoogleSheet import getCredentials
import pandas as pd
from pprint import pprint

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = 1zdn5n8yNJ9yQ1CIHc-zq1ud0QXWfVNAmcbcuSVuDqq8 # original!
SAMPLE_SPREADSHEET_ID = '1sakXLCKCg9GWM_cyVYmOBwy76k-iuU0fn7LAn7UKz-o'
SAVED_SPREADSHEET_ID = '1d7Mj-Dyho4vPNYZppv_U96JbV5yb79OGzskkZQsSFrM'
SHEET_ID = 52488024
SAVED_SHEET_ID = 0
COPY_REQUEST = {
    # The ID of the spreadsheet to copy the sheet to.
    'destination_spreadsheet_id': SAVED_SPREADSHEET_ID}

SHEET_NAME = 'תגובות לטופס 1'
SAMPLE_RANGE_NAME = SHEET_NAME + "!A2:J"

DF_FILENAME = "previous_data.csv"

def checkChanges():
    creds = getCredentials(SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    with open('saved_start_page_token.txt', 'r') as tokenFile:
        saved_start_page_token = tokenFile.readline()

    page_token = saved_start_page_token
    while page_token is not None:
        response = drive_service.changes().list(pageToken=page_token,
                                                spaces='drive').execute()
        for change in response.get('changes'):
            # Process change
            print('Change found for file: %s' % change.get('fileId'))
        if 'newStartPageToken' in response:
            # Last page, save this token for the next polling interval
            saved_start_page_token = response.get('newStartPageToken')
        page_token = response.get('nextPageToken')

    with open('saved_start_page_token.txt', 'w') as tokenFile:
        tokenFile.write(saved_start_page_token)
        print(saved_start_page_token)


def resetToken():
    creds = getCredentials(SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
    response = drive_service.changes().getStartPageToken().execute()
    start_page_token = response.get('startPageToken')
    with open('saved_start_page_token.txt', 'w') as tokenFile:
        tokenFile.write(start_page_token)
        print(start_page_token)
    print('Start token: %s' % start_page_token)


def readSheet():
    creds = getCredentials(SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return

    columns = ["timeStamp", "fullName", "phoneNumber", "mailAddress", "area",
               "leadCommunity", "helpWith", "remarks", "city", "status"]
    new = pd.DataFrame(values, columns=columns)
    writeSavedDf(new)
    # saved = readSavedDf()
    # compareData(saved, new)


def compareData(saved, new):
    df = pd.concat([saved, new])
    df = df.reset_index(drop=True)
    df_gpby = df.groupby(list(df.columns))
    idx = [x[0] for x in df_gpby.groups.values() if len(x) == 1]
    diff = df.reindex(idx)


def writeSavedDf(df):
    with open(DF_FILENAME, "w", encoding="utf-8") as fd:
        df.to_csv(fd)


def readSavedDf():
    with open(DF_FILENAME, "r", encoding="utf-8") as fd:
        df = pd.read_csv(fd)
        return df


def copySpreadsheet(creds):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets().sheets()
    request = sheet.copyTo(spreadsheetId=SAMPLE_SPREADSHEET_ID, sheetId=SHEET_ID, body=COPY_REQUEST)
    response = request.execute()
    pprint(response)

if __name__ == '__main__':
    # readSheet()
    copySpreadsheet(getCredentials(SCOPES))
