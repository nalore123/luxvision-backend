from rest_framework import serializers
from .models import Gallery, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "alt_text", "order", "width", "height"]


class GalleryListSerializer(serializers.ModelSerializer):
    cover_image = serializers.SerializerMethodField()

    class Meta:
        model = Gallery
        fields = ["id", "title", "slug", "cover_image", "order", "is_published"]

    def get_cover_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            return ImageSerializer(first_image, context=self.context).data
        return None


class GalleryDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Gallery
        fields = [
            "id", "title", "slug", "description",
            "images", "meta_title", "meta_description",
        ]

class ReorderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order = serializers.IntegerField(min_value=0)

class GalleryWriteSerializer(serializers.ModelSerializer):
    title_hr = serializers.CharField(max_length=200, allow_blank=False)
    title_en = serializers.CharField(max_length=200, allow_blank=False)

    class Meta:
        model = Gallery
        fields = [
            "id", "title_hr", "title_en", "slug_hr", "slug_en",
            "description_hr", "description_en",
            "meta_title_hr", "meta_title_en",
            "meta_description_hr", "meta_description_en",
            "is_published", "order",
        ]


class ImageWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "image", "alt_text_hr", "alt_text_en", "order"]