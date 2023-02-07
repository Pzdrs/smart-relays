from django.contrib.auth.views import LoginView


class SmartRelaysLoginView(LoginView):
    template_name = 'sign_in.html'
    redirect_authenticated_user = True




