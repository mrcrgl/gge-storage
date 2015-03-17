from __future__ import unicode_literals

__author__ = 'marc'


import json
import logging
logger = logging.getLogger(__name__)


def handmade_command(cmd, data):

    def command(cls):
        message = "%".join((
            "",
            "xt",
            cls.product_name,
            cmd,
            unicode(cls.product_number),
            json.dumps(data, separators=(',', ':')),
            cls.close_bit
        ))

        if '##RSKEY##' in message and not cls.resource_key:
            logger.warning("Drop handmade command. Invalid cls.resource_key")
            return

        message = message.replace('"##RSKEY##"', cls.resource_key)

        logger.info("Handmade command: %r", message)
        cls.to_server(message)

    return command