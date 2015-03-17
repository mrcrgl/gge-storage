__author__ = 'mriegel'

from gge_proxy_manager.models import Player, PlayerEconomy, Kingdom
from gge_proxy_manager.methods import clean_duplicate_players
from django.core.cache import cache
from .alliance import import_alliance
from lib.core import DATA_IMPORT_LOCK_TIME
from pushover.api.client import PushoverClient
from django.conf import settings
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
User = get_user_model()

import logging
logger = logging.getLogger(__name__)


#def import_players(ais, kingdom):
#    return [import_castle(ai, kingdom) for ai in ais]


def import_player(oi, kingdom):
    alliance_id = import_alliance(oi, kingdom)
    bypass_alliance = False

    if oi.get("AID", None) is None:
        bypass_alliance = True

    if int(oi.get("OID")) < 0:
        return

    key = "-".join(("update", "player", str(kingdom.game_id), str(oi.get("OID", "null"))))
    player_id = cache.get(key)
    if player_id:
        return player_id

    defaults = {
        "name": oi.get("N"),
        "level": int(oi.get("L", 0)),
        "honor": int(oi.get("H", 0)),
        "fame": int(oi.get("CF", 0)),
        "success": int(oi.get("AVP", 0)),
        "is_ruin": bool(oi.get("R", 0)),
        # "alliance_rank": int(oi.get("AR")) if oi.get("AR", None) is not None else None,
        # "alliance": alliance
    }

    if oi.get("AR", None) is not None:
        defaults['alliance_rank'] = int(oi.get("AR"))

    if not bypass_alliance:
        defaults['alliance_id'] = alliance_id

    try:
        player, created = Player.objects.get_or_create(game=kingdom.game, gge_id=int(oi.get("OID")),
                                                       defaults=defaults)
    except Player.MultipleObjectsReturned:
        qs = Player.objects.filter(game=kingdom.game, gge_id=int(oi.get("OID")))
        clean_duplicate_players(qs)
        player = Player.objects.get(game=kingdom.game, gge_id=int(oi.get("OID")))

    if not created:
        player.name = oi.get("N")
        if oi.get("L"):
            player.level = int(oi.get("L"))
        if oi.get("H"):
            player.honor = int(oi.get("H"))
        if oi.get("CF"):
            player.fame = int(oi.get("CF"))
        if oi.get("AVP"):
            player.success = int(oi.get("AVP"))
        is_ruin = bool(oi.get("R", 0))

        if is_ruin and not player.is_ruin and not player.alliance_id:
            # notify if player becomes a ruin
            notify_new_ruin(player)

        if player.is_ruin and (player.alliance_id and not alliance_id):
            # Notify if a ruin becomes non alliance member
            notify_new_ruin(player)

        player.is_ruin = is_ruin

        if oi.get("AR", None) is not None:
            player.alliance_rank = int(oi.get("AR"))

        if not bypass_alliance:
            # logger.info("Alliance ID: %r", alliance_id)
            player.alliance_id = alliance_id

        try:
            player.save()
        except IntegrityError as e:
            transaction.rollback()
            logger.warning("IntegrityError player_id=%r alliance_id=%r oi='%r' error=%r"
                           % (player_id, alliance_id, oi, e))

    cache.set(key, player.pk, DATA_IMPORT_LOCK_TIME)

    return player.pk


def notify_new_ruin(player):

    if player.castles_who_are_villages().count() < 1:
        return

    PUSHOVER_NEW_RUIN_TOKEN = getattr(settings, "PUSHOVER_NEW_RUIN_TOKEN")

    if not PUSHOVER_NEW_RUIN_TOKEN:
        return

    villages = {}

    for village in player.castles_who_are_villages():
        if village.kingdom_id not in villages:
            villages[village.kingdom.name] = 0

        villages[village.kingdom.name] += 1

    title = "Neue Ruine: %s" % player.name
    message = "Doerfer:\n" + "\n".join(["%s: %d" % (k, villages[k]) for k in villages])

    api = PushoverClient()
    api.push(PUSHOVER_NEW_RUIN_TOKEN, message, title, priority=0)

    #notify = getattr(settings, "NOTIFY_NEW_RUIN", {})
    #notify_users = notify.get(player.game.product_key, list())

    #for email, username in notify_users:
    #    user = None
    #    if username:
    #        try:
    #            user = User.objects.get(username=username)
    #        except User.DoesNotExist:
    #            pass

    #    send_message(
    #        "socket.notify.new_ruin",
    #        email,
    #        {
    #            "user": user,
    #            "ruin": player,
    #        }
    #    )


def import_player_economy(ai, player):

    try:
        economy = player.economy
    except PlayerEconomy.DoesNotExist:
        economy = PlayerEconomy.objects.create(player=player, ruby=0, gold=0)

    economy.ruby = ai.get("C2", 0)
    economy.gold = ai.get("C1", 0)

    try:
        economy.save()
    except Exception, e:
        logger.exception("PlayerEconomy save failed with exception: %s (%s)", e, ai)