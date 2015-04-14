__author__ = 'mriegel'

from gge_proxy_manager.models import Player, Castle, CastleEconomy, UnitList
from lib.cache import cache
from .unit import import_unit_list
from lib.core import DATA_IMPORT_LOCK_TIME
import logging
logger = logging.getLogger(__name__)


def import_castles(ais, kingdom):
    return [import_castle(ai, kingdom) for ai in ais]


def import_castle(ai, kingdom):
    key = "-".join(("update", "castle", str(kingdom.game_id), str(ai[3])))
    castle_id = cache.get(key)
    if castle_id:
        return castle_id

    player = None

    try:
        player_id = int(ai[4])
    except IndexError:
        return None

    if player_id > 0:
        try:
            player, created = Player.objects.get_or_create(game_id=kingdom.game_id, gge_id=player_id)
        except BaseException as e:
            logger.exception("Player.get_or_create failed (id: %d): %s", player_id, e)
    else:
        player = None

    if int(ai[0]) == 11:
        #  Barbarenfestung
        return None

    if int(ai[0]) == 17:
        #  Unbekannt
        return None

    try:
        if int(ai[0]) == 10:
            name = ai[8]  # RSD
        else:
            name = ai[10]
    except IndexError:
        name = ""

    if int(ai[3]) == -1:
        #  is ruin
        #try:
        #    c = Castle.objects.get(kingdom=kingdom, pos_x=ai[1], pos_y=ai[2], is_ruin=False)
        #    c.is_ruin = True
        #    c.save()
        #except Castle.DoesNotExist:
        #    pass
        return

    if not isinstance(name, unicode) or not len(name):
        name = None

    castle, created = Castle.objects.get_or_create(
        game_id=kingdom.game_id,
        gge_id=int(ai[3]),
        kingdom=kingdom,
        defaults={
            "pos_x": ai[1],
            "pos_y": ai[2],
            "player": player,
            "type": ai[0],
            "resource_type": ai[5],
            "name": name,
            "kid": kingdom.kid,
            "kingdom": kingdom})

    if not created:
        castle.pos_x = ai[1]
        castle.pos_y = ai[2]
        castle.player = player
        castle.type = ai[0]
        castle.resource_type = ai[5]
        castle.name = name
        castle.kingdom = kingdom
        castle.save()

    cache.set(key, castle.pk, DATA_IMPORT_LOCK_TIME)

    return castle.pk


def import_castle_economy(ai, kingdom, castle=None):
    if not ai.get("AID") or int(ai.get("AID")) < 0:
        return None

    if not castle:
        try:
            castle = Castle.objects.get(kingdom=kingdom, gge_id=ai.get("AID"))
        except Castle.DoesNotExist:
            return None

    try:
        economy = castle.economy
    except CastleEconomy.DoesNotExist:
        economy = CastleEconomy.objects.create(castle=castle)

    economy.defence_points = ai.get("D")
    economy.wood_stock = ai.get("W", 0)
    economy.stone_stock = ai.get("S", 0)
    economy.cole_stock = ai.get("C", 0)
    economy.food_stock = ai.get("F", 0)
    economy.barrows = ai.get("MC", 0)

    gpa = ai.get("gpa", {})

    economy.guards = gpa.get("GRD", 0)
    economy.citizen = gpa.get("P", 0)
    economy.stock_size = gpa.get("MRF", 0)
    economy.public_order = gpa.get("NDP", 0)
    economy.wood_production = gpa.get("DW", 0) / 10
    economy.stone_production = gpa.get("DS", 0) / 10
    economy.cole_production = gpa.get("DC", 0) / 10
    economy.food_production = gpa.get("DF", 0) / 10
    economy.food_consumption = gpa.get("DFC", 0) / 1000 * gpa.get("FCR", 100)

    ac = ai.get("AC", [])

    if not economy.unit_list_id:
        economy.unit_list = UnitList.objects.create(title="")

    economy.unit_list = import_unit_list(ac, castle.game, unit_list=economy.unit_list)

    try:
        economy.save()
    except Exception, e:
        logger.exception("CastleEconomy save failed with exception: %s (%s)", e, ai)
    # economy.warrior_list =
