from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):

    def get_absolute_url(self):
        return reverse('accounts:user-detail', kwargs={'pk': self.pk})

    def get_verbose_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} ({self.username})'
        return self.username
