from django.contrib import admin
from .models import Gallery, Image


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ("image", "alt_text", "order")


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "order")
    inlines = [ImageInline]