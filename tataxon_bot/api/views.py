from rest_framework import viewsets

from .models import Advertisement
from .serializers import AdvertisementSerializer


class AdvertisementViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с рекламными объявлениями.

    Этот ViewSet предоставляет CRUD-операции для модели Advertisement.
    Он использует сериализатор AdvertisementSerializer
    для преобразования данных модели в формат, подходящий для передачи по сети,
    и обратно.

    Атрибуты:
    - queryset: QuerySet, содержащий все экземпляры модели Advertisement.
    - serializer_class: Класс сериализатора, используемый для обработки
    данных модели.
    """

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
