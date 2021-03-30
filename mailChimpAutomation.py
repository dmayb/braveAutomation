import mailchimp3
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
LIST_ID = os.getenv("LIST_ID")

api = mailchimp3.MailChimp(API_KEY)

#can add email and names from the list
api.lists.members.create(LIST_ID, data={'email_address': 'rebeccacaine42@gmail.com', 'status': 'subscribed'})
