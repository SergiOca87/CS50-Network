# Generated by Django 3.1 on 2020-09-22 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_remove_post_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='following',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='user_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
