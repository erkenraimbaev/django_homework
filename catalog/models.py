from django.db import models
from django.db import connection

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name_category = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name_category}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name_product = models.CharField(max_length=100, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='products/', verbose_name='изображение', **NULLABLE)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='категория')
    price = models.IntegerField(verbose_name='цена за покупку')
    date_making = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    date_changing = models.DateTimeField(auto_now_add=True, verbose_name='дата последнег оизменения')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='автор', **NULLABLE)
    is_published = models.BooleanField(default=False, verbose_name='опубликовано')

    def __str__(self):
        return f'{self.name_product} {self.category} {self.price} {self.date_making}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            (
                "set_is_published",
                "Can publish product"
            )
        ]


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='название продукта')
    version = models.PositiveIntegerField(verbose_name='номер версии')
    name_version = models.CharField(max_length=150, verbose_name='название версии')
    current_version = models.BooleanField(default=True, verbose_name='признак текущей версии')

    def __str__(self):
        return f'{self.version} {self.name_version} {self.product} {self.current_version}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'
