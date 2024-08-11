from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post, Like, Comment, CommentLike, CommentReply, ReplyLike


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'text', 'created_at']

class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_at']

class CommentReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = CommentReply
        fields = ['id', 'user', 'comment', 'text', 'created_at']

class ReplyLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ReplyLike
        fields = ['id', 'user', 'reply', 'created_at']
        



class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'user', 'caption', 'media', 'feeling_status', 'created_at', 'likes', 'comments'] 