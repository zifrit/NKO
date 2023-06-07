from django.db import models
from django.contrib.auth.models import User


class MainTableKO(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название проекта', db_index=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Кто создал')
    stages_mass = models.CharField(max_length=255, verbose_name='Массив из id этапов')
    stages = models.ManyToManyField(to='KoStage', verbose_name='Список Этапов', related_name='base')


class KoFiles(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'file/%Y/%m.%d/', verbose_name='Файл')
    ko = models.ForeignKey(to='MainTableKO', on_delete=models.CASCADE, verbose_name='Объект привязки')


class KoImages(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'images/%Y/%m.%d/', verbose_name='Файл')
    ko = models.ForeignKey(to='MainTableKO', on_delete=models.CASCADE, verbose_name='Объект привязки')


class KoStage(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название этапа', db_index=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Кто создал')
    date = models.ManyToManyField(to='FieldDate', verbose_name='Дата', blank=True)
    SF_time = models.ManyToManyField(to='FieldStartFinishTime', verbose_name='Срок', blank=True)
    text = models.ManyToManyField(to='FieldText', verbose_name='Текст', blank=True)
    textarea = models.ManyToManyField(to='FieldTextarea', verbose_name='Большой текст', blank=True)
    date_create = models.DateTimeField(verbose_name='Дата создание')
    date_start = models.DateTimeField(verbose_name='Дата начала работы')
    date_end = models.DateTimeField(verbose_name='Дата конца работы')


class FieldText(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля')
    name_field = models.CharField(max_length=255, verbose_name='Имя поля', default='Текст')
    text = models.CharField(max_length=255, verbose_name='Текст')


class FieldTextarea(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля')
    name_field = models.CharField(max_length=255, verbose_name='Имя поля', default='Большой текс')
    textarea = models.TextField(verbose_name='Большой текст')


class FieldDate(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля')
    name_field = models.CharField(max_length=255, verbose_name='Имя поля', default='Дата')
    time = models.DateField(verbose_name='Дата')


class FieldStartFinishTime(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля')
    name_field = models.CharField(max_length=255, verbose_name='Имя поля', default='Начало-Конец время')
    start = models.DateTimeField(verbose_name='Начало')
    finish = models.DateTimeField(verbose_name='Конец')
