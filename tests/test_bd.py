import tempfile

import pytest
from django.utils import timezone

from api.models import Advertisement


@pytest.mark.django_db
def test_advertisement_creation(advertisement_with_image):
    """Тест для проверки создания объявления через фикстуру"""
    ad = Advertisement.objects.get(pk=advertisement_with_image.pk)
    assert ad.title == "Тестовое объявление"
    assert ad.short_description == "Описание тестового объявления"
    assert ad.full_url == "http://example.com"
    assert ad.category.title == "Тестовая категория"


@pytest.mark.django_db
def test_create_new_advertisement(category):
    """Тест для создания нового объявления в базе данных"""
    ad = Advertisement.objects.create(
        title="Новое тестовое объявление",
        short_description="Описание нового тестового объявления",
        image=tempfile.NamedTemporaryFile(suffix=".jpg").name,
        full_url="http://example.com/new",
        category=category,
        pud_date=timezone.now()
    )
    assert Advertisement.objects.count() == 1
    assert ad.title == "Новое тестовое объявление"


@pytest.mark.django_db
def test_update_advertisement(advertisement_with_image):
    """Тест для обновления объявления"""
    advertisement_with_image.title = "Обновленное название объявления"
    advertisement_with_image.short_description = ("Обновленное "
                                                  "описание объявления")
    image = tempfile.NamedTemporaryFile(suffix=".jpg").name
    advertisement_with_image.image = image
    advertisement_with_image.save()

    updated_ad = Advertisement.objects.get(pk=advertisement_with_image.pk)
    assert updated_ad.title == "Обновленное название объявления"
    assert updated_ad.short_description == "Обновленное описание объявления"
    assert updated_ad.image == image


@pytest.mark.django_db
def test_delete_advertisement(advertisement_with_image):
    """Тест для удаления объявления"""
    advertisement_with_image.delete()
    assert Advertisement.objects.count() == 0
