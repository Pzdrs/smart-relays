from urllib.parse import urlparse, ParseResult

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView, DetailView, CreateView

from accounts.forms import SmartRelaysPasswordChangeForm, UserUpdateForm, UserCreateForm
from accounts.models import User
from accounts.utils.access.user_access_tests import superuser, same_user_or_superuser
from smart_relays.utils.config import get_accounts_config
from smart_relays.utils.template import push_form_errors_to_messages
from smart_relays.views import SmartRelaysView


class SmartRelaysLoginView(SmartRelaysView, LoginView):
    template_name = 'sign_in.html'
    redirect_authenticated_user = True
    title = 'Sign in'
    login_required = False

    def form_invalid(self, form):
        push_form_errors_to_messages(self.request, form)
        return super().form_invalid(form)


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

    def test_func(self, request: HttpRequest):
        return superuser(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_form'] = UserCreateForm()
        return context


class UserDeleteView(SmartRelaysView, DeleteView):
    model = User
    success_url = reverse_lazy('accounts:user-management')

    def test_func(self, request: HttpRequest):
        return same_user_or_superuser(request, self.get_object())

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'User deleted successfully.')
        return super().delete(request, *args, **kwargs)


class UserUpdateView(SmartRelaysView, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'user_update.html'
    title = 'User update'
    http_referrer: ParseResult = None

    def test_func(self, request: HttpRequest):
        return same_user_or_superuser(request, self.get_object())

    def get_page_subtitle(self):
        return self.get_object()

    def get_success_url(self):
        user_list_url = reverse('accounts:user-management')
        if self.http_referrer.path == user_list_url:
            return user_list_url
        return super().get_success_url()

    def post(self, request, *args, **kwargs):
        self.http_referrer = urlparse(request.session.pop('http_referrer'))
        messages.success(self.request, 'User updated successfully.')
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.session['http_referrer'] = request.META.get('HTTP_REFERER')
        return super().get(request, *args, **kwargs)


class UserDetailView(SmartRelaysView, DetailView):
    model = User
    template_name = 'user_detail.html'
    title = 'My profile'

    def test_func(self, request: HttpRequest):
        return same_user_or_superuser(request, self.get_object())

    def get_page_subtitle(self):
        return self.get_object()


class UserCreateView(SmartRelaysView, CreateView):
    http_method_names = ('post',)
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('accounts:user-management')

    def test_func(self, request: HttpRequest):
        return superuser(request)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'User created successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        push_form_errors_to_messages(self.request, form)
        return HttpResponseRedirect(reverse('accounts:user-management'))


def toggle_user_active_status_view(request: HttpRequest, pk: int, *args, **kwargs):
    user: User = User.objects.get(pk=pk)
    if same_user_or_superuser(request, user):
        user.is_active = not user.is_active
        user.save()
        messages.success(request, 'User activity status changed successfully.')
        return HttpResponseRedirect(reverse('accounts:user-management'))
    else:
        return HttpResponse(status=403)
