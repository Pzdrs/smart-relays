from django.contrib.auth.models import User
from django.db import models
from django.db.models import Manager, Model, QuerySet
from django.urls import reverse


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

    objects = RelayManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('relays:relay-detail', args=(self.pk,))


class RelayAuditRecord(Model):
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RelayManager()

    class Meta:
        abstract = True


class RelayStateChangeQuerySet(QuerySet):
    def get_relay(self, relay: Relay):
        return self.filter(relay_id=relay.pk)

    def last_known_state(self, relay: Relay):
        return self.get_relay(relay).last()


class RelayStateChange(RelayAuditRecord):
    new_state = models.BooleanField()

    objects = RelayStateChangeQuerySet.as_manager()
