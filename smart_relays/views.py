from django.views.generic.base import ContextMixin


class SmartRelaysView(ContextMixin):
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.get_title()

        return context

    def get_title(self):
        return self.title
