from django.contrib import admin
from django.contrib.admin import ModelAdmin

from relays.models import Relay, RelayStateChange


@admin.register(Relay)
class RelayAdmin(ModelAdmin):
    list_display = ('name', 'state', 'description')


@admin.register(RelayStateChange)
class RelayStateChangeAdmin(ModelAdmin):
    list_display = ('relay', 'user', 'get_new_state', 'timestamp')

    @admin.display(description='New State')
    def get_new_state(self, obj):
        return 'ON' if obj.new_state else 'OFF'
