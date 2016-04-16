import textwrap

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.utils import timezone

from abaoblog.models import Post
from abaoblog.forms import PostForm, RegistrationForm
from abaoblog.configure import post_conf
from abaoblog.common import smart_truncate

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from abaoblog.api.serializers import PostSerializers
from django.views.decorators.csrf import csrf_exempt

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    post_length = post_conf().post_list_text_length
    for post in posts:
        # simple solution
        # post.text = (post.text[:post_length]+'...') if len(post.text)>post_length else post.text

        # smart truncate
        post.text = smart_truncate(post.text, post_length, '...')
    is_login = request.user.is_authenticated()
    return render(request, 'abaoblog/post_list.html', {'posts': posts, 'is_login': is_login})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'abaoblog/post_detail.html', {'post': post})


def post_new(request):
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/error')

    if request.user.is_authenticated():
        form = PostForm()
        return render(request, 'abaoblog/post_new.html', {'form': form})
    else:
        return HttpResponseRedirect('/login')

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            register_user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password_1'],
                email=form.cleaned_data['email']
            )
            username = form.cleaned_data['username']
            password = form.cleaned_data['password_1']

            login_user = authenticate(username=username, password=password)
            if login_user is not None:
                if login_user.is_active:
                    login(request, login_user)
                    return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'abaoblog/user_register.html', {'form': form})


def user_login(request):
    state = "Please log in below..."
    username = password = ''
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."
        else:
            state = "Your username and/or password were incorrect."
        return render_to_response('abaoblog/login_success.html', {'state': state, 'username': username})
    else:
        return render(request, 'abaoblog/user_login.html', {})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


