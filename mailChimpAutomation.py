import mailchimp3
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

API_KEY = os.getenv("API_KEY")
LIST_ID = os.getenv("LIST_ID")

api = mailchimp3.MailChimp(API_KEY)

def getHashedEmail(email):
    return hashlib.md5(email.encode('utf-8').lower()).hexdigest()

# only tag is tel aviv
# add recurring tag if you want 'nudnik', it'll send a mail three days after
def createMember(email, firstName, lastName, tags=['tel aviv']):
    api.lists.members.create_or_update(LIST_ID,  subscriber_hash=getHashedEmail(email), data={'email_address': email, 'status': 'subscribed', 'tags': tags,
                                            'merge_fields': {'FNAME': firstName, 'LNAME': lastName, }});
