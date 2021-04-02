__author__ = 'Nopnithi Khaokaew'

import requests
import urllib.parse

LINE_TOKEN = ''
URL = 'https://notify-api.line.me/api/notify'


def send_alert(message):
    msg = urllib.parse.urlencode({"message": message})
    headers = {'Content-Type': 'application/x-www-form-urlencoded', "Authorization": "Bearer " + LINE_TOKEN}
    session = requests.Session()
    session.post(URL, headers=headers, data=msg)
