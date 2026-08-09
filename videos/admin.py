from django.contrib import admin
from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("title", "platform", "is_published", "order")
    list_filter = ("platform", "is_published")