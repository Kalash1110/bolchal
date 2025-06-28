from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    # path('', views.index,name='index'),
    path('', views.tweet_list,name='tweet_list'),
    path('create/', views.tweet_create,name='tweet_create'),
    #we write tweet_id because in views for tweet_edit we have written this only.
    path('<int:tweet_id>/edit/', views.tweet_edit,name='tweet_edit'),
    path('<int:tweet_id>/delete/', views.tweet_delete,name='tweet_delete'),
    path('register/', views.register,name='register'),
]