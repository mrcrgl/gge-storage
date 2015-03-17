__author__ = 'mriegel'
from gge_proxy_manager.models import SoldierList, SoldierListRelation, Soldier
import logging
logger = logging.getLogger(__name__)


def import_soldier_list(list, game, title="", soldier_list=None):
    if not soldier_list:
        soldier_list = SoldierList.objects.create(title=title)
    else:
        for relation in soldier_list.soldier_relations.all():
            relation.delete()

    for gge_id, count in list:
        try:
            soldier = Soldier.objects.get(game=game, gge_id=gge_id)
            SoldierListRelation.objects.create(list=soldier_list, soldier=soldier, amount=count)
        except Soldier.DoesNotExist:
            logger.error("Solder for game=%s and gge_id=%d not imported!", game.name, gge_id)

    return soldier_list