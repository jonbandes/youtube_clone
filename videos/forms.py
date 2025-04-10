from django import forms
from .models import Video, Comment

class VideoForm(forms.ModelForm):
    """
    Form for uploading new videos.
    Extracts YouTube ID from various URL formats.
    """
    youtube_url = forms.URLField(label='YouTube URL')
    
    class Meta:
        model = Video
        fields = ['title', 'description', 'youtube_url']
    
    def clean_youtube_url(self):
        """Extracts YouTube ID from URL, raises ValidationError if invalid."""
        url = self.cleaned_data['youtube_url']
        if 'youtube.com/watch?v=' in url:
            return url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[1]
        raise forms.ValidationError("Invalid YouTube URL format")

class CommentForm(forms.ModelForm):
    """Form for adding comments to videos."""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add your comment...'
            }),
        }