from __future__ import unicode_literals

from django import template
from gge_proxy_manager.models import Castle
from lib.map.utils import distance_to_castle
from decimal import Decimal

register = template.Library()


@register.filter(name='distance_to')
def distance_to(from_castle, to_castle):
    return Decimal("%.1f" % distance_to_castle(from_castle, to_castle))


@register.filter()
def distance_to_user(from_castle, to_user):
    to_castles = to_user.castles.filter(kingdom=from_castle.kingdom, type__in=Castle.TYPE_WITH_WARRIORS)

    if not to_castles.count():
        return ""

    distance = None
    for to_castle in to_castles:
        if to_castle:
            temp_distance = distance_to(from_castle, to_castle)
            if not distance or temp_distance < distance:
                distance = temp_distance

    return distance or ""


class CastleByPosNode(template.Node):
    def __init__(self, castle_varname, varname):
        self.castle_varname = castle_varname
        self.varname = varname

    @classmethod
    def handle_token(cls, parser, token):
        tokens = token.contents.split()

        if len(tokens) != 4:
            raise template.TemplateSyntaxError(
                "Require 3 arguments")

        if tokens[2] != 'as':
            raise template.TemplateSyntaxError(
                "First argument in '%s' must be 'as'" % tokens[0])

        castle_varname = tokens[1]
        varname = tokens[3]

        return cls(castle_varname, varname)

    def render(self, context):
        castle = context[self.castle_varname]
        context[self.varname] = Castle.objects.filter(kingdom_id=castle.kingdom_id, pos_x=castle.pos_x, pos_y=castle.pos_y)\
            .order_by('-gge_id')
        return ''


@register.tag
def castles_by_pos(parser, token):
    """
    Returns a list of castles by given kingdom and coordinates.

    Usage::

        {% castles_by_pos castle as varname %}
    """
    return CastleByPosNode.handle_token(parser, token)