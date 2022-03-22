# users/forms.py

from django.db import models
from django import forms
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, SetPasswordForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from .choice import *


# 로그인 폼
class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget = forms.TextInput(
            attrs={'class':'form-control',}),
        error_messages = {'required' : '아이디를 입력해주세요.'},
        max_length = 17,
        label = '아이디'
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'class' : 'form-control',}),
        error_messages = {'required' : '비밀번호를 입력해주세요.'},
        label = '비밀번호'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        
        if user_id and password:
            try:
                user = User.objects.get(user_id = user_id)
            except User.DoesNotExist:
                self.add_error('user_id', '아이디가 존재하지 않습니다.')
                return
            if not check_password(password, user.password):
                self.add_error('password', '비밀번호가 틀렸습니다.')
                

# 회원가입 폼
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['user_id'].label = '아이디'
        self.fields['user_id'].widget.attrs.update({'class' : 'form-control', 'autofocus' : False})
        
        self.fields['password1'].label = '비밀번호'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['name'].label = '모임명'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
        })      
        self.fields['member'].label = '소속회원'
        self.fields['member'].widget.attrs.update({
            'class': 'form-control',
        })      
        self.fields['manager'].label = '총무'
        self.fields['manager'].widget.attrs.update({
            'class': 'form-control',
        })      
        self.fields['account'].label = '계좌정보'
        self.fields['account'].widget.attrs.update({
            'class': 'form-control',
        })      
        
    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2', 'name', 'member', 'manager', 'account']
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.level='2'
        user.save()
        
        return user
    
    
# 모임 정보 수정 폼
class CustomUserChangeForm(UserChangeForm):
    
    # UserChangeForm에서는 password를 수정할 수 없다.
    # 하지만 이렇게 None 값으로 지정해주지 않으면 password를 변경할 수 없다는 설명이 화면에 표현된다.
    password = None
    
    name = forms.CharField(label="모임명", widget=forms.TextInput(
        attrs={'class':'form-control', 'max-length':'256',}),
    )
    member = forms.CharField(label="소속회원", widget=forms.TextInput(
        attrs={'class':'form-control','max-length':'256',}),
    )
    manager = forms.CharField(label="총무", widget=forms.TextInput(
        attrs={'class':'form-control', 'max-length':'8',}),
    )
    account = forms.CharField(label="회비 계좌", widget=forms.TextInput(
        attrs={'class':'form-control', 'max-length':'256',}),
    )
    profile_img= forms.ImageField()


# profile_img = models.ImageField(upload_to='profile', null=True, verbose_name='프로필사진')    
    
    class Meta:
        model = get_user_model()
        fields = ['name', 'member', 'manager', 'account']
    
# class ProfileForm(models.Model):
#     profile_img = forms.ImageField(label="이미지", required=False)
    
#     class Meta:
#         model = Profile
#         fields = ['profile_img']