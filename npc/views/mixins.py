from gge_proxy_manager.models import NonPlayerCastle
from django.shortcuts import Http404


class NonPlayerCastleMixin(object):

    def npc_or_404(self, **kwargs):
        try:
            return NonPlayerCastle.objects.get(**kwargs)
        except NonPlayerCastle.DoesNotExist:
            raise Http404