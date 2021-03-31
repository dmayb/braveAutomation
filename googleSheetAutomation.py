import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import pandas as pd

# todo: changes the credntials to be on the brave-toghethe account


def getCredentials(scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def readSheet(credentials, spreadsheetID, spreadsheetRange, sheetColumns):
    """
    this function reads SAMPLE_SPREADSHEET_ID and checks if there's a new line (new volunteer)
    if so, it sends it a welcome email through mailchimp api
    :return:
    """
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheetID,
                                range=spreadsheetRange).execute()
    values = result.get('values', [])  # the rows of the spreadsheet

    if not values:
        print('No data found.')  # todo: what to do when cant read data?
        return

    # columnsOfInterest = ["timeStamp", "fullName", "phoneNumber", "mailAddress", "city", "status"]
    columnsOfInterest = sheetColumns
    recent = pd.DataFrame(values, columns=sheetColumns)
    recent = recent.loc[:, columnsOfInterest]
    return recent


def checkChanges(credentials):
    drive_service = build('drive', 'v3', credentials=credentials)
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


# not in use
def copySpreadsheet(credentials):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets().sheets()
    request = sheet.copyTo(spreadsheetId=SAMPLE_SPREADSHEET_ID, sheetId=SHEET_ID, body=COPY_REQUEST)
    response = request.execute()
    print(response)