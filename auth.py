
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
