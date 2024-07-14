# chat/urls.py

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('initiate/<int:user_id>/', views.initiate_chat, name='initiate_chat'),
    path('room/<str:room_name>/', views.room, name='room'),
]
