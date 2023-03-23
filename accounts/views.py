from django.contrib.auth.views import LoginView, LogoutView


class SmartRelaysLoginView(LoginView):
    template_name = 'sign_in.html'
    redirect_authenticated_user = True


class SmartRelaysLogoutView(LogoutView):
    template_name = 'logout.html'
