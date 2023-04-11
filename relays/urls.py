from django.urls import path

from relays.views import RelayListView, RelayDetailView, RelayUpdateView, RelayDeleteView, AuditLogView, \
    RelayCreateView, CreateRelayShareView, RevokeRelayShareView, RelayShareUpdateView, RelayChangeStateView

app_name = 'relays'

urlpatterns = [
    path('', RelayListView.as_view(), name='relay-list'),
    path('create/', RelayCreateView.as_view(), name='relay-create'),
    path('<int:pk>/', RelayDetailView.as_view(), name='relay-detail'),
    path('<int:pk>/update/', RelayUpdateView.as_view(), name='relay-update'),
    path('<int:pk>/delete/', RelayDeleteView.as_view(), name='relay-delete'),
    path('<int:pk>/toggle/', RelayChangeStateView.as_view(), name='relay-toggle'),

    # Audit Log
    path('auditlog/', AuditLogView.as_view(), name='audit-log'),

    # Shares
    path('<int:pk>/share', CreateRelayShareView.as_view(), name='share-relay'),
    path('shares/<int:pk>/revoke', RevokeRelayShareView.as_view(), name='revoke-share'),
    path('shares/<int:pk>/bump', RelayShareUpdateView.as_view(), name='bump-share-permissions')
]
