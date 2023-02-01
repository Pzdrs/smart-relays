class MenuItem:
    def html(self):
        pass


class Label(MenuItem):
    def __init__(self, label: str):
        self.label = label

    def html(self):
        return f'<p class="menu-label">{self.label}</p>'


class Link(MenuItem):
    def __init__(self, label: str, url: str):
        self.label = label
        self.url = url

    def html(self):
        return f'<li><a href="{self.url}">{self.label}</a></li>'
