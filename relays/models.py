from django.db import models


# Create your models here.
def default_relay_name():
    return "Relay #" + str(Relay.objects.count() + 1)


class Relay(models.Model):
    name = models.CharField(max_length=100, default=default_relay_name)
    description = models.TextField(blank=True, null=True)
    state = models.BooleanField(default=False)
