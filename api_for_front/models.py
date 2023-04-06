from django.db import models
from django.contrib.auth.models import User


class MainTableKO(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название проекта')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Кто создал')
    stages = models

    pass


class KoFiles(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'file/%Y/%m.%d/', verbose_name='Файл')
    ko = models.ForeignKey(to='MainTableKO', on_delete=models.CASCADE, verbose_name='Объект привязки')


class KoImages(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'images/%Y/%m.%d/', verbose_name='Файл')
    ko = models.ForeignKey(to='MainTableKO', on_delete=models.CASCADE, verbose_name='Объект привязки')
