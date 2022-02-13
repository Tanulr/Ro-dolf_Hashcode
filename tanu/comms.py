# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'ACac5935985082c6f397e2580ae3b4d47f'
auth_token = '24eb2516f1bb6f2f1e721b8d164f97c5'
client = Client(account_sid, auth_token)

def call():
    call = client.calls.create(
                            twiml='<Response><Say voice="alice">Meera is in danger! She just collapsed. </Say></Response>',
                            to='+919742944225',
                            from_='+19035825610'
                        )

    print(call.sid)