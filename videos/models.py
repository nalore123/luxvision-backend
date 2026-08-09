from django.db import models
from common.validators import validate_image_size

class Video(models.Model):
    class Platform(models.TextChoices):
        YOUTUBE = "youtube", "YouTube"
        VIMEO = "vimeo", "Vimeo"

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    platform = models.CharField(max_length=10, choices=Platform.choices)
    video_url = models.URLField(help_text="Puni link na YouTube ili Vimeo video.")
    thumbnail = models.ImageField(
        upload_to="videos/thumbnails/",
        validators=[validate_image_size],
    )
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        if self.platform == self.Platform.YOUTUBE:
            video_id = self._extract_youtube_id()
            return f"https://www.youtube.com/embed/{video_id}" if video_id else None
        if self.platform == self.Platform.VIMEO:
            video_id = self._extract_vimeo_id()
            return f"https://player.vimeo.com/video/{video_id}" if video_id else None
        return None

    def _extract_youtube_id(self):
        import re
        match = re.search(r"(?:v=|youtu\.be/|embed/)([a-zA-Z0-9_-]{11})", self.video_url)
        return match.group(1) if match else None

    def _extract_vimeo_id(self):
        import re
        match = re.search(r"vimeo\.com/(\d+)", self.video_url)
        return match.group(1) if match else None