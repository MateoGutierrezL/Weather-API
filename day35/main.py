import requests 
import smtplib
import os

MY_LAT = 6.244203
MY_LONG = -75.581215

api_key = os.getenv("OWN_API_WEATHER_KEY")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "cnt": 4,
    "appid": api_key
}

response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
print(response)
data = response.json()
weather_id = data["list"][0]["weather"][0]["id"]
weather_id_list = [data["list"][item]["weather"][0]["id"] for item in range(4)]

will_rain = False

for id in weather_id_list:
    if id < 700:
        will_rain = True
        break

if will_rain:
    email = os.getenv("MY_EMAIL")
    password = os.getenv("MY_PASSWORD")

    if not email or not password:
        raise ValueError("Error: EMAIL_USER o EMAIL_PASS no están definidas en las variables de entorno.")

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user= email, password=password)
        connection.sendmail(
            from_addr=email,
            to_addrs=email,
            msg=f"Subject: Get an Umbrella!!\n\nToday is going to rain so if you don't want to get wet, please bring an umbrella. Your not going to look like a gay"
        )
