from django.views.generic import View
from intern.forms.tools import CastlesByDistanceForm
from django.shortcuts import render_to_response, RequestContext
from gge_proxy_manager.models import Castle
from lib.map.utils import distance_to_castle
from decimal import Decimal, getcontext


class CastleByDistanceView(View):
    form_class = CastlesByDistanceForm

    def get_form(self, request, post=None):
        form = self.form_class(post)

        if request.player:
            castle_choices = Castle.objects.all().filter(game=request.player.game, player=request.player)\
                .order_by('kingdom', 'type', 'resource_type')

            form.fields["castle"].choices = [(castle.pk, "%s, %d:%d (%s)" % (castle.name, castle.pos_x, castle.pos_y, castle.kingdom.name)) for castle in castle_choices]

        return form

    def get(self, request):

        form = self.get_form(request)

        return render_to_response(
            "tools/castles_by_distance.html",
            {
                "form": form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request):

        form = self.get_form(request, request.POST)
        result_list = []
        from_castle = None

        if form.is_valid():
            from_castle = Castle.objects.get(pk=form.cleaned_data.get("castle"))
            distance = form.cleaned_data.get("distance")
            min_distance = int(distance)-1
            max_distance = int(distance)+1

            castles = Castle.objects.filter(
                kingdom=from_castle.kingdom,
                pos_x__gte=from_castle.pos_x-max_distance,
                pos_x__lte=from_castle.pos_x+max_distance,
                pos_y__gte=from_castle.pos_y-max_distance,
                pos_y__lte=from_castle.pos_y+max_distance
            )#.exclude(
             #   pos_x__gte=from_castle.pos_x-min_distance,
             #   pos_x__lte=from_castle.pos_x+min_distance,
             #   pos_y__gte=from_castle.pos_y-min_distance,
             #   pos_y__lte=from_castle.pos_y+min_distance
            #)

            for to_castle in castles.all():
                dist = Decimal("%.1f" % distance_to_castle(from_castle, to_castle))
                #print "%r" % dist
                #print repr(dist)
                #if isinstance(dist, Decimal):
                #    print "Decimal"

                #print "%f - %f" % (distance, dist)

                if distance == dist:
                #    print "Match %r" % dist
                    result_list.append(to_castle)

        return render_to_response(
            "tools/castles_by_distance.html",
            {
                "form": form,
                "from_castle": from_castle,
                "result_list": result_list
            },
            context_instance=RequestContext(request)
        )


def castles_by_distance(from_castle, distance):
    result_list = list()

    max_distance = int(distance)+1

    castles = Castle.objects.filter(
        kingdom=from_castle.kingdom,
        pos_x__gte=from_castle.pos_x-max_distance,
        pos_x__lte=from_castle.pos_x+max_distance,
        pos_y__gte=from_castle.pos_y-max_distance,
        pos_y__lte=from_castle.pos_y+max_distance
    )

    for to_castle in castles.all():
        dist = Decimal("%.1f" % distance_to_castle(from_castle, to_castle))

        if distance == dist:
            result_list.append(to_castle)

    return result_list