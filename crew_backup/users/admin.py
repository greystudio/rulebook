# users/admin.py

from django.contrib import admin
from .models import User,Profile
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 
        'level',
        'date_joined'
        )

# StackedInline : 유저 밑에 프로필 파트 붙이기. 
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)  #Admin페이지의 GROUP삭제

# 프로필
# admin.site.register(Profile)
# admin.site.register(User, CustomUserAdmin)
