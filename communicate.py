# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACac5935985082c6f397e2580ae3b4d47f'
auth_token = 'ebaf0f57b99a225c69a31a73ee51d665'
client = Client(account_sid, auth_token)

def call():
    call = client.calls.create(
                            twiml='<Response><Say voice="alice">Dont let go now. Youre going to regret it. Keep exercising</Say></Response>',
                            to='+916364002445',
                            from_='+19035825610'
                        )

    print(call.sid)