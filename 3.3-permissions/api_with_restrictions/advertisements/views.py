from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Advertisement, Likes
from .serializers import AdvertisementSerializer, LikesSerializer
from .permissions import IsOwner
from .filters import AdvertisementFilter



class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter
    
    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsOwner()]
        if self.action == "create":
            return [IsAuthenticated()]
        return []

class LikesViewSet(ModelViewSet):
    """ViewSet для лайков."""

    queryset = Likes.objects.all()
    serializer_class = LikesSerializer

    filterset_fields = ['creator']

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsOwner()]
        return []

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)