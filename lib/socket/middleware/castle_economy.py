from __future__ import unicode_literals

from gge_proxy_manager.models import Kingdom
from lib.core.api2object.castle import import_castle_economy
from lib.socket.response import Response
from django.utils.timezone import now, timedelta
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

fifteen_minutes = timedelta(minutes=15)


class CastleEconomyMiddleware():
    @staticmethod
    def inbound(context, message):
        player = context.get_player()
        if not player:
            return context, message

        if not message.type == 'in' or not message.command == 'dcl':

            # maybe we request it
            got_castle_economy = context.session_get("got_castle_economy")
            request_castle_economy = context.session_get("request_castle_economy")
            if request_castle_economy:
                # already requested
                pass
            elif not got_castle_economy or (
                    isinstance(got_castle_economy, datetime) and got_castle_economy < (now() - fifteen_minutes)):
                request_castle_economy = context.session_get("request_castle_economy")
                if not request_castle_economy:
                    # add response
                    context.session_set("request_castle_economy", True)
                    response = Response(command='fwd_srv', data={
                        "cmd": "dcl",
                        "data": {
                            "CD": player.gge_id
                        }
                    })
                    logger.info("Request economy player=%s last_economy=%s", player.name, got_castle_economy)
                    context.add_response(response)

            return context, message

        """
        request_castle_economy
        got_castle_economy
        """

        context.session_set("request_castle_economy", False)
        context.session_set("got_castle_economy", now())

        game = context.get_game()
        if not game:
            return context, message

        data = message.get_data()

        economy_data = data.get("C", {})

        for in_kingdom in economy_data:
            kingdom = Kingdom.objects.get(game=game, kid=in_kingdom.get("KID"))
            for economy_by_castle in in_kingdom.get("AI", []):
                import_castle_economy(economy_by_castle, kingdom)
                logger.info("Economy imported player=%s castle_id=%d", player.name, economy_by_castle.get('AID', 0))

        return context, message
