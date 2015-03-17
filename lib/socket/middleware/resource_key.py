from __future__ import unicode_literals

__author__ = 'mriegel'
from lib.socket.response import Response
import logging
logger = logging.getLogger(__name__)


class ResourceKeyMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command == 'rsc':
            #print "Drop command %s" % message.command
            return context, message

        data = message.get_data()

        resource_key = data.get("RS")

        if resource_key:
            context.add_response(Response(command='rs', data={"RS": resource_key}))

        return context, message