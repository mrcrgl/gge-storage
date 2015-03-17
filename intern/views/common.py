from __future__ import unicode_literals

from django.views.generic import View
from django.db.models import Q
from django.shortcuts import render_to_response, RequestContext, HttpResponse
from gge_proxy_manager.models import AttackLog, Player
import json
import requests
from django.conf import settings


class IndexView(View):

    def get(self, request):
        user = request.user

        last_attacks = None
        last_outbound_attacks = None
        my_buddys = None
        player = request.player

        proxy_connected_players = Player.objects.filter(proxy_connected__isnull=False).order_by('-proxy_connected')

        try:
            my_buddys = user.players.all()
        except (Player.DoesNotExist, AttributeError):
            pass

        try:
            if player:
                last_attacks = AttackLog.objects.filter(to_player__alliance=player.alliance).order_by('-weft')[:10]
                last_outbound_attacks = AttackLog.objects.filter(from_player__alliance=player.alliance).order_by('-weft')[:10]
        except Player.DoesNotExist:
            pass

        return render_to_response(
            "dashboard.html",
            {
                "last_attacks": last_attacks,
                "last_outbound_attacks": last_outbound_attacks,
                "my_buddys": my_buddys,
                "proxy_connected_players": proxy_connected_players
            },
            context_instance=RequestContext(request)
        )


class GameLoginView(View):

    def post(self, request):
        username = request.POST.get('bot_playername')
        password = request.POST.get('bot_playerpassword')
        secret = settings.LOGIN_SERVICE_SECRET
        service_host = settings.LOGIN_SERVICE_URL

        payload = {
            "username": username,
            "password": password,
            "secret": secret
        }
        headers = {'content-type': 'application/json'}

        r = requests.post(service_host, data=json.dumps(payload), headers=headers)

        if r.status_code == 202:
            # OK
            try:
                player = Player.objects.get(name=username)

                if not player.user_id:
                    player.user = request.user
                    player.save()
            except Player.DoesNotExist:
                pass

            return HttpResponse(json.dumps({'status': 'ok'}), content_type="application/json")

        return HttpResponse({'status': 'failed'}, content_type="application/json")