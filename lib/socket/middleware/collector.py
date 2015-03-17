from __future__ import unicode_literals

from gge_proxy_manager.models import CollectLog
import logging
logger = logging.getLogger(__name__)


class CollectorMiddleware():

    @staticmethod
    def inbound(context, message):
        if True:
            return context, message

        if not message.type == 'in' or not message.command == 'irc':
            return context, message

        if not context.player:
            logger.warning("Drop. Missing player.")
            return context, message

        data = message.get_data()

        CollectLog.objects.create(
            player=context.player,
            wood=int(data['G'][0]),
            stone=int(data['G'][1]),
            food=int(data['G'][2]),
            gold=int(data['G'][3]),
            cole=int(0)
        )

        return context, message