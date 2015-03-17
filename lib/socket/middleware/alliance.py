from __future__ import unicode_literals

from gge_proxy_manager.models import Alliance, AllianceRelation
import logging

logger = logging.getLogger(__name__)


class AllianceMiddleware():
    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command == 'ain':
            return context, message

        kingdom = context.get_kingdom()
        if not kingdom:
            return context, message

        data = message.get_data()

        alliance_data = data.get("A", {})
        alliance_id = alliance_data.get("AID")

        if not alliance_id:
            return context, message

        related_list_data = alliance_data.get("ADL", [])
        alliance = Alliance.objects.get(game=kingdom.game, gge_id=alliance_id)

        for relation in alliance.get_relations():
            relation.delete()

        for related_data in related_list_data:
            acknowledged = bool(related_data.get("AC", 0))

            if not acknowledged:
                continue

            type = related_data.get("AS")  # 3=BND, 2=NAP, 1=?
            related_alliance_id = related_data.get("AID")
            related_alliance = Alliance.objects.get(game=kingdom.game, gge_id=related_alliance_id)
            ar = AllianceRelation(alliance_a=alliance, alliance_b=related_alliance, type=type)
            ar.save()

        return context, message
