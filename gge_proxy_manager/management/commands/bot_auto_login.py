from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from gge_proxy_manager.models import BotAutoLogin
from gge_proxy_manager.methods import bot_login
import time


class Command(BaseCommand):
    args = '<object object ...>'

    def handle(self, *args, **options):
        bots = BotAutoLogin.objects.filter(enabled=True, from_hour__lte=now().hour, to_hour__gte=now().hour)

        for bot in bots:
            if bot.player.is_proxy_connected():
                print "%s: connected" % bot.player.name
                continue

            res = bot_login(bot.username, bot.password)

            if res:
                print "%s: reconnected (wait 5s)" % bot.player.name
                time.sleep(5)
            else:
                print "%s: failed (disable bot)" % bot.player.name
                bot.enabled = False
                bot.save(fields=['enabled'])