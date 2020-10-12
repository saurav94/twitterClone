from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import Tweet

class TweetListView(ListView):
    model = Tweet
    template_name = 'tweet/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'tweets'
    ordering = ['-date_posted']


class TweetDetailView(DetailView):
    model = Tweet


class TweetCreateView(CreateView):
    model = Tweet
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


