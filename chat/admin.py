# chat/admin.py
from django.contrib import admin
from .models import ChatMessage, CallLog

admin.site.register(ChatMessage)
admin.site.register(CallLog)
