from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Tweet


def about(request):
    return render(request, 'tweet/about.html')


@api_view(['GET'])
@login_required
def like_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)

    like_data = {
        "id": pk,
        "like": False,
        "count": 0
    }
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
    else:
        like_data['like'] = True
        tweet.likes.add(request.user)

    like_data['count'] = tweet.get_likes_count()
    return Response(like_data)


@api_view(['GET'])
@login_required
def users_who_liked(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    users = tweet.likes.all()

    users_list = []
    for user in users:
        users_list.append(user.username)

    return Response(users_list)


class TweetListView(ListView):
    model = Tweet
    template_name = 'tweet/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'tweets'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_liked"] = {}

        for tweet in context['tweets']:
            if tweet.likes.filter(id=self.request.user.id).exists():
                context["is_liked"][tweet.id] = True
            # else:
            #     context["is_liked"][tweet.id] = False

        return context


class UserTweetListView(ListView):
    model = Tweet
    template_name = 'tweet/user_tweets.html'
    context_object_name = 'tweets'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Tweet.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_liked"] = {}

        for tweet in context['tweets']:
            if tweet.likes.filter(id=self.request.user.id).exists():
                context["is_liked"][tweet.id] = True
            # else:
            #     context["is_liked"][tweet.id] = False

        return context


class TweetDetailView(DetailView):
    model = Tweet

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["is_liked"] = False
        tweet = self.get_object()

        if tweet.likes.filter(id=self.request.user.id).exists():
            context["is_liked"] = True

        return context


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
