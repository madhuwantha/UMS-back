import requests
import os

from datetime import datetime
from pytz import timezone
import pytz

appid = os.getenv('appid', "01e1f7b3f577354a625365b930973c3c")

# Alert System #
# h = requests.post("http://144.126.145.207/alert/", data={'latitude': '12', 'longitude': '12', 'radius': '30'})


# print(h.text)
# Get A Particular Object #
# h = requests.post("http://144.126.145.207/get_object/", data={'reference_id':'31b7d08ef1cf11eb9f4e683e261a1863'})
# print(h.text)
# Get All Objects #
# h = requests.post("http://144.126.145.207/get_all_object/")
# with open('text.json', 'w', encoding='utf-8') as f:
#     f.write(h.text)
#     f.close()
#     print(h.text)
#

def get_tim_in_zone(t, tz='US/Pacific'):
    dt = datetime.fromtimestamp(t)
    date = dt.astimezone(timezone(tz))
    return date


def fire_api(lat: float, lon: float, radius: float):
    h = requests.post("http://144.126.145.207/alert/", data={'latitude': lat, 'longitude': lon, 'radius': radius})
    return h.json()


def _has_storm_weather(dic: dict):
    weathers = list(dic["weather"])
    for weather in weathers:
        id = weather["id"]
        if 799 < id < 900:
            return True
    return False


def _get_hourly_today(dic, now):
    dt = dic["dt"]
    dt = get_tim_in_zone(dt)
    return (now.date().year == dt.date().year) and (now.date().month == dt.date().month) and (
            now.date().day == dt.date().day)


def has_storm(lat: float, lon: float):
    data = requests.get("https://api.openweathermap.org/data/2.5/onecall", params={
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,daily',
        'appid': appid
    })
    now = datetime.utcnow()
    hourly = list(filter(lambda dic: _get_hourly_today(dic, now), list(data.json()["hourly"])))
    return list(filter(lambda dic: _has_storm_weather(dic), hourly))


# a = fire_api(37.52, -122.349, 100)
# print(a)
#
# h = requests.post("http://144.126.145.207/get_object/", data={'reference_id':'31b7d08ef1cf11eb9f4e683e261a1863'})
