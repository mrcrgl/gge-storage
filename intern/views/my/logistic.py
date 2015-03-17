from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext, Http404, HttpResponseRedirect
from gge_proxy_manager.models import LogisticJob
from django.core.urlresolvers import reverse
from intern.forms.my import MyLogisticJobForm
from .production import set_active, set_inactive, clone, delete
from . import PlayerMixin


class LogisticJobMixin(object):

    def get_queryset(self):
        player = self.player_or_404()
        return LogisticJob.objects.filter(player=player).order_by('castle__gge_id', 'receiver__gge_id')


class LogisticFormMixin(object):

    def get_form(self, id):
        player = self.player_or_404()

        initial = {}
        job = LogisticJob()

        if id:
            try:
                job = LogisticJob.objects.get(pk=id, player=player)
            except LogisticJob.DoesNotExist:
                raise Http404

            initial = {
                "castle": job.castle,
                "receiver_name": "%s / %d:%d [%d]" % (job.receiver.name, job.receiver.pos_x, job.receiver.pos_y, job.receiver.pk),
                "speed": job.speed,
                "resource": job.resource,
                "gold_limit": job.gold_limit,
                "resource_limit": job.resource_limit,
                "is_active": job.is_active,
            }

        form = self.form_class(self.request.POST if self.request.POST else None, player=player, initial=initial)

        return form, job


class JobActionMixin(object):

    ACTIONS = {
        'set_active': set_active,
        'set_inactive': set_inactive,
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


class MyLogisticJobListView(View, PlayerMixin, LogisticJobMixin, JobActionMixin):
    template_name = 'my/logistic_job_list.html'

    def get(self, request):

        object_list = self.get_queryset()

        return render_to_response(
            self.template_name,
            {
                'object_list': object_list
            },
            context_instance=RequestContext(request)
        )


class MyLogisticJobFormView(View, PlayerMixin, LogisticJobMixin, LogisticFormMixin):
    template_name = 'my/logistic_job_form.html'
    form_class = MyLogisticJobForm

    def get(self, request, id):

        form, job = self.get_form(id)

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, id):

        form, job = self.get_form(id)

        if form.is_valid():
            job.player = self.player_or_404()
            job.castle = form.cleaned_data.get("castle")
            job.receiver = form.clean_receiver()
            job.speed = form.cleaned_data.get("speed")
            job.resource = form.cleaned_data.get("resource")
            job.gold_limit = form.cleaned_data.get("gold_limit")
            job.resource_limit = form.cleaned_data.get("resource_limit")
            job.is_active = form.cleaned_data.get("is_active")
            job.save()

            return HttpResponseRedirect(reverse('intern:my_logistic_job_list'))

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )