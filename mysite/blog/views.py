from django.shortcuts import render, get_object_or_404
from .models import Post
# pagination import
from django.core.paginator import Paginator


def post_list(request):
    posts = Post.published.all()
    #pagination with 4 per page
    paginator = Paginator(post_list, 4)
    page_number = request.Get.get('page', 1)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})