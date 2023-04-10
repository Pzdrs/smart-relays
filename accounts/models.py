from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def get_verbose_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name} ({self.username})'
        return self.username
