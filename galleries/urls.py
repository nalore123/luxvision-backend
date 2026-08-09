from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import GalleryViewSet, ImageViewSet

router = DefaultRouter()
router.register("galleries", GalleryViewSet, basename="gallery")

image_list = ImageViewSet.as_view({"get": "list", "post": "create"})
image_detail = ImageViewSet.as_view({
    "get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy",
})

image_reorder = ImageViewSet.as_view({"post": "reorder"})

urlpatterns = router.urls + [
    path("galleries/<slug:gallery_slug>/images/", image_list, name="gallery-images-list"),
    path("galleries/<slug:gallery_slug>/images/<int:pk>/", image_detail, name="gallery-images-detail"),
    path("galleries/<slug:gallery_slug>/images/reorder/", image_reorder, name="gallery-images-reorder"),
]