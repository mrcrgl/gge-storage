from __future__ import unicode_literals

from django.db import models

Q = models.Q


class Unit(models.Model):
    TYPE = (
        ('soldier', 'Soldat'),
        ('tool', 'Werkzeug'),
    )
    VALUE_TYPE = (
        ('absolute', 'Absolut'),
        ('percentage', 'Prozentual'),
    )
    ORIENTATION = (
        ('off', 'Offensiv'),
        ('deff', 'Defensiv'),
    )
    DISTANCE = (
        ('close', 'Nah'),
        ('far', 'Fern'),
    )
    title = models.CharField(max_length=128, null=True, blank=True, default=None)
    game = models.ForeignKey("gge_proxy_manager.Game", related_name='units')
    gge_id = models.PositiveIntegerField(default=0, db_index=True)
    type = models.CharField(max_length=16, choices=TYPE, null=True, blank=True, default=None)
    value_type = models.CharField(max_length=16, choices=VALUE_TYPE, default='absolute')
    orientation = models.CharField(max_length=8, choices=ORIENTATION, null=True, blank=True, default=None)
    distance = models.CharField(max_length=8, choices=DISTANCE, null=True, blank=True, default=None)
    offence_close = models.IntegerField(default=0)
    offence_far = models.IntegerField(default=0)
    defence_close = models.IntegerField(default=0)
    defence_far = models.IntegerField(default=0)
    food_consumption = models.IntegerField(default=0)
    booty_space = models.IntegerField(default=0)
    travel_speed = models.IntegerField(default=0)

    class Meta:
        index_together = [['game', 'gge_id']]
        app_label = 'gge_proxy_manager'
        ordering = ['game', 'type', 'orientation', 'distance']

    def __unicode__(self):
        return self.title or self.__repr__()

    def __repr__(self):
        return "<%s %s-%d>" % ('Unit', self.game.name, self.gge_id)


class UnitList(models.Model):
    title = models.CharField(max_length=128, blank=True)
    units = models.ManyToManyField(Unit, through='gge_proxy_manager.UnitListRelation')

    class Meta:
        app_label = 'gge_proxy_manager'


class UnitListRelation(models.Model):
    unit = models.ForeignKey(Unit, related_name='list_relations')
    list = models.ForeignKey(UnitList, related_name='unit_relations')
    amount = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'gge_proxy_manager'


class UnitFormation(models.Model):
    left = models.ForeignKey(UnitList, related_name='formations_on_left', null=True, blank=True, default=None)
    right = models.ForeignKey(UnitList, related_name='formations_on_right', null=True, blank=True, default=None)
    center = models.ForeignKey(UnitList, related_name='formations_on_center', null=True, blank=True, default=None)
    inner = models.ForeignKey(UnitList, related_name='formations_on_inner', null=True, blank=True, default=None)

    class Meta:
        app_label = 'gge_proxy_manager'