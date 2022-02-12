import datetime
import time
#send data 
import urllib.request
def sendmessage(msg1, msg2):
    msg1 = msg1.replace(' ', "%20")
    msg1 = msg1.replace('\n', "%0A")
    msg2 = msg2.replace(' ', "%20")
    msg2 = msg2.replace('\n', "%0A")
    b=urllib.request.urlopen('https://api.thingspeak.com/update?api_key=VMG64YAQU62YASKO&field1='+msg1) #Enter api id 
    b=urllib.request.urlopen('https://api.thingspeak.com/update?api_key=VMG64YAQU62YASKO&field2='+msg2) #Enter api id 
    print("\nYour message has successfully been sent!")
    return
 #receive data 
 

import csv
import urllib.request
import os
def getMessage():

    import requests
    msg1=requests.get("https://thingspeak.com/channels/1653587/field/1")
    msg1=msg1.json()['feeds'][-1]['created_at']
    # msg2=requests.get("https://thingspeak.com/channels/1653587/Time/1")
    # msg2=msg2.json()['feeds'][-1]['Time']
    print("\nThe Message sent was: \n\n"+str(msg1))
    # print("\nThe Message sent was: \n\n"+str(msg2))
    return msg1

#sendmessage(str(datetime.date.today()), str(time.time()))
#print(type(getMessage()))
