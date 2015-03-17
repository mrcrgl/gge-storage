from __future__ import unicode_literals

from django.conf import settings
import requests
import json
import logging
logger = logging.getLogger(__name__)

PUSHOVER_APP_TOKEN = getattr(settings, "PUSHOVER_APP_TOKEN", None)


class PushoverClient(object):

    api_url = 'https://api.pushover.net/1/%s.json'

    def __init__(self):
        pass

    def push(self, user, message, title=None, priority=0, retry=None, expire=None):
        url = self.api_url % 'messages'

        if priority is 2 and (not retry or not expire):
            raise AttributeError("priority=2 requires retry and expire")

        payload = {
            'token': PUSHOVER_APP_TOKEN,
            'user': user,
            'message': message,
            'title': title,
            'priority': priority,
            'retry': retry,
            'expire': expire
        }

        try:
            response = requests.post(url, data=payload)
        except requests.RequestException, e:
            logger.error("url=%s payload=%r error=%r", url, payload, e)
            return False

        if response.status_code == 200:
            logger.info("api.push user=%s code=%d message=%s", user, response.status_code, response.text)
            return True

        if response.status_code >= 400 and response.status_code < 500:
            # Invalid input, maybe do some stuff
            pass

        logger.warning("api.push user=%s code=%d message=%s", user, response.status_code, response.text)
        # json.loads(response.text)
        return False

    def verify(self, user):
        url = self.api_url % 'users/validate'

        payload = {
            'token': PUSHOVER_APP_TOKEN,
            'user': user
        }

        try:
            response = requests.post(url, data=payload)
        except requests.RequestException, e:
            logger.error("url=%s payload=%r error=%r", url, payload, e)
            return False

        r = json.loads(response.text)
        status = r.get('status', 0)

        if status:
            logger.info("api.verify user=%s status=%d", user, status)
            return True

        logger.warning("api.verify user=%s status=%d", user, status)
        # json.loads(response.text)
        return False