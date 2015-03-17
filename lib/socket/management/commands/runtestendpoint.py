from __future__ import unicode_literals

import socket
import multiprocessing
from django.core.management.base import BaseCommand, CommandError
import time
import datetime
import logging
logger = logging.getLogger(__name__)


class Socket:
    '''demonstration class only
      - coded for clarity, not efficiency
    '''
    close_bit = "\x00"
    processor = None
    connection = None
    context = None
    address = None
    chunk_size = 2048

    def __init__(self, connection, address):
        print("Connected %r at %r", self.connection, self.address)

        self.connection = connection
        self.address = address

    def run(self):
        try:

            while True:
                time.sleep(5)
                self.send(datetime.datetime.now().isoformat())

        except Exception as e:
            logger.critical("Problem handling request: %s" % e)
        finally:
            logger.critical("Closing socket")
            self.connection.shutdown(socket.SHUT_RDWR)

    def send(self, response):

        message = response

        if not message.endswith(self.close_bit):
            message += self.close_bit

        logger.debug("Sending: %s", message)

        total_sent = 0
        while total_sent < len(message):
            sent = self.connection.send(message[total_sent:].encode('utf-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent


def handle_client(connection, address):
    socket = Socket(connection, address)
    socket.run()


class Command(BaseCommand):
    args = '<object object ...>'
    #help = 'Help text goes here'

    def handle(self, *args, **options):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('127.0.0.1', 7710))
        sock.listen(1)
        logger.info("Ready. Listening on %s:%d", '127.0.0.1', 7710)

        while True:
            conn, address = sock.accept()
            logger.info("Got connection")
            process = multiprocessing.Process(target=handle_client, args=(conn, address))
            process.daemon = True
            process.start()
            logger.info("Started process %r", process)