from __future__ import print_function
from googleapiclient.discovery import build
from connectGoogleSheet import getCredentials
import pandas as pd
import numpy as np

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = 1zdn5n8yNJ9yQ1CIHc-zq1ud0QXWfVNAmcbcuSVuDqq8 # original!
SAMPLE_SPREADSHEET_ID = '1sakXLCKCg9GWM_cyVYmOBwy76k-iuU0fn7LAn7UKz-o'
SHEET_ID = 52488024

SAVED_SPREADSHEET_ID = '1d7Mj-Dyho4vPNYZppv_U96JbV5yb79OGzskkZQsSFrM'
SAVED_SHEET_ID = 0
COPY_REQUEST = {
    # The ID of the spreadsheet to copy the sheet to.
    'destination_spreadsheet_id': SAVED_SPREADSHEET_ID}

SHEET_NAME = 'תגובות לטופס 1'
SAMPLE_RANGE_NAME = SHEET_NAME + "!A2:J"

DF_FILENAME = "saved_spreadsheet_data"

COLUMNS_NAMES = ["timeStamp", "fullName", "phoneNumber", "mailAddress", "area",
                 "leadCommunity", "helpWith", "remarks", "city", "status"]


# not in use
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


# not in use
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
    """
    this function reads SAMPLE_SPREADSHEET_ID and checks if there's a new line (new volunteer)
    if so, it sends it a welcome email through mailchimp api
    :return:
    """
    creds = getCredentials(SCOPES)  # for connecting to google sheet
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])  # the rows of the spreadsheet

    if not values:
        print('No data found.')  # todo: what to do when cant read data?
        return

    # columnsOfInterest = ["timeStamp", "fullName", "phoneNumber", "mailAddress", "city", "status"]
    columnsOfInterest = COLUMNS_NAMES
    recent = pd.DataFrame(values, columns=COLUMNS_NAMES)
    recent = recent.loc[:, columnsOfInterest]
    saved = readSavedDf()  # read the saved data to compare to it
    newLines = getNewLines(saved, recent)  # get new added lines

    if newLines is None:
        return

    # todo:
    # sendEmail()  # ~~~~~~Karin add here~~~~~~~~~
    # addTo ?
    # add to our database (our pickled DataFrame)
    saved = saved.append(newLines, ignore_index=True)  # append new data
    print(saved)
    writeSavedDf(saved)   # save new data


def getNewLines(saved, recent):
    """
    this function checks if there are new lines in the google spreadsheet
    :param saved: DataFrame pandas object
    :param recent: DataFrame pandas object
    :return: DataFrame object - the new lines
    """
    savedTimestamps = saved["timeStamp"]
    newTimestamps = recent["timeStamp"]
    indexes = []
    for i, newTime in enumerate(newTimestamps):
        if not np.any(savedTimestamps.isin([newTime])):
            indexes.append(i)
    if len(indexes) == 0:
        return
    newLines = recent.iloc[indexes]
    print("new lines found: ")
    print(newLines)
    return newLines


def writeSavedDf(df):
    df.to_pickle(DF_FILENAME)


def readSavedDf():
    return pd.read_pickle(DF_FILENAME)

# not in use
def copySpreadsheet(creds):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets().sheets()
    request = sheet.copyTo(spreadsheetId=SAMPLE_SPREADSHEET_ID, sheetId=SHEET_ID, body=COPY_REQUEST)
    response = request.execute()
    print(response)

if __name__ == '__main__':
    # readSheet()
    # copySpreadsheet(getCredentials(SCOPES))
    readSheet()