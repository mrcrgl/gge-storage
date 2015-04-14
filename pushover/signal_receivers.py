from gge_proxy_manager.models import Castle
from gge_proxy_manager.models.log import AttackLog
from django.db.models.signals import post_save
from django.dispatch import receiver
from .methods import notify_new_village, notify_ruin_village, notify_attack


@receiver(post_save, sender=Castle)
def catch_available_villages(instance, **kwargs):

    if instance.is_village:
        if instance.player_id and instance.is_ruin:
            if not instance.player.alliance_id:
                notify_ruin_village(instance)
        elif not instance.player_id:
            notify_new_village(instance)


@receiver(post_save, sender=AttackLog)
def notify_incoming_attack(instance, **kwargs):
    if instance.type < 4:
        notify_attack(instance)