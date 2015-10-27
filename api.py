
import time
import json
import datetime
from datetime import timedelta

from django.conf import settings

from firebase import Firebase
from firebase_token_generator import create_token


class FirebaseApi(object):

    def __init__(self, user_id=None):

        self.app_name = settings.FIREBASE_DB
        self.secret = settings.FIREBASE_SECRET
        self.user_id = user_id

    def get_auth_token(self):
        auth_payload = {'uid': str(self.user_id)}
        expire = datetime.datetime.now() + timedelta(days=2)
        token = create_token(self.secret, auth_payload, options={'expires': expire.strftime('%s')})
        return token

    def _request(self, path):
        return Firebase(path, auth_token=self.secret)

    def create_room(self, room):
        path = '%s/%s' % (self.app_name, room)
        print("creating room %s " % path)
        room = self._request(path)
        room.put({
            str(self.user_id): 'created room %s for user %s ' % (room, self.user_id)
        })
        return room

    def get_room(self, room):
        path = '%s/%s' % (self.app_name, room)
        return self._request(path).get()

    def get_or_create_room(self, room_name):

        # if settings.DEBUG:
        #     return

        room = self.get_room(room_name)
        if room is  None:
            room = self.create_room(room_name)
        return room

    def create_user_rooms(self):
        rooms = ['message', 'messages', 'notification', 'notifications']
        user_room = 'room-for-user-%s/' % self.user_id
        for room in rooms:
            self.get_or_create_room('%s%s' % (user_room, room))

    def put_message(self, room, data):
        path = '%s/%s/messages' % (self.app_name, room)
        return self._request(path).post(data)
        # path = '%s/%s/message' % (self.app_name, room)
        # self.save_message(room=room, data=data)
        # # return self._request(path).put(message)

    def save_message(self, room, data):
        path = '%s/%s/messages' % (self.app_name, room)
        message = self._request(path).post(data)
        return message

    def put_notification(self, room, data):
        # notify only one message
        path = '%s/%s/notification' % (self.app_name, room)
        message = data.get('message')
        message['time'] = str(time.time())
        message = json.dumps(message)
        message = self._request(path).put(str(message))
        # save notifications on 'notifications' location
        self.save_notification(room, data)
        return message

    def save_notification(self, room, data):
        # notify only one message
        path = '%s/%s/notifications' % (self.app_name, room)
        message = self._request(path).post(data.get('message'))
        return message
