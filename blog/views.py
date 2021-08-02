from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Act like JSON-python library dictionaruy
posts = [
    {
        'author': 'Mania',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'August 27,2020'
    },
    {
        'author': 'Melany',
        'title': 'Blog Post 2',
        'content': 'Clinical Medicine',
        'date_posted': 'August 27,2021'
    },  {
        'author': 'Malesi',
        'title': 'Blog Post 3',
        'content': 'Relax dont have title',
        'date_posted': 'August 27,2021'
    }
]


def home(request):
    context = {
        'posts': posts
    }
    return render(request, "blog/home.html", context)


def aboout(request):
    return render(request, "blog/about.html", {'title': 'About'})
