from django.db import models

class Advertisement(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок объявления')
    short_description = models.TextField(verbose_name='Краткое описание')
    image = models.ImageField(upload_to='advert_images/', null=True, blank=True, verbose_name='Основное изображение')
    full_url = models.URLField(max_length=500, verbose_name='Ссылка на полное объявление')

    def __str__(self):
        return self.title
