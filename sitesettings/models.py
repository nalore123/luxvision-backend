from django.db import models
from common.validators import validate_image_size


def hero_image_upload_path(instance, filename):
    return f"hero/{filename}"


class HeroSection(models.Model):
    image = models.ImageField(
        upload_to=hero_image_upload_path,
        validators=[validate_image_size],
    )
    alt_text_hr = models.CharField(max_length=200, blank=True)
    alt_text_en = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj