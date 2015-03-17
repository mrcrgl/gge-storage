from django.contrib import admin
from gge_proxy_manager.models import NonPlayerCastleType


class NonPlayerCastleTypeAdmin(admin.ModelAdmin):

    list_display = ('name', 'level', 'experience', 'honor', 'alliance', 'is_proxy_connected', 'created', 'updated')
    # 'alliance__name', 'alliance__level',
    list_filter = ('game',)
    search_fields = ['name', 'alliance__name']
    raw_id_fields = ("alliance",)


# admin.site.register(NonPlayerCastleType, NonPlayerCastleTypeAdmin)