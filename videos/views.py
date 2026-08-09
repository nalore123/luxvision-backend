from rest_framework import viewsets
from .models import Video
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

class VideoPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"

class VideoViewSet(viewsets.ModelViewSet):
    serializer_class = VideoSerializer
    pagination_class = VideoPagination

    def get_queryset(self):
        queryset = Video.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        return queryset

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return VideoWriteSerializer
        return VideoSerializer

    @action(detail=True, methods=["get"])
    def admin_detail(self, request, pk=None):
        video = self.get_object()
        data = VideoWriteSerializer(video, context={"request": request}).data
        return Response(data)