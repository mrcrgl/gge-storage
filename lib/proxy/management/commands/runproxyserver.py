from __future__ import unicode_literals

from django.conf import settings
from lib.proxy.conf import settings as proxy_settings
from lib.daemonextension import DaemonCommand
import os
import logging
logger = logging.getLogger(__name__)

from lib.proxy import start_proxy

PATH_RUN = os.path.join(settings.ROOT_DIR, 'run')

if not os.path.isdir(PATH_RUN):
    os.mkdir(PATH_RUN)

PROCESS = "_".join(('proxy', proxy_settings.get("GAME")))


class Command(DaemonCommand):
    args = '<object object ...>'
    #help = 'Help text goes here'

    PID_FILE = os.path.join(
        PATH_RUN,
        ".".join((
            PROCESS,
            'pid'
        ))
    )

    def loop_callback(self, *args, **options):
        start_proxy()