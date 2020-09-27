from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.core.paginator import Paginator

from .models import User, Post

def index(request):
    posts = Post.objects.order_by('-published_date').all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # .order_by("-timestamp").all()
    # posts = posts.order_by("-timestamp").all()
    return render(request, "network/index.html", {
        "posts": posts,
        'page_obj': page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def author(request, author_id):
    author = User.objects.get(id=author_id)
    current_user = request.user
    following = author.following.all().count
    followers = author.followers.all().count
    posts = Post.objects.filter(author=author.id).order_by('-published_date').all()
    
    is_author = False
    if author.id == current_user.id:
        is_author = True

    if request.method == "POST":
        if 'follow' in request.POST and request.POST['follow']:
            current_user.following.add(author)
            author.followers.add(current_user)
            return HttpResponseRedirect(reverse('following'))

   
    
    return render(request, "network/author.html", {
        "author": author,
        "is_author": is_author,
        "following": following,
        "followers": followers,
        "posts": posts
    })

def new_post(request):
    if request.method == "POST":
        author = request.user
        post_text = request.POST["post_text"]
        # timestamp = datetime.now()

        f = Post(author = author, post_text = post_text)
        f.save()

        # Instead return the all posts url, once defined
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "network/new_post.html")

def following(request):
    following = request.user.following.all()
    posts = list(Post.objects.filter(author__in=[user for user in following]))
    print(posts)
    return render(request, "network/following.html", {
        "posts": posts
    })