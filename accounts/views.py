from urllib.parse import urlparse, ParseResult

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse, reverse_lazy, resolve
from django.views.generic import ListView, DeleteView, UpdateView, DetailView

from accounts.forms import SmartRelaysPasswordChangeForm
from accounts.models import User
from relays.utils.session import delete_session_parameter, set_session_parameter
from smart_relays.utils.config import get_accounts_config
from smart_relays.views import SmartRelaysView


class SmartRelaysLoginView(SmartRelaysView, LoginView):
    template_name = 'sign_in.html'
    redirect_authenticated_user = True
    title = 'Sign in'
    login_required = False


class SmartRelaysLogoutView(SmartRelaysView, LogoutView):
    template_name = 'logout.html'
    title = 'Signed out'


class SmartRelaysPasswordChangeView(SmartRelaysView, PasswordChangeView):
    form_class = SmartRelaysPasswordChangeForm
    template_name = 'password_change.html'
    title = 'Change password'

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('accounts:password-change')


class UserManagementView(SmartRelaysView, ListView):
    template_name = 'user_management.html'
    title = 'User management'
    model = User
    ordering = ('date_joined',)
    paginate_by = get_accounts_config().pagination['USERS']


class UserDeleteView(SmartRelaysView, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:user-management')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'User deleted successfully.')
        return super().delete(request, *args, **kwargs)


class UserUpdateView(SmartRelaysView, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']
    template_name = 'user_update.html'
    title = 'User update'
    http_referrer: ParseResult = None

    def get_page_subtitle(self):
        return self.get_object()

    def get_success_url(self):
        user_list_url = reverse('accounts:user-management')
        if self.http_referrer.path == user_list_url:
            return user_list_url
        return super().get_success_url()

    def post(self, request, *args, **kwargs):
        self.http_referrer = urlparse(request.session.get('http_referrer'))
        delete_session_parameter(request, 'http_referrer')
        messages.success(self.request, 'User updated successfully.')
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        set_session_parameter(request, 'http_referrer', request.META.get('HTTP_REFERER'))
        return super().get(request, *args, **kwargs)


class UserDetailView(SmartRelaysView, DetailView):
    model = User
    template_name = 'user_detail.html'
    title = 'My profile'

    def get_page_subtitle(self):
        return self.get_object()
