from rest_framework import serializers
from .models import Video


class VideoSerializer(serializers.ModelSerializer):
    embed_url = serializers.ReadOnlyField()

    class Meta:
        model = Video
        fields = ["id", "title", "description", "thumbnail", "embed_url", "order"]

class VideoWriteSerializer(serializers.ModelSerializer):
    embed_url = serializers.ReadOnlyField()

    class Meta:
        model = Video
        fields = [
            "id", "title_hr", "title_en", "description_hr", "description_en",
            "platform", "video_url", "thumbnail", "order", "is_published",
            "embed_url",
        ]