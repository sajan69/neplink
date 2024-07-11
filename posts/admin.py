# posts/admin.py
from django.contrib import admin
from .models import Post, Like, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at')
    search_fields = ('caption', 'user__username')
    list_filter = ('created_at',)
    list_per_page = 20
    

admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)