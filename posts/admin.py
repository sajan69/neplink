# posts/admin.py
from django.contrib import admin
from .models import Post, Like, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_text', 'content_video', 'content_image', 'content_audio', 'feeling_status', 'created_at']
    list_filter = ['user', 'created_at']
    search_fields = ['user', 'content_text', 'feeling_status']
    list_per_page = 10

admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)