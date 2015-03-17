from __future__ import unicode_literals

__author__ = 'marc'


import logging
logger = logging.getLogger(__name__)


def user_is_afk(cls):
    message = "%xt%GGEProxy%proxy_afk%" + unicode(cls.product_number) + "%{\"AFK\":1}%"
    message += cls.close_bit

    logger.info("AFK: set=true")
    cls.to_storage(message)


def user_is_back(cls):
    message = "%xt%GGEProxy%proxy_afk%" + unicode(cls.product_number) + "%{\"AFK\":-1}%"
    message += cls.close_bit

    logger.info("AFK: set=false")
    cls.to_storage(message)