from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from .views import common, map as mapviews, player, alliance, castle, tools, confederation, rest
from .views.my.settings import MySettingsView
from .views.my.economy import MyEconomyView
from .views.my.production import MyProductionJobListView, MyRecruitmentJobListView, MyRecruitmentJobFormView, \
    MyProductionJobFormView, MyJobStatisticView
from .views.my.logistic import MyLogisticJobListView, MyLogisticJobFormView
from .views.my.trading import MyTradingListView, MyTradingView
from .views.my.push import MyPushView, MyPushNotificationFormView
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gge_storage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login_required(common.IndexView.as_view()), name='index'),
    url(r'^game-login/$', login_required(common.GameLoginView.as_view()), name='game_login'),
    url(r'^map/$', login_required(mapviews.MapView.as_view()), name='map'),
    url(r'^map/icemrc/$', login_required(mapviews.MapView.as_view()), {"kid": 2}, name='map'),
    url(r'^map/greentom/$', login_required(mapviews.MapView.as_view()), {"kid": 3}, name='map'),
    url(r'^map/sandmrc/$', login_required(mapviews.MapView.as_view()), {"kid": 5}, name='map'),

    url(r'^zeitraffer/$', login_required(mapviews.DropMapView.as_view()), name='drop_map'),

    url(r'^players/$', login_required(player.PlayerListView.as_view()), name='player_list'),
    url(r'^players/(?P<pk>\d+)/$', login_required(player.PlayerDetailView.as_view()), name='player_detail'),

    url(r'^castles/$', login_required(castle.CastleListView.as_view()), name='castle_list'),
    url(r'^castles/unassigned/$', login_required(castle.CastleListUnassignedView.as_view()), name='castle_list_unassigned'),
    url(r'^castles/ruine_ap/$', login_required(castle.CastleListRuineApView.as_view()), name='castle_list_ruine_ap'),
    url(r'^castles/(?P<pk>\d+)/$', login_required(castle.CastleDetailView.as_view()), name='castle_detail'),

    url(r'^alliances/$', login_required(alliance.AllianceListView.as_view()), name='alliance_list'),
    url(r'^alliances/(?P<pk>\d+)/$', login_required(alliance.AllianceDetailView.as_view()), name='alliance_detail'),
    url(r'^alliances/(?P<pk>\d+)/neighborhood/(?P<kingdom_id>\d+)/$', login_required(alliance.AllianceMapView.as_view()), name='alliance_neighborhood'),
    url(r'^alliances/(?P<pk>\d+)/neighborhood/$', login_required(alliance.AllianceMapNoKdView.as_view()), name='alliance_neighborhood'),

    url(r'^my/settings/$', login_required(MySettingsView.as_view()), name='my_settings'),
    url(r'^my/economy/$', login_required(MyEconomyView.as_view()), name='my_economy'),
    url(r'^my/jobs/stats/$', login_required(MyJobStatisticView.as_view()), name='my_job_statistic'),
    url(r'^my/jobs/recruitment/$', login_required(MyRecruitmentJobListView.as_view()), name='my_recruitment_job_list'),
    url(r'^my/jobs/recruitment/new/$', login_required(MyRecruitmentJobFormView.as_view()), {'id': None}, name='my_recruitment_job_new'),
    url(r'^my/jobs/recruitment/(?P<id>\d+)/$', login_required(MyRecruitmentJobFormView.as_view()), name='my_recruitment_job_edit'),
    url(r'^my/jobs/production/$', login_required(MyProductionJobListView.as_view()), name='my_production_job_list'),
    url(r'^my/jobs/production/new/$', login_required(MyProductionJobFormView.as_view()), {'id': None}, name='my_production_job_new'),
    url(r'^my/jobs/production/(?P<id>\d+)/$', login_required(MyProductionJobFormView.as_view()), name='my_production_job_edit'),
    url(r'^my/jobs/logistic/$', login_required(MyLogisticJobListView.as_view()), name='my_logistic_job_list'),
    url(r'^my/jobs/logistic/new/$', login_required(MyLogisticJobFormView.as_view()), {'id': None}, name='my_logistic_job_new'),
    url(r'^my/jobs/logistic/(?P<id>\d+)/$', login_required(MyLogisticJobFormView.as_view()), name='my_logistic_job_edit'),
    url(r'^my/push/$', login_required(MyPushView.as_view()), name='my_push'),
    url(r'^my/push/notification/(?P<id>\d+)/$', login_required(MyPushNotificationFormView.as_view()), name='my_push_notification_form'),
    url(r'^my/push/notification/new/$', login_required(MyPushNotificationFormView.as_view()), name='my_push_notification_new'),
    url(r'^my/tradings/$', login_required(MyTradingListView.as_view()), name='my_trading_list'),

    url(r'^confederation/(?P<slug>[\w-]+)/$', login_required(confederation.ConfederationDashboardView.as_view()),
        name='confederation_dashboard'),

    url(r'^confederation/(?P<slug>[\w-]+)/members/$', login_required(confederation.ConfederationMembersView.as_view()),
        name='confederation_members'),

    url(r'^confederation/(?P<slug>[\w-]+)/related-alliances/$', login_required(confederation.ConfederationRelatedAlliancesView.as_view()),
        name='confederation_related_alliances'),

    url(r'^tools/castle-by-distance/$', login_required(tools.CastleByDistanceView.as_view()), name='tools_castlesbydistance'),

    url(r'^rest/(?P<app_name>[\w-]+)/(?P<model>[\w-]+)/$', login_required(rest.RestObjectListView.as_view()), name='rest_object_list'),
    url(r'^rest/(?P<app_name>[\w-]+)/(?P<model>[\w-]+)/(?P<id>\d+)/$', login_required(rest.RestObjectDetailView.as_view()), name='rest_object_detail'),
)
