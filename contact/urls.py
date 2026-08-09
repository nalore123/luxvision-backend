from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageCreateView, ContactMessageAdminViewSet

router = DefaultRouter()
router.register("messages", ContactMessageAdminViewSet, basename="contact-message")

urlpatterns = [
    path("", ContactMessageCreateView.as_view(), name="contact-create"),
    path("", include(router.urls)),
]