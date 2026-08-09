from modeltranslation.translator import register, TranslationOptions
from .models import Gallery, Image


@register(Gallery)
class GalleryTranslationOptions(TranslationOptions):
    fields = ("title", "slug", "description", "meta_title", "meta_description")


@register(Image)
class ImageTranslationOptions(TranslationOptions):
    fields = ("alt_text",)