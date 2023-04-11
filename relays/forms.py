from django import forms

from accounts.models import User
from relays.models import Relay, UserRelayShare
from smart_relays.utils.config import get_project_config


class RelayUpdateForm(forms.ModelForm):
    class Meta:
        model = Relay
        fields = '__all__'
        labels = {
            'user': ''
        }
        widgets = {
            'user': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].required = False

    def clean(self):
        try:
            if self.instance.user != self.cleaned_data['user']:
                raise forms.ValidationError('You cannot change the owner of a relay.')
        except KeyError:
            return super().clean()


class RelayCreateForm(forms.ModelForm):
    class Meta:
        model = Relay
        fields = '__all__'
        labels = {
            'user': ''
        }
        widgets = {
            'user': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input'}),
        }
        help_texts = {
            'name': 'The name of the relay',
            'description': 'A description of the relay',
        }

    def clean(self):
        if Relay.objects.count() >= get_project_config().max_relays:
            raise forms.ValidationError('There are no relay slots left.')
        return super().clean()


class ShareRelayForm(forms.ModelForm):
    class Meta:
        model = UserRelayShare
        fields = '__all__'
        widgets = {
            'relay': forms.HiddenInput(),
        }

    def __init__(self, user: User = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.exclude(pk=user.pk) if user else User.objects.all()
        self.fields['permission_level'].choices = UserRelayShare.PermissionLevel.choices
