import requests
from rest_framework import generics, permissions, throttling
from django.conf import settings
from .models import ContactMessage
from .serializers import *
from rest_framework import viewsets, permissions


class ContactThrottle(throttling.AnonRateThrottle):
    scope = "contact"


class ContactMessageCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ContactThrottle]

    def perform_create(self, serializer):
        ip = self.request.META.get("REMOTE_ADDR")
        instance = serializer.save(ip_address=ip)

        try:
            requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": "LUX Vision <onboarding@resend.dev>",
                    "to": [settings.CONTACT_RECIPIENT_EMAIL],
                    "subject": f"Nova poruka s kontakt forme — {instance.first_name} {instance.last_name}",
                    "text": (
                        f"Ime i prezime: {instance.first_name} {instance.last_name}\n"
                        f"Email: {instance.email}\n"
                        f"Telefon: {instance.phone or '—'}\n\n"
                        f"Poruka:\n{instance.message}"
                    ),
                },
                timeout=10,
            )
        except requests.RequestException:
            pass


class ContactMessageAdminViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageAdminSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch", "delete"]