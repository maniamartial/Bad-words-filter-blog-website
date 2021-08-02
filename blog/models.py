from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


'''
class Product(models.Model):
    image=models.ImageField()
    title=models.CharField(max_length=200)
    description=models.CharField(max_length=500)
    properties=models.CharField(max_length=1000)
    available=models.BooleanField()
    available_sizes=models.IntegerField()
'''
