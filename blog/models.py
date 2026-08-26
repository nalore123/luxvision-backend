from django.conf import settings
from django.db import models
from common.models import SEOModelMixin
import bleach
from common.validators import validate_image_size
from common.utils import generate_unique_slug

ALLOWED_TAGS = [
    "p", "br", "strong", "em", "u", "h2", "h3", "h4",
    "ul", "ol", "li", "a", "blockquote", "img",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "img": ["src", "alt"],
}

class BlogPost(SEOModelMixin, models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="blog_posts",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    content = models.TextField()
    featured_image = models.ImageField(
        upload_to="blog/", blank=True, null=True,
        validators=[validate_image_size],
    )
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug_hr:
            self.slug_hr = generate_unique_slug(self, self.title_hr, slug_field_name="slug_hr")
        if not self.slug_en:
            self.slug_en = generate_unique_slug(self, self.title_en, slug_field_name="slug_en")

        self.content = bleach.clean(
            self.content,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            strip=True,
        )
        super().save(*args, **kwargs)