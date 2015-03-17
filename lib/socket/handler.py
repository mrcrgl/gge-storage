from __future__ import unicode_literals

from .context import RequestContext
from .message import SocketMessage
from .processor import MessageProcessor
from .exceptions import DeadConnectionException
import socket
#import os
import logging
logger = logging.getLogger(__name__)

close_bit = "\x00"


class Socket:
    """
    demonstration class only
      - coded for clarity, not efficiency
    """
    close_bit = u"\x00"
    processor = None
    connection = None
    context = None
    address = None
    chunk_size = 2048

    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.context = RequestContext(self)
        self.processor = MessageProcessor(self)
        logger.info("Connected %s at %s", self.connection, self.address)

    def run(self):
        message = u""
        data = ""

        try:

            while True:
                try:
                    data = self.connection.recv(self.chunk_size)
                except Exception as e:
                    logger.critical("Exception while receiving data: %r", e)
                    message = ""
                    continue

                #try:
                #    data = data.decode('utf-8')
                #except UnicodeError as e:
                #    logger.critical("UnicodeError while decoding data: '%s' %s" % (data, e))
                #    message = ""
                #    continue

                if data == "":
                    logger.warning("Empty data received. Socket closed remotely")
                    self.connection.shutdown(socket.SHUT_RDWR)
                    #self.connection.close()
                    break

                try:
                    # message += unicode(data, 'ascii')
                    # message += unicode(data, errors='replace')  # Places ??? everywhere
                    message += data.decode('utf-8', errors='replace')
                except UnicodeDecodeError as e:
                    logger.critical("UnicodeDecodeError while forcing unicode: '%r'", e)
                    message += unicode(data)
                except UnicodeEncodeError as e:
                    logger.critical("UnicodeEncodeError while forcing unicode: '%r'", e)
                    message = u""
                    continue

                if self.close_bit in message:

                    try:
                        #message = message.decode("utf-8")
                        pos = message.index(close_bit)
                        partial_message = message[0:pos]
                        message = message[pos+len(close_bit):]

                        logger.debug("Received data %r", partial_message)
                        try:
                            socket_message = SocketMessage(partial_message)
                            self.context = self.processor.process_message(message=socket_message)
                        except DeadConnectionException:
                            logger.info("Connection dead.")
                            return
                        except:
                            logger.exception("Message process failed.")
                    except UnicodeDecodeError as e:
                        logger.critical("UnicodeDecodeError while forcing unicode: '%s' %s", data, e)
                        message = ""
                        continue
                    except UnicodeEncodeError as e:
                        logger.critical("UnicodeEncodeError while forcing unicode: '%s' %s", data, e)
                        message = ""
                        continue

                while len(self.context.responses):
                    response = self.context.responses.pop()
                    self.send(response)

        except Exception as e:
            logger.critical("Unknown problem handling request: [%r]", e)
        finally:
            logger.warning("Closing socket. Kill process.")
            self.connection.shutdown(socket.SHUT_RDWR)
            #self.connection.close()
            #pid = os.getpid()
            #os.kill(pid, 1)

    def send(self, response):

        message = response.to_string()

        if not message.endswith(self.close_bit):
            message += self.close_bit

        logger.debug("Sending data: %r", message)

        total_sent = 0
        while total_sent < len(message):
            sent = self.connection.send(message[total_sent:].encode('utf-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent


def handle_client(connection, address):
    from django import db
    db.close_connection()

    socket = Socket(connection, address)
    socket.run()

    db.close_old_connections()

    logger.info("Process terminated.")