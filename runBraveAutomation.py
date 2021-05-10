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

# not in use
SAVED_SPREADSHEET_ID = '1d7Mj-Dyho4vPNYZppv_U96JbV5yb79OGzskkZQsSFrM'
SAVED_SHEET_ID = 0
COPY_REQUEST = {
    # The ID of the spreadsheet to copy the sheet to.
    'destination_spreadsheet_id': SAVED_SPREADSHEET_ID}

# the data frame pickled filename where we save the updated data after reading the sheet
DF_FILENAME = "saved_spreadsheet_data"

# column names of the google sheet (in english for convenience)
COLUMNS_NAMES = ["timeStamp", "fullName", "phoneNumber", "mailAddress", "area",
                 "leadCommunity", "helpWith", "remarks", "city", "status"]

# todo: could be added to a google spreadsheet "front-end" - a sheet where all the automation configurations
#  could be saved in
TEXT_MSG_TEMPLATE = "תודה על הצטרפותך לגיבורים לשבת!\n" + "קישור לקבוצת ווטסאפ: " + "https://chat.whatsapp.com/groupid"

# currently configured cities in mailchimp
EXISTING_CITIES = {"תל אביב", "ירושלים", "רמת גן", "אריאל", "גן יבנה", "באר שבע", "נהריה", "סירקין", "חיפה"}


def runAutomation():
    """
    the main automation script. it connects to google sheets API, reads the volunteers doc
    finds new volunteers and sends them email, SMS, whatsApp
    """
    credentials = googleSheetAutomation.getCredentials(SCOPES)  # for connecting to google sheet
    recent = googleSheetAutomation.readSheet(credentials, SPREADSHEET_ID,
                                             SPREADSHEET_RANGE_NAME, COLUMNS_NAMES)
    saved = readSavedDf()  # read the saved data to compare to it
    newLines = getNewLines(saved, recent)  # get new added lines
    if newLines is None:
        return

    sendSnoozer(recent)  # send snoozer to doers@brave-together if a volunteer doesnt have an activity yet
    onNewVolunteers(newLines)
    saved = saved.append(newLines, ignore_index=True)  # append new data
    print(saved)
    writeSavedDf(saved)   # save new data


def sendSnoozer(volunteers):
    for index, volunteer in volunteers.iterrows():
        sendEmail(volunteer)


def sendEmail(volunteer):
    """
    send and email to the volunteer if it is a new one
    send an email to the volunteer's area organizer of the volunteer doesnt have an activity yet
    (status column on the google sheet)
    :param volunteer: DataFrame object with volunteer data (with the columns COLUMNS_NAMES)
    """
    firstName, lastName = getSeparatedName(volunteer["fullName"])
    city = volunteer["city"]
    if city not in EXISTING_CITIES:
        city = mailChimpAutomation.DEFAULT_TAG
    tags = [city]
    if volunteer["status"] == "1":
        tags.append(mailChimpAutomation.NUDNIK_TAG)
    print("sending msgs to: " + firstName + " " + lastName)
    print("email: " + volunteer["mailAddress"] + " , city: " + city)
    # when adding a new member it sends a mail
    mailChimpAutomation.createOrUpdateMember(volunteer["mailAddress"], firstName, lastName, tags)


def onNewVolunteers(newData):
    """
    gets the new volunteers data and runs whatever it is configured to do
    currently: sends mail (through mailchimp API)
    on trial version (from a specific number only): sends WhatsApp and SMS (the numbers it can send to are limited)
    :param newData: a DataFrame (pandas) object holding the new volunteers data with the columns COLUMNS_NAMES
    """
    for index, newVolunteer in newData.iterrows():
        sendEmail(newVolunteer)
        messagesAutomation.sendSMS(newVolunteer["phoneNumber"], newVolunteer["fullName"], TEXT_MSG_TEMPLATE)
        messagesAutomation.sendWhatsApp(newVolunteer["phoneNumber"], newVolunteer["fullName"], TEXT_MSG_TEMPLATE)


def getNewLines(saved, recent):
    """
    this function checks if there are new lines in the google spreadsheet
    it does that by comparing the timestamp column
    :param saved: DataFrame pandas object (with columns COLUMNS_NAMES)
    :param recent: DataFrame pandas object (with columns COLUMNS_NAMES)
    :return: DataFrame object - the new lines (with columns COLUMNS_NAMES)
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
    """
    saves the updated DataFrame object with pickle
    :param df: DataFrame object to be saved

    """
    df.to_pickle(DF_FILENAME, protocol=4)  # this will work for python 3.6 and above


def readSavedDf():
    """
    reads saved DataFrame of volunteers
    :return:
    """
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
