import tempfile

import pytest
from django.utils import timezone

from api.models import Advertisement, Category


@pytest.fixture
def category(db):
    return Category.objects.create(title='Тестовая категория')


@pytest.fixture
def advertisement_with_image(category, db):
    return Advertisement.objects.create(
        title="Тестовое объявление",
        short_description="Описание тестового объявления",
        image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        full_url="http://example.com",
        category=category,
        pud_date=timezone.now()
    )
