from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
from .jobs import LogisticJob
Q = models.Q


class CollectLog(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='resource_collect_logs')
    wood = models.PositiveIntegerField(default=0)
    stone = models.PositiveIntegerField(default=0)
    food = models.PositiveIntegerField(default=0)
    gold = models.PositiveIntegerField(default=0)
    cole = models.PositiveIntegerField(default=0)
    collected = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'gge_proxy_manager'


class ResourceBalanceLog(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='resource_balances')
    castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='resource_balances')
    wood = models.FloatField()
    stone = models.FloatField()
    food = models.FloatField()
    cole = models.FloatField()
    collected = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'gge_proxy_manager'


class AccountCollectLog(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='collect_logs')
    gold = models.PositiveIntegerField()
    ruby = models.PositiveIntegerField()
    collected = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'gge_proxy_manager'


class AccountBalanceLog(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='balance_logs')
    gold = models.FloatField()
    ruby = models.FloatField()
    collected = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'gge_proxy_manager'


class AttackLog(models.Model):
    TYPE = (
        (1, "Angriff"),
        (2, "Eroberung"),
        (3, "Schattenangriff"),
        (4, "Raubritter Angriff"),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE)
    from_castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='sent_attacks', null=True, blank=True, default=None)
    from_player = models.ForeignKey("gge_proxy_manager.Player", related_name='sent_attacks', null=True, blank=True, default=None)
    to_castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='got_attacks')
    to_player = models.ForeignKey("gge_proxy_manager.Player", related_name='got_attacks', null=True, blank=True, default=None)
    message_id = models.PositiveIntegerField(db_index=True, unique=True)
    count_warriors = models.PositiveIntegerField(null=True, blank=True, default=None)
    count_tools = models.PositiveIntegerField(null=True, blank=True, default=None)
    total_time = models.PositiveIntegerField()
    weft = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def in_future(self):
        return now() < self.weft

    def get_progress_percentage(self):
        if now() > self.weft:
            return 100

        diff = self.weft - now()
        time_gone = self.total_time - diff.total_seconds()
        #timedelta(seconds=self.total_time)

        return 100 / self.total_time * time_gone

    def get_time_until(self):
        return self.weft - now()


class ProductionLog(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='production_logs')
    castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='production_logs')
    unit = models.ForeignKey("gge_proxy_manager.Unit")
    amount = models.PositiveIntegerField(default=5)
    produced = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        index_together = [
            ['castle', 'unit']
        ]
        ordering = ['-produced']
        app_label = 'gge_proxy_manager'


class LogisticLog(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='transports_sent')
    castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='transports_sent')
    receiver = models.ForeignKey("gge_proxy_manager.Castle", related_name='transports_received')
    resource = models.CharField(max_length=6, choices=LogisticJob.RESOURCE)
    amount = models.PositiveIntegerField(default=0)
    sent = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        index_together = [
            ['castle', 'receiver', 'resource']
        ]
        ordering = ['-sent']
        app_label = 'gge_proxy_manager'