from __future__ import unicode_literals

from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponse
from django.views.generic import (View)
from django.db.models import get_model
from .mixins import GameFilterMixin, game_queryset
from django.utils.timezone import now, timedelta
from django.core import serializers
import json


class ContentTypeMixin(object):

    def get_model(self, app_name, model):
        return get_model(app_name, model)

    def get_instance(self, app_name, model, id):
        Model = self.get_model(app_name, model)
        try:
            return Model.objects.get(pk=id)
        except Model.DoesNotExist:
            raise Http404


class RestMixin(object):

    def get_filters(self):
        filters = dict()

        if hasattr(self, 'pk'):
            return {'pk': self.pk}

        for key in self.request.GET.keys():
            filters[key] = unicode(self.request.GET.get(key)).encode('utf-8')

            if filters[key] == 'TYPE_WITH_WARRIORS':
                filters[key] = [1, 4, 12]

        # print filters
        return filters

    def queryset(self):
        queryset = self.get_queryset()
        filters = self.get_filters()
        return queryset.filter(**filters)[:10]

    def json_response(self, queryset):
        response_data = serializers.serialize("json", queryset)
        return HttpResponse(response_data, content_type="application/json")


class RestObjectListView(View, RestMixin, GameFilterMixin, ContentTypeMixin):
    model = None

    def get(self, request, app_name, model):
        self.model = self.get_model(app_name, model)

        return self.json_response(self.queryset())


class RestObjectDetailView(View, RestMixin, GameFilterMixin, ContentTypeMixin):
    model = None
    pk = None

    def get(self, request, app_name, model, id):
        self.model = self.get_model(app_name, model)
        self.pk = id

        return self.json_response(self.queryset())