from __future__ import unicode_literals

from lib.proxy.timer import SetTimeout
from lib.proxy import commands

import logging
logger = logging.getLogger(__name__)


class EndpointMixin(object):

    package_prefix_afk = None

    def client_to_server(self, msg):

        decoded = msg.decode('utf-8')

        if not self.package_prefix_afk:
            self.package_prefix_afk = "%".join(("%xt", self.product_name, "core_afk%"))

        if decoded.startswith(self.package_prefix_afk):
            try:
                substr = decoded[decoded.index(self.package_prefix_afk):]
                if "true" is substr.split("%")[5]:
                    # user is back
                    self.clear_timeout('afk')
                    commands.user_is_back(self)
                else:
                    # user is afk
                    self.set_timeout('afk', SetTimeout(commands.user_is_afk, 600))

                return None
            except KeyError:
                pass

        return msg