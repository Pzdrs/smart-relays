from urllib.parse import urlsplit

from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest

from smart_relays.utils.config import get_project_config


class SmartRelaysView(AccessMixin):
    title: str = None
    page_title: str = None
    page_subtitle: str = None
    login_required: bool = True

    def test_func(self, request: HttpRequest):
        """
        Yoinked from the Django built-in UserPassesTestMixin
        """
        pass

    def handle_test_fail(self, request) -> HttpResponse:
        messages.error(request, 'You do not have permission to access that page.')
        try:
            referrer = request.META['HTTP_REFERER']
            if urlsplit(referrer).path != request.path:
                return HttpResponseRedirect(referrer)
        except KeyError:
            pass
        finally:
            return HttpResponseRedirect(get_project_config().default_page)

    def dispatch(self, request, *args, **kwargs):
        test_func = self.test_func(request)
        if test_func is not None and not test_func:
            return self.handle_test_fail(request)
        if not request.user.is_authenticated and self.login_required:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.get_title()
        context['page_title'] = self.get_page_title()
        context['page_subtitle'] = self.get_page_subtitle()

        return context

    def get_title(self):
        return self.title

    def get_page_title(self):
        return self.page_title

    def get_page_subtitle(self):
        return self.page_subtitle
