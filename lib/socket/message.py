from __future__ import unicode_literals

import json
import logging
logger = logging.getLogger(__name__)


class SocketMessage():
    type = None
    product = None
    version = None
    command = None
    data = None
    data_raw = None
    is_valid = False

    def __init__(self, message):

        try:
            if u"EmpireEx_2" in message or u"EmpirefourkingdomsExGG" in message or "GGEProxy" in message:
                # Client message
                non, xt, product, command, version, data, end = message.split("%")
                self.type = 'out'
            else:
                non, xt, command, version, non2, data, end = message.split("%")
                product = "EmpireEx_2" if int(version) == 2 else "EmpirefourkingdomsExGG"
                self.type = 'in'

            self.product = product
            self.version = version
            self.command = command
        except ValueError as e:
            logger.warning("Message cannot be read: %s [%s]", message, e)
            return

        self.data_raw = data
        self.is_valid = True

    def convert_data(self):
        if self.data_raw:
            #print "data raw: %s" % self.data_raw
            if self.data_raw == 'true':
                #print "result: %s" % True
                self.data = True
                return True

            if self.data_raw == 'false':
                #print "result: %s" % False
                self.data = False
                return True

            try:
                self.data = json.loads(self.data_raw)
            except ValueError:
                logger.warning("Error while parse data to json: '%s'", self.data_raw)
                return False

        return False

    def get_data(self):
        if self.data is None and self.is_valid:
            if self.convert_data() is None:
                return {}

        return self.data