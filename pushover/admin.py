from django.contrib import admin
from .models import Client, Notify, NotifyVillage


class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'client_token', 'enabled', )
    raw_id_fields = ('user', )

    def username(self, cls):
        return cls.user.username


class NotifyAdmin(admin.ModelAdmin):
    list_display = ('username', 'match_alliance', 'match_my_players', 'priority', 'is_enabled', )
    raw_id_fields = ('match_alliance', )

    def username(self, cls):
        return unicode(cls.client)

    def is_enabled(self, cls):
        return cls.client.enabled


class NotifyVillageAdmin(admin.ModelAdmin):
    list_display = ('username', 'kingdom', 'match_ruin', 'match_unassigned', 'priority', 'is_enabled', )

    def username(self, cls):
        return unicode(cls.client)

    def is_enabled(self, cls):
        return cls.client.enabled


admin.site.register(Client, ClientAdmin)
admin.site.register(Notify, NotifyAdmin)
admin.site.register(NotifyVillage, NotifyVillageAdmin)