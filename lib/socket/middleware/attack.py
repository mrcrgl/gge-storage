from __future__ import unicode_literals

from gge_proxy_manager.models import Player, Castle, Alliance, Kingdom, Game, AttackLog
from pushover.models import Notify
from pushover.api.client import PushoverClient
from lib.core.api2object.castle import import_castle
from lib.core.api2object.player import import_player
from django.utils.timezone import timedelta, now
from django.db.models import Q
from django.conf import settings
from django.utils import formats

__author__ = 'riegel'
import logging
logger = logging.getLogger(__name__)


class AttackLogMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command in ['asr', 'abr']:
            return context, message

        data = message.get_data()

        A = data.get("A")
        O = data.get("O")

        M = A.get("M")

        GS = A.get("GS", 0)  # Count warrior

        GA = A.get("GA", {})  # Warrior detail list {L, M, R}
        GA_L = GA.get("L", [])
        GA_M = GA.get("M", [])
        GA_R = GA.get("R", [])

        PT = M.get("PT")  # seconds elapsed
        TT = M.get("TT")  # total time

        SID = M.get("SID")  # gge_id of source player
        TID = M.get("TID")  # gge_id of target player

        MID = M.get("MID")  # Message id

        TA = M.get("TA")  # target attack
        SA = M.get("SA")  # source attack

        HBW = M.get("HBW")  # ???

        KID = M.get("KID")

        type = 1  # By default, normal attack

        game, created = Game.objects.get_or_create(product_key=message.product)
        kingdom, created = Kingdom.objects.get_or_create(kid=int(KID), game=game)
        from_player_id = None

        if O:
            from_player_id = import_player(O, kingdom)

        time_left = int(TT) - int(PT)
        delta_left = timedelta(seconds=time_left)
        # minutes_to_go = delta_left.total_seconds() / 60

        weft = now() + delta_left

        target_castle_id = import_castle(TA, kingdom)

        if SA[0] == 9:  # Shadow
            source_castle_id = None
            type = 3
        elif SA[0] == 2:  # Raubritter
            source_castle_id = None
            type = 4
        else:
            source_castle_id = import_castle(SA, kingdom)

        if not target_castle_id or not source_castle_id:
            return context, message

        target_player_id = Castle.objects.get(pk=target_castle_id).player_id

        attack, created = AttackLog.objects.get_or_create(message_id=int(MID), defaults={
            "type": type,
            "from_castle_id": source_castle_id,
            "from_player_id": from_player_id,
            "to_castle_id": target_castle_id,
            "to_player_id": target_player_id,
            "count_warriors": None,
            "count_tools": None,
            "total_time": int(TT),
            "weft": weft,
        })

        if not created:
            attack.type = type
            attack.from_castle_id = source_castle_id
            attack.from_player_id = from_player_id
            attack.to_castle_id = target_castle_id
            attack.to_player_id = target_player_id
            attack.count_warriors = None
            attack.count_tools = None
            attack.total_time = int(TT)
            attack.weft = weft
            attack.save()

        """
        message_id = models.PositiveIntegerField()
        count_warrior = models.PositiveIntegerField(null=True, blank=True, default=None)
        count_tools = models.PositiveIntegerField(null=True, blank=True, default=None)
        total_time = models.PositiveIntegerField()
        weft = models.DateTimeField()
        """

        return context, message