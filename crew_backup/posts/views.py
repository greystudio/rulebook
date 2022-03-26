# posts/views.py

from email import message
from urllib import request
from django.views.generic import ListView
from .models import Posts, Comment
from users.models import User
from django.shortcuts import redirect
from .forms import PostsWriteForm
from users.decorators import login_message_required
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
from django.core.serializers.json import DjangoJSONEncoder

# # 페이퍼 목록
# @login_message_required
# class PostsListView(ListView):
#     model = Posts
#     paginate_by = 10    
#     template_name = 'posts/posts_list.html'  #DEFAULT : <app_label>/<model_name>_list.html
#     context_object_name = 'posts_list'         #DEFAULT : <model_name>_list
    
#     # 게시글의 리스트를 최근 작성순으로 표시
#     def get_queryset(self):
#         my_posts = Posts.objects.filter(writer=2)
#         all_posts = Posts.objects.all()
#         posts_list = Posts.objects.order_by('-id')
#         return my_posts
    
#     # 페이징 처리
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         paginator = context['paginator']
#         page_numbers_range = 5
#         max_index = len(paginator.page_range)
        
#         page = self.request.GET.get('page')
#         current_page = int(page) if page else 1
        
#         start_index = int((current_page-1) / page_numbers_range) * page_numbers_range
#         end_index = start_index + page_numbers_range
#         if end_index >=max_index:
#             end_index = max_index
            
#         page_range = paginator.page_range[start_index:end_index]
#         context['page_range'] = page_range
#         return context


# 페이퍼 목록
@login_message_required
def PostsListView(request):
    user = request.session['user_id']
    user_id = User.objects.get(user_id =  user)
    
    if(request.user.level == '0'):
        posts = Posts.objects.all().order_by('-id')
    else:    
        posts = Posts.objects.filter(writer = user_id).order_by('-id') # 내가 쓴글만
        
    posts_fixed = Posts.objects.filter(top_fixed=True).order_by('-registered_date')
    
    context={
        'posts' : posts,
        'posts_fixed' : posts_fixed
    }
    
    # 페이징 처리
    # paginator = Paginator(posts, 6) # 3개씩 잘라내기
    # page = request.GET.get('page') # 페이지 번호 알아오기
    # if page is None:
    #         page = 1
    # else:
    #         page = int(page)
    # firstPage= (page//10) * 10 +1   # 페이지 시작
    # LastPage= firstPage+10           # 페이지 끝
    # posts = paginator.get_page(page) # 페이지 번호 인자로 넘겨주기
    # count = [1,2,3]
    # if LastPage>posts.paginator.num_pages:
    #         LastPage=posts.paginator.num_pages+1
    # pageRange=range(firstPage,LastPage)
    
    return render(request, 'posts/posts_list.html', context)


    
# 페이퍼 상세 + 조회수 + 댓글
@login_message_required
def posts_detail_view(request, pk):
    posts = get_object_or_404(Posts, pk=pk)
    session_cookie = request.session['user_id']
    cookie_name = F'posts_hits:{session_cookie}'
    comment = Comment.objects.filter(posts=pk).order_by('created')
    comment_count = comment.exclude(deleted=True).count()
    #reply = comment.exclude(reply='0')
    
    if request.user == posts.writer:
        posts_auth = True
    else:
        posts_auth = False
    
    context={
        'posts' : posts,
        'posts_auth': posts_auth,
        'comments': comment,
        'comment_count': comment_count,
        #'replys': reply,
    }
    response = render(request, 'posts/posts_detail.html', context)
    
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(pk) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{pk}', expires=None)
            posts.hits += 1
            posts.save()
            return response
    else:
        response.set_cookie(cookie_name, pk, expires=None)
        posts.hits += 1
        posts.save()
        return response
    return render(request, 'posts/posts_detail.html', context)


# 페이퍼 작성
@login_message_required
def posts_write_view(request):
    if request.method == "POST":
        form = PostsWriteForm(request.POST)
        user = request.session['user_id']
        user_id = User.objects.get(user_id = user)

        if form.is_valid():
            posts = form.save(commit = False)
            posts.writer = user_id
            posts.save()
            return redirect('posts:posts_list')
    else:
        form = PostsWriteForm()
    return render(request, "posts/posts_write.html", {'form': form})
        

# 페이퍼 수정
@login_message_required
def posts_edit_view(request, pk):
    posts  = Posts.objects.get(id=pk)
    
    if request.method == "POST":
        if(posts.writer == request.user or request.user.level == '0'):
            #instance : 기존 해당 게시글 정보 가져오기
            form = PostsWriteForm(request.POST, instance=posts)
            if form.is_valid():
                posts = form.save(commit=True)
                posts.save()
                messages.success(request, "Crew Paper가 수정되었습니다.")
                return redirect('/posts/'+str(pk))
            
    else:
        posts = Posts.objects.get(id=pk)
        if (posts.writer == request.user or request.user.level == '0'):
            form = PostsWriteForm(instance=posts)
            context={
                'form' : form,
                'edit' : '페이퍼 수정',
            }
            return render(request, "posts/posts_write.html", context)
        else:
            messages.error(request, "우리 모임의 paper가 아닙니다.")
            return redirect('/posts/'+str(pk))
        
          
# 페이퍼 삭제       
@login_message_required
def posts_delete_view(request, pk):
    posts = Posts.objects.get(id=pk)
    if posts.writer == request.user or request.user.level == '0':
        posts.delete()
        messages.success(request, "crew paper가 삭제되었습니다.")
        return redirect('/posts/')
    else:
        messages.error(request, "우리 모임의 paper가 아닙니다.")
        return redirect('/posts/'+str(pk))
    
    
    
# 댓글 쓰기
@login_message_required
def comment_write_view(request, pk):
    posts = get_object_or_404(Posts, id=pk)
    writer = request.POST.get('writer')
    content = request.POST.get('content')    
    #reply = request.POST.get('reply')
    if content:
        comment = Comment.objects.create(posts=posts, content=content, writer=request.user)
        #comment = Comment.objects.create(post=posts, content=content, writer=request.user, reply=reply)
        comment_count = Comment.objects.filter(posts=pk).exclude(deleted=True).count()
        posts.comments = comment_count
        posts.save()
        data = {
            'writer': writer,
            'content': content,
            'created': '방금 전',
            'comment_count': comment_count,
            'comment_id': comment.id
        }
        if request.user == posts.writer:
            data['self_comment'] = '(글쓴이)'
        
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")
    

# 댓글 삭제
@login_message_required
def comment_delete_view(request, pk):
    posts = get_object_or_404(Posts, id=pk)
    comment_id = request.POST.get('comment_id')
    target_comment = Comment.objects.get(pk = comment_id)

    if request.user == target_comment.writer or request.user.level == '1' or request.user.level == '0':
        target_comment.deleted = True
        target_comment.save()
        comment_count = Comment.objects.filter(posts=pk).exclude(deleted=True).count()
        posts.save()
        data = {
            'comment_id': comment_id,
            'comment_count': comment_count
        }
        return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type = "application/json")
