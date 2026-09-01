from rest_framework import serializers
from .models import HeroSection


class HeroSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroSection
        fields = ["image", "alt_text_hr", "alt_text_en", "updated_at"]
        read_only_fields = ["updated_at"]