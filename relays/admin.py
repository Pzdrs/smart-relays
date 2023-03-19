from django.contrib import admin
from django.contrib.admin import ModelAdmin

from relays.models import Relay, RelayStateChange, RelayUpdateLog


@admin.register(Relay)
class RelayAdmin(ModelAdmin):
    list_display = ('name', 'description')

    def save_model(self, request, obj, form, change):
        # Push the request to the queue, so that we have access to it later
        Relay.update_requests.put(request)
        super().save_model(request, obj, form, change)


@admin.register(RelayUpdateLog)
class RelayUpdateLogAdmin(ModelAdmin):
    list_display = ('relay', 'user', 'timestamp', 'field', 'old_value', 'new_value')


@admin.register(RelayStateChange)
class RelayStateChangeAdmin(ModelAdmin):
    list_display = ('relay', 'user', 'get_new_state', 'timestamp')

    @admin.display(description='New State')
    def get_new_state(self, obj):
        return 'ON' if obj.new_state else 'OFF'
