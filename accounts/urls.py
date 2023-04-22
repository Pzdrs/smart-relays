from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import path

from accounts.views import SmartRelaysLoginView, SmartRelaysLogoutView, SmartRelaysPasswordChangeView, \
    UserManagementView, UserDeleteView, UserUpdateView, UserDetailView

app_name = 'accounts'

urlpatterns = [
    path(
        "login/", SmartRelaysLoginView.as_view(), name="login"
    ),
    path(
        "logout/", SmartRelaysLogoutView.as_view(), name="logout"
    ),
    path(
        "password_change/", SmartRelaysPasswordChangeView.as_view(),
        name="password-change"
    ),
    path(
        "password_change/done/", PasswordChangeDoneView.as_view(),
        name="password-change-done",
    ),
    path(
        "users/", UserManagementView.as_view(), name='user-management'
    ),
    path(
        "users/<int:pk>/", UserDetailView.as_view(), name='user-detail'
    ),
    path(
        "users/<int:pk>/delete/", UserDeleteView.as_view(), name='user-delete'
    ),
    path(
        "users/<int:pk>/update/", UserUpdateView.as_view(), name='user-update'
    ),
]
