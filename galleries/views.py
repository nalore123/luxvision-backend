from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import Gallery, Image
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ReorderItemSerializer

class GalleryViewSet(viewsets.ModelViewSet):
    serializer_class = GalleryDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Gallery.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return GalleryListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return GalleryWriteSerializer
        return GalleryDetailSerializer

    @action(detail=False, methods=["post"])
    def reorder(self, request):
        serializer = ReorderItemSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        galleries = {g.id: g for g in Gallery.objects.all()}
        updated = []
        for item in serializer.validated_data:
            gallery = galleries.get(item["id"])
            if gallery is None:
                continue
            gallery.order = item["order"]
            updated.append(gallery)

        Gallery.objects.bulk_update(updated, ["order"])
        return Response({"updated": len(updated)})

    @action(detail=True, methods=["get"])
    def admin_detail(self, request, slug=None):
        gallery = self.get_object()
        data = GalleryWriteSerializer(gallery, context={"request": request}).data
        data["images"] = ImageSerializer(
            gallery.images.all(), many=True, context={"request": request}
        ).data
        return Response(data)

class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer

    def get_queryset(self):
        return Image.objects.filter(gallery__slug=self.kwargs["gallery_slug"])

    def perform_create(self, serializer):
        gallery = get_object_or_404(Gallery, slug=self.kwargs["gallery_slug"])
        serializer.save(gallery=gallery)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ImageWriteSerializer
        return ImageSerializer

    @action(detail=False, methods=["post"])
    def reorder(self, request, gallery_slug=None):
        serializer = ReorderItemSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        images = {
            img.id: img
            for img in Image.objects.filter(gallery__slug=gallery_slug)
        }
        updated = []
        for item in serializer.validated_data:
            image = images.get(item["id"])
            if image is None:
                continue
            image.order = item["order"]
            updated.append(image)

        Image.objects.bulk_update(updated, ["order"])
        return Response({"updated": len(updated)})