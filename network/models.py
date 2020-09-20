from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# Posts
class Post(models.Model):
    author = models.ForeignKey(User, related_name="author", on_delete=models.CASCADE)
    post_text = models.CharField(max_length=280)
    # timestamp = models.DateTimeField('Created On', auto_now_add=True)

# Likes

# Followers

# python manage.py makemigrations and then python manage.py