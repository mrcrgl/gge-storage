from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from gge_proxy_manager.models import Alliance
from .constants import MESSAGE_PRIORITY
from .api.client import PushoverClient


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='pushover_client')
    client_token = models.CharField(max_length=128)
    enabled = models.BooleanField(default=True)

    def __repr__(self):
        return "<%s %s:%s>" % (self.__class__.__name__, self.user.username, self.client_token)

    def __unicode__(self):
        return "%s:%s" % (self.user.username, self.client_token)


class Notify(models.Model):
    client = models.ForeignKey(Client, related_name='notifications')
    match_alliance = models.ForeignKey(Alliance, blank=True, null=True, default=None, db_index=True)
    match_my_players = models.BooleanField(default=False, db_index=True)
    priority = models.SmallIntegerField(choices=MESSAGE_PRIORITY, default=0)
    retry = models.PositiveIntegerField(default=30)
    expire = models.PositiveIntegerField(default=300)

    class Meta:
        ordering = ('-priority',)

    def test(self):
        if not self.pk or not self.client.enabled:
            return False

        title = 'Test'
        message = 'Dies ist eine Testnachricht'

        api = PushoverClient()
        return api.push(self.client.client_token, message, title=title, priority=self.priority,
                        retry=self.retry, expire=self.expire)


class NotifyVillage(models.Model):
    client = models.ForeignKey(Client, related_name='village_notifications')

    kingdom = models.ForeignKey("gge_proxy_manager.Kingdom", default=None, null=True)
    match_ruin = models.BooleanField(default=False)
    match_unassigned = models.BooleanField(default=False)

    priority = models.SmallIntegerField(choices=MESSAGE_PRIORITY, default=0)
    retry = models.PositiveIntegerField(default=30)
    expire = models.PositiveIntegerField(default=300)

    class Meta:
        ordering = ('-priority',)

    def test(self):
        if not self.pk or not self.client.enabled:
            return False

        title = 'Test'
        message = 'Dies ist eine Testnachricht'

        api = PushoverClient()
        return api.push(self.client.client_token, message, title=title, priority=self.priority,
                        retry=self.retry, expire=self.expire)