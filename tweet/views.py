from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Tweet

class TweetListView(ListView):
    model = Tweet
    template_name = 'tweet/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'tweets'
    ordering = ['-date_posted']


class TweetDetailView(DetailView):
    model = Tweet


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ['text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TweetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    fields = ['text']

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.author


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    success_url = '/'

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.author

