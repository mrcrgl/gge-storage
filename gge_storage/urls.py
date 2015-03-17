from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gge_storage.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^intern/', include('intern.urls', app_name='intern', namespace='intern')),
    url(r'^auth/', include('authentication.urls', app_name='auth', namespace='auth')),
    url(r'^npc/', include('npc.urls', app_name='npc', namespace='npc')),
    url(r'^', include('cms.urls')),
    url(r'^', include('frontend.urls', app_name='fe', namespace='fe')),
    url(r'^400/', TemplateView.as_view(template_name="400.html")),
    url(r'^403/', TemplateView.as_view(template_name="403.html")),
    url(r'^404/', TemplateView.as_view(template_name="404.html")),
    url(r'^500/', TemplateView.as_view(template_name="500.html")),
    url(r'^npc/', include('npc.urls', app_name='npc', namespace='npc')),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)