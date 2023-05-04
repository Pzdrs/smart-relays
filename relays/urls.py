from django.urls import path

from relays.views import RelayListView, RelayDetailView, RelayUpdateView, RelayDeleteView, AuditLogView, \
    RelayCreateView, CreateRelayShareView, RevokeRelayShareView, RelayShareUpdateView, RelayChangeStateView, \
    ChannelListView, ChannelUpdateView, ChannelDeleteView, ChannelTestView

app_name = 'relays'

urlpatterns = [
    path('', RelayListView.as_view(), name='relay-list'),
    path('create/', RelayCreateView.as_view(), name='relay-create'),
    path('<int:pk>/', RelayDetailView.as_view(), name='relay-detail'),
    path('<int:pk>/update/', RelayUpdateView.as_view(), name='relay-update'),
    path('<int:pk>/delete/', RelayDeleteView.as_view(), name='relay-delete'),
    path('<int:pk>/toggle/', RelayChangeStateView.as_view(), name='relay-toggle'),

    # Channels
    path('channels/', ChannelListView.as_view(), name='channel-list'),
    path('channels/<int:pk>/update', ChannelUpdateView.as_view(), name='update-channel'),
    path('channels/<int:pk>/delete', ChannelDeleteView.as_view(), name='delete-channel'),
    path('channels/<int:pk>/test', ChannelTestView.as_view(), name='test-channel'),

    # Audit Log
    path('auditlog/', AuditLogView.as_view(), name='audit-log'),

    # Shares
    path('<int:pk>/share', CreateRelayShareView.as_view(), name='share-relay'),
    path('shares/<int:pk>/revoke', RevokeRelayShareView.as_view(), name='revoke-share'),
    path('shares/<int:pk>/bump', RelayShareUpdateView.as_view(), name='bump-share-permissions')
]
