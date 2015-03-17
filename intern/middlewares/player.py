from gge_proxy_manager.models import Player
from django.http import HttpResponseRedirect


class EnrichPlayerMiddleware(object):

    def process_request(self, request):

        request.player = None
        redirect_to = False

        if request.user.is_authenticated():
            # get player id by session
            player = None
            player_id = request.session.get('player_id', None)

            if request.GET.get('player_id'):
                if request.user.players.filter(pk=request.GET.get('player_id')).count() or request.user.is_superuser:
                    player_id = int(request.GET.get('player_id'))
                    redirect_to = request.META.get('HTTP_REFERER', '/')

            if not player_id and request.user.players.count():
                player = request.user.players.first()
                player_id = player.pk

            request.session['player_id'] = player_id
            if not player and player_id:
                player = Player.objects.get(pk=player_id)

            request.player = player

        if redirect_to:
            return HttpResponseRedirect(redirect_to)