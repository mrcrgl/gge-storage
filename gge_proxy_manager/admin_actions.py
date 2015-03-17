from django.utils.timezone import now


def copy(modeladmin, request, queryset):
    for obj in queryset.all():
        obj.pk = None
        obj.save()


def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)


def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)


def enable_burst_mode(modeladmin, request, queryset):
    queryset.update(burst_mode=True)


def disable_burst_mode(modeladmin, request, queryset):
    queryset.update(burst_mode=False)


def force_unclock(modeladmin, request, queryset):
    queryset.update(locked_till=now())
