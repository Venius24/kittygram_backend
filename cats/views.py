from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination

from .models import Achievement, Cat

from .serializers import AchievementSerializer, CatSerializer


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    pagination_class = PageNumberPagination 
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Cat.objects.select_related('owner').prefetch_related('achievements')

    def get_object(self):
        obj = super().get_object()
        if self.request.method not in permissions.SAFE_METHODS and obj.owner != self.request.user:
            raise PermissionDenied('Изменять кота может только владелец.')
        return obj

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
