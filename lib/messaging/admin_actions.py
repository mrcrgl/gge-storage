from .base import send_message
from django.contrib import messages


def send_test_mail(modeladmin, request, queryset):

    send_to = request.user.email

    for template in queryset:
        send_message(template.slug, send_to)

    messages.success(request, "Test messages sent to %(send_to)s" % {"send_to": send_to})


send_test_mail.short_description = "Send template to your own email address"