
import json
import httplib

from django.conf import settings

from common.utils import app_logger


class Parse(object):

    def __init__(self, *args, **kwargs):
        self.parse_domain   = 'https://api.parse.com'
        self.parse_app_id  = settings.PARSE_APP_ID
        self.parse_rest_key = settings.PARSE_REST_KEY
        self.parse_master_key = settings.PARSE_MASTER_KEY
        self.connection = httplib.HTTPSConnection('api.parse.com', 443)
        self.connection.connect()

    def get_keys(self):
        return {
           "X-Parse-Application-Id": self.parse_app_id,
           "X-Parse-REST-API-Key": self.parse_rest_key,
           "Content-Type": "application/json"
        }

    def create_installation(self, data):
        self.connection.request('POST', '/1/installations', json.dumps(data), self.get_keys())
        result = json.loads(self.connection.getresponse().read())
        return result

    def get_installation(self, object_id):
        self.connection.request('GET', '/1/installations/%s' % object_id, '', self.get_keys())
        result = json.loads(self.connection.getresponse().read())
        return result

    def get_all_installations(self):
        self.connection.request('GET', '/1/installations', '', {
            "X-Parse-Application-Id": self.parse_app_id,
            "X-Parse-Master-Key": self.parse_master_key
        })
        result = json.loads(self.connection.getresponse().read())
        return result

    def create_object(self, data, location='Articles'):
        path = '/1/classes/%s/' % location
        self.connection.request('POST', path, json.dumps(data), self.get_keys())
        results = json.loads(self.connection.getresponse().read())
        return results

    def get_object(self, object_id, location='Articles'):
        path = '/1/classes/%s/%s' % (location, object_id)
        self.connection.request('GET', path, '', self.get_keys())
        result = json.loads(self.connection.getresponse().read())
        return result

    def send_push_to_channel(self, channel, data, title='', location='Articles'):
        object_created = self.create_object(data=data, location=location)
        object_id = object_created.get('objectId')

        push_type = data.get('object_type', 'article')

        self.connection.request('POST', '/1/push', json.dumps({
            'channels': [channel],
            'data': {
                'alert': '',
                'title': title,
                'content-available': 1,
                'object_id': object_id,
                'push_type': push_type,
                'user_id': data.get('user_id', 0),
                'conversation_channel': data.get('conversation_channel', '')
            }
        }), self.get_keys())
        result = json.loads(self.connection.getresponse().read())
        return result

    def send_push_to_all(self, data):
        article = self.create_object(data)
        object_id = article.get('objectId')

        installations = self.get_all_installations().get('results', [])
        all_channels = []
        for installation in installations:
            if 'channels' in installation:
                all_channels += installation['channels']

        self.connection.request('POST', '/1/push', json.dumps({
            'channels': all_channels,
            'data': {
                'alert': '',
                'object_id': object_id
            }
        }), self.get_keys())

        result = json.loads(self.connection.getresponse().read())
        return result
