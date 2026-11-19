from rest_framework import viewsets

from .models import InboundItem
from .serializers import InboundItemSerializer


class InboundItemViewSet(viewsets.ModelViewSet):
    serializer_class = InboundItemSerializer
    http_method_names = ['get']

    def get_queryset(self):
        # Shared on purpose: every signed-in officer sees every inbound item, read-only.
        return InboundItem.objects.all()
