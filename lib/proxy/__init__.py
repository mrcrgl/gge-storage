from __future__ import unicode_literals

import socket
import multiprocessing

import logging
logger = logging.getLogger(__name__)


def start_proxy():
    from .handler.client import handle_client
    from .conf import settings

    PROXY_BIND = settings.get("PROXY_BIND")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(PROXY_BIND)
    sock.listen(1)
    logger.info("Ready. Listening on %s:%d", *PROXY_BIND)

    while True:
        conn, address = sock.accept()
        logger.info("Got connection")
        process = multiprocessing.Process(target=handle_client, args=(conn, address))
        process.daemon = True
        process.start()
        logger.info("Started process %r", process)