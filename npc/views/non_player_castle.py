from django.views.generic import View
from django.shortcuts import render_to_response, RequestContext, HttpResponseRedirect
from npc.forms import NonPlayerCastleForm
from gge_proxy_manager.models import NonPlayerCastle
from .mixins import NonPlayerCastleMixin


class EditView(View, NonPlayerCastleMixin):
    template_name = "npc/form.html"
    form_class = NonPlayerCastleForm

    def get_form(self, pk):
        if pk:
            npc = self.npc_or_404(pk=pk)
            print npc
            form = self.form_class(self.request.POST, instance=npc) \
                if self.request.POST else self.form_class(instance=npc)
        else:
            form = self.form_class(self.request.POST) \
                if self.request.POST else self.form_class()

        return form

    def get(self, request, pk=None):

        form = self.get_form(pk)

        return render_to_response(
            self.template_name,
            {
                "form": form
            },
            context_instance=RequestContext(request)
        )

    def post(self, request, pk=None):

        form = self.get_form(pk)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(request.get_full_path())

        return render_to_response(
            self.template_name,
            {
                "form": form
            },
            context_instance=RequestContext(request)
        )


class DetailView(View, NonPlayerCastleMixin):
    template_name = "npc/detail.html"

    def get(self, request, type_slug, npc_slug):

        npc = self.npc_or_404(slug=npc_slug, type__slug=type_slug)

        return render_to_response(
            self.template_name,
            {
                "npc": npc
            },
            context_instance=RequestContext(request)
        )


class FormationEditView(View):
    template_name = "npc/formation/form.html"

    def get(self, request, type_slug, npc_slug):

        npc = self.npc_or_404(type__slug=type_slug, slug=npc_slug)
        # npc = NonPlayerCastle.objects.get(slug=npc_slug, type__slug=type_slug)

        return render_to_response(
            self.template_name,
            {
                "npc": npc
            },
            context_instance=RequestContext(request)
        )
