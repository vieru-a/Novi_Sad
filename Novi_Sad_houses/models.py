from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


def get_slug(slug, model):
    unique_slug = slug
    number = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{slug}-{number}'
        number += 1

    return unique_slug


class House(models.Model):
    title = models.CharField(max_length=255, verbose_name='Адрес')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    structureName = models.CharField(max_length=255, verbose_name='Тип постройки')
    roomCount = models.CharField(max_length=255, verbose_name='Количество комнат')
    m2 = models.IntegerField(verbose_name='Площадь')
    price = models.IntegerField(verbose_name='Цена')
    pricePerM2 = models.CharField(max_length=255, verbose_name='Цена за квадратный метр')
    desc = models.TextField(max_length=255, verbose_name='Описание')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return f'{self.title} - {self.price}€, {self.m2}m2'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_slug(slugify(f'{self.title} - {self.price}€, {self.m2}m2'), House)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('about_house_page', kwargs={'house_slug': self.slug})

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'
        ordering = ['id', 'price', 'm2']


class HouseImage(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название фото')
    house = models.ForeignKey('House', on_delete=models.PROTECT, verbose_name='Дом')
    image = models.ImageField(upload_to=f'new_data/%Y/%m/%d', verbose_name='Изображение')
    default = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = 'Фото дома'
        verbose_name_plural = 'Фото домов'
        ordering = ['house_id']

