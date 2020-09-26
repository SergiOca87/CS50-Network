from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    followers = models.ManyToManyField('User', default=None, null=True, blank=True, related_name='user_followers')
    following = models.ManyToManyField('User', default=None, null=True, blank=True, related_name='user_following')


# Posts
class Post(models.Model):
    published_date = models.DateTimeField(default=now, editable=False)
    author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
    post_text = models.CharField(max_length=280, default=None, null=True, blank=True)
    # published_date = models.DateTimeField(default=now, editable=False)
    # timestamp = models.DateTimeField('Created On', auto_now_add=True)

# Likes

# Followers

# python manage.py makemigrations and then python manage.py