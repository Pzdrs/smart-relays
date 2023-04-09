from queue import Queue

from django.db import models
from django.db.models import Model, QuerySet, Q
from django.urls import reverse

from accounts.models import User


def default_relay_name() -> str:
    return f'Relay #{Relay.objects.count() + 1}'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ----------------------------------------------
# Relay Models
# ----------------------------------------------

class RelayQuerySet(QuerySet):
    def for_user(self, user: User) -> 'RelayQuerySet':
        return self.all()


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

    def get_current_state(self):
        """
        Returns the current state of a relay
        if no prior states have been recorded, False is returned by default
        """
        return RelayStateChange.objects.last_known_state(self)

    def get_current_state_bool(self):
        return self.get_current_state().new_state if self.get_current_state() else False

    def get_audit_log(self):
        return RelayUpdateLog.objects.get_relay(self)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self._state.adding:
            request = self.update_requests.get()
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

    def toggle(self):
        current_state = self.get_current_state_bool()
        RelayStateChange(new_state=not current_state, relay=self).save()
        return not current_state

    @staticmethod
    def get_last_update_user() -> User | None:
        # If an empty queue is queried, it hangs up the main thread instead of throwing an exception smh
        if Relay.update_requests.empty():
            return None
        return Relay.update_requests.get().user


# ----------------------------------------------
# Audit Log Models
# ----------------------------------------------
class RelayAuditRecordQuerySet(QuerySet):
    def get_relay(self, relay: Relay):
        return self.filter(relay=relay)


class RelayAuditRecord(Model):
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RelayAuditRecordQuerySet.as_manager()

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


class RelayCreateLog(RelayAuditRecord):
    pass


class RelayUpdateLog(RelayAuditRecord):
    field = models.CharField(max_length=50)
    old_value = models.CharField(max_length=65535)
    new_value = models.CharField(max_length=65535)


# ----------------------------------------------
# User Permissions
# ----------------------------------------------
class UserRelayPermission(BaseModel):
    class PermissionLevel(models.TextChoices):
        read_only = 'readonly', 'Read Only'
        control = 'control', 'Control'
        all_access = 'all', 'All Access'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    permission_level = models.CharField(max_length=10, choices=PermissionLevel.choices)
