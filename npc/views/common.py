from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext
from gge_proxy_manager.models import NonPlayerCastle


class IndexView(View):
    template_name = "npc/index.html"

    def get(self, request):

        npc_list = NonPlayerCastle.objects.all().order_by('level', '-fights_left')

        return render_to_response(
            self.template_name,
            {
                "npc_list": npc_list
            },
            context_instance=RequestContext(request)
        )