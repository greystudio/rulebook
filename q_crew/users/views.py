# users/views.py

from django.shortcuts import redirect, render
from .models import User
from django.views.generic import CreateView
from .forms import LoginForm, RegisterForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from .decorators import logout_message_required, login_message_required
from django.contrib.auth import logout
from django.contrib import messages

# 메인 (로그인전)
def index(request):
    return render(request, 'main/main.html')

# 메인 (로그인후)

# 회원가입
class RegisterView(CreateView):
    model = User
    template_name = 'users/register.html'
    form_class = RegisterForm
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        # return redirect(self.get_success_url())
        return redirect('/users/login')
    
    # def get_success_url(self):
    #     messages.success(self.request, '회원가입 성공')
    #     return redirect('/users/login')
    
    
    
# 로그인
@method_decorator(logout_message_required, name='dispatch')
class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = '/'
    
    def form_valid(self, form):
        user_id = form.cleaned_data.get("user_id")
        password = form.cleaned_data.get("password")
        
        user = authenticate(self.request, username=user_id, password = password)
        if user is not None:
            self.request.session['user_id'] = user_id
            login(self.request, user)
            
        return super().form_valid(form)

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('/')

# 모임 정보 보기
@login_message_required
def profile_view(request):
    if request.method == 'GET':
        return render(request, 'users/profile.html')

    
# 모임 정보 수정
@login_message_required
def profile_update_view(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance = request.user)

        if user_change_form.is_valid():
            user_change_form.save()
            messages.success(request, '회원정보가 수정되었습니다.')
            return render(request, 'users/profile.html')
    else:
        user_change_form = CustomUserChangeForm(instance = request.user)

        return render(request, 'users/profile_update.html', {'user_change_form':user_change_form})