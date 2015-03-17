from __future__ import unicode_literals

from django.conf.urls import patterns, url
# from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',
        {'login_url': '/'}, name='logout'),
)
