import mailchimp3
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
LIST_ID = os.getenv("LIST_ID")

api = mailchimp3.MailChimp(API_KEY)

#only tag is tel aviv
def createMember(email, firstName, lastName, tags=['tel aviv']):
    api.lists.members.create(LIST_ID, data={'email_address': email, 'status': 'subscribed', 'tags': tags,
                                        'merge_fields': {'FNAME': firstName, 'LNAME': lastName, }});
