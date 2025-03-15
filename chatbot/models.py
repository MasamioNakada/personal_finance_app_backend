from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"Chat session {self.id} - {self.user.username}"

class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    SENDER_CHOICES = [
        ('user', 'User'),
        ('bot', 'Bot')
    ]
    sender_type = models.CharField(max_length=4, choices=SENDER_CHOICES)
    
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text Message'),
        ('img', 'Image'),
        ('aud', 'Audio'),
        ('vid', 'Video'),
        ('file', 'File'),
        ('link', 'Link')
    ]
    message_type = models.CharField(max_length=4, choices=MESSAGE_TYPE_CHOICES, default='text')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_type} message in session {self.session.id}"

    class Meta:
        ordering = ['sent_at']