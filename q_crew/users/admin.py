# users/admin.py

from profile import Profile
from pyexpat import model
from django.contrib import admin
from .models import User
from django.contrib.auth.models import Group

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'user_id', 
        'name',
        'member',
        'manager',
        'account',
        'level',
        'date_joined'
        )
    search_fields = ('user_id', 'name')

# # StackedInline : 유저 밑에 프로필 파트 붙이기. 
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     can_delete = False
    
# class CustomUserAdmin(UserAdmin):
#     inlines = (ProfileInline,)


admin.site.register(User, UserAdmin)
# 프로필
# admin.site.register(Profile)
admin.site.unregister(Group)  #Admin페이지의 GROUP삭제
# admin.site.register(User, CustomUserAdmin)
