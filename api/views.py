from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from relays.models import Relay
from smart_relays.serializers import RelaySerializer


class StatusView(APIView):
    def get(self, request, format=None):
        return Response({'status': 'ok'})


class RelayDetail(APIView):
    def get(self, request, pk, format=None):
        relay: Relay = Relay.objects.get(pk=pk)
        serializer = RelaySerializer(relay)
        return JsonResponse(serializer.data | {
            'current_state': relay.get_current_state()
        })


class RelayToggle(APIView):
    def post(self, request, pk, format=None):
        relay: Relay = Relay.objects.get(pk=pk)
        new_state = relay.toggle()
        return Response({
            'status': 'ok',
            'new_state': new_state
        })
