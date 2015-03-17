from django.http.response import Http404


class PlayerMixin(object):

    def player_or_404(self):

        if not self.request.player:
            raise Http404

        return self.request.player