from __future__ import unicode_literals

from django.views.generic import (ListView, DetailView, View)
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from gge_proxy_manager.models import Alliance, Kingdom, Castle
# from django.db.models import Q
from .mixins import GameFilterMixin, game_queryset


class AllianceListView(GameFilterMixin, ListView):
    model = Alliance
    template_name = "alliance/list.html"
    paginate_by = 25

    def get_queryset(self):
        queryset = game_queryset(self)
        #super(GameFilterMixin, self).get_queryset()

        query = self.request.GET.get("q", None)
        if not query:
            return queryset

        for word in query.split():
            queryset = queryset.filter(name__icontains=word)

        return queryset


class AllianceDetailView(DetailView):
    model = Alliance
    template_name = "alliance/detail.html"
    template_name_field = "alliance"


class AllianceMapNoKdView(View, GameFilterMixin):

    def get(self, request, pk):
        kingdom = Kingdom.objects.filter(game=self.get_game()).order_by('kid').first()
        return HttpResponseRedirect(reverse("intern:alliance_neighborhood", kwargs={"pk": pk, "kingdom_id": kingdom.pk}))


class AllianceMapView(View, GameFilterMixin):

    x_start = 0
    x_stop = 1400
    y_start = 0
    y_stop = 1400

    def get_kingdoms(self):
        return Kingdom.objects.filter(game=self.get_game()).order_by('kid')

    def kingdom_or_404(self, kingdom_id):
        try:
            return Kingdom.objects.get(pk=kingdom_id)
        except Kingdom.DoesNotExist:
            raise Http404

    def alliance_or_404(self, alliance_id):
        try:
            return Alliance.objects.get(pk=alliance_id)
        except Alliance.DoesNotExist:
            raise Http404

    def get(self, request, pk, kingdom_id):
        alliance = self.alliance_or_404(pk)
        kingdom = self.kingdom_or_404(kingdom_id)
        kingdoms = self.get_kingdoms()

        castles = Castle.objects.filter(kingdom=kingdom, player__alliance=alliance)
        # , type__in=Castle.TYPE_WITH_WARRIORS

        ruler_steps = [i for i in range(self.x_start, self.x_stop, 100)]

        return render_to_response(
            "alliance/neighborhood.html",
            {
                "kingdom_list": kingdoms,
                "kingdom": kingdom,
                "alliance": alliance,
                "castle_list": castles,
                "x_start": self.x_start,
                "x_stop": self.x_stop,
                "y_start": self.y_start,
                "y_stop": self.y_stop,
                "ruler_steps": ruler_steps,
            },
            context_instance=RequestContext(request)
        )