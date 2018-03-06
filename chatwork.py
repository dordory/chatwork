# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from urllib import urlencode
import urllib2
import json
import os

# TKN = os.getenv('CHATWORK_TOKEN', 'd64d734986d8e47d9224e121ca53003d')
# VER = os.getenv('CHATWORK_API_V', 'https://api.chatwork.com/v2')
TKN = os.getenv('CHATWORK_TOKEN', '')
VER = os.getenv('CHATWORK_API_V', '')


class ChatworkWrapper:
    def __init__(self, token=TKN, ver=VER):
        self.TOKEN = token
        self.API_V = ver

    def api(self, path, data=None):
        if data:
            data = urlencode(data)

        header = {"X-ChatWorkToken": self.TOKEN}
        req = urllib2.Request(self.API_V + path, data=data, headers=header)
        res = urllib2.urlopen(req)

        # get response data
        bffr = res.read()

        # binary literal to utf-8
        strg = bffr.decode('utf-8')

        # str to json
        rslt = json.loads(strg)
        info = dict(res.info())
        return (rslt, info)

    def message(self, name, message):
        room = self.room_id(name)
        data = {"body": message.encode('utf-8')}
        return self.api('/rooms/%s/messages' % room, data)

    def status(self):
        return self.api('/my/status', None)[0]

    def rooms(self, name=None):
        rooms = self.api('/rooms', None)[0]
        if name:
            return [ Room(self, **room) for room in rooms if room['name'].find(name) > 0 ]
        else:
            return [ Room(self, **room) for room in rooms ]

    def room(self, name):
        rooms = self.api('/rooms', None)[0]
        l = [ Room(self, **room) for room in rooms if room['name'] == name ]
        return l[0] if l else None
        
        
    def contacts(self, name=None):
        cs = self.api('/contacts', None)[0]
        if name:
            return [ Contact(self, **c) for c in cs if c['name'].find(name) > 0 ]
        else:
            return [ Contact(self, **c) for c in cs ]

    def contact(self, name):
        cs = self.api('/contacts', None)[0]
        l =  [ Contact(self, **c) for c in cs if c['name'] == name ]
        return l[0] if l else None


class Contact:
    def __init__(self, cw, **kwargs):
        self.cw = cw
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __str__(self):
        return self.name.encode('utf-8')

    def send(self, msg):
        data = {'body': msg.encode('utf-8')}
        return self.cw.api('/rooms/{}/messages'.format(self.room_id), data)

    def get(self, force=0):
        msgs, r =  self.cw.api('/rooms/{}/messages?force={}'.format(self.room_id, force), None)
        print('msgs:', msgs)
        return [ Message(**msg) for msg in msgs ]


class Room(Contact):
    def __init__(self, cw, **kwargs):
        self.cw = cw
        for k, v in kwargs.iteritems():
            setattr(self, k, v)


class Message:
    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

    def __str__(self):
        return self.body.encode('utf-8')

    def sender(self):
        return self.account['name'].encode('utf-8')
