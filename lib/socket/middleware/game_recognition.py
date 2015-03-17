from __future__ import unicode_literals

from gge_proxy_manager.models import Game

__author__ = 'riegel'
import logging
logger = logging.getLogger(__name__)


class GameRecognitionMiddleware():

    @staticmethod
    def inbound(context, message):
        if message.product == 'GGEProxy' or context.get_game() or not message.is_valid:
            return context, message

        game = Game.objects.get(product_key=message.product)

        context.set_game(game)

        return context, message