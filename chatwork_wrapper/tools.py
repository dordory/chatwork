# coding: utf-8
from __future__ import unicode_literals

from django.conf import settings

import urllib2
import urllib
import requests
import pprint
import json


class ChatWork:
    TOKEN = settings.CHATWORK_TOKEN
    API_V = settings.ENDPOINT

    def message(self, name, message):
        room = room_id(name)
        data = {"body": message.encode('utf-8')}
        print '/rooms/%s/messages' % room
        return api('/rooms/%s/messages' % room, data)


def dailyReportToChatWork(message):
    sendMessage(settings.DAILY_REPORT_ROOM_ID, message)


def sendMessage(room_id, message):
    TOKEN = settings.CHATWORK_TOKEN
    API_V = settings.ENDPOINT

    url = '{}/rooms/{}/messages'.format(API_V, room_id)
    header = {'X-ChatWorkToken': TOKEN}
    message = {'body': message}

    pprint.pprint(requests.post(url, headers=header, params=message).content)


def api(path, data=None):
    TOKEN = settings.CHATWORK_TOKEN
    API_V = settings.ENDPOINT

    if data is not None:
        data = urllib.urlencode(data)
        data = data.encode('utf-8')

    header = {"X-ChatWorkToken": TOKEN}
    req = urllib2.Request(API_V + path, data=data, headers=header)
    rslt = urllib2.urlopen(req)
    r = json.loads(rslt.read().decode("utf-8"))
    f = dict(rslt.info())
    return (r, f)


def room_id(name):
    rooms, info = api('/rooms', None)
    for room in rooms:
        if room['name'] == name:
            return room['room_id']
    return None


def message(name, message):
    room = room_id(name)
    data = {"body": message.encode('utf-8')}
    print '/rooms/%s/messages' % room
    return api('/rooms/%s/messages' % room, data)
