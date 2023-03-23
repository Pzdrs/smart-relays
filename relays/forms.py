from django import forms

from relays.models import Relay
from smart_relays.utils.config import get_project_config


class RelayUpdateForm(forms.ModelForm):
    class Meta:
        model = Relay
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'textarea'}),
        }


class RelayCreateForm(forms.ModelForm):
    class Meta:
        model = Relay
        fields = '__all__'
        widgets = {
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
