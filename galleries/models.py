from django.db import models
from common.models import SEOModelMixin
from common.validators import validate_image_size
from common.utils import generate_unique_slug

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

    def save(self, *args, **kwargs):
        if not self.slug_hr:
            self.slug_hr = generate_unique_slug(self, self.title_hr, slug_field_name="slug_hr")
        if not self.slug_en:
            self.slug_en = generate_unique_slug(self, self.title_en, slug_field_name="slug_en")
        super().save(*args, **kwargs)


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
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "created_at"]

    def __str__(self):
        return f"{self.gallery.title} - #{self.order}"

    def save(self, *args, **kwargs):
        is_new_or_changed = self.image and (not self.width or not self.height)
        super().save(*args, **kwargs)

        if is_new_or_changed:
            self.width = self.image.width
            self.height = self.image.height
            super().save(update_fields=["width", "height"])