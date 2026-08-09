from rest_framework import serializers
from .models import BlogPost


class BlogPostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ["id", "title", "slug", "featured_image", "published_at"]


class BlogPostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            "id", "title", "slug", "content", "featured_image",
            "published_at", "meta_title", "meta_description",
        ]

class BlogPostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = [
            "id", "title_hr", "title_en", "slug_hr", "slug_en",
            "content_hr", "content_en",
            "meta_title_hr", "meta_title_en",
            "meta_description_hr", "meta_description_en",
            "featured_image", "is_published", "published_at",
        ]