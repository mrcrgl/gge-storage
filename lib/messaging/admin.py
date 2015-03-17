__author__ = 'riegel'
from django.contrib import admin
from .models import Template, TemplateAttachment
from .admin_actions import send_test_mail


class TemplateAttachmentInline(admin.TabularInline):
    """
    TemplateAttachment inline
    """
    model = TemplateAttachment
    extra = 0


class TemplateAdmin(admin.ModelAdmin):
    """
    Template admin
    """
    #model = Template

    list_display = ('__unicode__',)
    #list_filter = ('type',)
    search_fields = ('title',
                     'subject',)

    actions = [send_test_mail]

    inlines = [
        TemplateAttachmentInline,
    ]


admin.site.register(Template, TemplateAdmin)
