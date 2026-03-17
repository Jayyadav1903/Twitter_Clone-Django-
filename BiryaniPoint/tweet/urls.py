
from django.urls import path
from . import views

urlpatterns = [
   path('', views.tweet_list, name='tweet_list'),
   path('create/', views.tweet_create, name='tweet_create'),
   
   path('edit/<int:tweet_id>/', views.tweet_edit, name='tweet_edit'),
   
   path('delete/<int:tweet_id>/', views.tweet_delete, name='tweet_delete'), 
   
   path('register/', views.register,
   name='register'),
   
   path('search/', views.search, name='search'),
 
 #New features
 
   path('like/<int:tweet_id>/', views.toggle_like, name="toggle_like"),
   
   path('reply/<int:tweet_id>/', views.reply_tweet, name="reply_tweet"),
   
   
   path('follow/<int:user_id>/', views.follow_user, name="follow_user"),
   
   path('unfollow/<int:user_id>/', views.unfollow_user, name="unfollow_user"),
   
   path("retweet/<int:tweet_id>/", views.toggle_retweet, name="toggle_retweet"),

   path("profile/<int:user_id>/", views.profile, name="profile"),
   
   path("twwet/<int:tweet_id>/", views.tweet_detail, name="tweet_detail")
   ] 