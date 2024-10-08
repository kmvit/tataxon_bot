from django.db import models


class Advertisement(models.Model):
    """
    Модель для представления рекламного объявления.

    Эта модель используется для хранения информации о рекламных объявлениях,
    включая заголовок, краткое описание, основное изображение и ссылку
    на полное объявление.

    Атрибуты:
    - title: str
        Заголовок объявления, максимальная длина 255 символов.
    - short_description: str
        Краткое описание объявления.
    - image: ImageField
        Основное изображение объявления, которое может быть пустым.
    - full_url: str
    Полный URL ссылки на объявление, максимальная длина 500 символов.
    """
    title = models.CharField(max_length=255,
                             verbose_name='Заголовок объявления')
    short_description = models.TextField(verbose_name='Краткое описание')
    image = models.ImageField(
        upload_to='advert_images/',
        null=True,
        blank=True,
        verbose_name='Основное изображение'
    )
    full_url = models.URLField(max_length=500,
                               verbose_name='Ссылка на полное объявление')

    def __str__(self):
        """
        Возвращает строковое представление объекта Advertisement.

        Строковое представление - это заголовок объявления.
        """

        return self.title
