from django.urls import path
from .views import HeroSectionPublicView, HeroSectionAdminView

urlpatterns = [
    path("hero/", HeroSectionPublicView.as_view(), name="hero-public"),
    path("hero/manage/", HeroSectionAdminView.as_view(), name="hero-admin"),
]