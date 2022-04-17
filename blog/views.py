import requests
from email import message
from pyexpat.errors import messages
from .models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views.generic.edit import DeleteView, UpdateView
from matplotlib.style import context
from django.contrib import messages
from django.db.models import Q
from .models import Post
from django.contrib.auth.models import User
# We want to create delete, update views
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
#from profanity_filter import ProfanityFilter


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
    # if want to arrange the blogs from older put a minus before the dates
    ordering = ['-date_posted']
    paginate_by = 5

# implementing the search bar
    def get_queryset(self):
        try:
            keyword = self.request.GET['q']
        except:
            keyword = ''
        if (keyword != ''):
            object_list = self.model.objects.filter(
                Q(content__icontains=keyword) | Q(title__icontains=keyword))
        else:
            object_list = self.model.objects.all()
        return object_list


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


# Creating a new blog
# We cannot use decoraters with classes
class PostCreateView(LoginRequiredMixin,  CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# if author wants to update the posts
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


# incase the author wants to delete their post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# allow people to comment
@login_required
def add_comment(request, pk):
    # the comment to be on the specific page opened.
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(id=request.POST.get('user_id'))
        text = request.POST.get('text')
        Comment(author=user, post=post, text=text).save()
        messages.success(request, "Your comment has been added successfully.")
    else:
        return redirect('post_detail', pk=pk)
    return redirect('post_detail', pk=pk)


def aboout(request):
    return render(request, "blog/about.html", {'title': 'About'})


@login_required
@staff_member_required
def reportCase(request):
    words = ["Umbwa", "Fuck off", "Piss off", "bugger off", "Bloody hell", "bastard", "Bollocks",
             "fuck", "shit", "cock", "titties", "boner", "muff", "pussy", "asshole", "cunt", "social", "status"]
    for sensitive_words in words:

        db_title = Post.objects.values('title')
        db_content = Post.objects.values('content')

        #print(predict(['fuck you']))
# Word(uncensored='fuck', censored='****', original_profane_word='fuck')

        if sensitive_words in db_content:
            print("Error occurred")
        else:
            print("You are good")

    context = {sensitive_words: "sensitive_words"}
    return render(request, "blog/report.html", context)


def index(request):
    r = requests.get('https://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<pre>' + r.text + '</pre>')
