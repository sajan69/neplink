from rest_framework import viewsets
from .models import ChatMessage, CallLog
from .serializers import ChatMessageSerializer, CallLogSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

class CallLogViewSet(viewsets.ModelViewSet):
    queryset = CallLog.objects.all()
    serializer_class = CallLogSerializer


from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def initiate_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if request.user.id == other_user.id:
        return redirect('users:profile', user_id=user_id)  # Prevent chatting with oneself
    room_name = f"{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}"
    return redirect('chat:room', room_name=room_name)

@login_required
def room(request, room_name):
    user_ids = room_name.split('_')
    if str(request.user.id) not in user_ids:
        return redirect('home')  # Prevent accessing a room user is not part of
    
    # Fetch chat messages between the users
    messages = ChatMessage.objects.filter(
        sender_id__in=user_ids,
        receiver_id__in=user_ids
    ).order_by('timestamp')
    
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })