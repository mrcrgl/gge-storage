from __future__ import unicode_literals

__author__ = 'riegel'
import socket
#import threading
import multiprocessing
from .handler import handle_client
#from .context import RequestConte
import logging
logger = logging.getLogger(__name__)


class Server(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        logger.info("listening")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            logger.info("Got connection")
            process = multiprocessing.Process(target=handle_client, args=(conn, address))
            process.daemon = True
            process.start()
            logger.info("Started process %r", process)


def runserver():

    server = Server("0.0.0.0", 7766)
    try:
        logger.info("Listening")
        server.start()
    except Exception as e:
        logger.exception("Unexpected exception: %s", e)
    finally:
        logger.info("Shutting down")
        for process in multiprocessing.active_children():
            logger.info("Shutting down process %r", process)
            process.terminate()
            process.join()
    logger.info("All done")
