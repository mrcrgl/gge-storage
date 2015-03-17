from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from gge_proxy_manager.methods import clean_duplicate_alliances, clean_duplicate_castles, clean_duplicate_players
from gge_proxy_manager.models import Castle, Player, Alliance
from django.utils.timezone import now, timedelta
# from pprint import pprint


class Command(BaseCommand):
    args = '<object object ...>'
    #help = 'Help text goes here'

    def handle(self, *args, **options):
        print "Clean duplicate castles..."
        clean_duplicate_castles()

        print "Clean duplicate players..."
        clean_duplicate_players()

        print "Clean duplicate alliances..."
        clean_duplicate_alliances()

        too_old = now() - timedelta(days=30)

        print "Clean old castles..."
        print "...removed %d castles." % len([c.delete() for c in Castle.objects.filter(updated__lte=too_old)])

        print "Clean old players..."
        print "...removed %d players." % len([p.delete() for p in Player.objects.filter(updated__lte=too_old)])

        print "Clean old alliances..."
        print "...removed %d alliances." % len([a.delete() for a in Alliance.objects.filter(updated__lte=too_old)])