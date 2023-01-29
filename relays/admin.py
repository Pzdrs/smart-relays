from django.contrib import admin
from django.contrib.admin import ModelAdmin

from relays.models import Relay


@admin.register(Relay)
class RelayAdmin(ModelAdmin):
    list_display = ('name', 'state', 'description')
