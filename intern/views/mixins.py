from gge_proxy_manager.models import Player


def game_queryset(self, queryset=None):
    #if not queryset:
    #    queryset = self.get_queryset()

    if not self.model:
        raise AssertionError("self.model is not defined")

    queryset = self.model.objects.all()

    request = getattr(self, "request")

    if not request or not request.user.is_authenticated():
        return queryset

    player = request.player

    if not player:
        return queryset

    return queryset.filter(game=player.game)


class GameFilterMixin(object):

    def get_game(self):
        request = getattr(self, "request")

        if not request or not request.user.is_authenticated():
            return None

        player = request.player

        if not player:
            return None

        return player.game

    def get_queryset(self):

        #print "get_queryset"

        if not self.model:
            raise AssertionError("self.model is not defined")

        queryset = self.model.objects.all()

        game = self.get_game()

        if not game:
            return queryset

        return queryset.filter(game=game)