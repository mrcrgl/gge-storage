from __future__ import unicode_literals

__author__ = 'riegel'
import logging
logger = logging.getLogger(__name__)


class AfkMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.command == 'core_afk':
            return context, message

        afk = message.get_data()

        if afk is False:
            context.set_afk(True)
        else:
            context.set_afk(False)

        return context, message


        #if not message.product == 'GGEProxy' or not message.command == 'xxx_afk':
        #    return context, message

        #data = message.get_data()

        #try:
        #    afk = data.get("AFK")
        #    context.set_afk(afk)
        #except KeyError:
        #    logger.exception("Auth middleware failed. KeyError on data")

        #return context, message