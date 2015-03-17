from .api.client import PushoverClient
from .models import NotifyVillage, Notify
from django.db.models import Q
from django.utils import formats
from django.utils.timezone import now


def distinct_fix(qs):
    new = []
    clients_in = []

    for q in qs:
        if q.client_id not in clients_in:
            new.append(q)
            clients_in.append(q.client_id)

    return new


def notify_new_village(castle):
    qs = NotifyVillage.objects.filter(match_unassigned=True)\
        .filter(Q(kingdom_id=castle.kingdom_id) | Q(kingdom__isnull=True))\
        .order_by('client', '-priority')

    title = "Leeres %s RSD" % castle.get_resource_type_display()
    message = "%s, %d:%d" % (castle.kingdom.name, castle.pos_x, castle.pos_y)

    send_push_messages(title, message, distinct_fix(qs))


def notify_ruin_village(castle):
    qs = NotifyVillage.objects.filter(match_ruin=True)\
        .filter(Q(kingdom_id=castle.kingdom_id) | Q(kingdom__isnull=True))\
        .order_by('client', '-priority')

    title = "%s RSD Ruine" % castle.get_resource_type_display()
    message = "%s, %d:%d" % (castle.kingdom.name, castle.pos_x, castle.pos_y)

    send_push_messages(title, message, distinct_fix(qs))


def notify_attack(attack):
    f = {
        'client__enabled': True
    }
    match_alliance = Q(match_alliance_id=attack.to_castle.player.alliance_id, match_alliance_id__isnull=False)
    match_myself = Q(match_my_players=True, client__user_id=attack.to_player.user_id)
    notifiers = Notify.objects.filter(**f).filter(match_alliance | match_myself)
    notifiers = notifiers.order_by('client', '-priority')

    notifiers = distinct_fix(notifiers)

    datetime_string = formats.date_format(attack.weft, "SHORT_DATETIME_FORMAT")

    try:
        alliance_name = attack.to_castle.player.alliance.name
    except AttributeError:
        alliance_name = None

    try:
        attack_source = attack.from_player.name
    except AttributeError:
        attack_source = None

    delta_left = attack.weft - now()
    minutes_to_go = delta_left.total_seconds() / 60

    title = "%s auf %s" % (attack.get_type_display(), attack.to_castle.player.name)

    message_parts = ["%s" % attack.to_castle.name]

    if alliance_name:
        message_parts.append("%s" % alliance_name)

    if attack_source:
        message_parts.append("von: %s" % attack_source)

    message_parts.append("%s" % attack.to_castle.kingdom.name)
    message_parts.append("in %d Minuten" % minutes_to_go)
    message_parts.append("%s" % datetime_string)

    push_msg = "\n".join(message_parts)

    send_push_messages(title, push_msg, notifiers)


def send_push_message(title, message, notifier, api_client=None):

    if not api_client:
        api_client = PushoverClient()

    if not notifier.client.enabled:
        return

    api_client.push(notifier.client.client_token, message=message, title=title,
                    retry=notifier.retry, expire=notifier.expire,
                    priority=notifier.priority)


def send_push_messages(title, message, queryset, api_client=None):

    if not api_client:
        api_client = PushoverClient()

    for notifier in queryset:
        send_push_message(title, message, notifier, api_client=api_client)