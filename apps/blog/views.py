"""
Public-facing blog views. Only PUBLISHED posts are shown to visitors —
drafts are visible exclusively through the admin.
"""
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Post


def post_list_view(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).select_related("category", "author")
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {"posts": page_obj, "page_obj": page_obj, "is_paginated": page_obj.has_other_pages()})


def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    return render(request, "blog/detail.html", {"post": post})