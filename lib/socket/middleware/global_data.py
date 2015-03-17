from __future__ import unicode_literals

__author__ = 'mriegel'
from gge_proxy_manager.models import Castle, Player, Alliance, AccountBalanceLog, Game, Kingdom
import logging
logger = logging.getLogger(__name__)


class GlobalDataMiddleware():

    @staticmethod
    def inbound(context, message):
        if not message.type == 'in' or not message.command == 'gbd':
            return context, message

        game, created = Game.objects.get_or_create(name=message.product)

        data = message.get_data()

        try:
            gxp = data.get('gxp')  # Player XP
            gpi = data.get('gpi')  # Player info
            gcl = data.get('gcl')  #
            gcu = data.get('gcu')  #
            gal = data.get('gal')  # Alliance
            boi = data.get('boi')  # Rubinunterstuetzungen wie haendler etc.
        except KeyError:
            logger.exception("Error parsing global data: %s", message)

        logger.info("global data: %s", boi.get("BO", []))

        for option in boi.get("BO", []):
            if int(option.get("ID")) == int(11):
                context.add_dealer(int(option.get("RT")))

        alliance_id = int(gal.get('AID'))
        if alliance_id > 1:
            try:
                alliance, created = Alliance.objects.get_or_create(game=game, gge_id=int(gal.get('AID')))
                alliance.name = gal.get('AN')
                alliance.save()
            except:
                logger.exception("Cannot create alliance with id=%d", int(gal.get('AID')))
                return context, message
        else:
            alliance = None

        try:
            try:
                player = Player.objects.get(game=game, gge_id=int(gpi['PID']))
            except Player.DoesNotExist:
                player = Player(game=game, gge_id=int(gpi['PID']))

            player.alliance = alliance
            player.experience = int(gxp['XP'])
            player.level = int(gxp['LVL'])
            player.name = gpi['PN']
            player.save()
        except:
            logger.exception("Cannot create player with id=%d", int(gpi['PID']))
            return context, message

        context.set_player(player)

        AccountBalanceLog.objects.create(
            player=player,
            gold=int(gcu['C1']),
            ruby=int(gcu['C2'])
        )

        for c in gcl['C']:  # Iterate kingdoms
            kingdom, created = Kingdom.objects.get_or_create(kid=int(c['KID']), game=game)
            for ai in c['AI']:  # Iterate castles
                try:
                    castle = Castle.objects.get(game=game, gge_id=int(ai['AI'][3]))
                except Castle.DoesNotExist:
                    castle = Castle(game=game, gge_id=int(ai['AI'][3]))
                castle.player = player
                castle.kingdom = kingdom
                castle.type = int(ai['AI'][0])
                castle.kid = int(c['KID'])
                castle.name = ai['AI'][10]
                castle.pos_x = int(ai['AI'][1])
                castle.pos_y = int(ai['AI'][2])
                castle.save()

        return context, message