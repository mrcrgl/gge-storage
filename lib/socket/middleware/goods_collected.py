__author__ = 'mriegel'
from gge_proxy_manager.models import ResourceCollectLog


class GoodsCollectedMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command == 'irc':
            print "Drop command %s" % message.command
            return None

        if not context.player:
            print "Drop. Missing player."
            return None

        res = {}
        for type, value in message.data['G']:
            res['wood'] = value if type is "W" else 0
            res['stone'] = value if type is "S" else 0
            res['food'] = value if type is "F" else 0
            res['cole'] = value if type is "C" else 0

        ResourceCollectLog.objects.create(
            player=context.player,
            **res
        )