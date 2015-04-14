from __future__ import unicode_literals

from django.db import IntegrityError
from lib.core.api2object.player import import_player
from lib.core.api2object.castle import import_castle
from gge_proxy_manager.models import Player, Castle, Alliance, Kingdom, Game
import logging

logger = logging.getLogger(__name__)


class GeotrackingMiddleware():
    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command == 'gaa':
            return context, message

        data = message.get_data()

        if data.get("KID", None) is None:
            logger.warning("Missing KID attribute. Need code update. Ignore message.")
            return context, message

        game, created = Game.objects.get_or_create(product_key=message.product)
        kingdom, created = Kingdom.objects.get_or_create(kid=int(data.get("KID")), game=game)

        if data.get("OI"):
            for oi in data.get("OI", []):
                # Players
                try:
                    player_id = import_player(oi, kingdom)
                except (ValueError, IntegrityError) as e:
                    logger.error("Import player failed: '%r' %r", oi, e)

        if data.get("AI"):
            for ai in data.get("AI", []):
                # Castles
                castle_id = import_castle(ai, kingdom)

        return context, message
