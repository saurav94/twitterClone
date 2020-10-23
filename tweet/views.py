from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Tweet


def about(request):
    return render(request, 'tweet/about.html')


class TweetListView(ListView):
    model = Tweet
    template_name = 'tweet/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tweets'
    ordering = ['-date_posted']
    paginate_by = 5


class UserTweetListView(ListView):
    model = Tweet
    template_name = 'tweet/user_tweets.html'
    context_object_name = 'tweets'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Tweet.objects.filter(author=user).order_by('-date_posted')


class TweetDetailView(DetailView):
    model = Tweet


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ['text', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TweetUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tweet
    fields = ['text', 'image']

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.author


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    success_url = '/'

    def test_func(self):
        tweet = self.get_object()
        return self.request.user == tweet.author
