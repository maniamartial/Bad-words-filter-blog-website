from django.urls import path
from .import views
from .views import PostCreateView, PostDeleteView, PostListView, PostDetailedView, PostUpdateView, UserPostListView
urlpatterns = [

    #path("", views.home, name="blog-home"),
    path("about/", views.aboout, name="blog-about"),
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>', PostDetailedView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('reportcase/', views.reportCase, name="reportcase"),
    path('index', views.index, name="index")

]
