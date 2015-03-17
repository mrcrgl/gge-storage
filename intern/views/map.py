from __future__ import unicode_literals

from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext, HttpResponse
from gge_proxy_manager.models import Castle, Kingdom
from django.utils.timezone import datetime
import json


class MapView(View):

    def get(self, request, kid=4):

        min_x = 100
        max_x = 1200
        min_y = 100
        max_y = 1200
        step = 10

        coord = [min_x, min_x+step, min_y, min_y+step]

        matrix = []

        for x in range(min_x, max_x, step):

            y_lines = []

            for y in range(min_y, max_y, step):
                area = {
                    "x1": x,
                    "x2": x+step,
                    "y1": y,
                    "y2": y+step,
                    "castles": 0,
                    "population": "none"
                }

                castles = Castle.objects.all().filter(kingdom_id=kid, pos_x__range=(x, x+step),
                                                      pos_y__range=(y, y+step)).count()

                area["castles"] = castles
                if castles in range(1, 10):
                    area["population"] = "less"

                if castles in range(11, 20):
                    area["population"] = "middle"

                if castles in range(20, 99):
                    area["population"] = "high"

                y_lines.append(area)

            matrix.append(y_lines)

        return render_to_response(
            "map.html",
            {
                "matrix": matrix
            },
            context_instance=RequestContext(request)
        )


class DropMapView(View):

    def get(self, request):

        kingdoms = Kingdom.objects.filter(game=request.player.game)

        min_x = 100
        max_x = 1200
        min_y = 100
        max_y = 1200
        step = 10

        matrix = []

        for x in range(min_x, max_x, step):

            y_lines = []

            for y in range(min_y, max_y, step):
                area = {
                    "x1": x,
                    "x2": x+step,
                    "y1": y,
                    "y2": y+step
                }

                y_lines.append(area)

            matrix.append(y_lines)

        return render_to_response(
            "drop_map.html",
            {
                "matrix": matrix,
                "kingdoms": kingdoms
            },
            context_instance=RequestContext(request)
        )

    def post(self, request):

        kingdom = request.POST.get("kingdom")
        timestamp_from = request.POST.get("from")
        timestamp_to = request.POST.get("to")

        time_from = datetime.fromtimestamp(float(timestamp_from))
        time_to = datetime.fromtimestamp(float(timestamp_to))

        castles = Castle.objects.filter(kingdom_id=kingdom, type=10, created__gte=time_from, created__lte=time_to)

        castle_list = [castle.to_dict() for castle in castles]
        return HttpResponse(json.dumps({"castle_list": castle_list}), content_type="application/json")