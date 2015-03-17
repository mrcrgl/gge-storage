from __future__ import unicode_literals

__author__ = 'mriegel'

import json


class Response(object):

    product = "GGEStorage"
    command = None
    data = {}
    number = 1

    def __init__(self, command, data={}):
        self.command = command
        self.data = data

    def __repr__(self):
        return "<Response command=%s>" % self.command

    def to_string(self):
        return "%".join((
            "",
            "px",
            self.product,
            self.command,
            unicode(self.number),
            json.dumps(self.data, separators=(',', ':')),
            "",
        ))

    def __unicode__(self):
        self.to_string()
