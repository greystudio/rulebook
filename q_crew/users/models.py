
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .choice import *


# BaseUserManager : user 생성할때 사용하는 helper 클래스
# extra_fields : 별도 조건을 만족하게 하고 싶은 경우 따로 명시해 받은 후 조건 확인하면 됨.
class UserManager(BaseUserManager):
    def create_user(self, user_id, password, name=None, member=None, manager=None, account=None):
        user = self.model(
            user_id = user_id,
            name = name,
            member = member,
            manager = manager,
            account = account
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password, name=None, member=None, manager=None, account=None):
        user = self.create_user(user_id, password, name, member, manager, account)
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.level = 0
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=17, verbose_name="아이디", unique=True)
    
    # media/image/profile 저장
    profile_img = models.ImageField(upload_to='profile', null=True, verbose_name='프로필사진')
    name = models.CharField(max_length=256, verbose_name="모임명", null=True, blank=True)
    member = models.CharField(max_length=256, verbose_name="소속회원", null=True, blank=True)
    manager = models.CharField(max_length=8, verbose_name="총무", null=True, blank=True)
    account = models.CharField(max_length=256, verbose_name="계좌번호", null=True, blank=True)
    
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
        

# # 프로필 모델
# class Profile(models.Model):
#     # CASCADE : ForeignKeyField가 바라보는 값이 삭제될 때 ForeignKeyField를 포함하는 모델 인스턴스(row)도 삭제
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     profile_img = models.ImageField(upload_to='profile/', null=True, blank=True, default ="{% static '/img/main_img (1).jpeg' %}", verbose_name='프로필사진')
    
#     def __str__(self):
#         return self.profile_img
    