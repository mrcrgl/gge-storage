from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
# from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='index'),
)
