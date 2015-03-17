from __future__ import unicode_literals

import socket
import multiprocessing
from django.core.management.base import BaseCommand, CommandError
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
            message = ""

            while True:
                data = self.connection.recv(self.chunk_size).decode('utf-8')
                if data == "":
                    logger.warning("Socket closed remotely")
                    break

                message += data

                if self.close_bit in message:
                    pos = message.index(self.close_bit)
                    partial_message = message[0:pos]
                    message = message[pos+len(self.close_bit):]

                    logger.debug("Received data %r", partial_message)
                    self.send(partial_message)

                #context.add(data)
        except Exception as e:
            logger.critical("Problem handling request: %s" % e)
        finally:
            logger.critical("Closing socket")
            self.connection.close()

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
        sock.bind(('127.0.0.1', 7720))
        sock.listen(1)

        while True:
            conn, address = sock.accept()
            logger.info("Got connection")
            process = multiprocessing.Process(target=handle_client, args=(conn, address))
            process.daemon = True
            process.start()
            logger.info("Started process %r", process)