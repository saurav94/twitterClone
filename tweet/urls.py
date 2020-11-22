from django.urls import path
from . import views
# from .views import TweetListView, UserTweetListView, TweetDetailView, TweetCreateView, TweetUpdateView, TweetDeleteView, about, like_tweet

urlpatterns = [
    path('', views.about, name='tweet-about'),
    path('home/', views.TweetListView.as_view(), name='tweet-home'),
    path('user/<str:username>/', views.UserTweetListView.as_view(), name='user-tweets'),
    path('tweet/<int:pk>/', views.TweetDetailView.as_view(), name='tweet-detail'),
    path('tweet/<int:pk>/like/', views.like_tweet),
    path('tweet/<int:pk>/like/users/', views.liked_by),
    path('tweet/<int:pk>/comment/', views.create_comment, name='comment-create'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='comment-delete'),
    path('tweet/new/', views.TweetCreateView.as_view(), name='tweet-create'),
    path('tweet/<int:pk>/update/', views.TweetUpdateView.as_view(), name='tweet-update'),
    path('tweet/<int:pk>/delete/', views.TweetDeleteView.as_view(), name='tweet-delete')
]
