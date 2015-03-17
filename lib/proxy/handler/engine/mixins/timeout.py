from __future__ import unicode_literals

from lib.proxy.timer import SetTimeout
from lib.proxy import commands

import logging
logger = logging.getLogger(__name__)


class TimeoutMixin(object):

    timeouts = None
    _timeouts = None

    def __init__(self):
        self._timeouts = [
            ('tax_info', SetTimeout(commands.request_tax_information, 30))
        ]
        self.timeouts = {}

        super(TimeoutMixin, self).__init__()

    def set_timeout(self, key, timeout):
        self._timeouts.append((key, timeout))

    def float_timeouts(self):
        if self._timeouts:
            for key, timeout in self._timeouts:
                self.timeouts[key] = timeout

        self._timeouts = []

    def clear_timeout(self, key):
        try:
            del self.timeouts[key]
        except KeyError:
            pass