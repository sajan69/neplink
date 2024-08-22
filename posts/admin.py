# posts/admin.py
from django.contrib import admin
from .models import Post, Like, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'image_tag')
    search_fields = ('caption', 'user__username')
    list_filter = ('created_at',)
    list_per_page = 20

    def image_tag(self, obj):
        if obj.media:
            return f'<img src="{obj.media.url}" width="100" height="100" />'
        return 'No Image'
    

admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)