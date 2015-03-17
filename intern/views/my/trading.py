from django.views.generic import View
from . import PlayerMixin


class MyTradingListView(View, PlayerMixin):
    template_name = 'my/trading_list.html'


class MyTradingView(View, PlayerMixin):
    template_name = 'my/trading_form.html'