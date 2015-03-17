from __future__ import unicode_literals

__author__ = 'riegel'
import logging
logger = logging.getLogger(__name__)


class AuthMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'out' or not message.command == 'core_lga':
            return context, message

        data = message.get_data()

        try:
            username = data.get("NM")
        except KeyError:
            logger.exception("Auth middleware failed. KeyError on data")
            return context, message

        logger.info("Set username to: %s", username)
        context.set_username(username)

        return context, message