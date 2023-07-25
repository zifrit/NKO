from django.db import models
from django.contrib.auth.models import User


class MainProject(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название проекта', db_index=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Кто создал')
    date_create = models.DateTimeField(verbose_name='Дата создание', blank=True, null=True)
    date_start = models.DateTimeField(verbose_name='Дата начала работы', blank=True, null=True)
    date_end = models.DateTimeField(verbose_name='Дата конца работы', blank=True, null=True)
    last_change = models.DateTimeField(auto_now=True, verbose_name='последние изменения', blank=True, null=True)
    structure_project = models.JSONField(verbose_name='структура проекта', default=dict)
    id_steps = models.ManyToManyField(to='Step', verbose_name='Список Этапов', related_name='base', blank=True)

    def __str__(self):
        return f'{self.user.username} {self.name}'


class LinksStep(models.Model):
    start_id = models.PositiveIntegerField(verbose_name='начало связи')
    end_id = models.PositiveIntegerField(verbose_name='конец связи')
    description = models.CharField(max_length=255, verbose_name='описания')
    color = models.CharField(max_length=255, verbose_name='цвет', blank=True)


class ProjectFiles(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'file/%Y/%m.%d/', verbose_name='Файл')
    link_main_project = models.ForeignKey(to='MainProject', on_delete=models.CASCADE, verbose_name='связь с проектом',
                                          related_name='project_files')
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_files')


class ProjectImages(models.Model):
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to=f'images/%Y/%m.%d/', verbose_name='Файл')
    link_main_project = models.ForeignKey(to='MainProject', on_delete=models.CASCADE, verbose_name='Объект привязки')


class StepTemplates(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название этапа', db_index=True, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Кто создал')
    structure = models.JSONField(verbose_name='структура этапа', default=dict)
    structure_for_create = models.JSONField(verbose_name='структура для создания этапа', default=dict)


class Step(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название этапа', db_index=True)
    what_project = models.ForeignKey(to='MainProject', on_delete=models.CASCADE, verbose_name='id проекта',
                                     related_name='steps')
    date = models.ManyToManyField(to='FieldDate', verbose_name='Дата', blank=True)
    SF_time = models.ManyToManyField(to='FieldStartFinishTime', verbose_name='Срок', blank=True)
    text = models.ManyToManyField(to='FieldText', verbose_name='Текст', blank=True)
    textarea = models.ManyToManyField(to='FieldTextarea', verbose_name='Большой текст', blank=True)
    date_create = models.DateTimeField(verbose_name='Дата создание', auto_now_add=True)
    date_start = models.DateTimeField(verbose_name='Дата начала работы', blank=True, null=True)
    date_end = models.DateTimeField(verbose_name='Дата конца работы', blank=True, null=True)



    def __str__(self):
        return self.name

    class Meta:
        ...


class FieldText(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Текст')
    text = models.CharField(max_length=255, verbose_name='Текст', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_text')


class FieldTextarea(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Большой текс')
    textarea = models.TextField(verbose_name='Большой текст', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_textarea')


class FieldDate(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Дата')
    time = models.DateField(verbose_name='Дата', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_date')


class FieldStartFinishTime(models.Model):
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Начало-Конец время')
    start = models.DateTimeField(verbose_name='Начало', blank=True)
    finish = models.DateTimeField(verbose_name='Конец', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_f_s_time')
