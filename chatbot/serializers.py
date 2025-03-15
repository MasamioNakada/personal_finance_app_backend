from rest_framework import serializers
from .models import ChatSession, Message
from django.contrib.auth.models import User

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender_type', 'message_type', 'content', 'sent_at']
        read_only_fields = ['id', 'sent_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'started_at', 'ended_at', 'status', 'messages']
        read_only_fields = ['id', 'started_at', 'ended_at']