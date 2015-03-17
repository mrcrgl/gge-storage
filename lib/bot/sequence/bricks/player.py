from gge_proxy_manager.models import PlayerEconomy, CastleEconomy
from lib.bot.sequence.base import SequenceBrick
from lib.bot.sequence.exceptions import *
from django.utils.timezone import timedelta, now
from django.utils.timesince import timesince

__all__ = ['PlayerAvailableBrick', 'PlayerGoldCreditBrick',
           'PlayerColeCreditBrick', 'PlayerFoodCreditBrick',
           'PlayerStoneCreditBrick', 'PlayerWoodCreditBrick']


class PlayerAvailableBrick(SequenceBrick):

    def __init__(self):
        def expression(cls, context, message):
            return bool(context.get_player())

        self.set_expression(expression)


class PlayerIsAfkBrick(SequenceBrick):

    def __init__(self):
        def expression(cls, context, message):
            return bool(context.is_afk)

        self.set_expression(expression)


class PlayerGoldCreditBrick(SequenceBrick):

    def __init__(self, min_amount):
        def expression(cls, context, message):
            player = context.get_player()
            try:
                economy = player.economy
            except PlayerEconomy.DoesNotExist:
                economy = PlayerEconomy.objects.create(player=player, ruby=0, gold=0)

            if economy.updated < now() - timedelta(minutes=30):
                raise ShortTemporalExpressionError(
                    "Economy data too old max_age=30 age=%s" % timesince(economy.updated)
                )

            if not bool(economy.gold >= min_amount):
                raise LongTemporalExpressionError(
                    "Not enough Gold required=%d available=%d" % (min_amount, economy.gold)
                )

            return True

        self.set_expression(expression)


class HasPositiveFoodBalanceBrick(SequenceBrick):

    def __init__(self, castle, burst_mode=False, food_balance_limit=None):
        def expression(cls, context, message):
            try:
                economy = castle.economy
            except CastleEconomy.DoesNotExist:
                return False

            if burst_mode:
                return True

            food_balance = economy.food_balance()

            if food_balance_limit and food_balance > food_balance_limit:
                return True

            if not food_balance_limit and food_balance > 0:
                return True

            raise LongTemporalExpressionError(
                "Negative food balance balance=%d balance_limit=%s in_stock=%d"
                % (food_balance, food_balance_limit, economy.food_stock)
            )

        self.set_expression(expression)


class PlayerUnitAmountBrick(SequenceBrick):

    def __init__(self, castle, unit, max_amount=None, burst_mode=False):
        def expression(cls, context, message):

            if not max_amount:
                return True

            try:
                economy = castle.economy
            except CastleEconomy.DoesNotExist:
                return False

            if burst_mode:
                # logger.info("Burst mode activated.")
                return True

            if economy.updated < now() - timedelta(minutes=30):
                raise ShortTemporalExpressionError("Economy data too old max_age=30 age=%s" % timesince(economy.updated))

            relation = None
            if economy.unit_list:
                relation = economy.unit_list.unit_relations.filter(unit=unit).first()

            amount = relation.amount if relation else 0

            if max_amount and not bool(int(max_amount or 0) > int(amount or 0)):
                raise LongTemporalExpressionError(
                    "Unit count reached player=%s castle=%s unit=%s should=%d is=%d" % (
                        context.get_player().name, castle.name, unit.title, max_amount, amount
                    )
                )

            return True

        self.set_expression(expression)


class PlayerResourceCreditBrick(SequenceBrick):

    def __init__(self, castle, min_amount=None, max_amount=None, type=None):
        def expression(cls, context, message):
            try:
                economy = castle.economy
            except CastleEconomy.DoesNotExist:
                return False

            attr = "%s_stock" % type
            value = getattr(economy, attr)

            if hasattr(value, '__call__'):
                value = value()

            if economy.updated < now() - timedelta(minutes=15):
                raise ShortTemporalExpressionError("Economy data too old max_age=15 age=%s" % timesince(economy.updated))

            if (min_amount is None or min_amount <= value) and (max_amount is None or max_amount >= value):
                return True

            raise LongTemporalExpressionError(
                "Resource credit check failed type=%s castle=%s min_amount=%s max_amount=%s available=%d" % (
                type, castle.name, min_amount, max_amount, value)
            )

        self.set_expression(expression)


class PlayerWoodCreditBrick(PlayerResourceCreditBrick):

    def __init__(self, castle, min_amount=None, max_amount=None):
        super(self.__class__, self).__init__(castle, min_amount, max_amount, type='wood')


class PlayerStoneCreditBrick(PlayerResourceCreditBrick):

    def __init__(self, castle, min_amount=None, max_amount=None):
        super(self.__class__, self).__init__(castle, min_amount, max_amount, type='stone')


class PlayerFoodCreditBrick(PlayerResourceCreditBrick):

    def __init__(self, castle, min_amount=None, max_amount=None):
        super(self.__class__, self).__init__(castle, min_amount, max_amount, type='food')


class PlayerColeCreditBrick(PlayerResourceCreditBrick):

    def __init__(self, castle, min_amount=None, max_amount=None):
        super(self.__class__, self).__init__(castle, min_amount, max_amount, type='cole')
