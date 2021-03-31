import pandas as pd
import numpy as np
import mailChimpAutomation
import googleSheetAutomation
import messagesAutomation


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
# The ID and range of a sample spreadsheet.
# SPREADSHEET_ID = 1zdn5n8yNJ9yQ1CIHc-zq1ud0QXWfVNAmcbcuSVuDqq8 # original!
SPREADSHEET_ID = '1sakXLCKCg9GWM_cyVYmOBwy76k-iuU0fn7LAn7UKz-o'
SHEET_ID = 52488024
SHEET_NAME = 'תגובות לטופס 1'
SPREADSHEET_RANGE_NAME = SHEET_NAME + "!A2:J"

SAVED_SPREADSHEET_ID = '1d7Mj-Dyho4vPNYZppv_U96JbV5yb79OGzskkZQsSFrM'
SAVED_SHEET_ID = 0
COPY_REQUEST = {
    # The ID of the spreadsheet to copy the sheet to.
    'destination_spreadsheet_id': SAVED_SPREADSHEET_ID}


DF_FILENAME = "saved_spreadsheet_data"

COLUMNS_NAMES = ["timeStamp", "fullName", "phoneNumber", "mailAddress", "area",
                 "leadCommunity", "helpWith", "remarks", "city", "status"]

TEXT_MSG_TEMPLATE = ""


def runAutomation():
    credentials = googleSheetAutomation.getCredentials(SCOPES)  # for connecting to google sheet
    recent = googleSheetAutomation.readSheet(credentials, SPREADSHEET_ID,
                                             SPREADSHEET_RANGE_NAME, COLUMNS_NAMES)
    saved = readSavedDf()  # read the saved data to compare to it
    newLines = getNewLines(saved, recent)  # get new added lines
    if newLines is None:
        return

    onNewVolunteers(newLines)
    saved = saved.append(newLines, ignore_index=True)  # append new data
    print(saved)
    writeSavedDf(saved)   # save new data


def onNewVolunteers(newData):
    for index, newVolunteer in newData.iterrows():
        firstName, lastName = getSeparatedName(newVolunteer["fullName"])
        print("sending msgs to: " + firstName + " " + lastName)
        print("email: " + newVolunteer["mailAddress"])
        # when adding a new member it sends a mail
        mailChimpAutomation.createMember(newVolunteer["mailAddress"], firstName, lastName)
        # messagesAutomation.sendSMS(newVolunteer["phoneNumber"], newVolunteer["fullName"], TEXT_MSG_TEMPLATE)
        # messagesAutomation.sendWhatsApp(newVolunteer["phoneNumber"], newVolunteer["fullName"], TEXT_MSG_TEMPLATE)


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


def getSeparatedName(fullName):
    firstLastName = fullName.split()
    if len(firstLastName) == 0:
        return "", ""  # todo
    firstName = firstLastName[0]
    lastName = ""
    if len(firstLastName) > 1:
        lastName = " ".join(firstLastName[1:])
    return firstName, lastName


if __name__ == '__main__':
    runAutomation()
