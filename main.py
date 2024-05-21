import requests
import datetime as dt
import smtplib
import time

my_email = "thisisnotmyemail@gmail.com"
my_password = "thisisnotmypassword"

MY_LAT = 41.182999
MY_LNG = -8.679770

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}


def is_iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    
    if -5 <= (iss_latitude - MY_LAT) <= 5 and -5 <= (iss_longitude - MY_LNG) <= 5:
        return True

def is_night():

    parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}

    response = requests.get(url="http://api.open-notify.org/iss-now.json", params=parameters)
    response.raise_for_status()
    
    data = response.json()
    
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = dt.datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_iss_overhead() and is_day():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(my_email, my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=my_email,
                msg=f"Subject:Diz olá ao ISS\n\nIts above our heads ;)"
            )

