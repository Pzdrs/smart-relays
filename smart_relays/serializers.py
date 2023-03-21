from rest_framework import serializers

from relays.models import Relay


class RelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Relay
        fields = '__all__'
