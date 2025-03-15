from django.contrib import admin
from .models import ChatSession, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sent_at',)
    fields = ('sender_type', 'message_type', 'content', 'sent_at')

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'started_at', 'ended_at')
    list_filter = ('status', 'started_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('started_at',)
    inlines = [MessageInline]

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender_type', 'message_type', 'content', 'sent_at')
    list_filter = ('sender_type', 'message_type', 'sent_at')
    search_fields = ('content', 'session__user__username')
    readonly_fields = ('sent_at',)
