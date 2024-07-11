from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import viewsets

from posts.forms import PostForm
from .models import CommentLike, CommentReply, Post, Like, Comment, ReplyLike
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST





def home(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('posts:home')
    else:
        form = PostForm()
    
    posts = Post.objects.all().order_by('-created_at')

    context={
        'posts': posts,
        'form': form,
    }
    return render(request, 'index.html', context)


@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('posts:home')

@require_POST
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment_text = request.POST.get('comment')
    if comment_text:
        Comment.objects.create(user=request.user, post=post, text=comment_text)
    return redirect('posts:home')


@login_required
@require_POST
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.text = request.POST.get('text')
        comment.save()
    return redirect('posts:home')

@login_required
@require_POST
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
    return redirect('posts:home')

@login_required
@require_POST
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
    return redirect('posts:home')

@login_required
@require_POST
def reply_to_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    reply_text = request.POST.get('reply_text')
    if reply_text:
        CommentReply.objects.create(user=request.user, comment=comment, text=reply_text)
    return redirect('posts:home')

@login_required
@require_POST
def edit_reply(request, reply_id):
    reply = get_object_or_404(CommentReply, id=reply_id)
    if reply.user == request.user:
        reply.text = request.POST.get('text')
        reply.save()
    return redirect('posts:home')

@login_required
@require_POST
def delete_reply(request, reply_id):
    reply = get_object_or_404(CommentReply, id=reply_id)
    if reply.user == request.user:
        reply.delete()
    return redirect('posts:home')

@login_required
@require_POST
def like_reply(request, reply_id):
    reply = get_object_or_404(CommentReply, id=reply_id)
    like, created = ReplyLike.objects.get_or_create(user=request.user, reply=reply)
    if not created:
        like.delete()
    return redirect('posts:home')