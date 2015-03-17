from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
Q = models.Q


class Alliance(models.Model):
    game = models.ForeignKey("gge_proxy_manager.Game", db_index=True, null=True, default=None, blank=True)
    confederation = models.ForeignKey("gge_proxy_manager.Confederation", related_name='alliances', null=True, default=None, blank=True)
    related_a = models.ManyToManyField('self', through="AllianceRelation", symmetrical=False, related_name='related_b')
    name = models.CharField(max_length=128)
    gge_id = models.PositiveIntegerField(db_index=True)
    level = models.SmallIntegerField(default=0, blank=True)
    fame = models.PositiveIntegerField(default=0)
    info = models.TextField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'gge_proxy_manager'

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("intern:alliance_detail", kwargs={"pk": self.pk})

    def get_relations(self, type=None):
        queryset = AllianceRelation.objects.filter(Q(alliance_a=self) | Q(alliance_b=self))

        if type:
            queryset = queryset.filter(type=type)

        return queryset


class AllianceRelation(models.Model):
    TYPE = (
        (1, "Maybe war"),
        (2, "NAP"),
        (3, "BND")
    )
    alliance_a = models.ForeignKey(Alliance, related_name='relation_a')
    alliance_b = models.ForeignKey(Alliance, related_name='relation_b')
    type = models.PositiveSmallIntegerField(choices=TYPE)

    class Meta:
        app_label = 'gge_proxy_manager'


class AllianceRankMixin(object):
    ALLIANCE_RANK_MAPPING = {
        "EmpirefourkingdomsExGG": (
            (None, "(unbekannt)"),
            (0, "Anfuehrer"),
            (1, "Stellv. Anfuehrer"),
            (2, "Kriegsmarschall"),
            (3, "Schatzmeister"),
            (4, "Diplomat"),
            (5, "Anwerber"),
            (6, "General"),
            (7, "Feldwebel"),
            (8, "Mitglied"),
        ),
        "EmpireEx_2": (
            (None, "(unbekannt)"),
            (0, "Anfuehrer"),
            (1, "Stellv. Anfuehrer"),
            (2, "Kriegsmarschall"),
            (3, "Schatzmeister"),
            (4, "Diplomat"),
            (5, "Anwerber"),
            (6, "General"),
            (7, "Feldwebel"),
            (8, "Mitglied"),
        ),
    }

    class Meta:
        app_label = 'gge_proxy_manager'

    def get_alliance_rank_display(self):
        if hasattr(self, 'game'):
            game = self.game
        elif hasattr(self, 'player'):
            game = self.player.game
        else:
            return "ERROR"

        for id, name in AllianceRankMixin.ALLIANCE_RANK_MAPPING[game.product_key]:
            if id == self.alliance_rank:
                return name

        return "Rang %s" % self.alliance_rank