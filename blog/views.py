from django.shortcuts import render, get_object_or_404, redirect
from blog.forms import CommentForm, PostForm
from blog.models import Post
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie 

import logging

logger = logging.getLogger(__name__)

def index(request):
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
    logger.debug("Got %d posts", len(posts))
    return render(request, 'blog/index.html', {"posts": posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                logger.info("Created comment on Post %d for user %s", post.pk, request.user)
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    return render(request, 'blog/post-detail.html', {'post': post, 'comment_form': comment_form})

def post_create(request):
    if request.user.is_active:
        if request.method == "POST":
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.slug = slugify(post.title)
                post.author = request.user
                post.save()
                logger.info("Created post %d for user %s", post.pk, request.user)
                return redirect(reverse('main_page'))
        else:
            post_form = PostForm()
    else:
        post_form = None
    return render(request, 'blog/post-create.html', {'post_form': post_form})

