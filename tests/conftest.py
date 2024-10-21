from django.utils import timezone
import pytest

from api.models import Advertisement, Category


@pytest.fixture
def category(db):
    return Category.objects.create(title='Тестовая категория')


@pytest.fixture
def advertisement(category, db):
    return Advertisement.objects.create(
        title="Тестовое объявление",
        short_description="Описание тестового объявления",
        full_url="http://example.com",
        category=category,
        pud_date=timezone.now()
    )
