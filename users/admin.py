# users/admin.py
from django.contrib import admin
from .models import Profile, Friendship

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'avatar', 'created_at')
    search_fields = ('user__username', 'bio')

    

admin.site.register(Profile, ProfileAdmin) 





admin.site.register(Friendship)