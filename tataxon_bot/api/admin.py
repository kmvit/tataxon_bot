from django.contrib import admin

from api.models import Advertisement, Category


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_description', 'image', 'full_url',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
