from rest_framework import serializers
from .models import ChatMessage, CallLog

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp']

class CallLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallLog
        fields = ['id', 'caller', 'receiver', 'call_type', 'call_start_time', 'call_end_time']
