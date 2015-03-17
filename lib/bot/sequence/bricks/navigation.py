from lib.bot.sequence.base import SequenceBrick
from lib.socket.response import Response

import logging
logger = logging.getLogger(__name__)


class GoToCastleBrick(SequenceBrick):

    def __init__(self, castle):
        def action(cls, context, message):

            context.add_response(
                Response(command='fwd_srv', data={
                    "cmd": "jaa",
                    "data": {
                        "PY": castle.pos_y,
                        "PX": castle.pos_x,
                        "KID": castle.kingdom.kid,
                    }
                })
            )

            logger.info("Visit castle=%s x=%d y=%d kingdom=%s", castle.name, castle.pos_x, castle.pos_y,
                        castle.kingdom.name)

            return context, message

        self.set_action(action)