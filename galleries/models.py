from django.db import models
from common.models import SEOModelMixin
from common.validators import validate_image_size

class Gallery(SEOModelMixin, models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(
        default=0,
        help_text="Manji broj = prikazuje se prije na početnoj stranici.",
    )
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name_plural = "Galleries"

    def __str__(self):
        return self.title


def gallery_image_upload_path(instance, filename):
    return f"galleries/{instance.gallery.slug}/{filename}"


class Image(models.Model):
    gallery = models.ForeignKey(
        Gallery, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to=gallery_image_upload_path,
        validators=[validate_image_size],
    )
    alt_text = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.gallery.title} - #{self.order}"