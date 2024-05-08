import mh_z19
import re
import datetime
from time import sleep
import schedule
import requests
import csv

CO2_array = []
time_array = []
ppm_array = []

url = "https://slack.com/api/chat.postMessage"
data = {
    "token": "token(hided)",
    "channel": "channel ID (hided)",
    "text": "CO2 measurement started"
}
requests.post(url, data=data)

mh_z19.read()

while True:
    CO2 = str(mh_z19.read())
    #print(CO2)
    number = re.sub(r"\D","",CO2)
    ppm = int(number.lstrip("2"))
    #print(ppm)

    detailed_time = datetime.datetime.now().time()
    hour = str(detailed_time.hour)
    minute = str(detailed_time.minute)
    if len(hour)==1:
        hour = "0" + hour
    if len(minute)==1:
        minute = "0" + minute
    time = hour + minute
    #print(time)
    time = int(time)
    CO2_array = [time,ppm]
    
    with open(f'/home/kammmmow/CO2sensor_results/{datetime.date.today()}_{hour}','a') as f:
        writer = csv.writer(f)
        writer.writerow(CO2_array)
        
    if time % 5 == 0:
        if ppm > 1000:
            url = "https://slack.com/api/chat.postMessage"
            data = {
                "token": "token(hided)",
                "channel": "channel ID (hided)",
                "text": f"{hour}:{minute} Carbon dioxide concentration is {ppm} ppm now and it is over 1000. Let's ventilate the room."
            }
            requests.post(url, data=data)
    
    sleep(60)