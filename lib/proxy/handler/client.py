from __future__ import unicode_literals

__author__ = 'marc'
from .engine import ProxySocket

import logging
logger = logging.getLogger(__name__)


def handle_client(connection, address):
    socket = ProxySocket(connection, address)
    socket.run()
    logger.warning("Session ended connection=%r address=%r", connection, address)
    return False