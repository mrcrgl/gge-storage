from __future__ import unicode_literals

from django.core.management.base import BaseCommand, CommandError
from lib.socket.server import runserver
#from optparse import make_option
#from daemonize import Daemonize
#import logging


class Command(BaseCommand):
    #option_list = BaseCommand.option_list + (
    #    make_option('--pid',
    #                type='string',
    #                action='store',
    #                dest='pid',
    #                help='PID file'),
    #)

    def handle(self, *args, **options):
        #pid = options.get('pid')

        #keep_fds = [logging.root.handlers[0].stream.fileno()]

        #daemon = Daemonize(app="runsocketserver", pid=pid, action=runserver, keep_fds=keep_fds)
        #daemon.start()
        runserver()