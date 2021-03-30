import os
from twilio.rest import Client

# should be set as environment variables (for security?)
# these are taken from twilio.com/console
account_sid = 'ACe0261db7f26db08b41d562493718d824'
auth_token = 'fc451cb3a1cc54111f189bcfa464cf1b'

client = Client(account_sid, auth_token)
fromWhatsAppNumber = 'whatsapp:+14155238886'
toWhatsAppNumber = 'whatsapp:+972525527284'

msg = client.messages.create(body='היי זאת מאי',
                       from_=fromWhatsAppNumber,
                       to=toWhatsAppNumber)


print(msg.sid)

