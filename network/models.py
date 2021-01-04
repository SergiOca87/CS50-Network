from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now


class User(AbstractUser):
    followers = models.ManyToManyField(
        'User', default=None, null=True, blank=True, related_name='user_followers')
    following = models.ManyToManyField(
        'User', default=None, null=True, blank=True, related_name='user_following')
    likes = models.ManyToManyField(
        'Post', default=None, null=True, blank=True, related_name='likes')


# Posts
class Post(models.Model):
    published_date = models.DateTimeField(default=now, editable=False)
    author = models.ForeignKey(
        User, related_name="author", on_delete=models.CASCADE)
    post_text = models.CharField(
        max_length=280, default=None, null=True, blank=True)
    # add post likes, a number that is incremented?
    like_count = models.IntegerField(default=0, null=True, blank=True)

# Likes


# python manage.py makemigrations and then python manage.py
