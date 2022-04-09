from operator import contains
import re
from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError

from django.conf import settings

'''with open("badwords.txt") as f:
    CENSORED_WORDS = f.readlines()'''

CENSORED_WORDS = ['Fuck off', 'Piss off', "fuck", "penisfucker", "porn", "pussy", "pono", "ponography",
                  "orgasm", "cocksuck", "cock", "damn", "erection", "douch", "fuckhole", "asshole",
                  "blcak cock", "arse", "anal", "assfucker", "bloodyhell", "fuckass", "gook", "blood hel", "boong", "coon", "dick", "nigga", "sex", "bitch", "son of bitch", "suck", "viagra", "nigro", ]


def validate_comment_text(text):
    words = set(re.sub("[^\w]", " ",  text).split())
    for censored_word in CENSORED_WORDS:
        # print(words)
        # print(censored_word)
      #  if any(str(censored_word in words)):
        if censored_word in words:
            print(censored_word)
            raise ValidationError(
                f"{censored_word} Is a bad word, try using good language")


class PostManager(models.Manager):
    def like_toggle(self, user, post_obj):
        if user in post_obj.liked.all():
            is_liked = False
            post_obj.liked.remove(user)
        else:
            is_liked = True
            post_obj.liked.add(user)
        return is_liked


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=300, validators=[
                               validate_comment_text])
    liked = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    objects = PostManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


# If a person wants to comment
class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.author
