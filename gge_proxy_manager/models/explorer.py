from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now, timedelta
Q = models.Q


class MapExplorer(models.Model):
    """
    - active?
    - starttime
    - endtime
    - step_delay (in sec.)

    - area_x1
    - area_x2
    - area_y1
    - area_y2

    - screen_width = 12
    - screen_height = 51

    - current_x1
    - current_x2
    - current_y1
    - current_y2
    """
    LOCK_CIRCLE_FOR = (
        (60*60, "1 hour"),
        (60*60*3, "3 hours"),
        (60*60*6, "6 hours"),
        (60*60*12, "12 hours"),
        (60*60*24, "24 hours"),
    )
    kingdom = models.ForeignKey("gge_proxy_manager.Kingdom")
    active = models.BooleanField(default=True)
    circle_started = models.DateTimeField(default=None, null=True, blank=True)
    circle_ended = models.DateTimeField(default=None, null=True, blank=True)
    lock_for = models.PositiveIntegerField(default=30)
    area_x1 = models.PositiveIntegerField()
    area_x2 = models.PositiveIntegerField()
    area_y1 = models.PositiveIntegerField()
    area_y2 = models.PositiveIntegerField()
    screen_width = models.PositiveIntegerField()
    screen_height = models.PositiveIntegerField()
    current_x1 = models.PositiveIntegerField(default=None, null=True, blank=True)
    current_x2 = models.PositiveIntegerField(default=None, null=True, blank=True)
    current_y1 = models.PositiveIntegerField(default=None, null=True, blank=True)
    current_y2 = models.PositiveIntegerField(default=None, null=True, blank=True)
    lock_circle_for = models.PositiveIntegerField(choices=LOCK_CIRCLE_FOR, default=LOCK_CIRCLE_FOR[1][0])
    circle_locked_until = models.DateTimeField(default=now, db_index=True)

    class Meta:
        app_label = 'gge_proxy_manager'
        index_together = (
            ('active', 'kingdom', ),
        )

    def progress(self):
        if not self.current_x1:
            return float(0.0)

        range_x = self.area_x2 - self.area_x1
        range_y = self.area_y2 - self.area_y1
        field_total = range_x * range_y

        range_x1 = self.current_x2 - self.area_x1
        range_y1 = self.current_y2 - self.area_y1
        field_scanned = range_x1 * range_y1

        range_x2 = self.area_x2 - self.current_x1
        range_y2 = self.current_y1 - self.area_y1
        field_scanned += range_x2 * range_y2

        return float( float(float(100) / float(field_total)) * float(field_scanned) )

    def get_progress_display(self):
        return "%f %%" % self.progress()

    def circle(self):
        if not self.current_x1:
            self.circle_started = now()
            # First time
            self.current_x1 = self.area_x1
            self.current_x2 = self.area_x1 + self.screen_width
            self.current_y1 = self.area_y1
            self.current_y2 = self.area_y1 + self.screen_height

        elif self.current_x2 > self.area_x2:
            # horizontal ueberschritten, naechste zeile

            if self.current_y2 > self.area_y2:
                # vertikal ueberschritten, somit ende
                self.circle_ended = now()
                self.current_x1 = None
                self.current_x2 = None
                self.current_y1 = None
                self.current_y2 = None
                self.circle_locked_until = now() + timedelta(seconds=self.lock_circle_for)
                self.save()
                return False

            self.current_x1 = self.area_x1
            self.current_x2 = self.area_x1 + self.screen_width
            self.current_y1 = self.current_y2
            self.current_y2 += self.screen_height

        else:
            # Not the first time, just one step right

            self.current_x1 = self.current_x2
            self.current_x2 += self.screen_width

        self.save()

        return True