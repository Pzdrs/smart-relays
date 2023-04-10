from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse

from accounts.forms import SmartRelaysPasswordChangeForm
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
