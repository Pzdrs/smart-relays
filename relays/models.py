from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager, Model, QuerySet


def default_relay_name():
    return "Relay #" + str(Relay.objects.count() + 1)


class RelayQuerySet(QuerySet):
    pass


class RelayManager(Manager):
    pass


class Relay(Model):
    name = models.CharField(max_length=100, default=default_relay_name)
    description = models.TextField(blank=True, null=True)
    state = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelayManager()


class RelayAuditRecord(Model):
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    state = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
