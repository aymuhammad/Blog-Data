# send mail
from django.core.mail import send_mail
# pagination import
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
# class-based view
from django.views.generic import ListView
from django.views.decorators.http import require_POST

from .forms import EmailPostForm, CommentForm
from .models import Post, Comment

def post_list(request):
    posts = Post.published.all()
    #pagination with 4 per page
    paginator = Paginator(post_list, 4)
    page_number = request.Get.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number isn't an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED, slug=post, publish__year=year, publish__month=month, publish__day=name)
    return render(request, 'blog/post/detail.html', {'post': post})


# class based-view 
class PostListView(ListView):

    # alternative post list view
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'


# forms
def post_share(request, post_id):
    # retrive post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method =='POST':
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}" f"{cd['name']}\'s commnets:' {cd['comments']}"
            send_mail(subject, message, 'auwalyah@gmail.com', [cd['to']])
            sent= True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create a comment object without saving it to the database
        comment = form.save(commit=False)
        # assign comment to the post
        comment.post = post
        # save comment to the db
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})