from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Tweet(models.Model):
    text = models.TextField()
    # image = models.ImageField(upload_to='tweet_pics')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

