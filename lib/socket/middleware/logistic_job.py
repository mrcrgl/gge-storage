from __future__ import unicode_literals

from gge_proxy_manager.models import LogisticJob, CastleEconomy, PlayerEconomy, LogisticLog
from lib.socket.response import Response
from django.utils.timezone import now, timedelta
import logging
logger = logging.getLogger(__name__)

forty_five_minutes = timedelta(minutes=45)


class LogisticJobMiddleware():
    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command == 'cmi':

            kd_change_in_progress = context.session_get("-".join((__name__, 'kingdom-change')))
            if kd_change_in_progress and kd_change_in_progress > now() - timedelta(minutes=15):
                kd_change_in_progress = True
            else:
                kd_change_in_progress = False
                context.session_unset("-".join((__name__, 'kingdom-change')))

            # maybe we request it
            if context.session_get('logistic_job'):
                # wrong message
                return context, message

            if context.is_locked() and not context.locked_infinite_by == __name__:
                return context, message

            player = context.get_player()

            if not player:
                logger.debug("Missing player.")
                return context, message

            try:
                player_economy = player.economy
            except PlayerEconomy.DoesNotExist:
                logger.warning("Economy missing for player=%s", player)
                return context, message

            if player_economy.updated < now() - timedelta(minutes=15):
                logger.warning("Economy too old for player=%s", player)
                return context, message

            for job in LogisticJob.objects.filter(player=player, is_active=True, locked_till__lte=now()).order_by('locked_till'):
                # Check the job
                if context.session_get('logistic_job'):
                    continue

                try:
                    economy = job.castle.economy
                except CastleEconomy.DoesNotExist:
                    logger.warning("Economy missing for player=%s castle=%s", context.get_player(), job.castle)
                    job.delay()
                    continue

                if economy.updated < now() - timedelta(minutes=15):
                    logger.warning("Economy too old for player=%s castle=%s", player, job.castle)
                    job.delay()
                    continue

                if player_economy.gold < job.gold_limit:
                    logger.warning("Not enough gold player=%s job=%d", player, job.pk)
                    job.delay()
                    continue

                if getattr(economy, "".join((job.resource, '_stock'))) < job.resource_limit:
                    logger.warning(
                        "Not enough resource=%s player=%s castle=%s job=%d", job.resource, player, job.castle, job.pk
                    )
                    job.delay()
                    continue

                if not context.get_kingdom() or context.get_kingdom().pk != job.castle.kingdom_id:
                    # Wrong kingdom!

                    if not context.is_afk:
                        logger.warning("Wrong Kingdom but player not afk kingdom=%s job=%d", job.castle.kingdom.name, job.pk)
                        job.delay()
                        return context, message

                    if kd_change_in_progress:
                        return context, message

                    response = Response(command='fwd_srv', data={
                        "cmd": "jca",
                        "data": {
                            "KID": int(job.castle.kingdom.kid),
                            "CID": int(job.castle.gge_id)
                        }
                    })
                    context.add_response(response)
                    context.lock_infinite_for(__name__)
                    context.lock_for(15)

                    context.session_set("-".join((__name__, 'kingdom-change')), now())

                    logger.info("Wrong Kingdom, move to kingdom=%s job=%d", job.castle.kingdom.name, job.pk)

                    return context, message

                context.unlock(__name__)

                # limits are ok, kingdom is fine.
                # what's left is to check if we have enough karren
                response = Response(command='fwd_srv', data={
                    "cmd": "cmi",
                    "data": {
                        "S": int(0)
                    }
                })
                context.add_response(response)
                context.session_set('logistic_job', job)

            return context, message

        """
        We check now 'cmi'
        """
        job = context.session_get('logistic_job')
        context.unlock(__name__)
        context.session_unset('logistic_job')

        if not job or not isinstance(job, LogisticJob):
            return context, message

        data = message.get_data()

        # check karren
        castle_information = None

        for c in data.get("C", []):
            if not c.get("CID") == job.castle.gge_id:
                continue

            castle_information = c

        if not castle_information:
            logger.warning("Missing castle information for logistic job=%d castle=%s", job.pk, job.castle.name)
            job.delay()
            return context, message

        if castle_information.get("TC") != castle_information.get("AC"):
            logger.info("Carts are not available for logistic job=%d castle=%s", job.pk, job.castle.name)
            job.delay()
            return context, message

        if job.resource == 'cole':
            logger.info("Resource 'cole' is not supported job=%d castle=%s", job.pk, job.castle.name)
            job.delay()
            return context, message

        amount = int(castle_information.get("AC")) * 100

        if context.has_dealer():
            amount *= 2

        try:
            eco = job.receiver.economy
            diff = eco.stock_size - getattr(eco, "".join((job.resource, '_stock')))
            if diff < amount:
                logger.info(
                    "Receivers stock has not enough free space job=%d castle=%s free=%d amount=%d",
                    job.pk,
                    job.castle.name,
                    diff,
                    amount
                )
                job.delay()
                return context, message
        except CastleEconomy.DoesNotExist:
            pass

        wood = amount if job.resource == 'wood' else 0
        stone = amount if job.resource == 'stone' else 0
        food = amount if job.resource == 'food' else 0

        response = Response(command='fwd_srv', data={
            "cmd": "crm",
            "data": {
                "HBW": int(job.speed),
                "SID": job.castle.gge_id,
                "TX": job.receiver.pos_x,
                "TY": job.receiver.pos_y,
                "KID": job.castle.kingdom.kid,
                "G": [["W", wood], ["S", stone], ["F", food]]
            }
        })
        context.add_response(response)

        job.delay()

        log = LogisticLog(
            player=job.player,
            castle=job.castle,
            receiver=job.receiver,
            resource=job.resource,
            amount=amount
        )
        log.save()

        return context, message
