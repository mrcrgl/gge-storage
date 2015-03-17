from django.contrib import admin
from .admin_actions import *
from .models import *


class MyModelAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        if not self.can_delete:
            return False
        return super(MyModelAdmin, self).has_delete_permission(request, obj)

    def has_add_permission(self, request):
        if not self.can_add:
            return False
        return super(MyModelAdmin, self).has_add_permission(request)


class CollectLogAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('player', 'gold', 'wood', 'stone', 'food', 'cole', 'collected')
    raw_id_fields = ("player",)


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'experience', 'honor', 'alliance', 'is_proxy_connected', 'created', 'updated')
    # 'alliance__name', 'alliance__level',
    list_filter = ('game',)
    search_fields = ['name', 'alliance__name']
    raw_id_fields = ("alliance",)
    exclude = ('proxy_connected', )

    def is_proxy_connected(self, obj):
        return obj.is_proxy_connected()


class CastleAdmin(admin.ModelAdmin):
    list_display = ('name', 'pos_x', 'pos_y', 'type', 'kid', 'player', 'created', 'updated')
    list_filter = ('kingdom',)
    search_fields = ['player__name', 'name', 'pos_x', 'pos_y']
    raw_id_fields = ("player",)


class AccountBalanceLogAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('player', 'gold', 'ruby', 'collected')
    list_filter = ('player',)
    raw_id_fields = ("player",)


class MapExplorerAdmin(admin.ModelAdmin):
    list_display = ('kingdom', 'circle_started', 'circle_ended', 'circle_locked_until', 'get_progress_display')
    list_filter = ('kingdom',)


class AttackLogAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('message_id', 'type', 'from_player_name', 'to_castle_name', 'count_warriors', 'count_tools',
                    'total_time', 'weft', 'created')
    list_filter = ('to_castle__game', 'type',)
    #search_fields = ['from_player__name', 'to_castle__name', 'message_id']
    raw_id_fields = ("from_player", "to_player", "from_castle", "to_castle",)

    def from_player_name(self, obj):
        return obj.from_player.name

    def to_castle_name(self, obj):
        return obj.to_castle.name


class AllianceAdmin(admin.ModelAdmin):
    list_display = ('name', 'game_name', 'gge_id', 'updated',)
    list_filter = ('game',)
    search_fields = ['name']

    def game_name(self, obj):
        return obj.game.name


class KingdomAdmin(admin.ModelAdmin):
    list_display = ('name', 'visual_key',)


class PlayerLevelHistoryAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('player', 'level', 'reached')
    list_filter = ('reached',)
    search_fields = ['player__name']
    raw_id_fields = ("player",)


class PlayerHonorHistoryAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('player', 'honor', 'reached')
    list_filter = ('reached',)
    search_fields = ['player__name']
    raw_id_fields = ("player",)


class PlayerAllianceHistoryAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('player', 'alliance', 'alliance_rank', 'reached')
    list_filter = ('reached',)
    search_fields = ['player__name']
    raw_id_fields = ("player",)


class ConfederationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'game_name', 'gge_id', 'type', 'value_type', 'orientation', 'distance', 'defence_close', 'defence_far', 'offence_close', 'offence_far')
    list_filter = ('game', 'type', 'value_type', 'orientation', 'distance',)
    search_fields = ['title', 'gge_id']

    def game_name(self, obj):
        return obj.game.name


class LogisticJobAdmin(admin.ModelAdmin):
    list_display = ('player', 'castle', 'receiver', 'resource', 'resource_limit', 'gold_limit', 'is_active')
    list_filter = ('is_active', 'resource')
    search_fields = ['player__name', 'castle__name', 'receiver__name']
    raw_id_fields = ("player", 'castle', 'receiver',)
    actions = [copy, activate, deactivate]


class ProductionJobAdmin(admin.ModelAdmin):
    list_display = ('player', 'castle', 'unit', 'valid_until', 'is_active', 'burst_mode', 'last_succeed')
    search_fields = ['player__name', 'castle__name', 'unit__title']
    list_filter = ('is_active', 'burst_mode', 'player__game',)
    raw_id_fields = ("player", 'castle', 'unit',)
    actions = [copy, activate, deactivate, enable_burst_mode, disable_burst_mode, force_unclock]


class ProductionLogAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_filter = ('player__game',)
    list_display = ('player', 'castle', 'unit', 'amount', 'produced',)
    search_fields = ['player__name', 'castle__name', 'unit__title']


class LogisticLogAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_filter = ('player__game',)
    list_display = ('player', 'castle', 'receiver', 'resource', 'amount', 'sent')
    search_fields = ['player__name', 'castle__name', 'receiver__name']


class ResourceBalanceLogAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('player', 'castle', 'wood', 'stone', 'food', 'cole', 'collected',)
    search_fields = ['player__name', 'castle__name', 'unit__title']


class AccountCollectLogAdmin(MyModelAdmin):
    can_add = False
    can_delete = False

    list_display = ('player', 'gold', 'ruby', 'collected',)
    search_fields = ['player__name']


class NonPlayerCastleTypeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}


class BotAutoLoginAdmin(admin.ModelAdmin):
    list_display = ('player', 'username', 'from_hour', 'to_hour', 'enabled')
    raw_id_fields = ('player',)


admin.site.register(NonPlayerCastleType, NonPlayerCastleTypeAdmin)
admin.site.register(LogisticJob, LogisticJobAdmin)
admin.site.register(ProductionJob, ProductionJobAdmin)
admin.site.register(LogisticLog, LogisticLogAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(PlayerLevelHistory, PlayerLevelHistoryAdmin)
admin.site.register(PlayerHonorHistory, PlayerHonorHistoryAdmin)
admin.site.register(PlayerAllianceHistory, PlayerAllianceHistoryAdmin)
admin.site.register(Confederation, ConfederationAdmin)
admin.site.register(Alliance, AllianceAdmin)
admin.site.register(AttackLog, AttackLogAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Kingdom, KingdomAdmin)
admin.site.register(Game)
admin.site.register(ProductionLog, ProductionLogAdmin)
admin.site.register(Castle, CastleAdmin)
admin.site.register(ResourceBalanceLog, ResourceBalanceLogAdmin)
admin.site.register(CollectLog, CollectLogAdmin)
admin.site.register(AccountBalanceLog, AccountBalanceLogAdmin)
admin.site.register(AccountCollectLog, AccountCollectLogAdmin)
admin.site.register(MapExplorer, MapExplorerAdmin)
admin.site.register(BotAutoLogin, BotAutoLoginAdmin)