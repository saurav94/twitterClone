from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Tweet(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tweet_pics', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.author.username + " " + self.text[:20]

    def get_likes_count(self):
        return self.likes.count()

    def is_liked_by_user(self, userId):
        return self.likes.filter(id=userId).exists()

    def get_absolute_url(self):
        return reverse('tweet-detail', kwargs={'pk': self.pk})


