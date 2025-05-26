import requests
from datetime import datetime
from send_telegram_message import send_telegram_message
from send_mail import send_mail
from dotenv import load_dotenv
import os
# This script checks the current position of the International Space Station (ISS)
# and compares it with a predefined position. If the ISS is within a certain range
# and it's nighttime at the predefined position, it sends an email notification.
# You can also use the send_telegram_message function to send a message via Telegram.

SENDING_MODE = "telegram"  # Change to "email" to use email notifications, to "telegram" to use telegram notification or leave empty to use both
if SENDING_MODE == "telegram":
    send_notification = send_telegram_message
elif SENDING_MODE == "email":
    send_notification = send_mail
elif SENDING_MODE == "":
    send_notification = lambda message: (send_telegram_message(message), send_mail(message))
else:
    raise ValueError("Invalid SENDING_MODE. Use 'telegram', 'email' or leave empty.")

def get_iss_coords():
    try:
        response = requests.get(url="http://api.open-notify.org/iss-now.json", timeout=10)
        response.raise_for_status()
        data = response.json()
        longitude = float(data["iss_position"]["longitude"])
        latitude = float(data["iss_position"]["latitude"])
        iss_position = (longitude, latitude) # lat/long to adress see: https://www.latlong.net/Show-Latitude-Longitude.html
        return iss_position
    except requests.exceptions.RequestException as e:
        return f"[ERROR] Could not retrieve ISS position: {e}"

def get_sun_hours(parameters):
    try:
        response = requests.get("https://api.sunrise-sunset.org/json", params = parameters, timeout=10)
        response.raise_for_status()
        data = response.json()
        sunrise_hour = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset_hour = int(data["results"]["sunset"].split("T")[1].split(":")[0])
        daylight = (sunrise_hour, sunset_hour)
        return daylight
    except requests.exceptions.RequestException as e:
        return f"[ERROR] Could not retrieve sun data: {e}"

def compare_coords(data_iss, data_mycoords):
    if data_mycoords[0]-5 <= data_iss[0] <= data_mycoords[0]+5 and data_mycoords[1]-5 <= data_iss[1] <= data_mycoords[1]+5:
        return True
    else:
        return False

def check_daylight(hour_input):
    time_now_hour = datetime.now().hour
    if time_now_hour not in range(hour_input[0], hour_input[1]):
        return False
    else:
        return True

def main():
    load_dotenv()
    MY_POS_LAT = os.getenv("MY_POS_LAT")
    MY_POS_LNG = os.getenv("MY_POS_LNG") 

    if MY_POS_LAT is None or MY_POS_LNG is None:
        raise ValueError("Environment variables MY_POS_LAT and MY_POS_LNG must be set.")

    try:
        MY_POS_LAT = float(MY_POS_LAT)
        MY_POS_LNG = float(MY_POS_LNG)
    except ValueError:
        raise ValueError("Environment variables MY_POS_LAT and MY_POS_LNG must be valid numbers.")

    my_position = (MY_POS_LAT, MY_POS_LNG)

    parameters = {
        "lat": MY_POS_LAT,
        "lng": MY_POS_LNG,
        "formatted": 0,
    }

    iss_coords = get_iss_coords()
    sun_hours = get_sun_hours(parameters)
    
    if isinstance(iss_coords, str):
        print(iss_coords)
        send_notification(iss_coords)
    elif isinstance(sun_hours, str):
        print(sun_hours)
        send_notification(sun_hours)
    else:
        if compare_coords(iss_coords, my_position) and check_daylight(sun_hours):
            message = (
                f"ISS in range.\n"
                f"It's nighttime!\n"
                f"ISS-Position: {iss_coords}\n"
                f"My Position: {my_position}"
            )
            send_notification(message)            
        elif compare_coords(iss_coords, my_position) and not check_daylight(sun_hours):
            message = (
                f"ISS in range.\n"
                f"It's daytime!\n"
                f"ISS-Position: {iss_coords}\n"
                f"My Position: {my_position}"
            )
            send_notification(message)
        else:
            print("ISS not in range")
            print("ISS-Position: ", iss_coords)
            print("My Position: ", my_position)
        
main()
