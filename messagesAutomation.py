from twilio.rest import Client
import json
"""
SMS & WhatApp messages automation using Twillio 
This is currently the trial version and is limited
"""

# todo: open twilio account with the brave account
# todo: understand what twili can do with paid account
# todo: make this work with our numbers for example

CREDENTIALS_FILE = "twilioCredentials.json"
CREDENTIALS = json.load(open(CREDENTIALS_FILE))
ACCOUNT_SID = CREDENTIALS["ACCOUNT_SID"]
AUTH_TOKEN = CREDENTIALS["AUTH_TOKEN"]
SMS_SENDER_NUMBER = '+13018046615'
WHATSAPP_SENDER_NUMBER = "+14155238886"

DEFAULT_MSG = ""


def sendSMS(number, name="", msg=DEFAULT_MSG):
    __sendMessage(SMS_SENDER_NUMBER, getNumberInRightFormat(number), name, msg)


def sendWhatsApp(number, name, msg=DEFAULT_MSG):
    __sendMessage("whatsapp:" + WHATSAPP_SENDER_NUMBER, "whatsapp:" + getNumberInRightFormat(number), name, msg)


def getNumberInRightFormat(number):
    if number.startswith("0"):
        return "+972" + number[1:]
    if number.startswith("+"):
        return number
    return "+972" + number


def __sendMessage(numberFrom, numberTo, name, msg):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    msg = " היי " + name + "\n" + msg
    message = client.messages.create(
                body=msg,
                from_=numberFrom,
                to=numberTo)