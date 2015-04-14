from django.views.generic import View
from . import PlayerMixin
from intern.forms.my import PushoverClientForm, PushoverNotificationForm
from pushover.models import Notify, Client
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect, Http404
from pushover.api.client import PushoverClient
from django.contrib import messages
from django.core.urlresolvers import reverse


def delete(request, queryset):
    for obj in queryset.all():
        obj.delete()
    messages.success(request, "Notifications wurden entfernt")


class JobActionMixin(object):

    ACTIONS = {
        'delete': delete,
    }

    def post_action(self, request):

        id_list = request.POST.getlist("ids")
        action = request.POST.get("action", None)

        if 'all' in id_list:
            id_list.remove('all')

        if action and action in self.ACTIONS:
            function = self.ACTIONS[action]
            function(request, request.user.pushover_client.notifications.filter(pk__in=id_list))

        return HttpResponseRedirect(request.get_full_path())


class MyPushView(View, PlayerMixin, JobActionMixin):
    template_name = 'my/push.html'

    def get(self, request):

        try:
            notification_list = request.user.pushover_client.notifications.all()
        except Client.DoesNotExist:
            notification_list = []

        return render_to_response(
            self.template_name,
            {
                'notification_list': notification_list
            },
            context_instance=RequestContext(request)
        )

    def post(self, request):

        if request.POST.get('action_mode', '') == 'on':
            return self.post_action(request)

        try:
            instance = request.user.pushover_client
        except Client.DoesNotExist:
            instance = None

        post = request.POST.copy()
        post['user'] = request.user.pk

        form = PushoverClientForm(post, instance=instance)

        if form.is_valid():

            api = PushoverClient()
            if api.verify(form.cleaned_data.get('client_token')):
                form.save()
            else:
                messages.error(request, "Token von Pushover abgelehnt '%s'" % form.cleaned_data.get('client_token'))

            return HttpResponseRedirect(reverse('intern:my_push'))

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )


class MyPushNotificationFormView(View, PlayerMixin):
    template_name = 'my/push_notification.html'
    form_class = PushoverNotificationForm
    object = None

    def get_object(self, pk):
        if self.object:
            return self.object

        if not pk:
            return Notify(client=self.request.user.pushover_client)

        try:
            self.object = self.request.user.pushover_client.notifications.get(pk=pk)
            return self.object
        except Client.DoesNotExist, Notify.DoesNotExist:
            raise Http404()

    def get_form(self, request, pk=None):
        if request.method == 'GET':
            data = None
        else:
            data = request.POST.copy()

        i = {
            'client': request.user.pushover_client.pk
        }

        if pk:
            try:
                n = self.get_object(pk)
                i['match_alliance'] = n.match_alliance
                i['match_my_players'] = n.match_my_players
                i['priority'] = n.priority
                i['retry'] = n.retry
                i['expire'] = n.expire
            except Client.DoesNotExist, Notify.DoesNotExist:
                raise Http404()

        return self.form_class(data, user=request.user, initial=i)

    def get(self, request, id=None):

        if id and request.GET.get('test'):
            n = self.get_object(id)
            if n.test():
                messages.success(request, "Testnachricht erfolgreich gesendet")
            else:
                messages.error(request, "Testnachricht fehlgeschlagen")

            return HttpResponseRedirect(reverse('intern:my_push'))

        form = self.get_form(request, id)

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, id=None):

        form = self.get_form(request, id)

        if form.is_valid():
            try:
                n = self.get_object(id)
            except Http404:
                n = Notify()

            n.client = request.user.pushover_client
            n.match_alliance = form.cleaned_data.get('match_alliance')
            n.match_my_players = form.cleaned_data.get('match_my_players')
            n.priority = form.cleaned_data.get('priority')
            n.retry = form.cleaned_data.get('retry')
            n.expire = form.cleaned_data.get('expire')
            n.save()
            return HttpResponseRedirect(reverse('intern:my_push'))

        return render_to_response(
            self.template_name,
            {
                'form': form
            },
            context_instance=RequestContext(request)
        )