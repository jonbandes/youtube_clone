from django.views.generic import DetailView, CreateView, TemplateView, ListView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse, reverse_lazy
from .models import Video, Comment
from .forms import VideoForm, CommentForm
from django.http import JsonResponse

class VideoDetailView(FormMixin, DetailView):
    """
    Displays video details and handles comment submissions.
    - GET: Shows video and existing comments.
    - POST: Processes new comments (login required).
    """
    model = Video
    template_name = 'videos/video_detail.html'
    form_class = CommentForm
    context_object_name = 'video'

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        """Handles comment submission."""
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.video = self.object
            comment.save()
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        """Adds comments to template context (newest first)."""
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(video=self.object).order_by('-created_at')
        return context

@login_required
def like_video(request, video_id):
    """Handles video likes (AJAX-friendly JSON response)."""
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.dislikes.all():
        video.dislikes.remove(request.user)
    video.likes.add(request.user)
    return JsonResponse({
        'likes': video.likes.count(),
        'dislikes': video.dislikes.count()
    })

@login_required
def dislike_video(request, video_id):
    """Handles video dislikes (AJAX-friendly JSON response)."""
    video = get_object_or_404(Video, id=video_id)
    if request.user in video.likes.all():
        video.likes.remove(request.user)
    video.dislikes.add(request.user)
    return JsonResponse({
        'likes': video.likes.count(),
        'dislikes': video.dislikes.count()
    })

class VideoCreateView(CreateView):
    """Handles video uploads (login required)."""
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """Sets uploader and extracts YouTube ID before saving."""
        form.instance.uploader = self.request.user
        form.instance.youtube_id = form.cleaned_data['youtube_url']
        return super().form_valid(form)

class HomeView(TemplateView):
    """Displays 12 random videos on the homepage."""
    template_name = 'videos/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.order_by('?')[:12]
        return context

class PopularVideosView(ListView):
    """Displays the 5 most popular videos of the month."""
    model = Video
    template_name = 'videos/popular_videos.html'
    context_object_name = 'videos'
    
    def get_queryset(self):
        return Video.get_popular_videos()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "This Month's Popular Videos"
        return context