from __future__ import unicode_literals

from django.views.generic import (ListView, DetailView)
from gge_proxy_manager.models import Player
from django.db.models import Q
from .mixins import game_queryset


class PlayerListView(ListView):
    model = Player
    template_name = "player/list.html"
    paginate_by = 25

    def get_queryset(self):
        queryset = game_queryset(self)

        query = self.request.GET.get("q", None)
        if not query:
            return queryset

        #queryset = self.model.objects
        for word in query.split():
            queryset = queryset.filter(Q(name__icontains=word) | Q(alliance__name__icontains=word))

        return queryset


class PlayerDetailView(DetailView):
    model = Player
    template_name = "player/detail.html"
    template_name_field = "player"