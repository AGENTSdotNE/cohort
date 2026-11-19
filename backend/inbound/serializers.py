from rest_framework import serializers

from .models import InboundItem


class InboundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InboundItem
        fields = [
            'id',
            'reference',
            'received_raw',
            'received_at',
            'channel',
            'sender',
            'subject',
            'message',
            'logged_by',
        ]
        read_only_fields = fields
