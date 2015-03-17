from django.views.generic import View
from . import PlayerMixin


class MySettingsView(View, PlayerMixin):
    template_name = 'my/settings.html'