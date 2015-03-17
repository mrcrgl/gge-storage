from __future__ import unicode_literals

from django.conf import settings
from lib.core.utils import load_class
from .exceptions import DeadConnectionException
import logging
logger = logging.getLogger(__name__)


class MiddlewareCache(object):
    _cache = None

    def __init__(self):
        self._cache = {}

    def get(self, key):

        if not key in self._cache:
            self.set(key, self.load(key))

        return self._cache.get(key)

    def set(self, key, value):
        self._cache[key] = value

    def load(self, key):
        return load_class(key)


class MessageProcessor():

    context = None
    socket = None
    middleware = None
    _middleware_classes = None

    def __init__(self, socket):
        self.socket = socket
        self.context = socket.context
        self._middleware_classes = getattr(settings, 'SOCKET_MIDDLEWARE_CLASSES')
        self.middleware = MiddlewareCache()

    def process_message(self, message):

        for middleware in self._middleware_classes:

            try:
                Middleware = self.middleware.get(middleware)
                context, message = Middleware.inbound(self.context, message)
                self.context = context
            except KeyError:
                logger.exception("KeyError in middleware '%s' at '%s' ", middleware, message)
            except DeadConnectionException as e:
                #raise e
                pass
            #except InterfaceError:
            #    close_connection()
            except Exception as e:
                logger.exception(
                    "Unknown Exception thrown in middleware '%s' [%s] [%s] with '%s'",
                    middleware,
                    e.message,
                    e.args,
                    message
                )

        return self.context