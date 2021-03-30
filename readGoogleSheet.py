from __future__ import print_function
from googleapiclient.discovery import build
from connectGoogleSheet import getCredentials
import pandas as pd
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1sakXLCKCg9GWM_cyVYmOBwy76k-iuU0fn7LAn7UKz-o'
SHEET_NAME = 'תגובות לטופס 1'
SAMPLE_RANGE_NAME = SHEET_NAME + "!A2:J"


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
    df1 = pd.DataFrame(values, columns=columns)
    df2 = df1.copy(deep=True)
    df2["fullName"][0] = "שם"
    





if __name__ == '__main__':
    readSheet()
