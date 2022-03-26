from email.policy import default
from re import T
from turtle import Turtle
from django.conf import settings
from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .level import *
from django.db.models.signals import post_save

# BaseUserManager : user 생성할때 사용하는 helper 클래스
# extra_fields : 별도 조건을 만족하게 하고 싶은 경우 따로 명시해 받은 후 조건 확인하면 됨.
class UserManager(BaseUserManager):
    
    # 일반 유저 생성
    def create_user(self, user_id, password, **extra_fields):
        
        user = self.model(
            user_id = user_id
        )
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 슈퍼 유저 생성
    def create_superuser(self, user_id, password):
        
        user = self.create_user(user_id, password)
        
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0
        
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=17, verbose_name="아이디", unique=True)
    level = models.CharField(choices=LEVEL_CHOICES, max_length=18, verbose_name="등급", default=2)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='가입일', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    # user model에서 사용할 고유 식별자
    USERNAME_FIELD = 'user_id'
    
    def __str__(self):
        return self.user_id

    # class Meta:
    #     db_table = "회원목록"
    #     verbose_name = "사용자"
    #     verbose_name_plural = "사용자"
        

# 프로필 모델
class Profile(models.Model):
    # CASCADE : ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField를 포함하는 모델 인스턴스(row)도 삭제
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name="모임명", null=True)
    member = models.CharField(max_length=256, verbose_name="소속회원", blank=True)
    manager = models.CharField(max_length=8, verbose_name="총무", blank=True)
    account = models.CharField(max_length=20, verbose_name="계좌번호", blank=True)
    profile_img = models.ImageField(default='default.jpg', upload_to='profile', blank=True)
    
    def __str__(self):
        return f'{self.user.user_id} Profile'
    

def on_post_save_for_user(sender, **kwargs):
    if kwargs['created']:
        user = kwargs['instance']
        Profile.objects.create(user=user)

# User 회원 가입 시 Profile 생성하기
post_save.connect(on_post_save_for_user, sender=settings.AUTH_USER_MODEL)
