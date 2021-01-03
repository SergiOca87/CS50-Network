from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
import json
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.order_by('-published_date').all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_likes = list(request.user.likes.all())
    # .order_by("-timestamp").all()
    # posts = posts.order_by("-timestamp").all()
    print(user_likes)
    return render(request, "network/index.html", {
        "posts": posts,
        'page_obj': page_obj,
        "user_likes": user_likes
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
    following = author.following.all()
    followers = author.followers.all()
    is_following = True
    posts = Post.objects.filter(
        author=author.id).order_by('-published_date').all()

    if current_user in list(author.followers.all()):
        is_following = False

    is_author = False
    if author.id == current_user.id:
        is_author = True

    if request.method == "POST":
        if 'follow' in request.POST and request.POST['follow']:
            current_user.following.add(author)
            author.followers.add(current_user)
            return HttpResponseRedirect(reverse('following'))
        elif 'unfollow' in request.POST and request.POST['unfollow']:
            current_user.following.remove(author)
            author.followers.remove(current_user)
            return HttpResponseRedirect(reverse("index"))

    return render(request, "network/author.html", {
        "author": author,
        "is_author": is_author,
        "following": following,
        "followers": followers,
        "is_following": is_following,
        "posts": posts
    })


def new_post(request):
    if request.method == "POST":
        author = request.user
        post_text = request.POST["post_text"]
        # timestamp = datetime.now()

        f = Post(author=author, post_text=post_text)
        f.save()

        # Instead return the all posts url, once defined
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "network/new_post.html")


def likes(request, post_id):
    current_user = request.user
    post = Post.objects.get(pk=post_id)
    print(current_user.likes.all())

    if request.method == "PUT":
        data = json.loads(request.body)

        print('user is', current_user)
        if data.get('like') == 'true':
            current_user.likes.add(post)
        else:
            current_user.likes.remove(post)

    return HttpResponse(status=204)

# get, to show the form with the post content (retrieve post by id)
# post, to modify existing post in the database


def edit_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        post_text = request.POST["post_text"]
        # timestamp = datetime.now()
        post.post_text = post_text
        post.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        post = Post.objects.get(pk=post_id)
        return render(request, "network/edit_post.html", {
            "post": post
        })


def following(request):
    following = request.user.following.all()
    posts = list(Post.objects.filter(author__in=[user for user in following]))
    print(posts)
    return render(request, "network/following.html", {
        "posts": posts
    })
