from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Player, PlayerAllianceHistory, PlayerHonorHistory, PlayerLevelHistory
import logging
logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Player)
def collect_player_changes(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        player = Player.objects.get(pk=instance.pk)
    except Player.DoesNotExist:
        return

    if instance.level != player.level:
        PlayerLevelHistory.objects.create(player_id=instance.pk, level=instance.level)

    if int(instance.honor) != int(player.honor):
        PlayerHonorHistory.objects.create(player_id=instance.pk, honor=instance.honor)

    if instance.alliance_id != player.alliance_id:
        kwargs = {
            'player_id': instance.pk,
            'alliance_id': instance.alliance_id[0] if isinstance(instance.alliance_id, list) else instance.alliance_id,
            'alliance_rank': instance.alliance_rank
        }
        try:
            PlayerAllianceHistory.objects.create(**kwargs)
        except Exception as e:
            logger.exception("PlayerAllianceHistory.create failed {%r} %s", kwargs, e)

    #if instance.level and instance.honor:
    #    instance.dangerously = calc_players_dangerously(instance.level, instance.honor)