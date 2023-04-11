from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include

from smart_relays.utils.config import get_project_config


def redirect_to_default_page(request):
    return redirect(get_project_config().default_page, permanent=True)


urlpatterns = [
    path('', redirect_to_default_page),
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls')),
    path('relays/', include('relays.urls')),
    path('admin/', admin.site.urls),
]
