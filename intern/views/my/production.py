from __future__ import unicode_literals

from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from gge_proxy_manager.models import ProductionJob, ProductionLog, Player
from django.core.urlresolvers import reverse
from intern.forms.my import MyProductionJobForm, MyRecruitmentJobForm
from django.contrib import messages
from . import PlayerMixin
from django.utils.timezone import now, timedelta
from django.db.models import Sum
import json
import random


def set_active(request, queryset):
    queryset.update(is_active=True)
    messages.success(request, "Jobs wurden aktiviert")


def set_inactive(request, queryset):
    queryset.update(is_active=False)
    messages.success(request, "Jobs wurden deaktiviert")


def enable_burst_mode(request, queryset):
    queryset.update(burst_mode=True)
    messages.success(request, "Burstmode wurde eingeschaltet")


def disable_burst_mode(request, queryset):
    queryset.update(burst_mode=False)
    messages.success(request, "Burstmode wurde ausgeschaltet")


def clone(request, queryset):
    for obj in queryset.all():
        obj.pk = None
        obj.is_active = False
        obj.save()
    messages.success(request, "Jobs wurden kopiert")


def delete(request, queryset):
    for obj in queryset.all():
        obj.delete()
    messages.success(request, "Jobs wurden entfernt")


class ProductionJobMixin(object):

    def get_queryset(self):
        player = self.player_or_404()
        return ProductionJob.objects.filter(player=player).order_by('castle__gge_id', 'unit__gge_id')


class ProductionFormMixin(object):

    def get_form(self, id, unit_type):
        player = self.player_or_404()

        initial = {}
        job = ProductionJob()

        if id:
            try:
                job = ProductionJob.objects.get(pk=id, player=player)
            except ProductionJob.DoesNotExist:
                raise Http404

            initial = {
                "castle": job.castle,
                "unit": job.unit,
                "food_balance_limit": job.food_balance_limit,
                "valid_until": job.valid_until,
                "gold_limit": job.gold_limit,
                "wood_limit": job.wood_limit,
                "stone_limit": job.stone_limit,
                "is_active": job.is_active,
                "burst_mode": job.burst_mode
            }

        form = self.form_class(self.request.POST if self.request.POST else None, player=player, unit_type=unit_type, initial=initial)

        return form, job


class JobActionMixin(object):

    ACTIONS = {
        'set_active': set_active,
        'set_inactive': set_inactive,
        'enable_burst_mode': enable_burst_mode,
        'disable_burst_mode': disable_burst_mode,
        'clone': clone,
        'delete': delete,
    }

    def post(self, request):

        id_list = request.POST.getlist("ids")
        action = request.POST.get("action", None)

        if 'all' in id_list:
            id_list.remove('all')

        if action and action in self.ACTIONS:
            function = self.ACTIONS[action]
            function(request, self.get_queryset().filter(pk__in=id_list))

        return HttpResponseRedirect(request.get_full_path())


class MyProductionJobListView(View, PlayerMixin, ProductionJobMixin, JobActionMixin):
    template_name = 'my/production_job_list.html'

    def get(self, request):

        object_list = self.get_queryset().filter(unit__type='tool')

        return render_to_response(
            self.template_name,
            {
                'object_list': object_list
            },
            context_instance=RequestContext(request)
        )


class MyProductionJobFormView(View, PlayerMixin, ProductionJobMixin, ProductionFormMixin):
    template_name = 'my/production_job_form.html'
    form_class = MyProductionJobForm

    def get(self, request, id):

        form, job = self.get_form(id, 'tool')

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, id):

        form, job = self.get_form(id, 'tool')

        if form.is_valid():
            job.player = self.player_or_404()
            job.castle = form.cleaned_data.get("castle")
            job.unit = form.cleaned_data.get("unit")
            job.valid_until = form.cleaned_data.get("valid_until")
            job.food_balance_limit = form.cleaned_data.get("food_balance_limit")
            job.gold_limit = form.cleaned_data.get("gold_limit")
            job.wood_limit = form.cleaned_data.get("wood_limit")
            job.stone_limit = form.cleaned_data.get("stone_limit")
            job.is_active = form.cleaned_data.get("is_active")
            job.burst_mode = form.cleaned_data.get("burst_mode")
            job.save()

            return HttpResponseRedirect(reverse('intern:my_production_job_list'))

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )


class MyRecruitmentJobListView(View, PlayerMixin, ProductionJobMixin, JobActionMixin):
    template_name = 'my/recruitment_job_list.html'

    def get(self, request):

        object_list = self.get_queryset().filter(unit__type='soldier')

        return render_to_response(
            self.template_name,
            {
                'object_list': object_list
            },
            context_instance=RequestContext(request)
        )


class MyRecruitmentJobFormView(View, PlayerMixin, ProductionJobMixin, ProductionFormMixin):
    template_name = 'my/production_job_form.html'
    form_class = MyRecruitmentJobForm

    def get(self, request, id):

        form, job = self.get_form(id, 'soldier')

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, id):

        form, job = self.get_form(id, 'soldier')

        if form.is_valid():
            job.player = self.player_or_404()
            job.castle = form.cleaned_data.get("castle")
            job.unit = form.cleaned_data.get("unit")
            job.valid_until = form.cleaned_data.get("valid_until")
            job.food_balance_limit = form.cleaned_data.get("food_balance_limit")
            job.gold_limit = form.cleaned_data.get("gold_limit")
            job.wood_limit = form.cleaned_data.get("wood_limit")
            job.stone_limit = form.cleaned_data.get("stone_limit")
            job.is_active = form.cleaned_data.get("is_active")
            job.burst_mode = form.cleaned_data.get("burst_mode")
            job.save()

            return HttpResponseRedirect(reverse('intern:my_recruitment_job_list'))

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )


class MyJobStatisticView(View):
    template_name = 'my/job_statistic.html'

    colors = [
        '#adfe09',
        '#28b3a9',
        '#cbce58',
        '#df5058',
        '#e3f3a5',
        '#ad115d',
        '#94e3d8',
        '#be9710',
        '#4174b1',
    ]

    def get_production_amount(self, f):
        n = now()
        r = []

        for d in range(0, 7):
            date = n - timedelta(hours=24*d)
            #f['produced__year'] = date.year
            #f['produced__month'] = date.month
            #f['produced__day'] = date.day
            f['produced__gte'] = date.replace(hour=0, minute=0, second=0)
            f['produced__lte'] = date.replace(hour=23, minute=59, second=59)

            r.append(ProductionLog.objects.filter(**f).aggregate(Sum('amount')).get('amount__sum', 0))

        return r

    def active_player_ids(self, f):
        #res = ProductionLog.objects.filter(**f).order_by('player').distinct('player').values('player')
        res = ProductionLog.objects.filter(**f).values_list('player', flat=True)

        return set(res)

    def get(self, request):

        if not request.player:
            raise Http404()

        datasets = list()
        f = dict(player=request.player, unit__type='soldier')

        datasets += ({
            'label': 'Rekrutierung',
            'fillColor': "rgba(220,220,220,0.2)",
            'strokeColor': "rgba(220,220,220,1)",
            'pointColor': "rgba(220,220,220,1)",
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': "rgba(220,220,220,1)",
            'data': self.get_production_amount(f)
        }, )

        f = dict(player=request.player, unit__type='tool')

        datasets += ({
            'label': 'Produktion',
            'fillColor': "rgba(151,187,205,0.2)",
            'strokeColor': "rgba(151,187,205,1)",
            'pointColor': "rgba(151,187,205,1)",
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': "rgba(151,187,205,1)",
            'data': self.get_production_amount(f)
        }, )

        total_datasets = list()
        f = dict(unit__type='soldier')

        total_datasets += ({
            'label': 'Rekrutierung',
            'fillColor': "rgba(220,220,220,0.2)",
            'strokeColor': "rgba(220,220,220,1)",
            'pointColor': "rgba(220,220,220,1)",
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': "rgba(220,220,220,1)",
            'data': self.get_production_amount(f)
        }, )

        f = dict(unit__type='tool')

        total_datasets += ({
            'label': 'Produktion',
            'fillColor': "rgba(151,187,205,0.2)",
            'strokeColor': "rgba(151,187,205,1)",
            'pointColor': "rgba(151,187,205,1)",
            'pointStrokeColor': "#fff",
            'pointHighlightFill': "#fff",
            'pointHighlightStroke': "rgba(151,187,205,1)",
            'data': self.get_production_amount(f)
        }, )

        try:
            players = self.active_player_ids(dict(produced__gte=now() - timedelta(hours=24*7)))
            players = [Player.objects.get(pk=player_id) for player_id in players]

            player_tool_datasets = list()
            player_soldier_datasets = list()

            for player in players:
                f = dict(player=player, unit__type='tool')

                color = ''.join(random.choice("0123456789abcdef") for _ in range(6))
                color = "#" + color

                player_tool_datasets += ({
                    'label': player.name,
                    'strokeColor': color,
                    'pointColor': color,
                    'pointStrokeColor': "#fff",
                    'pointHighlightFill': "#fff",
                    'pointHighlightStroke': color,
                    'data': self.get_production_amount(f)
                }, )

                f = dict(player=player, unit__type='soldier')

                player_soldier_datasets += ({
                    'label': player.name,
                    'strokeColor': color,
                    'pointColor': color,
                    'pointStrokeColor': "#fff",
                    'pointHighlightFill': "#fff",
                    'pointHighlightStroke': color,
                    'data': self.get_production_amount(f)
                }, )
        except NotImplementedError:
            player_soldier_datasets = list()
            player_tool_datasets = list()

        labels = ["heute", "gestern", "vorgestern", "vor 3 Tagen", "vor 4 Tagen", "vor 5 Tagen", "vor 6 Tagen"]

        return render_to_response(
            self.template_name,
            {
                'chart_data': json.dumps({
                    'labels': labels,
                    'datasets': datasets
                }),

                'chart_two_data': json.dumps({
                    'labels': labels,
                    'datasets': player_tool_datasets
                }),

                'chart_three_data': json.dumps({
                    'labels': labels,
                    'datasets': player_soldier_datasets
                }),

                'chart_total_data': json.dumps({
                    'labels': labels,
                    'datasets': total_datasets
                })
            },
            context_instance=RequestContext(request)
        )