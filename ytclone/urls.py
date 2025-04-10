from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
#from videos.views import VideoListView 

urlpatterns = [
    path('', include('videos.urls')), 
    path('users/', include('users.urls')), 
]