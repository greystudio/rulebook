# posts/urls.py

from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'posts'

urlpatterns = [
    # path('', views.PostsListView.as_view(), name='posts_list'),
    path('', views.PostsListView, name='posts_list'),
    path('<int:pk>/', views.posts_detail_view, name='posts_detail'),
    path('write/', views.posts_write_view, name='posts_write'),
    path('<int:pk>/edit/', views.posts_edit_view, name='posts_edit'),
    path('<int:pk>/delete/', views.posts_delete_view, name='posts_delete'),
    path('<int:pk>/comment/write/', views.comment_write_view, name='comment_write'),
    path('<int:pk>/comment/delete/', views.comment_delete_view, name='comment_delete'),
]

