from rest_framework import viewsets
from .models import BlogPost
from .serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

class BlogPostPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "page_size"

class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostDetailSerializer
    lookup_field = "slug"
    pagination_class = BlogPostPagination

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(is_published=True)
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return BlogPostListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return BlogPostWriteSerializer
        return BlogPostDetailSerializer

    @action(detail=True, methods=["get"])
    def admin_detail(self, request, slug=None):
        post = self.get_object()
        data = BlogPostWriteSerializer(post, context={"request": request}).data
        return Response(data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)