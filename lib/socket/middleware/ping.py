from __future__ import unicode_literals

__author__ = 'riegel'

from lib.socket.response import Response
# import unicodedata


class PingMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'out' or not message.command == 'ping':
            context.is_not_silent()
            return context, message

        context.is_silent()
        context.add_response(Response(command='pong'))

        return context, message