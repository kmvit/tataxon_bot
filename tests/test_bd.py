import pytest

from django.utils import timezone

from api.models import Advertisement


@pytest.mark.django_db
def test_advertisement_creation(advertisement):
    """Тест для проверки создания объявления через фикстуру"""
    ad = Advertisement.objects.get(pk=advertisement.pk)
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
        full_url="http://example.com/new",
        category=category,
        pud_date=timezone.now()
    )
    assert Advertisement.objects.count() == 1
    assert ad.title == "Новое тестовое объявление"


@pytest.mark.django_db
def test_update_advertisement(advertisement):
    """Тест для обновления объявления"""
    advertisement.title = "Обновленное название объявления"
    advertisement.save()
    updated_ad = Advertisement.objects.get(pk=advertisement.pk)
    assert updated_ad.title == "Обновленное название объявления"


@pytest.mark.django_db
def test_delete_advertisement(advertisement):
    """Тест для удаления объявления"""
    advertisement.delete()
    assert Advertisement.objects.count() == 0
