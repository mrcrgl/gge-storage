from __future__ import unicode_literals

from gge_proxy_manager.models import MapExplorer, Kingdom, Castle
from lib.socket.response import Response
from django.utils.timezone import now

__author__ = 'riegel'
import logging
logger = logging.getLogger(__name__)


class MapExplorerMiddleware():

    ticket = 'map_explorer'

    @staticmethod
    def inbound(context, message):

        if not context.is_afk:
            logger.debug("Player is not afk")
            return context, message

        if context.is_locked(module=__name__):
            logger.debug("Player context is locked")
            return context, message

        kingdom = context.get_kingdom()

        if not kingdom:
            logger.debug("Missing kingdom in context")
            return context, message

        # Try to get the correct explorer
        explorer = MapExplorer.objects.filter(kingdom__in=context.get_available_kingdoms(),
                                              active=True, circle_locked_until__lte=now())\
            .order_by('circle_locked_until').first()

        if not explorer:
            logger.debug("No MapExplorer matching this user is available. Lets wait for 10 mins.")
            context.lock_for(60*10, by=__name__, module=__name__)
            return context, message

        if not explorer.kingdom_id == kingdom.pk:

            castle = Castle.objects.filter(player=context.get_player(), kingdom=explorer.kingdom,
                                           type__in=Castle.TYPE_WITH_WARRIORS).first()

            if not castle:
                logger.warning("Player '%s' has no castle in kingdom '%s' but should.",
                               context.get_player().name, explorer.kingdom.name)
                return context, message

            response = Response(command='fwd_srv', data={
                "cmd": "jca",
                "data": {
                    "KID": int(explorer.kingdom.kid),
                    "CID": int(castle.gge_id)
                }
            })
            context.add_response(response)
            context.lock_for(120, by=__name__, module=__name__)

            logger.debug("Explorer changes kingdom '%s' to '%s'. Wait two minutes.",
                         kingdom.name, explorer.kingdom.name)

            return context, message

        do_circle = explorer.circle()

        if not do_circle:
            # logger.debug("Explorer circle is done.")
            logger.info("Map explored kingdom=%s start=%s end=%s duration=%s", explorer.kingdom.name,
                        explorer.circle_started, explorer.circle_ended,
                        (explorer.circle_ended - explorer.circle_started))
            return context, message

        logger.debug("Walk to KID=%d X1=%d X2=%d Y1=%d Y2=%d" % (kingdom.pk, explorer.current_x1, explorer.current_x2,
                                                                 explorer.current_y1, explorer.current_y2))
        response = Response(command='fwd_srv', data={
            "cmd": "gaa",
            "data": {
                "KID": int(kingdom.kid),
                "AX1": int(explorer.current_x1),
                "AX2": int(explorer.current_x2),
                "AY1": int(explorer.current_y1),
                "AY2": int(explorer.current_y2)
            }
        })
        #logger.info("Prepared to send: %s" % response)
        context.add_response(response)

        context.lock_for(explorer.lock_for, by=__name__, module=__name__)

        return context, message
