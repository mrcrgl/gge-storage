from .base import Sequence
from .bricks.player import (PlayerAvailableBrick, PlayerGoldCreditBrick, PlayerWoodCreditBrick,
                            PlayerStoneCreditBrick, PlayerFoodCreditBrick, PlayerIsAfkBrick,
                            PlayerUnitAmountBrick, HasPositiveFoodBalanceBrick)
from .bricks.navigation import GoToCastleBrick
from .bricks.production import ProduceUnitBrick, CheckSoldierRelationBrick, ProductionSlotPrecheckBrick
from django.utils.timezone import now, timedelta

import logging
logger = logging.getLogger(__name__)


class ProductionSequence(Sequence):
    """
    TODO:
    - long term delta (amount too high, resources not available)
    - short term delta (eg slots locked)

    short term should not change the delta.
    long term is used if a short recheck would not solve the problem.
    mid term is used to lock the job while producing.

    """

    delta = timedelta(minutes=25)

    def __init__(self, production_order):
        type = ProduceUnitBrick.TYPE_SOLDIER if production_order.unit.type == 'soldier' else ProduceUnitBrick.TYPE_UTIL

        # self.append_brick(PlayerAvailableBrick())
        self.append_brick(PlayerIsAfkBrick())

        self.append_brick(ProductionSlotPrecheckBrick(type=type, castle=production_order.castle))

        if production_order.gold_limit:
            self.append_brick(PlayerGoldCreditBrick(min_amount=production_order.gold_limit))

        if production_order.wood_limit:
            self.append_brick(PlayerWoodCreditBrick(production_order.castle, min_amount=production_order.wood_limit))

        if production_order.stone_limit:
            self.append_brick(PlayerStoneCreditBrick(production_order.castle, min_amount=production_order.stone_limit))

        if type == ProduceUnitBrick.TYPE_SOLDIER:
            self.append_brick(HasPositiveFoodBalanceBrick(production_order.castle, production_order.burst_mode,
                                                          production_order.food_balance_limit))
            self.append_brick(CheckSoldierRelationBrick(production_order.castle, production_order))

        self.append_brick(PlayerUnitAmountBrick(production_order.castle, production_order.unit,
                                                production_order.valid_until, production_order.burst_mode))

        self.append_brick(GoToCastleBrick(castle=production_order.castle))

        self.append_brick(ProduceUnitBrick(type=type, unit=production_order.unit,
                                           max_units=production_order.valid_until, castle=production_order.castle,
                                           burst_mode=production_order.burst_mode))

        self.production_order = production_order

        if production_order.burst_mode:
            self.delta = timedelta(minutes=5)

        logger.info("Initialized sequence=%s player=%s castle=%s unit=%s delta=%s burst_mode=%s", self.__class__.__name__,
                    production_order.player.name, production_order.castle.name, production_order.unit.title,
                    self.delta, production_order.burst_mode)

    def post_process(self, faulty=False, delta=None):
        if not delta:
            delta = self.delta

        # TODO: Respect burst mode
        if not faulty:
            delta = timedelta(minutes=5)

        logger.info("Post Process called on sequence=%s added_delay=%s", self.__class__.__name__, delta)
        self.production_order.locked_till = now() + delta
        self.production_order.save()