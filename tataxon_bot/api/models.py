from django.db import models


class Category(models.Model):
    """
    Модель для представления категории объявления.
    """
    title = models.CharField(max_length=100, verbose_name='Название категории объявления')

    def __str__(self):
        """Возвращает строковое представление объекта Category."""
        return self.title


class Advertisement(models.Model):
    """
    Модель для представления рекламного объявления.

    Эта модель используется для хранения информации о рекламных объявлениях,
    включая заголовок, краткое описание, основное изображение, ссылку
    на полное объявление, категорию, дату и время создания.

    Атрибуты:
    - title: str
        Заголовок объявления, максимальная длина 255 символов.
    - short_description: str
        Краткое описание объявления.
    - image: ImageField
        Основное изображение объявления, которое может быть пустым.
    - full_url: str
        Полный URL ссылки на объявление, максимальная длина 500 символов.
    - category: ForeignKey
        Категория объявления
    - pud_date: datetime
        Дата и время создания объявления.
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория объявления')
    pud_date = models.DateTimeField(verbose_name='Дата создания объявления')

    def __str__(self):
        """
        Возвращает строковое представление объекта Advertisement.

        Строковое представление - это заголовок объявления.
        """

        return self.title
