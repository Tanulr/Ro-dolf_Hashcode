from datetime import datetime
import time


import thingspeak
import communicate

x = str(thingspeak.getMessage())[-9:-1]
y = str(datetime.utcnow())[-15:-7]
print(x)
print(y)
mins = (int(y[-5:-3]) - int(x[-5:-3]))*60
diff = int(y[-2:]) - int(x[-2:]) + mins
if diff >=20:
    communicate.call()