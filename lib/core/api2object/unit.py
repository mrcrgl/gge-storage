__author__ = 'mriegel'
from gge_proxy_manager.models import UnitList, UnitListRelation, Unit
from lib.core import DATA_IMPORT_LOCK_TIME
from django.core.cache import cache
import logging
logger = logging.getLogger(__name__)


def import_unit_list(list, game, title="", unit_list=None):

    if unit_list:
        key = "-".join(("update", "unit-list", str(game.pk), str(unit_list.pk)))
        if cache.get(key):
            return

        cache.set(key, 1, DATA_IMPORT_LOCK_TIME)

        for relation in unit_list.unit_relations.all():
            relation.delete()

    else:
        unit_list = UnitList.objects.create(title=title)

    for gge_id, count in list:
        unit, created = Unit.objects.get_or_create(game=game, gge_id=gge_id)
        relation, created = UnitListRelation.objects.get_or_create(list=unit_list, unit=unit,
                                                                   defaults={"amount": count})
        if not created:
            relation.amount += count
            relation.save()

    #logger.info("Unit list raw: %r", list)
    #logger.info("Unit list result: %r", unit_list.unit_relations.all())

    return unit_list