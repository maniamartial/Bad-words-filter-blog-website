from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views.generic.edit import DeleteView, UpdateView
from .models import Post
from django.contrib.auth.models import User
# We want to create delete, update views
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


# Create your views here.

# Act like JSON-python library dictionaruy


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, "blog/home.html", context)


# This allows arrangements of staffs lets say sorting of staffs in certain recommended order
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    # if  want to arrange the blogs from olded put a minus before teh dates


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailedView(DetailView):
    model = Post

# CReating a new blog

# We cannot use decoraters with classes


class PostCreateView(LoginRequiredMixin,  CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/ '

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def aboout(request):
    return render(request, "blog/about.html", {'title': 'About'})
