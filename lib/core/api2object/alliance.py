__author__ = 'mriegel'

from gge_proxy_manager.models import Alliance
from lib.cache import cache
from lib.core import DATA_IMPORT_LOCK_TIME
import logging
logger = logging.getLogger(__name__)


def import_alliance(oi, kingdom):
    response = import_alliance_(oi, kingdom)

    logger.info("Import alliance AID=%r response=%r", oi.get('AID', None), response)

    return response


def import_alliance_(oi, kingdom):
    if not oi.get("AID") or int(oi.get("AID")) < 0:
        return None

    key = "-".join(("update", "alliance", str(kingdom.game_id), str(oi.get("AID", "null"))))
    alliance_id = cache.get(key)
    if alliance_id:
        logger.info("Import alliance key=%s AID=%r cached=True alliance_id=%r", key, oi.get('AID', None), alliance_id)
        return alliance_id

    if not isinstance(alliance_id, int) and alliance_id is not None:
        logger.info("Import alliance AID=%r skipped=True alliance_id=%r", oi.get('AID', None), alliance_id)
        return None

    alliance, created = Alliance.objects.get_or_create(game_id=kingdom.game_id, gge_id=int(oi.get("AID")),
                                                       defaults={
                                                           "name": oi.get("AN"),
                                                           "fame": int(oi.get("ACF", 0))  #,
                                                           #"level": int(oi.get("AR"))
                                                       })

    if not created:
        alliance.name = oi.get("AN")
        alliance.fame = int(oi.get("ACF", 0))
        alliance.level = 0
        alliance.save()

    logger.info("Import alliance key=%s AID=%r created=%r alliance_id=%r", key, oi.get('AID', None), created, alliance.id)
    cache.set(key, alliance.id, DATA_IMPORT_LOCK_TIME)
    
    return alliance.pk