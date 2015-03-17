from gge_proxy_manager.models import Castle, Player, Alliance
from django.conf import settings
import requests
import json


def bot_login(username, password):
    secret = settings.LOGIN_SERVICE_SECRET
    service_host = settings.LOGIN_SERVICE_URL

    payload = {
        "username": username,
        "password": password,
        "secret": secret
    }
    headers = {'content-type': 'application/json'}

    r = requests.post(service_host, data=json.dumps(payload), headers=headers)
    if r.status_code == 202:
        return True

    return False


def calc_players_dangerously(level, honor):
    """
    Returns a float between 0 and 1

    honor influences this calculation:
        Min honor = 0
        Max honor = 5000

    honor_index is a value between 0.003 and 0.00469
    and represents the honor in this calc

    the courve works fine for levels 5-60
    """

    honor_index = ((0.00469 - 0.003) / 5000 * honor) + 0.003

    return (level ** (honor_index * (level ** 2)/100)) - 1


def clean_duplicate_castles():
    castles = Castle.objects.raw("select * from gge_proxy_manager_castle c1 where (select count(*) from gge_proxy_manager_castle c2 where c1.kingdom_id=c2.kingdom_id and c1.gge_id=c2.gge_id) > 1")

    mapped = map_by_gge(castles)

    print "Found: %d castles with duplicates." % len(mapped)

    for gge_id in mapped.keys():
        duplicates = mapped[gge_id]
        original = duplicates.pop()

        # What relations do we have?
        # AttackLog, ResourceBalanceLog
        for duplicate in duplicates:

            for received_attack in duplicate.got_attacks.all():
                print "Change relation of %r" % received_attack
                received_attack.to_castle = original
                received_attack.save()

            for sent_attack in duplicate.sent_attacks.all():
                print "Change relation of %r" % sent_attack
                sent_attack.from_castle = original
                sent_attack.save()

            #
            for resource_balance in duplicate.resource_balances.all():
                print "Change relation of %r" % resource_balance
                resource_balance.castle = original
                resource_balance.save()

            print "Remove duplicate: %d" % duplicate.pk
            duplicate.delete()


def clean_duplicate_players(players=None):
    if not players:
        players = Player.objects.raw("select * from gge_proxy_manager_player c1 where (select count(*) from gge_proxy_manager_player c2 where c1.game_id=c2.game_id and c1.gge_id=c2.gge_id) > 1")

    mapped = map_by_gge(players)

    print "Found: %d players with duplicates." % len(mapped)

    for gge_id in mapped.keys():
        duplicates = mapped[gge_id]
        original = duplicates.pop()

        # What relations do we have?
        # AttackLog, ResourceBalanceLog
        for duplicate in duplicates:

            for received_attack in duplicate.got_attacks.all():
                print "Change relation of %r" % received_attack
                received_attack.to_player = original
                received_attack.save()

            for sent_attack in duplicate.sent_attacks.all():
                print "Change relation of %r" % sent_attack
                sent_attack.from_player = original
                sent_attack.save()

            for resource_balance in duplicate.resource_balances.all():
                print "Change relation of %r" % resource_balance
                resource_balance.player = original
                resource_balance.save()

            for collect_log in duplicate.collect_logs.all():
                print "Change relation of %r" % collect_log
                collect_log.player = original
                collect_log.save()

            for balance_log in duplicate.balance_logs.all():
                print "Change relation of %r" % balance_log
                balance_log.player = original
                balance_log.save()

            for history in duplicate.alliance_history.all():
                print "Change relation of %r" % history
                history.player = original
                history.save()

            for history in duplicate.level_history.all():
                print "Change relation of %r" % history
                history.player = original
                history.save()

            for history in duplicate.honor_history.all():
                print "Change relation of %r" % history
                history.player = original
                history.save()

            for castle in duplicate.castles.all():
                print "Change relation of %r" % castle
                castle.player = original
                castle.save()

            for resource_collect_log in duplicate.resource_collect_logs.all():
                print "Change relation of %r" % resource_collect_log
                resource_collect_log.player = original
                resource_collect_log.save()

            print "Remove duplicate: %d" % duplicate.pk
            duplicate.delete()


def clean_duplicate_alliances():
    alliances = Alliance.objects.raw("select * from gge_proxy_manager_alliance c1 where (select count(*) from gge_proxy_manager_alliance c2 where c1.game_id=c2.game_id and c1.gge_id=c2.gge_id) > 1")

    mapped = map_by_gge(alliances)

    print "Found: %d alliances with duplicates." % len(mapped)

    for gge_id in mapped.keys():
        duplicates = mapped[gge_id]
        original = duplicates.pop()

        # What relations do we have?
        # AttackLog, ResourceBalanceLog
        for duplicate in duplicates:

            for relation in duplicate.relation_a.all():
                print "Change relation of %r" % relation
                relation.alliance_a = original
                relation.save()

            for relation in duplicate.relation_b.all():
                print "Change relation of %r" % relation
                relation.alliance_b = original
                relation.save()

            for player in duplicate.players.all():
                print "Change relation of %r" % player
                player.alliance = original
                player.save()

            for history in duplicate.player_history.all():
                print "Change relation of %r" % history
                history.alliance = original
                history.save()

            print "Remove duplicate: %d" % duplicate.pk
            duplicate.delete()


def map_by_gge(queryset):
    mapped = {}

    for object in queryset:
        if not object.gge_id in mapped.keys():
            mapped[object.gge_id] = []

        mapped[object.gge_id].append(object)

    return mapped