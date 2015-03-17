from lib.bot.sequence.base import SequenceBrick
from gge_proxy_manager.models import CastleEconomy, UnitListRelation, ProductionLog
from lib.socket.response import Response
from lib.bot.sequence.exceptions import *
from django.db.models import Sum

import logging
logger = logging.getLogger(__name__)


class CheckSoldierRelationBrick(SequenceBrick):

    def __init__(self, castle, production):
        def expression(cls, context, message):

            unit = production.unit

            if unit.type != 'soldier' or not production.valid_until:
                return True

            try:
                economy = castle.economy
            except CastleEconomy.DoesNotExist:
                return False

            total_amount = castle.production_jobs.filter(
                is_active=True, unit__type='soldier'
            ).exclude(valid_until=None).aggregate(Sum('valid_until'))['valid_until__sum']

            try:
                relation = production.valid_until / total_amount
            except TypeError:
                relation = 0

            rel = UnitListRelation.objects.filter(unit=unit, list=economy.unit_list).first()
            if not rel:
                return True

            castle_total_amount = 0
            for rel in economy.unit_list.unit_relations.all():
                castle_total_amount += rel.amount

            try:
                castle_relation = rel.amount / castle_total_amount
            except TypeError:
                castle_relation = 0

            if relation and relation < castle_relation:
                raise TemporalExpressionError("Amount relation of soldiers differ: castle=%s is=%.3f should=%.3f" % (
                    castle.name, castle_relation, relation
                ))

            return True

        self.set_expression(expression)


class ProductionSlotPrecheckBrick(SequenceBrick):

    def __init__(self, type, castle):
        type_key, lid = type

        def expression(cls, context, message):

            if context.are_slots_locked(castle, lid):
                delta = context.next_slot_available_in(castle, lid)

                raise TemporalExpressionError("No slot available (context precheck) delta=%s" % delta, delta=delta)

            return True

        self.set_expression(expression)


class ProduceUnitBrick(SequenceBrick):
    """
    Requires change into castle
    Action is open Production Info
    """
    TYPE_SOLDIER = ('gpa', 0,)
    TYPE_UTIL = ('gui', 1,)

    # %xt%EmpirefourkingdomsExGG%gpa%1%{}%
    # %xt%EmpirefourkingdomsExGG%gui%1%{}%

    def __init__(self, type, unit, max_units, castle, burst_mode):
        type_key, lid = type
        self.invalid_call_count = 0

        def expression(cls, context, message):
            # Require response for accessing a castle
            if not message.type == 'in' or not message.command == 'jaa':
                return False

            data = message.get_data()

            grc = data.get("grc", {})  # Resource info
            castle_gge_id = grc.get("AID", 0)
            if int(castle_gge_id) != castle.gge_id:
                raise TemporalExpressionError("condition failed. Castle gge_id=%d mismatch expected one gge_id=%d" % (
                    int(castle_gge_id), castle.gge_id))

            spl = data.get("spl%d" % lid, {})
            pidl = spl.get("PIDL", [])

            context.set_production_slots(castle, 0, data.get("spl%d" % 0, {}).get("PIDL", []))
            context.set_production_slots(castle, 1, data.get("spl%d" % 1, {}).get("PIDL", []))

            available_slots = [slot for slot in pidl if slot[0] == -1]

            available_slot_count = len(available_slots)

            logger.info("Available slots=%d", available_slot_count)

            if not bool(available_slot_count):
                msg = "No slot available slots=%d" % available_slot_count
                if len([slot for slot in pidl if int(slot[0]) <= 60]):
                    # locked under a minute: short
                    raise ShortTemporalExpressionError(msg)
                elif len([slot for slot in pidl if int(slot[0]) <= 60*10]):
                    # locked under 10 mins: default
                    raise TemporalExpressionError(msg)

                # long term
                raise LongTemporalExpressionError(msg)

            return True

        def action(cls, context, message):
            amount = 5

            # %xt%EmpirefourkingdomsExGG%jaa%1%{"PY":1219,"KID":0,"PX":1018}%
            available_slot_count = context.get_free_slot_count(castle, lid)

            for x in range(available_slot_count):
                context.add_response(
                    Response(command='fwd_srv', data={
                        "cmd": "bup",
                        "data": {
                            "A": amount,
                            "LID": lid,
                            "WID": unit.gge_id
                        }
                    })
                )

                logger.info("Producing unit=%d title=%s type=%s castle=%s player=%s", unit.gge_id, unit.title,
                            unit.type, castle.name, context.get_player().name)

                log = ProductionLog(player=castle.player, castle=castle, unit=unit, amount=amount)
                log.save()

            return context, message

        self.set_expression(expression)
        self.set_action(action)