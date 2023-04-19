from typing import Callable

from django.http import HttpRequest


class MenuItem:

    def __init__(self, enabled: bool | Callable[[HttpRequest], bool] = True) -> None:
        self.enabled = enabled

    def is_enabled(self, request: HttpRequest = None):
        if callable(self.enabled):
            return self.enabled(request)
        return self.enabled

    def html(self):
        pass


class Label(MenuItem):

    def __init__(self, label: str, enabled: bool | Callable[[HttpRequest], bool] = True) -> None:
        super().__init__(enabled)
        self.label = label

    def html(self):
        return f'<p class="menu-label">{self.label}</p>'


class Link(MenuItem):

    def __init__(self, label: str, url: str, enabled: bool | Callable[[HttpRequest], bool] = True) -> None:
        super().__init__(enabled)
        self.label = label
        self.url = url

    def html(self):
        return f'<li><a href="{self.url}">{self.label}</a></li>'


class Menu:
    __items: tuple[MenuItem] = None

    def __init__(self, *items: MenuItem) -> None:
        self.__items = items

    def get_items(self, request: HttpRequest):
        return_items = []
        for item in self.__items:
            if item.is_enabled(request):
                return_items.append(item)
        return tuple(return_items)
