from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Tweet, Comment
from users.models import Profile


def about(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)

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
def liked_by(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    users = tweet.likes.all()

    users_list = []
    for user in users:
        users_list.append(user.username)

    return Response(users_list)

# @api_view(['POST'])


@login_required
def create_comment(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)

    if request.method == "POST":
        body = request.POST.get('body')
        print("comment body: ", body)
        comment = Comment.objects.create(
            tweet=tweet, user=request.user, body=body)
        comment.save()
        messages.success(request, f'Comment added sucessfully')

    return redirect(tweet.get_absolute_url())


@api_view(['GET'])
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    response_msg = "Success"
    comments_count = comment.tweet.comments.count()
    tweetId = comment.tweet.id

    if comment.user == request.user:
        comment.delete()
        comments_count = comments_count - 1
    else:
        response_msg = "Unauthorized"

    return Response({"message": response_msg, "comments_on_tweet": comments_count, "tweet_id": tweetId})


@api_view(['GET'])
@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)

    follow_data = {
        "followers": 0,
        "following": 0,
        "followed": ''
    }

    if user.profile.is_followed_by_user(request.user.profile.id):
        user.profile.followers.remove(request.user.profile)
    else:
        user.profile.followers.add(request.user.profile)

    follow_data["followers"] = user.profile.get_followers_count()
    follow_data["following"] = user.profile.get_following_count()
    follow_data["followed"] = user.profile.is_followed_by_user(
        request.user.profile.id)

    return Response(follow_data)


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
        context['profile'] = get_object_or_404(
            User, username=self.kwargs.get('username'))
        context["is_liked"] = {}
        context['is_followed'] = context['profile'].profile.is_followed_by_user(
            self.request.user.profile.id)

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

        print(context['object'].comments)
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
