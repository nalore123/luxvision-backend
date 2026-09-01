from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import HeroSection
from .serializers import HeroSectionSerializer


class HeroSectionPublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        hero = HeroSection.load()
        serializer = HeroSectionSerializer(hero, context={"request": request})
        return Response(serializer.data)


class HeroSectionAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hero = HeroSection.load()
        serializer = HeroSectionSerializer(hero, context={"request": request})
        return Response(serializer.data)

    def patch(self, request):
        hero = HeroSection.load()
        serializer = HeroSectionSerializer(
            hero, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)