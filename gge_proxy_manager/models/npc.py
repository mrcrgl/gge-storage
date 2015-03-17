from __future__ import unicode_literals

from django.db import models
from .unit import UnitFormation
from django.core.urlresolvers import reverse


class NonPlayerCastleType(models.Model):
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'gge_proxy_manager'


class NonPlayerCastle(models.Model):
    type = models.ForeignKey(NonPlayerCastleType, related_name='non_player_castles')
    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128)
    level = models.PositiveSmallIntegerField()
    fights_left = models.PositiveSmallIntegerField(default=1)

    def __unicode__(self):
        return "%s %s" % (self.type, self.title)

    def get_absolute_url(self):
        return reverse("npc:npc_detail", kwargs={'type_slug': self.type.slug, 'npc_slug': self.slug})

    class Meta:
        app_label = 'gge_proxy_manager'


class NonPlayerCastleFormation(UnitFormation):
    castle = models.ForeignKey(NonPlayerCastle, related_name='formations')

    class Meta:
        app_label = 'gge_proxy_manager'


class NonPlayerCastleAttackSuggestion(models.Model):
    STATUS = (
        (1, 'akzeptiert'),
    )
    castle = models.ForeignKey(NonPlayerCastle, related_name='attack_suggestions')
    unit_formation = models.OneToOneField("gge_proxy_manager.UnitFormation", related_name='non_player_castle_attack_suggestion')
    losses = models.CharField(max_length=255, null=True, blank=True, default=None)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=1)

    class Meta:
        app_label = 'gge_proxy_manager'