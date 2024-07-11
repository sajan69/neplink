from django.urls import path
from . import views
from . import api_views

app_name = 'posts'

urlpatterns = [
    path('', views.home, name='home'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
     path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('reply-to-comment/<int:comment_id>/', views.reply_to_comment, name='reply_to_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('edit-reply/<int:reply_id>/', views.edit_reply, name='edit_reply'),
    path('delete-reply/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('like-reply/<int:reply_id>/', views.like_reply, name='like_reply'),

    #Api views
    path('api/posts/', api_views.PostListCreateAPIView.as_view(), name='post_list_create'),
    path('api/posts/<int:pk>/', api_views.PostDetailAPIView.as_view(), name='post_detail'),
    path('api/posts/<int:post_id>/like/', api_views.LikePostAPIView.as_view(), name='like_post'),
    path('api/posts/<int:post_id>/comments/', api_views.CommentCreateAPIView.as_view(), name='comment_create'),
    path('api/comments/<int:pk>/', api_views.CommentDetailAPIView.as_view(), name='comment_detail'),
    path('api/comments/<int:comment_id>/like/', api_views.LikeCommentAPIView.as_view(), name='like_comment'),
    path('api/comments/<int:comment_id>/replies/', api_views.CommentReplyCreateAPIView.as_view(), name='reply_create'),
    path('api/replies/<int:pk>/', api_views.CommentReplyDetailAPIView.as_view(), name='reply_detail'),
    path('api/replies/<int:reply_id>/like/', api_views.LikeReplyAPIView.as_view(), name='like_reply'),
]