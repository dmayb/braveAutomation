import mailchimp3
import hashlib
import json

CREDENTIALS_FILE = "mailchimpCredentials.json"
CREDENTIALS = json.load(open(CREDENTIALS_FILE))
API_KEY = CREDENTIALS["API_KEY"]
LIST_ID = CREDENTIALS["LIST_ID"]


api = mailchimp3.MailChimp(API_KEY)

def getHashedEmail(email):
    return hashlib.md5(email.encode('utf-8').lower()).hexdigest()

# only tag is tel aviv
# add recurring tag if you want 'nudnik', it'll send a mail three days after
def createMember(email, firstName, lastName, status='subscribed', tags=['tel aviv']):
    api.lists.members.create_or_update(LIST_ID,  subscriber_hash=getHashedEmail(email), data={'email_address': email, 'status': status, 'tags': tags, 'status_if_new': status,
                                            'merge_fields': {'FNAME': firstName, 'LNAME': lastName,  }});



