from django import forms

from relays.models import Relay


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
