# posts/admin.py

from re import search
from django.contrib import admin
from .models import Posts, Comment

class PostsAdmin(admin.ModelAdmin):
    list_display=(
        'title',
        'writer',
        'version',
        'hits',
        'registered_date',
    )
    search_fields = ('title', 'content', 'writer__user_id',)


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'posts', 
        'content',
        'writer',
        'created',
        'deleted',
    )
    search_fields = ('post__title', 'content', 'writer__user_id',)

    

admin.site.register(Posts, PostsAdmin)
admin.site.register(Comment, CommentAdmin)