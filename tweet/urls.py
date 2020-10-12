from django.urls import path

from . import views
from .views import TweetListView, TweetDetailView, TweetCreateView

urlpatterns = [
    path('', TweetListView.as_view(), name='tweet-home'),
    path('tweet/<int:pk>', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweet/new/', TweetCreateView.as_view(), name='tweet-create')
]