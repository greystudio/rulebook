# Generated by Django 4.0.3 on 2022-03-25 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_rename_post_comment_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='comments',
            field=models.PositiveIntegerField(null=True, verbose_name='댓글수'),
        ),
    ]
