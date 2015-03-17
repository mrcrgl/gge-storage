from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from npc.views import common, non_player_castle
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gge_storage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login_required(common.IndexView.as_view()), name='index'),
    url(r'^add/$', login_required(non_player_castle.EditView.as_view()), {"pk": None}, name='npc_add'),
    url(r'^edit/(?P<pk>\d+)/$', login_required(non_player_castle.EditView.as_view()), name='npc_edit'),
    url(r'^(?P<type_slug>[\w-]+)/(?P<npc_slug>[\w-]+)/$', login_required(non_player_castle.DetailView.as_view()), name='npc_detail'),

)
