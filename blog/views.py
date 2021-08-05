from django.shortcuts import render
from django.http import HttpResponse
from .models import Post

# Create your views here.

# Act like JSON-python library dictionaruy


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, "blog/home.html", context)


def aboout(request):
    return render(request, "blog/about.html", {'title': 'About'})
