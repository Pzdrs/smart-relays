from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect

from smart_relays.utils.config import get_project_config


class SmartRelaysView(AccessMixin):
    title: str = None
    page_title: str = None
    page_subtitle: str = None
    login_required: bool = True

    def test_func(self):
        """
        Yoinked from the Django built-in UserPassesTestMixin
        """
        pass

    def handle_test_fail(self):
        pass

    def dispatch(self, request, *args, **kwargs):
        test_func = self.test_func()
        if test_func is not None and not test_func:
            redirect_url = self.handle_test_fail()
            if redirect_url:
                return HttpResponseRedirect(redirect_url)
            try:
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            except KeyError:
                return HttpResponseRedirect(get_project_config().default_page)
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
