# Generated by Django 5.0.6 on 2024-07-10 13:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_alter_comment_user_alter_like_user_alter_post_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='content_text',
            new_name='caption',
        ),
        migrations.RemoveField(
            model_name='post',
            name='content_audio',
        ),
        migrations.RemoveField(
            model_name='post',
            name='content_image',
        ),
        migrations.RemoveField(
            model_name='post',
            name='content_video',
        ),
        migrations.AddField(
            model_name='post',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='media/'),
        ),
        migrations.AlterField(
            model_name='post',
            name='feeling_status',
            field=models.CharField(blank=True, choices=[('happy', 'Happy'), ('sad', 'Sad'), ('excited', 'Excited'), ('angry', 'Angry')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
