from datetime import datetime
import requests
import smtplib
import time

EMAIL = "your email"
PAS = "your password"

MY_LAT = 22.7179
MY_LNG= 75.8333

def is_iss_overhead():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data= response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_position = (iss_latitude,iss_longitude)
    # print(iss_position)

    if (MY_LAT-5 <= iss_latitude <= MY_LAT+5) and (MY_LNG-5 <= iss_longitude <= MY_LNG+5):
        return True

def is_night():
    parameters = {
        "lat":MY_LAT ,
        "lng": MY_LNG ,
        "formatted":0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json?lat=22.7179&lng=75.8333",params=parameters)
    response.raise_for_status()

    data = response.json()
    # print(data)

    sunrise =  int(data["results"]["sunrise"].split('T')[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split('T')[1].split(":")[0])

    print(f"sunrise :{sunrise}"+"\n" + f"sunset :{sunset}")

    time_now= datetime.now().hour
    # print(time_now.hour)
    if time_now> sunset or time_now < sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connect =smtplib.SMTP("smtp.gmail.com")
        connect.starttls()
        connect.login(EMAIL,PAS)
        connect.sendmail(
            from_addr=EMAIL,
            to_addrs=EMAIL,
            msg="Subject:Look Up\n\n ISS is here."
        )
