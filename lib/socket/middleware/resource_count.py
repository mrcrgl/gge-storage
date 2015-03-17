from __future__ import unicode_literals

__author__ = 'mriegel'
from gge_proxy_manager.models import ResourceBalanceLog, Castle
import logging
logger = logging.getLogger(__name__)


class ResourceCountMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command == 'grc' or not context.get_game():
            #print "Drop command %s" % message.command
            return context, message

        data = message.get_data()

        aid = int(data.get('AID', 0))

        if aid < 1:
            return context, message

        try:
            castle = Castle.objects.get(gge_id=aid, game=context.get_game())
        except Castle.DoesNotExist:
            logger.info("Castle with gge_id=%d not imported." % int(data['AID']))
            return context, message

        if not context.player or not context.castle or not context.kingdom:
            logger.warning("Drop. Missing player. Set to: %s" % castle.player.name)
            context.player = castle.player
            context.set_castle(castle)

        if not context.kingdom.pk == castle.kingdom_id:
            context.set_castle(castle)

        wood = data.get('W', 0)
        stone = data.get("S", 0)
        food = data.get("F", 0)
        cole = data.get("C", 0)

        ResourceBalanceLog.objects.create(
            player=context.player,
            castle=castle,
            wood=float(wood),
            stone=float(stone),
            food=float(food),
            cole=float(cole)
        )

        return context, message
