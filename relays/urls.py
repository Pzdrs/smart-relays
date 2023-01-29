from django.urls import path

from relays.views import RelayListView, RelayDetailView

app_name = 'relays'

urlpatterns = [
    path('', RelayListView.as_view(), name='relay-list'),
    path('<int:pk>', RelayDetailView.as_view(), name='relay-detail'),
]
