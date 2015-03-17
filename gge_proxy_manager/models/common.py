from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from .player import Player
from django.core.urlresolvers import reverse
Q = models.Q


class Game(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    product_key = models.CharField(max_length=32, unique=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        return self.name


class Kingdom(models.Model):
    name = models.CharField(max_length=128, null=True, default=None, blank=True)
    kid = models.SmallIntegerField(db_index=True)
    visual_key = models.CharField(max_length=8, default="-")
    game = models.ForeignKey(Game, db_index=True, null=True, default=None, blank=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        if not self.name:
            return "(unknown)"

        return self.name


class Confederation(models.Model):
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    slug = models.SlugField(max_length=128)
    logo = models.FileField(null=True, blank=True, default=None, upload_to='confederation_logos/')
    description = models.TextField(null=True, blank=True, default=None)

    class Meta:
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("intern:confederation_dashboard", kwargs={"slug": self.slug})

    def get_members(self):
        return Player.objects.filter(alliance__confederation=self).order_by('alliance_rank', '-level')