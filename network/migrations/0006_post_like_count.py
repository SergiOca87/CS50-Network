# Generated by Django 3.1 on 2021-01-04 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20210103_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]