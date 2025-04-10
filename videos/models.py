from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Video(models.Model):
    """
    Represents a YouTube video in the system.
    
    Attributes:
        title (CharField): Video title (max 100 chars).
        description (TextField): Video description.
        youtube_id (CharField): YouTube video ID (extracted from URL).
        uploader (ForeignKey): User who uploaded the video.
        upload_date (DateTimeField): Auto-set on creation.
        likes/dislikes (ManyToMany): Users who liked/disliked the video.
    """
    
    title = models.CharField(max_length=100)
    description = models.TextField()
    youtube_id = models.CharField(max_length=100)  # Para almacenar solo el ID del video
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_videos', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_videos', blank=True)

    def __str__(self):
        return self.title

    def get_embed_url(self):
        """Returns the YouTube embed URL for this video."""
        return f"https://www.youtube.com/embed/{self.youtube_id}"
    
    def get_likes_count(self):
        """Returns total likes count."""
        return self.likes.count()

    def get_dislikes_count(self):
        """Returns total dislikes count."""
        return self.dislikes.count()
    
    def calculate_popularity_score(self):
        """
        Calculates a dynamic popularity score based on:
        - Likes (+10 pts each)
        - Dislikes (-5 pts each)
        - Comments (+1 pt each)
        - Age penalty (-100 pts per day old)
        """

        days_old = (timezone.now() - self.upload_date).days
        
     
        likes_score = self.likes.count() * 10
        dislikes_score = self.dislikes.count() * 5
        comments_score = self.comments.count() * 1
        age_penalty = days_old * 100
        
        popularity_score = likes_score - dislikes_score + comments_score - age_penalty
        return popularity_score
    
    @classmethod
    def get_popular_videos(cls):
        """
        Returns the 5 most popular videos of the current month.
        Falls back to random videos if no recent uploads exist.
        """
        today = timezone.now()
        first_day_of_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        
        current_month_videos = cls.objects.filter(upload_date__gte=first_day_of_month)
        
        if current_month_videos.exists():
            
            videos = current_month_videos.annotate(
                likes_count=models.Count('likes'),
                dislikes_count=models.Count('dislikes'),
                comments_count=models.Count('comments'),
                days_old=models.ExpressionWrapper(
                    models.F('upload_date') - first_day_of_month,
                    output_field=models.DurationField()
                )
            ).annotate(
                days_old_int=models.ExpressionWrapper(
                    models.F('days_old') / timedelta(days=1),
                    output_field=models.IntegerField()
                )
            ).annotate(
                popularity_score=(
                    models.F('likes_count') * 10 -
                    models.F('dislikes_count') * 5 +
                    models.F('comments_count') * 1 -
                    models.F('days_old_int') * 100
                )
            ).order_by('-popularity_score')[:5]
        else:
            videos = cls.objects.order_by('?')[:5]
            
        return videos
    

class Comment(models.Model):
    """
    User comments on videos.
    
    Attributes:
        video (ForeignKey): Related Video object.
        user (ForeignKey): Comment author.
        text (TextField): Comment content (max 500 chars).
        created_at (DateTimeField): Auto-set on creation.
    """
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] 
    def __str__(self):
        return f"{self.user.username} - {self.text[:50]}"