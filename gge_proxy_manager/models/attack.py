from __future__ import unicode_literals

from django.db import models
Q = models.Q


class AttackPlanTarget(models.Model):
    attack_plan = models.ForeignKey('gge_proxy_manager.AttackPlanning')
    player = models.ForeignKey("gge_proxy_manager.Player")

    class Meta:
        app_label = 'gge_proxy_manager'


class AttackAssignment(models.Model):
    source_player = models.ForeignKey("gge_proxy_manager.Player", related_name='attack_assignments')
    to_target = models.ForeignKey(AttackPlanTarget, related_name='assignments')
    to_target_castle = models.ForeignKey("gge_proxy_manager.Castle", related_name='planned_attacks')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'gge_proxy_manager'


class AttackPlanning(models.Model):
    creator = models.ForeignKey("gge_proxy_manager.Player", related_name='planned_attacks')
    targets = models.ManyToManyField("gge_proxy_manager.Player", through=AttackPlanTarget)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=5000, null=True, blank=True, default=None)
    is_clarified = models.BooleanField(default=False)
    planned_impact = models.DateTimeField(null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'gge_proxy_manager'