# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    friends = models.ManyToManyField('self', through='Friendship', symmetrical=False)
    blocked_users = models.ManyToManyField('self', symmetrical=False, related_name='blocked_by', blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Custom related name
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Custom related name
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='user',
    )

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='friendships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='friend_requests', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('from_user', 'to_user')
