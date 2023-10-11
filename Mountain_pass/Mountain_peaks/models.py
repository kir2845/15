from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from django.utils import timezone
from django.urls import reverse


# Информация об авторе
class Author(models.Model):
    surname = models.CharField(max_length=64, verbose_name='фамилия')
    name = models.CharField(max_length=64, verbose_name='имя')
    patronymic = models.CharField(max_length=64, verbose_name='отчество')
    email = models.EmailField(verbose_name='электронная почта')
#    email = models.EmailField(verbose_name='электронная почта', unique=True)
    telephone = models.CharField(max_length=16, verbose_name='номер телефона')

    def __str__(self):
       return f'{self.surname} - {self.email}'

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'


# Координаты объекта
class Coordinate(models.Model):
    latitude = models.FloatField(max_length=64, verbose_name='широта')
    longitude = models.FloatField(max_length=64, verbose_name='долгота')
    height = models.IntegerField(verbose_name='высота')

    def __str__(self):
        return f'{self.latitude},{self.longitude},{self.height}'

    class Meta:
        verbose_name = 'координат'
        verbose_name_plural = 'Координаты'


# Уровень сложности прохождения маршрута
LEVEL = [
    ('', 'не указано'),
    ('1a', '1A'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('4a', '4А'),
    ('4b', '4Б'),
    ('5a', '5А'),
    ('5b', '5Б'),
]

class Level(models.Model):
    winter = models.CharField(max_length=3, choices=LEVEL, verbose_name='Зима', default='')
    spring = models.CharField(max_length=3, choices=LEVEL, verbose_name='Весна', default='')
    summer = models.CharField(max_length=3, choices=LEVEL, verbose_name='Лето', default='')
    autumn = models.CharField(max_length=3, choices=LEVEL, verbose_name='Осень', default='')

    def __str__(self):
        return f'зима: {self.winter}, весна: {self.spring}, лето: {self.summer}, осень: {self.autumn}'

    class Meta:
        verbose_name = 'уровень сложности'
        verbose_name_plural = 'Уровни сложности'


# Информация/данные о добавленном объекте (перевале)
class Peak(models.Model):
    # Cтатус объекта
    STATUS = [
        ('new', 'новый'),
        ('pending', 'на модерации'),
        ('accepted', 'принят'),
        ('rejected', 'не принят'),
    ]

    country = models.CharField(max_length=128, verbose_name='страна', default='')
    category = models.CharField(max_length=128, default='', blank=True, verbose_name='категория объекта/высоты')
    title = models.CharField(max_length=128, verbose_name='название')
    other_titles = models.CharField(max_length=128, verbose_name='другое название', default='', blank=True)
    connect = models.TextField(default='', verbose_name='соединение')
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS, verbose_name='статус', default='new')
    method_of_passage = models.CharField(max_length=128, default='', blank=True, verbose_name='способ прохождения')

    user = models.ForeignKey(Author, on_delete=models.CASCADE, default=None, verbose_name='автор')
    coords = models.ForeignKey(Coordinate, on_delete=models.CASCADE, verbose_name='координаты')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, verbose_name='уровень сложности')

    class Meta:
        verbose_name = 'вершину и перевал'
        verbose_name_plural = 'Вершины и перевалы'

# Изображения, добавленные автором
class Image(models.Model):
    title = models.CharField(max_length=128, verbose_name='название', blank=True,)
    photo = models.URLField(max_length=300, verbose_name='фотография', blank=True)

    peak = models.ForeignKey(Peak, verbose_name='вершина', related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} {self.title}'

    class Meta:
        verbose_name = 'фото'
        verbose_name_plural = 'Фотографии'






