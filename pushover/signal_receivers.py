from gge_proxy_manager.models import Castle, Player
from gge_proxy_manager.models.log import AttackLog
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .methods import notify_new_village, notify_ruin_village, notify_attack


@receiver(pre_save, sender=Player)
def catch_fresh_ruin(instance, **kwargs):

    if instance.is_ruin and instance.pk:
        if not Player.objects.get(pk=instance.pk).is_ruin:
            for c in instance.castles_who_are_villages():
                notify_ruin_village(c)


@receiver(post_save, sender=Castle)
def catch_available_villages(instance, **kwargs):

    if instance.is_village:
        if instance.player_id and instance.is_ruin:
            if not instance.player.alliance_id:
                notify_ruin_village(instance)
        elif not instance.player_id:
            notify_new_village(instance)


@receiver(post_save, sender=AttackLog)
def notify_incoming_attack(instance, created, **kwargs):
    if instance.type < 4 and created:
        notify_attack(instance)