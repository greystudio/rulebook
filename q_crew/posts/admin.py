# posts/admin.py

from re import search
from django.contrib import admin
from .models import Posts

class PostsAdmin(admin.ModelAdmin):
    list_display=(
        'title',
        'writer',
        'version',
        'hits',
        'registered_date',
    )
    search_fields = ('title', 'content', 'writer__user_id',)
    
admin.site.register(Posts, PostsAdmin)