from queue import Queue

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


class Relay(BaseModel):
    # Queue that stores the requests when an update is issues to a Relay object
    update_requests = Queue()

    name = models.CharField(max_length=100, default=default_relay_name)
    description = models.TextField(max_length=65535, blank=True, null=True)

    objects = RelayQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('relays:relay-detail', args=(self.pk,))

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        request = self.update_requests.get()
        if self._state.adding:
            pass
        else:
            original = Relay.objects.get(pk=self.pk)
            for field in self._meta.fields:
                original_value = getattr(original, field.name)
                new_value = getattr(self, field.name)
                if original_value != new_value:
                    update_log = RelayUpdateLog(
                        relay=self, user=request.user,
                        field=field.name,
                        old_value=original_value,
                        new_value=new_value
                    )
                    update_log.save()
        super().save(force_insert, force_update, using, update_fields)


class RelayAuditRecord(Model):
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

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


class RelayCreationLog(RelayAuditRecord):
    pass


class RelayUpdateLog(RelayAuditRecord):
    field = models.CharField(max_length=50)
    old_value = models.CharField(max_length=65535)
    new_value = models.CharField(max_length=65535)
