from django.contrib import admin

from api.models import Advertisement


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_description', 'image', 'full_url',)
