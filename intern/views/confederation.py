from __future__ import unicode_literals

from django.views.generic import (View,)
from django.shortcuts import render_to_response, RequestContext, Http404
from gge_proxy_manager.models import Player, Alliance, Confederation, AllianceRelation
from django.db.models import Q
from .mixins import game_queryset


class ConfederationMixin(object):

    def get_confederation_or_404(self, slug):
        try:
            confederation = Confederation.objects.get(slug=slug)
        except Confederation.DoesNotExist:
            raise Http404

        return confederation

    def check_user_permission(self, user, confederation):
        if not user.player:
            raise Http404

        if not user.player.alliance_id:
            raise Http404

        if not user.player.alliance.confederation_id:
            raise Http404

        if not user.player.alliance.confederation_id == confederation.pk:
            raise Http404


class RelatedAlliancesMixin(object):

    def get_related_alliances(self, alliances, types=[]):

        return Alliance.objects.filter(
            Q(relation_a__alliance_b__in=alliances, relation_a__type__in=types) |
            Q(relation_b__alliance_a__in=alliances, relation_b__type__in=types)
        ).distinct()


class ConfederationDashboardView(View, ConfederationMixin, RelatedAlliancesMixin):

    def get(self, request, slug):

        confederation = self.get_confederation_or_404(slug)
        self.check_user_permission(request.user, confederation)

        alliances_in_war = self.get_related_alliances(confederation.alliances.all(), [1])

        return render_to_response(
            "confederation/dashboard.html",
            {
                "confederation": confederation,
                "alliances_in_war": alliances_in_war
            },
            context_instance=RequestContext(request)
        )


class ConfederationMembersView(View, ConfederationMixin):

    def get(self, request, slug):

        confederation = self.get_confederation_or_404(slug)
        self.check_user_permission(request.user, confederation)

        member_list = confederation.get_members()

        return render_to_response(
            "confederation/member_list.html",
            {
                "confederation": confederation,
                "member_list": member_list
            },
            context_instance=RequestContext(request)
        )


class ConfederationRelatedAlliancesView(View, ConfederationMixin, RelatedAlliancesMixin):

    def get(self, request, slug):

        confederation = self.get_confederation_or_404(slug)
        self.check_user_permission(request.user, confederation)

        alliance_list = confederation.alliances.all()
        bnd_alliances = self.get_related_alliances(alliance_list, [3])
        nap_alliances = self.get_related_alliances(alliance_list, [2])

        return render_to_response(
            "confederation/related_alliances.html",
            {
                "confederation": confederation,
                "alliance_list": alliance_list,
                "bnd_alliances": bnd_alliances,
                "nap_alliances": nap_alliances
            },
            context_instance=RequestContext(request)
        )