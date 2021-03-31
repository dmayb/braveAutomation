import os
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACe0261db7f26db08b41d562493718d824'
auth_token = 'dc6c1ad4858f4ff8597f960bdbfcb874'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+13018046615',
                     to='+972525527284'
                 )

print(message.sid)