import json

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import datetime

from firebase_admin import messaging
from django.utils import timezone
from user.models import Property, User, Notification
from user.utils import has_storm, get_tim_in_zone, fire_api

from oauth2client.service_account import ServiceAccountCredentials
import requests

PROJECT_ID = 'inflame-wildfire'
BASE_URL = 'https://fcm.googleapis.com'
FCM_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/messages:send'
FCM_URL = BASE_URL + '/' + FCM_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.messaging']


def _get_access_token():
    """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
    credentials = ServiceAccountCredentials.from_json_keyfile_name('service-account.json', SCOPES)
    access_token_info = credentials.get_access_token()
    return access_token_info.access_token


def delete_24_early_notifications():
    dt = timezone.now() - timedelta(days=1)
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    Notification.objects.filter(created__lt=start).delete()


def save_notification(property: int, type: str, distance: float):
    p = Property.objects.get(pk=property)
    n = Notification(property=p, type=type, distance=distance)
    n.save()


def send_notification(device_token: str, title: str, text: str):
    """

    {
      "message":{
        "token":"...",
        "notification":{
          "title":"Portugal vs. Denmark",
          "body":"great match!"
        }
      }
    }

    :param device_token:
    :param title:
    :param text:
    :return:
    """

    headers = {
        'Authorization': 'Bearer ' + _get_access_token(),
        'Content-Type': 'application/json; UTF-8',
    }
    fcm_message = {
        "message": {
            "token": device_token,
            "notification": {
                "title": title,
                "body": text
            }
        }
    }
    resp = requests.post(FCM_URL, data=json.dumps(fcm_message), headers=headers)

    if resp.status_code == 200:
        print('Message sent to Firebase for delivery, response:')
        print(resp.text)
    else:
        print('Unable to send message to Firebase')
        print(resp.text)


def send_storm_notifications() -> str:
    print("-------------")
    users = User.objects.filter(weather_monitoring_is_on=True).values()
    for u in users:
        id = u["id"]
        device_token = u["device_token"]
        properties = Property.objects.filter(user=id).values()
        for property in properties:
            lat = property["latitude"]
            lon = property["longitude"]
            property_name = property["property_name"]
            storms = has_storm(lat, lon)
            for storm in storms:
                dt = get_tim_in_zone(storm["dt"])
                title = "Storm Detected"
                text = f'Storm Expected Around {dt} near {property_name}. Watch out for lightning-sparked fires'
                send_notification(device_token, title, text)


def sent_fire_notification():
    users = User.objects.filter(fire_monitoring_is_on=True).values()
    for u in users:
        id = u["id"]
        device_token = u["device_token"]
        properties = Property.objects.filter(user=id).values()
        for property in properties:
            property_id = property["id"]
            lat = property["latitude"]
            lon = property["longitude"]
            radius = float(property["radius"])
            property_name = property["property_name"]
            fire = dict(fire_api(lat, lon, radius))
            if "distance" in list(fire.keys()):
                distance = float(fire["distance"])
                if distance >= radius:  # TODO: change to <=
                    dt = timezone.now() - timedelta(days=1)
                    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
                    notification_sent_within_24 = Notification.objects.filter(property=property_id,
                                                                              created__gt=start).values()
                    title = "Fire Detected"
                    if not len(list(notification_sent_within_24)) > 0:  # Not sent within 24h
                        text = f'Urgent Fire Alert, Wildfire Detected {distance} from {property_name}.' \
                               f'Tap for more info.'
                        save_notification(property_id, 'fire', distance)
                        send_notification(device_token, title, text)
                    else:
                        last = list(notification_sent_within_24)[len(list(notification_sent_within_24)) - 1]


def check_storm():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(send_storm_notifications, 'interval', minutes=100, next_run_time=datetime.utcnow())
    # TODO: change time to start
    scheduler.start()


def check_fire():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(sent_fire_notification, 'interval', minutes=25, next_run_time=datetime.utcnow())
    scheduler.start()


def notification_garbage_cleaner():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(delete_24_early_notifications, 'interval', minutes=60, next_run_time=datetime.utcnow())
    scheduler.start()