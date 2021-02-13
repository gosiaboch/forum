import json
import os
#import requests
from requests import request


def send_email(text, subject, receiver_email):
   sender_email = os.getenv("email_Address")
   api_key = os.getenv("api_key")

   if sender_email and api_key:
      url = "https://api.sendgrid.com/v3/mail/send"

      data = {"personalizations": [{
         "to": [{"email": receiver_email}],
         "subject": subject
      }],

         "from": {"email": sender_email},

         "content": [{
            "type": "text/plain",
            "value": text
         }]
      }

      headers = {
         'authorization': "Bearer {0}".format(api_key),
         'content-type': "application/json"
      }

      response = request("POST", url=url, data=json.dumps(data), headers=headers)

      print("Sent to SendGrid")
      print(response.text)

   else:
      print("No env vars or no email address")