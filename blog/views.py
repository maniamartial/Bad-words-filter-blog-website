from email import message
from pyexpat.errors import messages
from .models import Comment
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.views.generic.edit import DeleteView, UpdateView
from matplotlib.style import context
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import User
# We want to create delete, update views
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


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

# Creating a new blog

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
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# allow people to comment


@login_required
def add_comment(request, pk):
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
    words = ["fuck", "Fuck off", "Piss off", "bugger off", "Bloody hell", "bastard", "Bollocks",
             "fuck", "shit", "cock", "titties", "boner", "muff", "pussy", "asshole", "cunt", "social", "status"]
    for sensitive_words in words:

        db_title = Post.objects.values('title')
        db_content = Post.objects.values('content')
       # print(db_title)
        # print(db_content)

        if sensitive_words in db_content:
            print("Error occurred")
        else:
            print("You are good")

    context = {sensitive_words: "sensitive_words"}
    return render(request, "blog/report.html", context)


''''@login_required
@staff_member_required
def reportCase(request):
    with open("badwords.txt") as f:
        sensitive_words = f.readlines()

        # print(sensitive_words)
    context = {sensitive_words: "sensitive_words"}
    return render(request, "blog/report.html", context)'''
