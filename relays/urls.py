from django.urls import path

from relays.views import RelayListView, RelayDetailView, RelayUpdateView, RelayDeleteView

app_name = 'relays'

urlpatterns = [
    path('', RelayListView.as_view(), name='relay-list'),
    path('<int:pk>', RelayDetailView.as_view(), name='relay-detail'),
    path('<int:pk>/update', RelayUpdateView.as_view(), name='relay-update'),
    path('<int:pk>/delete', RelayDeleteView.as_view(), name='relay-delete'),
]
