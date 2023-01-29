from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #path('', None),
    path('relays/', include('relays.urls')),
    path('admin/', admin.site.urls),
]
