from __future__ import unicode_literals

__author__ = 'marc'


import logging
logger = logging.getLogger(__name__)

from lib.proxy.timer import SetTimeout


def request_tax_information(cls):

    message = "%xt%" + cls.product_name + "%txi%" + unicode(cls.product_number) + "%{}%"
    message += cls.close_bit

    logger.info("BOT: requested tax information")
    cls.to_server(message)


def request_tax(cls):
    if not cls.resource_key:
        return

    message = "%xt%" + cls.product_name + "%txs%" + unicode(cls.product_number) \
              + "%{\"TT\":0,\"RS\":" + unicode(cls.resource_key) + "}%"
    message += cls.close_bit

    logger.info("BOT: requested new tax")
    cls.to_server(message)


def collect_tax(cls):
    if not cls.resource_key:
        return

    message = "%xt%" + cls.product_name + "%txc%" + unicode(cls.product_number) \
              + "%{\"ACT\":0,\"RS\":" + unicode(cls.resource_key) + "}%"
    message += cls.close_bit

    logger.info("BOT: collected tax")
    cls.to_server(message)

    cls.set_timeout('tax_request', SetTimeout(request_tax, 2))