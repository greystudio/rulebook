
   
# users/views.py

from django.shortcuts import redirect, render
from .models import User, Profile
from django.views.generic import CreateView
from .forms import LoginForm, RegisterForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.views.generic import FormView
from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from .decorators import logout_message_required, login_message_required
from django.contrib.auth import logout
from django.contrib import messages

# 메인 (로그인전)
def index(request):
    return render(request, 'main/main.html')

# 가이드 
def guideview(request):
    return render(request, 'main/guide.html')

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
        return redirect('/')
    
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


# 모임 프로필 보기
# class ProfileView(DetailView):
#     context_object_name = 'profile' # model로 지정해준 User모델에 대한 객체와 로그인한 사용자랑 명칭이 겹쳐버리기 때문에 이를 지정해줌.
#     model = Profile
#     template_name = 'users/profile.html'
    
#     # pk 왜 안되는지 모름.
#     def get_object(self):
#         return self.request

@login_message_required
def ProfileView(request):
    if request.method == 'GET':
        return render(request, 'users/profile.html')

    
    
# 모임 프로필 수정
def profile_update_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        # user_change_form = CustomUserChangeForm(request.POST, instance = request.user)
        profile_form = ProfileForm(request.POST, instance = request.user.profile)
        
        # if user_change_form.is_valid() and profile_form.is_valid():
        if profile_form.is_valid():
            # user = user_change_form.save()
            profile_form.save()
            return redirect('users:profile')
        return redirect('users:profile')


    else:
        # user_change_form = CustomUserChangeForm(instance = request.user)
        
        profile, create = Profile.objects.get_or_create(user = request.user)
        profile_form = ProfileForm(instance = profile)
        
        # return render(request, 'users/profile_update.html', {'user_change_form':user_change_form, 'profile_form':profile_form})
        return render(request, 'users/profile_update.html', {'profile_form':profile_form})
        