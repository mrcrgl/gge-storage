from __future__ import unicode_literals

from django.core.cache import cache
from django.db import models
from django.conf import settings
from django.utils.timezone import now, timedelta
from django.core.urlresolvers import reverse
import dateutil.parser
from .alliance import AllianceRankMixin
from .castle import Castle
Q = models.Q


class Player(models.Model, AllianceRankMixin):
    game = models.ForeignKey("gge_proxy_manager.Game", db_index=True, null=True, default=None, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='players', null=True, default=None, blank=True)
    alliance = models.ForeignKey("gge_proxy_manager.Alliance", related_name='players', null=True, blank=True, default=None)
    alliance_rank = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    name = models.CharField(max_length=128)
    gge_id = models.PositiveIntegerField(db_index=True)
    level = models.SmallIntegerField(default=0)
    experience = models.PositiveIntegerField(default=0)
    honor = models.PositiveIntegerField(default=0)
    fame = models.PositiveIntegerField(default=0)
    success = models.PositiveIntegerField(default=0)
    is_ruin = models.BooleanField(default=False, db_index=True)
    dangerously = models.FloatField(default=0.0)
    proxy_connected = models.DateTimeField(null=True, default=None, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("intern:player_detail", kwargs={"pk": self.pk})

    def get_alliance_rank_display(self):
        return AllianceRankMixin.get_alliance_rank_display(self)

    def alliance_members(self):
        if not self.alliance:
            return None

        return Player.objects.filter(alliance=self.alliance).exclude(pk=self.pk)

    def get_dangerously_display(self):
        return "%d%%" % int(self.dangerously * 100)

    def castles_with_environment(self):
        return self.castles.filter(type__in=Castle.TYPE_WITH_WARRIORS).order_by('type', 'kingdom')

    def castles_who_are_villages(self):
        return self.castles.filter(type=10).order_by('kingdom')

    def is_proxy_connected(self, set=None):
        key = "player-last-seen-%d" % self.pk
        if set:
            cache.set(key, str(now()), 60)
            self.proxy_connected = now()
            self.save(update_fields=['proxy_connected'])

            return self.proxy_connected

        previous = cache.get(key)

        if previous:
            previous = dateutil.parser.parse(previous)
            self.proxy_connected = previous
            self.save(update_fields=['proxy_connected'])

        elif self.proxy_connected:
            self.proxy_connected = None
            self.save(update_fields=['proxy_connected'])

        return bool(self.proxy_connected)


class PlayerLevelHistory(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='level_history')
    level = models.PositiveSmallIntegerField(default=0)
    reached = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-reached']
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        return self.player.__unicode__()


class PlayerAllianceHistory(models.Model, AllianceRankMixin):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='alliance_history')
    alliance = models.ForeignKey("gge_proxy_manager.Alliance", null=True, blank=True, default=None, related_name='player_history')
    alliance_rank = models.PositiveSmallIntegerField(null=True, blank=True, default=None)
    reached = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-reached']
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        return self.player.__unicode__()

    def get_alliance_rank_display(self):
        return AllianceRankMixin.get_alliance_rank_display(self)


class PlayerHonorHistory(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='honor_history')
    honor = models.PositiveIntegerField(default=0)
    reached = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ['-reached']
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        return self.player.__unicode__()


class BotAutoLogin(models.Model):
    player = models.OneToOneField(Player, related_name='bot_auto_login')
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    from_hour = models.PositiveSmallIntegerField(default=0)
    to_hour = models.PositiveSmallIntegerField(default=24)
    enabled = models.BooleanField(default=True)