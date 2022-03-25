# users/forms.py
# bootstrap 적용

from django.db import models
from django import forms
from django.contrib.auth.hashers import check_password
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model


# 로그인 폼
class LoginForm(forms.Form):
    user_id = forms.CharField(
        widget = forms.TextInput(
            attrs={'class':'form-control',}),
        error_messages = {'required' : '아이디를 입력해주세요.'},
        max_length = 17,
        label = 'Crew ID'
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs={'class' : 'form-control',}),
        error_messages = {'required' : '비밀번호를 입력해주세요.'},
        label = 'Password'
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
    
    # 필드 커스텀
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        self.fields['user_id'].label = 'ID'
        self.fields['user_id'].widget.attrs.update({'class' : 'form-control', 'autofocus' : False})
        
        self.fields['password1'].label = 'Password'
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password2'].label = 'Password Check'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
        })   
   
    class Meta:
        model = User
        fields = ['user_id', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.level='2'
        user.save()
        
        return user
    
    

        
        
# 모임 프로필 업데이트 폼 (2)    
class ProfileForm(forms.ModelForm):
    
    name = forms.CharField(label="모임명", widget=forms.TextInput(
    attrs={'class':'form-control', 'max-length':'50',}),
    )
    member = forms.CharField(label="회원", widget=forms.TextInput(
        attrs={'class':'form-control','max-length':'256',}),
    )
    manager = forms.CharField(label="총무", widget=forms.TextInput(
        attrs={'class':'form-control', 'max-length':'8',}),required=False
    )
    account = forms.CharField(label="회비 계좌", widget=forms.TextInput(
        attrs={'class':'form-control', 'max-length':'20',}),required=False
    )
    profile_img = forms.ImageField(label="프로필 사진", widget=forms.FileInput(
    attrs={'class':'form-control'}),required=False
    )
        
    class Meta:
        model = Profile
        fields = ['name', 'member', 'manager', 'account', 'profile_img']
