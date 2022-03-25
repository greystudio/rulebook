# posts/forms.py

from cProfile import label
from email import message
from multiprocessing import context
from tkinter import Label
from django import forms
from django.shortcuts import redirect, render
from .models import Posts
from users.decorators import login_message_required
from django.contrib import messages


# 글 작성
class PostsWriteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostsWriteForm, self).__init__(*args, **kwargs)
 
        self.fields['title'].label='Title'
        self.fields['title'].widget.attrs.update({
            'placeholder' : '제목을 입력해주세요.',
            'class' : 'form-control',
            'autofocus' : 'True',
        })
    
        
        self.fields['version'].label = 'Version'
        self.fields['version'].widget.attrs.update({
            'placeholder' : '버전을 입력해주세요.',
            'class': 'form-control',
        })  
        
        self.fields['content'].label = 'Crew Paper'
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
        }) 
        
      
    class Meta:
        model = Posts
        fields = ['title', 'version',  'content', 'top_fixed']
        
        
        

