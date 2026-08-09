from modeltranslation.translator import register, TranslationOptions
from .models import Video


@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ("title", "description")