from django.contrib import admin
from django.contrib.admin import ModelAdmin

from relays.models import Relay, RelayStateChange, RelayUpdateRecord, RelayCreateRecord, UserRelayShare, \
    RelayShareRecord


@admin.register(Relay)
class RelayAdmin(ModelAdmin):
    list_display = ('name', 'user', 'description')

    def save_model(self, request, obj, form, change):
        # Push the request to the queue, so that we have access to it later
        Relay.update_requests.put(request)
        super().save_model(request, obj, form, change)


@admin.register(RelayUpdateRecord)
class RelayUpdateRecordAdmin(ModelAdmin):
    list_display = ('relay', 'user', 'timestamp', 'field', 'old_value', 'new_value')


@admin.register(RelayCreateRecord)
class RelayCreateRecordAdmin(ModelAdmin):
    list_display = ('relay', 'user', 'timestamp')


@admin.register(RelayShareRecord)
class RelayShareRecordAdmin(ModelAdmin):
    list_display = ('relay', 'user', 'receiver', 'state', 'timestamp')


@admin.register(RelayStateChange)
class RelayStateChangeAdmin(ModelAdmin):
    list_display = ('relay', 'user', 'get_new_state', 'timestamp')

    @admin.display(description='New State')
    def get_new_state(self, obj):
        return 'ON' if obj.new_state else 'OFF'


@admin.register(UserRelayShare)
class UserRelayPermissionAdmin(ModelAdmin):
    list_display = ('user', 'relay', 'permission_level')
