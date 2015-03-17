from __future__ import unicode_literals

from django import template
from gge_proxy_manager.models import UnitListRelation, CastleEconomy
from django.db.models import Sum

register = template.Library()


def available_amount(castle, unit):

    try:
        rel = castle.economy.unit_list.unit_relations.get(unit=unit)
        return rel.amount
    except:
        return 0

register.filter('available_amount', available_amount)


def soldier_amount_of_type(castle, orientation=None):

    try:
        relations = castle.economy.unit_list.unit_relations.filter(unit__type='soldier')

        if orientation:
            relations = relations.filter(unit__orientation=orientation)

        sum = relations.aggregate(Sum('amount'))['amount__sum']
        if not sum:
            return 0

        return sum
    except Exception as e:
        return 0

register.filter('soldier_amount_of_type', soldier_amount_of_type)


def stock_sum_of(player, key):
    value = 0

    try:
        for castle in player.castles_with_environment():
            attr = getattr(castle.economy, key)
            if getattr(attr, "__call__", None):
                value += attr.__call__()
            else:
                value += attr

        return value
    except CastleEconomy.DoesNotExist:
        return ""

register.filter('stock_sum_of', stock_sum_of)