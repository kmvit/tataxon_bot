from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdvertisementViewSet

router = DefaultRouter()
router.register('advertisement',
                AdvertisementViewSet, basename='advertisement')

urlpatterns = [
    path('', include(router.urls)),
]
