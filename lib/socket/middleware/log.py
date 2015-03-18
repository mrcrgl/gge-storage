from __future__ import unicode_literals
from lib.cache import cache

__author__ = 'riegel'
import logging
logger = logging.getLogger(__name__)


class LogMiddleware():

    @staticmethod
    def inbound(context, message):

        data_raw = message.data_raw
        if not data_raw:
            data_raw = ''

        logger.debug("message player=%s type=%s cmd=%s len=%d castle=%s afk=%s response=%r",
                     context.get_player(), message.type, message.command, len(data_raw),
                     context.get_castle(), context.is_afk, context.responses)

        if context.get_player():
            context.get_player().is_proxy_connected(True)

            key_all = 'players_online'
            all_online = cache.get(key_all, list())
            new_online = list()

            if isinstance(all_online, list):
                for online_pk in all_online:
                    if cache.get('player-last-seen-%d' % online_pk):
                        new_online += (online_pk, )

            if context.get_player().pk not in new_online:
                new_online += (context.get_player().pk, )

            cache.set(key_all, new_online, 60)

        return context, message