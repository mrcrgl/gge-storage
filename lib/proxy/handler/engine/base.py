from __future__ import unicode_literals

import select
import time
from Queue import Queue, Empty as EmptyQueue
import socket
from lib.proxy import commands
from .mixins import *
from lib.proxy.conf import settings

STORAGE = settings.get("STORAGE")
ENDPOINT = settings.get("ENDPOINT")
CLIENT = settings.get("CLIENT")

STORAGE_HOST = settings.get("STORAGE_HOST")
ENDPOINT_HOST = settings.get("ENDPOINT_HOST")

GAME = settings.get("GAME")
PRODUCT_NUMBER = settings.get("PRODUCT_NUMBER")

DISABLE_PARTIALS_FOR = settings.get("DISABLE_PARTIALS_FOR", ())

import logging
logger = logging.getLogger(__name__)


class ProxySocket(TimeoutMixin, StorageMixin, EndpointMixin, ClientMixin):
    '''
      - coded for clarity, not efficiency
    '''
    close_bit = "\x00"
    processor = None
    context = None
    address = None
    chunk_size = 2048

    client = None

    message_queues = None

    storage_connected = False
    client_connected = False

    product_number = None
    product_name = None

    resource_key = None

    throttle_burst = 0.01
    throttle_normal = 0.05
    throttle = None
    storage = None
    endpoint = None

    # storage_connect

    def __init__(self, client, address):
        logger.info("Connected %r at %r", self.client, self.address)

        self.client = client
        self.client.setblocking(0)
        self.client_connected = True

        self.product_name = GAME
        self.product_number = PRODUCT_NUMBER

        self.address = address

        self.message_queues = {
            CLIENT: Queue(),
            ENDPOINT: Queue(),
            STORAGE: Queue()
        }
        self.partial_queues = {
            CLIENT: Queue(),
            ENDPOINT: Queue(),
            STORAGE: Queue()
        }

        self.connect_endpoint()
        self.connect_storage()

        super(ProxySocket, self).__init__()

        self.throttle = self.throttle_normal

    def connect_storage(self):
        try:
            self.storage = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.storage.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.storage.connect(STORAGE_HOST)
            self.storage.setblocking(0)
            logger.info("Storage: %r", self.storage)

            # Override queue. We don't want to send old stuff
            self.message_queues[STORAGE] = Queue()
            self.storage_connected = True
        except socket.error as e:
            logger.exception("Storage connection failed: %r", e)
            return False
        return True

    def connect_endpoint(self):
        self.endpoint = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.endpoint.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.endpoint.connect(ENDPOINT_HOST)
        self.endpoint.setblocking(0)
        logger.info("Endpoint: %r", self.endpoint)

    def run(self):
        self.connections = [self.client, self.endpoint]

        if self.storage_connected:
            self.connections.append(self.storage)

        while self.endpoint in self.connections:  # as long as we have connections
            time.sleep(self.throttle)

            self.float_timeouts()

            readable, writeable, exceptional = select.select(self.connections, self.connections, self.connections)

            for died in exceptional:
                logger.info("Died: %r", died)

                self.disconnect_connection(died)

            for s in readable:
                try:
                    data = s.recv(self.chunk_size)
                    # logger.info("RECV from=%r message=%s", s, data)
                    length = len(data)
                    if length >= self.chunk_size:
                        self.throttle = self.throttle_burst
                    else:
                        self.throttle = self.throttle_normal

                except socket.error, e:
                    logger.error("Failed receiving data: %r", e)
                    self.disconnect_connection(s)
                    continue

                if data == "":
                    logger.warning("Empty data received peer=%r", s)
                    self.disconnect_connection(s)
                    continue

                if s is self.client:
                    self.to_server(data)
                    self.to_storage(data)

                if s is self.endpoint:
                    self.to_client(data)
                    self.to_storage(data)

                if s is self.storage:
                    self.from_storage(data)

            for s in writeable:
                try:
                    next_msg = self.message_queues[QUEUE].get_nowait()
                except EmptyQueue:
                    # logger.warning("empty queue")
                    continue

                if s is self.client:
                    if not self.client_connected:
                        continue

                    QUEUE = CLIENT

                if s is self.endpoint:
                    QUEUE = ENDPOINT

                if s is self.storage:
                    if not self.storage_connected:
                        continue

                    QUEUE = STORAGE

                try:
                    logger.debug("SEND to=%r message=%s", s, next_msg)
                    self.send(s, next_msg)
                except socket.error, e:
                    logger.error("Failed sending data: %r", e)
                    self.disconnect_connection(s)
                    continue

            remove_keys = []
            timeouts = self.timeouts.copy()
            for key, timeout in timeouts.iteritems():
                if timeout.tick(proxy=self):
                    remove_keys.append(key)

            while remove_keys:
                self.clear_timeout(remove_keys.pop())

    def disconnect_connection(self, conn):
        if conn == self.client:
            logger.info("Client disconnected peer=%r", conn)
            # set to autopilot
            self.client_connected = False
            commands.user_is_afk(self)

        if conn == self.endpoint:
            logger.info("Endpoint disconnected peer=%r", conn)
            #self.storage.shutdown(socket.SHUT_RDWR)
            self.storage.close()
            #self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
            self.connections = []

        if conn == self.storage:
            logger.info("Storage disconnected peer=%r", conn)
            self.storage_connected = False

        conn.close()

        try:
            self.connections.remove(conn)
        except ValueError:
            pass

    def enqueue_to(self, destination, msg):
        messages = self.collect_partials(destination, msg)

        for message in messages:
            if destination == ENDPOINT:
                message = self.client_to_server(message)
            elif destination == CLIENT:
                message = self.server_to_client(message)

            if message:
                self.message_queues[destination].put_nowait(message)

    def to_server(self, msg):
        return self.enqueue_to(ENDPOINT, msg)

    def to_client(self, msg):
        return self.enqueue_to(CLIENT, msg)

    def to_storage(self, msg):
        return self.enqueue_to(STORAGE, msg)

    def from_storage(self, msg):
        logger.info("RECV STORAGE: message=%r", msg)
        self.execute_storage_command(msg)
        #messages = msg.split(self.close_bit)
        #for message in messages:
        #    self.execute_storage_command(message)

    def collect_partials(self, key, partial_message, fake=False):
        if not fake and key in DISABLE_PARTIALS_FOR:
            self.collect_partials(key, partial_message, True)
            return [partial_message]

        partial_message = partial_message.decode('utf-8', errors='replace')

        self.partial_queues[key].put_nowait(partial_message)

        if not self.close_bit in partial_message:
            # as long as the message isn't closed we don't need to collect
            if not fake:
                return []
            else:
                #logger.info("collect_partials: %r", [])
                pass

        # copy queue and create a new one to float partial messages to
        queue = self.partial_queues[key]
        self.partial_queues[key] = Queue()
        messages = []
        message = ""
        while not queue.empty():
            package = queue.get_nowait()
            #logger.debug(package)

            while self.close_bit in package:

                before, appendix = package.split(self.close_bit, 1)
                before += self.close_bit  # reappend close_bit
                package = package[len(before):]

                message += before
                if len(message) > 0:
                    messages.append(message)
                message = appendix

            else:
                # no close_bit. just append
                message += package

        self.partial_queues[key].put_nowait(message)

        if not fake:
            return [message.encode("utf-8") for message in messages]
        else:
            i = 0
            for message in messages:
                i += 1
                logger.debug("receiver=%s num=%d message=%r", key, i, message.encode("utf-8"))
            #logger.info("data %r", [message.encode("utf-8") for message in messages])

    def send(self, peer, message):

        total_sent = 0
        while total_sent < len(message):
            sent = peer.send(message[total_sent:])

            if sent == 0:
                raise RuntimeError("socket connection broken")
            total_sent = total_sent + sent

        return total_sent

    def shutdown(self):
        return False

    def set_resource_key(self, key):
        self.resource_key = int(key)
        logger.info("Resource key=%d", self.resource_key)
