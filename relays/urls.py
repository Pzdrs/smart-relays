from django.urls import path

from relays.views import RelayListView, RelayDetailView, RelayUpdateView, RelayDeleteView, AuditLogView, RelayCreateView
from smart_relays.urls import redirect_to_default_page

app_name = 'relays'

urlpatterns = [
    path('', RelayListView.as_view(), name='relay-list'),
    path('create/', RelayCreateView.as_view(), name='relay-create'),
    path('auditlog/', AuditLogView.as_view(), name='audit-log'),
    path('<int:pk>/', RelayDetailView.as_view(), name='relay-detail'),
    path('<int:pk>/update/', RelayUpdateView.as_view(), name='relay-update'),
    path('<int:pk>/delete/', RelayDeleteView.as_view(), name='relay-delete'),

    # Shares
    path('<int:pk>/share', redirect_to_default_page, name='share-relay'),
    path('shares/<int:pk>/revoke', redirect_to_default_page, name='revoke-share'),
]
