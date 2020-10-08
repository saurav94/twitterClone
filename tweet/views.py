from django.shortcuts import render
from django.http import HttpResponse

from .models import Tweet

def home(request):
    tweets = Tweet.objects.all()
    context = {
        'tweets': tweets
    }
    return render(request, 'tweet/home.html', context)