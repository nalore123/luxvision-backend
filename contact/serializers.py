from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "email", "phone", "message"]

class ContactMessageAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = [
            "id", "first_name", "last_name", "email", "phone",
            "message", "is_read", "created_at",
        ]
        read_only_fields = [
            "first_name", "last_name", "email", "phone", "message", "created_at",
        ]