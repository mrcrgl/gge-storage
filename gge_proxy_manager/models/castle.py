from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
Q = models.Q


class Castle(models.Model):
    TYPE = (
        (0, '?'),
        (1, 'Hauptburg'),
        (2, '?'),  # Raubritter
        (3, 'Hauptstadt'),  # Hauptstadt
        (4, 'Aussenposten'),
        (5, '?'),
        (6, '?'),
        (7, '?'),
        (8, '?'),
        (9, '?'),  # Schatteneumel
        (10, 'Rohstoffdorf'),
        (11, '?'),
        (12, 'Burg'),
        (13, '?'),
        (14, '?'),
        (15, '?'),
        (16, '?'),
        (17, '?'),
        (18, '?'),
        (19, '?'),
        (20, '?'),
        (21, '?'),
        (22, 'Handelsmetropole'),
        (23, 'Turm'),
    )
    TYPE_WITH_WARRIORS = [1, 4, 12]
    KID = (
        (0, "Green"),
        (1, "?"),
        (2, "Ice"),
        (3, "?"),
        (4, "?"),
        (5, "?"),
        (6, "?"),
        (7, "?"),
        (8, "?"),
    )
    RESOURCE_TYPE = (
        (0, "Wood"),
        (1, "Stone"),
        (2, "Food"),
        (3, "Castle"),
    )
    game = models.ForeignKey("gge_proxy_manager.Game", db_index=True, null=True, default=None, blank=True)
    player = models.ForeignKey("gge_proxy_manager.Player", null=True, default=None, blank=True, related_name='castles')
    type = models.PositiveIntegerField(choices=TYPE, db_index=True)
    resource_type = models.PositiveIntegerField(choices=RESOURCE_TYPE, null=True, default=None, blank=True)
    kid = models.PositiveSmallIntegerField(choices=KID)
    kingdom = models.ForeignKey("gge_proxy_manager.Kingdom", null=True, default=None, blank=True)
    gge_id = models.PositiveIntegerField(db_index=True)
    name = models.CharField(max_length=128, null=True, default=None, blank=True)
    pos_x = models.PositiveIntegerField()
    pos_y = models.PositiveIntegerField()
    # is_ruin = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        app_label = 'gge_proxy_manager'
        index_together = [
            ['kingdom', 'pos_x', 'pos_y'],
            ['game', 'updated', 'type', 'player'],
        ]

    def __unicode__(self):
        return "[%s] %s" % (self.kingdom.visual_key, self.name)

    @property
    def is_village(self):
        return self.type == 10

    @property
    def is_ruin(self):
        if self.player_id:
            return self.player.is_ruin

    def to_dict(self):
        return {
            "id": self.pk,
            "gge_id": self.gge_id,
            "kingdom_id": self.kingdom_id,
            "pos_x": self.pos_x,
            "pos_y": self.pos_y,
            "type": self.type
        }

    def get_absolute_url(self):
        return reverse("intern:castle_detail", kwargs={"pk": self.pk})

    def alliance_castles(self, around=100):
        if not self.player.alliance:
            return None

        return Castle.objects.filter(
            player__alliance=self.player.alliance,
            kingdom=self.kingdom,
            pos_x__range=(self.pos_x-around, self.pos_x+around),
            pos_y__range=(self.pos_y-around, self.pos_y+around),
            type__in=Castle.TYPE_WITH_WARRIORS).exclude(pk=self.pk)
