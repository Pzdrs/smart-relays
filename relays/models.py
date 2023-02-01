from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager, Model, QuerySet


def default_relay_name():
    return "Relay #" + str(Relay.objects.count() + 1)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RelayQuerySet(QuerySet):
    pass


class RelayManager(Manager):
    pass


class Relay(BaseModel):
    name = models.CharField(max_length=100, default=default_relay_name)
    description = models.TextField(blank=True, null=True)
    state = models.BooleanField(default=False)

    objects = RelayManager()

    def __str__(self):
        return self.name


class RelayAuditRecord(Model):
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = Manager()

    class Meta:
        abstract = True


class RelayStateChange(RelayAuditRecord):
    new_state = models.BooleanField()
