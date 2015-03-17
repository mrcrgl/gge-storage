from __future__ import unicode_literals

__author__ = 'riegel'

from gge_proxy_manager.models import ProductionJob, Castle
from lib.bot.sequence.production import ProductionSequence
from lib.socket.response import Response
from django.utils.timezone import now
from django.core.cache import cache

import logging
logger = logging.getLogger(__name__)


class ProductionMiddleware():

    @staticmethod
    def inbound(context, message):

        if message.type == 'in' and message.command == 'bup':
            data = message.get_data()

            grc = data.get("grc", {})  # Resource info
            castle_gge_id = grc.get("AID", 0)
            spl = data.get("sql", {})

            try:
                castle = Castle.objects.get(gge_id=castle_gge_id)
                lid = spl.get("LID", None)

                if lid is not None:
                    context.set_production_slots(castle, lid, spl.get("PIDL", []))

            except Castle.DoesNotExist:
                pass

            # Plus one
            for order in spl.get('PIDL', []):
                try:
                    order_id = order[6]
                    cache_key = '-'.join(('order-plus-one', unicode(order_id)))
                    if not cache.get(cache_key):

                        response = Response(command='fwd_srv', data={
                            "cmd": "ahr",
                            "data": {
                                "RID": int(order_id)
                            }
                        })
                        context.add_response(response)

                        cache.set(cache_key, 1, 3600)

                except KeyError:
                    pass

        if not context.get_player():
            return context, message

        if context.is_locked():
            if not context.locked_infinite_by == __name__:
                logger.info("Sequence locked by=%s till=%s", context.locked_infinite_by, context.locked_until)
                return context, message

        sequence = context.session_get("production_sequence")
        if not sequence:
            # Create new sequence
            job = ProductionJob.objects.filter(is_active=True, locked_till__lte=now(),
                                               player=context.get_player()).order_by('locked_till').first()
            if job:
                logger.info("Fetched new ProductionJob pk=%d player=%s unit=%s", job.pk, context.get_player().name,
                            job.unit.title)
                sequence = ProductionSequence(job)
                context.session_set("production_sequence", sequence)

        # Run the sequence
        if sequence:
            context.locked_infinite_by = __name__

            #response_count = len(context.responses)

            #while response_count == len(context.responses) and not sequence.is_closed():
                # Loop while there's no response added and sequence is active
            context, message = sequence.turn(context, message)

            #logger.info("DEBUG: closed=%s - vars=%s", sequence.is_closed(), vars(sequence))

            if sequence.is_closed():
                logger.info("Sequence closed. Unlock context.")
                context.unlock(__name__)
                context.session_set("production_sequence", None)

        return context, message
