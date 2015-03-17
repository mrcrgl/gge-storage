from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext
from . import PlayerMixin


class MyEconomyView(View, PlayerMixin):
    template_name = 'my/economy.html'

    def get(self, request):

        return render_to_response(
            self.template_name,
            {},
            context_instance=RequestContext(request)
        )