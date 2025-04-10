from django.urls import path
from .views import (
    HomeView, 
    VideoCreateView, 
    VideoDetailView,
    like_video, 
    dislike_video, 
    PopularVideosView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('video/new/', VideoCreateView.as_view(), name='video-create'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('video/<int:video_id>/like/', like_video, name='like-video'),
    path('video/<int:video_id>/dislike/', dislike_video, name='dislike-video'),
    path('popular/', PopularVideosView.as_view(), name='popular-videos'),
]