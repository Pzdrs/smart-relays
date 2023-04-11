from queue import Queue

from django.core.exceptions import ValidationError, ObjectDoesNotExist
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
        """
        Returns a queryset of relays, which either belong to the user or the user has a permission to access them
        """
        permitted_relay_ids = UserRelayShare.objects.filter(user=user).values_list('relay_id')
        return self.filter(
            Q(user=user) | Q(id__in=permitted_relay_ids)
        )


class Relay(BaseModel):
    # Queue that stores the requests when an update is issues to a Relay object
    update_requests = Queue()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=default_relay_name)
    description = models.TextField(max_length=65535, blank=True, null=True)

    objects = RelayQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('relays:relay-detail', args=(self.pk,))

    def get_current_state(self) -> 'RelayStateChange':
        """
        Returns the current state of a relay
        if no prior states have been recorded, False is returned by default
        """
        return RelayStateChange.objects.last_known_state(self)

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
        current_state = self.get_current_state().new_state if self.get_current_state() else False
        RelayStateChange(new_state=not current_state, relay=self).save()
        return not current_state

    def get_share(self, user: User):
        """
        Returns the UserRelayShare object for the given user, if this relay isn't shared with the user, None is returned
        """
        try:
            return UserRelayShare.objects.get(user=user, relay=self)
        except ObjectDoesNotExist:
            return None

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
    def for_relay(self, relay: Relay) -> 'RelayStateChangeQuerySet':
        return self.filter(relay_id=relay.pk)

    def last_known_state(self, relay: Relay) -> 'RelayStateChange':
        return self.for_relay(relay).last()


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
class UserRelayShareQuerySet(models.QuerySet):
    def for_user(self, user: User) -> 'UserRelayShareQuerySet':
        return self.filter(user=user)

    def for_relay(self, relay: Relay) -> 'UserRelayShareQuerySet':
        return self.filter(relay=relay)


class UserRelayShare(BaseModel):
    class PermissionLevel(models.IntegerChoices):
        READ_ONLY = 0, 'Read Only'
        CONTROL = 1, 'Control'
        FULL_ACCESS = 2, 'Full Access'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    permission_level = models.IntegerField(choices=PermissionLevel.choices)

    objects = UserRelayShareQuerySet.as_manager()

    def is_read_only(self) -> bool:
        return self.permission_level == self.PermissionLevel.READ_ONLY

    def is_control(self) -> bool:
        return self.permission_level == self.PermissionLevel.CONTROL

    def is_full_access(self) -> bool:
        return self.permission_level == self.PermissionLevel.FULL_ACCESS

    @staticmethod
    def highest_permission_level() -> int:
        return UserRelayShare.PermissionLevel.FULL_ACCESS

    @staticmethod
    def lowest_permission_level() -> int:
        return UserRelayShare.PermissionLevel.READ_ONLY

    def clean(self):
        if self.user == self.relay.user:
            raise ValidationError('User cannot have a permission on their own relay')

    def grantor(self) -> User:
        return self.relay.user
