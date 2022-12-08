import requests
import jwt
import json
from time import time

API_KEY = '8qtIsmFBRTaBH6lP3jZiHw'
API_SEC = 'LbGxOENDtYjokwnXWyTE9VxKpXza7FhO87vS'


def generateToken():
    token = jwt.encode(

        # Create a payload of the token containing
        # API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 10000000000},

        # Secret used to generate token signature
        API_SEC,

        # Specify the hashing alg
        algorithm='HS256'
    )
    return token


def createMeeting():
    """В данном документе находятся все основные параметры встречи.
        Я проверял start time, вроде                             там что-то не так.
        Но как мы и решили ранее, ссылка формируется именно в нужное время
    """
    meetingdetails = {"topic": "The title of your zoom meeting",
                      "type": 2,
                      "start_time": "2022-11-26T10: 14:00",
                      "duration": "45",
                      "timezone": "Europe/Minsk",
                      "agenda": "test",

                      "recurrence": {"type": 1,
                                     "repeat_interval": 1
                                     },
                      "settings": {"host_video": "true",
                                   "participant_video": "true",
                                   "join_before_host": "true",
                                   "mute_upon_entry": "False",
                                   "watermark": "true",
                                   "audio": "voip",
                                   "auto_recording": "cloud"
                                   }
                      }
    headers = {'authorization': 'Bearer ' + generateToken(),
               'content-type': 'application/json'}
    r = requests.post(
        f'https://api.zoom.us/v2/users/me/meetings',
        headers=headers, data=json.dumps(meetingdetails))

    # print(r.text)
    # converting the output into json and extracting the details
    y = json.loads(r.text)
    join_URL = y["join_url"]
    meetingPassword = y["password"]
    return join_URL, meetingPassword


'''
Работать будет только с коммерческим аккаунтом в Zoom
'''
# def getMeetingDetails():
#     meetingId = '82665194632'
#     headers = {'authorization': 'Bearer ' + generateToken(),
#                'content-type': 'application/json'}
#     r = requests.get(f'https://api.zoom.us/v2/metrics/meetings/{meetingId}/', headers=headers)
#     print(r.text)
#     y = json.loads(r.text)
#     duration = y['total_minutes']
#     return duration
