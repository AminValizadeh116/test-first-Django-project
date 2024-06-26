from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import logout

from .models import *
from .forms import *


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {'posts': posts}
    return render(request, 'post/post_list.html', context)


def post_detail(request, pk):
    post = Post.published.get(pk=pk)
    comment = post.comments.all()
    form = CommentForm()
    context = {'post': post, 'comment': comment, 'form': form}
    return render(request, 'post/post_detail.html', context)


def comment_view(request, post_pk):
    if request.method == 'POST':
        post = Post.published.get(pk=post_pk)
        form = CommentForm(request.POST)
        comment = None
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
        context = {'post': post, 'comment': comment, 'form': form}
        return render(request, 'post/comment.html', context)


def log_out(request):
    logout(request)
    return render(request, 'registration/logged_out.html')


def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(Paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {'posts': posts, 'user': user}
    return render(request, 'post/profile.html', context)


def delete_post(request, post_id):
    post = Post.published.get(id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('post:profile')
    else:
        context = {'post': post}
    return render(request, 'post/delete_post.html', context)


def create_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post, title=post.title + ' img1')
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post, title=post.title + ' img2')
            return redirect('post:profile')
    else:
        form = CreatePostForm()
    context = {'form': form}
    return render(request, 'post/create_post.html', context)


def edit_post(request, post_id):
    post = Post.published.get(id=post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post.author = request.user
            post = form.save(commit=False)
            if form.cleaned_data['image1']:
                Image.objects.create(post=post, image_file=form.cleaned_data['image1'])
            if form.cleaned_data['image2']:
                Image.objects.create(post=post, image_file=form.cleaned_data['image2'])
            return redirect('post:profile')
    else:
        form = CreatePostForm(instance=post)
    context = {'form': form, 'post': post}
    return render(request, 'post/create_post.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            form.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def create_account(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        account_form = AccountForm(request.POST, files=request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            account_form.save()
            user_form.save()
    else:
        user_form = UserForm(instance=request.user)
        account_form = AccountForm(instance=request.user.account)
    context = {'user_form': user_form, 'account_form': account_form}
    return render(request, 'post/create_account.html', context)


def search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.filter(title__icontains=query)
    context = {'query': query, 'results': results}
    return render(request, ''. context)
