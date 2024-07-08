# chat/models.py
from django.db import models
from users.models import User

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class CallLog(models.Model):
    caller = models.ForeignKey(User, related_name='outgoing_calls', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='incoming_calls', on_delete=models.CASCADE)
    call_type = models.CharField(max_length=10, choices=[('audio', 'Audio'), ('video', 'Video')])
    call_start_time = models.DateTimeField()
    call_end_time = models.DateTimeField(blank=True, null=True)
