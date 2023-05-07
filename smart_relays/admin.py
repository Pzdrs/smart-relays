from django.contrib import admin

from smart_relays.models import ApplicationData


@admin.register(ApplicationData)
class ApplicationDataAdmin(admin.ModelAdmin):
    list_display = ('key', 'data')
