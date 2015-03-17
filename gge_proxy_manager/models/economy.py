from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now, timedelta
Q = models.Q


class EconomyMixin(object):

    def is_outdated(self):
        return self.updated < now() - timedelta(minutes=15)


class PlayerEconomy(models.Model, EconomyMixin):
    player = models.OneToOneField("gge_proxy_manager.Player", related_name='economy')
    ruby = models.PositiveIntegerField()
    gold = models.PositiveIntegerField()
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'gge_proxy_manager'


class CastleEconomy(models.Model, EconomyMixin):
    castle = models.OneToOneField("gge_proxy_manager.Castle", related_name='economy')
    barrows = models.PositiveSmallIntegerField(default=0)
    guards = models.PositiveSmallIntegerField(default=0)
    citizen = models.PositiveSmallIntegerField(default=0)
    stock_size = models.PositiveIntegerField(default=0)
    public_order = models.IntegerField(default=0)
    unit_list = models.OneToOneField('gge_proxy_manager.UnitList', null=True, default=None, blank=True)
    defence_points = models.PositiveSmallIntegerField(default=0)
    wood_production = models.PositiveIntegerField(default=0)
    wood_stock = models.PositiveIntegerField(default=0)
    stone_production = models.PositiveIntegerField(default=0)
    stone_stock = models.PositiveIntegerField(default=0)
    cole_production = models.PositiveIntegerField(default=0)
    cole_stock = models.PositiveIntegerField(default=0)
    food_production = models.PositiveIntegerField(default=0)
    food_stock = models.PositiveIntegerField(default=0)
    food_consumption = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def food_balance(self):
        return self.food_production - self.food_consumption