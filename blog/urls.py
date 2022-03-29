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
]
'''<a class = "btn btn-outline-info mb-4" href = "?page=1" > First < /a >
<a class = "btn btn-outline-info mb-4" href = "?page = {{ page_obj.next_page_number }}" > Previous < /a >

{% endif % }
{ % for num in page_obj.paginator.page_range%}
{% if page_obj.number == num % }
<a class = "btn btn-info mb-4" href = "?page = {{ num }}" > {{num}} < /a >
{%elif num > page_obj.number | add: '-3' and num %}
<a class = "btn btn-outline-info mb-4" href = "?page = {{num }}" > {{num}} < /a >
{% endif%}
{% endfor % }
{ % if page_obj.has_next%}
<a class = "btn btn-outline-info mb-4" href = "?page={{page_obj.next_Page_number}}" > Next < /a >
<a class = "btn btn-outline-info mb-4" href = "?page = {{ page_obj.paginator.num_pages }}" > Last <
'''
