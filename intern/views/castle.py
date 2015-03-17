from __future__ import unicode_literals

from django.shortcuts import render_to_response, RequestContext
from django.views.generic import (ListView, DetailView, View)
from gge_proxy_manager.models import Castle
from django.db.models import Q
from .mixins import GameFilterMixin, game_queryset
from django.utils.timezone import now, timedelta


class CastleListView(GameFilterMixin, ListView):
    model = Castle
    template_name = "castle/list.html"
    paginate_by = 25

    def get_queryset(self):
        queryset = game_queryset(self)
        #queryset = super(GameFilterMixin, self).get_queryset()

        query = self.request.GET.get("q", None)
        if not query:
            return queryset

        for word in query.split():
            queryset = queryset.filter(name__icontains=word)

        return queryset


class CastleDetailView(DetailView):
    model = Castle
    template_name = "castle/detail.html"
    template_name_field = "castle"


class CastleListUnassignedView(View, GameFilterMixin):

    model = Castle

    def get(self, request):

        unassigned_castle_list = self.get_queryset()\
            .filter(updated__gte=now() - timedelta(days=5), type=10).filter(
                Q(player=None) | Q(player__alliance=None, player__is_ruin=True)
            ).order_by('-updated')

        return render_to_response(
            "castle/list_unassigned.html",
            {
                "object_list": unassigned_castle_list
            },
            context_instance=RequestContext(request)
        )


class CastleListRuineApView(View, GameFilterMixin):

    model = Castle

    def get(self, request):

        unassigned_castle_list = self.get_queryset().filter(type=4).filter(
            player__alliance=None, player__is_ruin=True, updated__gte=now() - timedelta(days=5)
        ).order_by('-updated')[:30]

        return render_to_response(
            "castle/list_ruine_ap.html",
            {
                "object_list": unassigned_castle_list
            },
            context_instance=RequestContext(request)
        )