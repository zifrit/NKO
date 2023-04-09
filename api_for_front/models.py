from django.db import models
from django.contrib.auth.models import User


class MainTableKO(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название проекта')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Кто создал')
    stages_mass = models.CharField(max_length=255, verbose_name='Массив из id этапов')


    pass


class KoFiles(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'file/%Y/%m.%d/', verbose_name='Файл')
    ko = models.ForeignKey(to='MainTableKO', on_delete=models.CASCADE, verbose_name='Объект привязки')


class KoImages(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'images/%Y/%m.%d/', verbose_name='Файл')
    ko = models.ForeignKey(to='MainTableKO', on_delete=models.CASCADE, verbose_name='Объект привязки')


class KoStage(models.Model):
    text = models.ManyToManyField(to='FieldText', verbose_name='Текст')
    textarea = models.ManyToManyField(to='FieldTextarea', verbose_name='Большой текст')
    date_create = models.DateTimeField(verbose_name='Дата создание')
    date_start = models.DateTimeField(verbose_name='Дата начала работы')
    date_end = models.DateTimeField(verbose_name='Дата конца работы')


class FieldText(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля')
    text = models.CharField(max_length=255, verbose_name='Текст')


class FieldTextarea(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля')
    textarea = models.TextField(verbose_name='Большой текст')
