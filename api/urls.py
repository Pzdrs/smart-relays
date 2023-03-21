from django.urls import path

from api.views import StatusView, RelayDetail

app_name = 'api'

urlpatterns = [
    path('', StatusView.as_view(), name='status'),
    path('relay/<int:pk>/', RelayDetail.as_view(), name='relay-detail'),
]
