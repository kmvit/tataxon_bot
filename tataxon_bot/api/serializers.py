from rest_framework import serializers

from .models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Advertisement.

    Используется для преобразования экземпляров модели
    Advertisement в формат, подходящий для передачи по сети,
    и обратно. Он включает все необходимые поля
    для представления рекламного объявления.

    Поля:
    - id: Уникальный идентификатор объявления.
    - title: Заголовок объявления.
    - short_description: Краткое описание объявления.
    - main_image: Основное изображение объявления.
    - full_url: Полный URL объявления.
    """

    class Meta:
        model = Advertisement
        fields = ['id', 'title', 'short_description', 'main_image', 'full_url']
