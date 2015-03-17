from __future__ import unicode_literals

__author__ = 'marc'


import logging
logger = logging.getLogger(__name__)


def collect_walking_resources(cls):
    if not cls.resource_key:
        return

    message = "%xt%" + cls.product_name + "%irc%" + unicode(cls.product_number) \
              + "%{\"RS\":" + unicode(cls.resource_key) + "}%"
    message += cls.close_bit

    logger.info("BOT: walking resources collected")
    cls.to_server(message)