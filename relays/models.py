from itertools import chain
from queue import Queue

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models import Model, QuerySet, Q
from django.urls import reverse

from accounts.models import User
from relays.utils.text import value_or_default, truncate_string, translate_bool


def default_relay_name() -> str:
    return f'Relay #{Relay.objects.count() + 1}'


def default_channel_name() -> str:
    return f'Channel #{Channel.objects.count() + 1}'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ----------------------------------------------
# Channels
# ----------------------------------------------

class Channel(Model):
    name = models.CharField(max_length=100, default=default_channel_name)
    pin = models.IntegerField()

    def __str__(self):
        return f'{self.name} ({self.pin})'

    @property
    def is_in_use(self):
        return self.relay is not None

    def test(self):
        from relays.tasks import test_channel
        test_channel.delay(self.pk)

    def synchronize(self):
        from relays.utils.gpio import set_channel_state
        set_channel_state(self, self.relay.get_current_state().new_state)


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

    def synchronized(self) -> 'RelayQuerySet':
        """
        Returns a queryset of relays, which are to be synchronized with the database
        """
        return self.filter(synchronized=True)


class Relay(BaseModel):
    # Queue that stores the requests when an update is issues to a Relay object
    update_requests = Queue()

    channel = models.OneToOneField(Channel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default=default_relay_name)
    description = models.TextField(max_length=65535, blank=True, null=True)
    # Determines whether the physical relay should be synced with the database upon startup
    synchronized = models.BooleanField(default=True)

    objects = RelayQuerySet.as_manager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('relays:relay-detail', args=(self.pk,))

    def get_current_state(self) -> 'RelayStateChange':
        """
        :return: the current state of a relay
        if no prior states have been recorded, False is returned by default
        """
        return RelayStateChange.objects.last_known_state(self)

    def get_audit_log(self, limit: int = -1):
        """
        :return: a tuple of all audit logs for this relay
        """
        return tuple(chain(
            self.get_create_audit_log(), self.get_update_audit_log(), self.get_state_audit_log())
        )[:limit]

    def get_state_audit_log(self):
        """
        :return: a queryset of all state changes for this relay
        """
        return RelayStateChange.objects.for_relay(self)

    def get_update_audit_log(self):
        """
        :return: a queryset of all update records for this relay
        """
        return RelayUpdateRecord.objects.for_relay(self)

    def get_create_audit_log(self):
        """
        :return: a queryset of all create records for this relay
        """
        return RelayCreateRecord.objects.for_relay(self)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self._state.adding:
            request = self.update_requests.get()
            original = Relay.objects.get(pk=self.pk)
            for field in self._meta.fields:
                original_value = getattr(original, field.name)
                new_value = getattr(self, field.name)
                if original_value != new_value:
                    update_log = RelayUpdateRecord(
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

    def get_possible_recipients(self) -> QuerySet:
        """
        Returns a queryset of users, which this relay isn't shared with, owner of the relay is excluded as well
        """
        return User.objects \
            .exclude(pk=self.user.pk) \
            .exclude(pk__in=UserRelayShare.objects.filter(relay=self).values_list('user_id'))

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
    def for_relay(self, relay: Relay):
        return self.filter(relay=relay)


class RelayAuditRecord(Model):
    class Meta:
        abstract = True

    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = RelayAuditRecordQuerySet.as_manager()

    def __str__(self):
        return f'{self.relay.name} - {self.timestamp} ({self.user})'

    def get_display(self):
        raise NotImplementedError(
            "{} is missing the implementation of the get_display() method.".format(
                self.__class__.__name__
            )
        )


class RelayStateChangeQuerySet(QuerySet):
    def create(self, relay: Relay, user: User, new_state: bool) -> 'RelayStateChange':
        return super().create(relay=relay, user=user, new_state=new_state)

    def toggle(self, relay: Relay, user: User) -> 'RelayStateChange':
        return self.create(relay=relay, user=user, new_state=not self.last_known_state(relay).new_state)

    def for_relay(self, relay: Relay) -> 'RelayStateChangeQuerySet':
        return self.filter(relay_id=relay.pk)

    def last_known_state(self, relay: Relay) -> 'RelayStateChange':
        return self.for_relay(relay).last()


class RelayStateChange(RelayAuditRecord):
    new_state = models.BooleanField()

    objects = RelayStateChangeQuerySet.as_manager()

    def __str__(self):
        return super().__str__() + f' - {self.new_state}'

    def get_display(self):
        return f'Relay state changed to <b>{translate_bool(self.new_state, "ON", "OFF")}</b>'


class RelayCreateRecord(RelayAuditRecord):
    def get_display(self):
        return f'Created new relay - <i>{self.relay}</i>'


class RelayUpdateRecord(RelayAuditRecord):
    field = models.CharField(max_length=50)
    old_value = models.CharField(max_length=65535)
    new_value = models.CharField(max_length=65535)

    def get_display(self):
        return f'The <b>{self.field}</b> field changed - {self._change_in_value(self.old_value, self.new_value)}'

    @staticmethod
    def _change_in_value(old, new):
        return f'''
            <i>{value_or_default(truncate_string(old, 25), "Blank")}</i>
            <i class="fa-solid fa-arrow-right px-1"></i>
            <i>{truncate_string(new, 25)}</i>
        '''


class RelayShareRecord(RelayAuditRecord):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    state = models.BooleanField(default=True)

    def clean(self):
        if self.user.pk == self.receiver.pk:
            raise ValidationError('User cannot share a relay with themselves')

    def get_display(self):
        if self.state:
            return f'Started sharing with <i>{self.receiver}</i>'
        else:
            return f'Revoked sharing with <i>{self.receiver}</i>'


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

    class Meta:
        unique_together = ('user', 'relay')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relay = models.ForeignKey(Relay, on_delete=models.CASCADE)
    permission_level = models.IntegerField(choices=PermissionLevel.choices)

    objects = UserRelayShareQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('relays:relay-detail', args=(self.relay_id,)) + '#sharing'

    def is_read_only(self) -> bool:
        return self.permission_level == self.PermissionLevel.READ_ONLY

    def is_control(self) -> bool:
        return self.permission_level == self.PermissionLevel.CONTROL

    def is_full_access(self) -> bool:
        return self.permission_level == self.PermissionLevel.FULL_ACCESS

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self._state.adding:
            RelayShareRecord.objects.create(relay=self.relay, user=self.grantor(), receiver=self.user)
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        RelayShareRecord.objects.create(relay=self.relay, user=self.grantor(), receiver=self.user, state=False)
        return super().delete(using, keep_parents)

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
