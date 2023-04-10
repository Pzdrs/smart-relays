from django.urls import path

from api.views import StatusView, RelayDetail, RelayToggle

app_name = 'api'

urlpatterns = [
    path('', StatusView.as_view(), name='status'),
    path('relay/<int:pk>/', RelayDetail.as_view(), name='relay-detail'),
    path('relay/<int:pk>/toggle/', RelayToggle.as_view(), name='relay-toggle'),
]
