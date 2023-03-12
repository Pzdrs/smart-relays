from django.views.generic.base import ContextMixin


class SmartRelaysView(ContextMixin):
    title = None
    page_title = None
    page_subtitle = None

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
