from __future__ import unicode_literals

__author__ = 'mriegel'
from gge_proxy_manager.models import AccountBalanceLog
from lib.core.api2object.player import import_player_economy
import logging
logger = logging.getLogger(__name__)


class GoodsCollectedMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'in':
            return context, message

        if message.command == 'txc':
            data = message.get_data().get("gcu")
        elif message.command == 'txs':
            data = message.get_data().get("gcu")
        elif message.command == 'gcu':
            data = message.get_data()
        else:
            return context, message

        if not context.player:
            logger.warning("Drop. Missing player.")
            return context, message

        # data = message.get_data()

        AccountBalanceLog.objects.create(
            player=context.player,
            gold=int(data.get('C1', 0)),
            ruby=int(data.get('C2', 0))
        )

        import_player_economy(data, context.get_player())

        return context, message