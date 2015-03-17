from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now, timedelta

Q = models.Q


class LogisticJob(models.Model):
    LOCK_FOR = (
        (60*15, '15 minutes'),
        (60*30, '30 minutes'),
        (60*45, '45 minutes'),
        (60*60, '1 hour'),
        (60*60*3, '3 hours'),
        (60*60*6, '6 hours'),
        (60*60*9, '9 hours'),
        (60*60*12, '12 hours'),
        (60*60*18, '18 hours'),
        (60*60*24, '24 hours'),
    )
    RESOURCE = (
        ('wood', 'Wood'),
        ('stone', 'Stone'),
        ('food', 'Food'),
        # ('cole', 'Cole'),
    )
    SPEED = (
        ('-1', 'Keine Pferde'),
        ('1001', 'Gold Pferde (test)'),
        ('1004', 'Rubi Pferde 1 (test)'),
        ('1007', 'Rubi Pferde 2 (test)'),
    )
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='logistic_jobs')
    castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='outgoing_logistic_jobs')
    receiver = models.ForeignKey("gge_proxy_manager.Castle", related_name='incoming_logistic_jobs')
    speed = models.CharField(max_length=5, choices=SPEED)
    is_active = models.BooleanField(default=True)
    resource = models.CharField(max_length=6, choices=RESOURCE)
    gold_limit = models.PositiveIntegerField(null=True, blank=True, default=None)
    resource_limit = models.PositiveIntegerField()
    lock_for = models.PositiveIntegerField(choices=LOCK_FOR, default=60*45)
    locked_till = models.DateTimeField(default=now, db_index=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def delay(self):
        self.locked_till = now() + timedelta(seconds=self.lock_for)
        self.save()

    def last_succeed(self):
        from .log import LogisticLog

        log = LogisticLog.objects.filter(castle=self.castle,
                                         receiver=self.receiver,
                                         resource=self.resource).order_by('-sent').first()
        if log:
            return log.sent

        return None


class ProductionJob(models.Model):
    player = models.ForeignKey("gge_proxy_manager.Player", related_name='production_jobs')
    castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='production_jobs')
    unit = models.ForeignKey("gge_proxy_manager.Unit")
    valid_until = models.PositiveIntegerField(null=True, blank=True, default=None,
                                              help_text='Bis zu welcher Menge ist der Auftrag gueltig')
    is_active = models.BooleanField(default=True)
    gold_limit = models.PositiveIntegerField(null=True, blank=True, default=None)
    food_balance_limit = models.IntegerField(null=True, blank=True, default=None)
    wood_limit = models.PositiveIntegerField(null=True, blank=True, default=None)
    stone_limit = models.PositiveIntegerField(null=True, blank=True, default=None)
    burst_mode = models.BooleanField(default=False, help_text='Ignoriert Nahrungsbilanz')
    locked_till = models.DateTimeField(default=now, db_index=True)
    last_fault_reason = models.CharField(null=True, default=None, max_length=128)
    last_fault_date = models.DateTimeField(default=None, null=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def last_succeed(self):
        from .log import ProductionLog

        log = ProductionLog.objects.filter(castle=self.castle, unit=self.unit).order_by('-produced').first()
        if log:
            return log.produced

        return None