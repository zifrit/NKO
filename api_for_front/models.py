from django.db import models
from django.contrib.auth.models import User


class MainProject(models.Model):
    """
    Model MainProject information about the main project
    """
    name = models.CharField(max_length=255, verbose_name='Название проекта', db_index=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Кто создал')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')
    date_start = models.DateTimeField(verbose_name='Дата начала работы', blank=True, null=True)
    date_end = models.DateTimeField(verbose_name='Дата конца работы', blank=True, null=True)
    last_change = models.DateTimeField(auto_now=True, verbose_name='последние изменения')

    def __str__(self):
        return f'{self.user.username} {self.name}'


class LinksStep(models.Model):
    """
    Model LinksStep information about the relationship between tables
    """
    start_id = models.PositiveIntegerField(verbose_name='начало связи')
    end_id = models.PositiveIntegerField(verbose_name='конец связи')
    description = models.CharField(max_length=255, verbose_name='описания', blank=True)
    data = models.JSONField(verbose_name='id фронта')
    color = models.CharField(max_length=255, verbose_name='цвет', blank=True)


class ProjectFiles(models.Model):
    """
    Model files main projects
    """
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to='file/%Y/%m.%d/', verbose_name='Файл')
    link_main_project = models.ForeignKey(to='MainProject', on_delete=models.CASCADE, verbose_name='связь с проектом',
                                          related_name='project_files')
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_files')


class ProjectImages(models.Model):
    """
    Model images main projects
    """
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to='images/%Y/%m.%d/', verbose_name='Файл')
    link_main_project = models.ForeignKey(to='MainProject', on_delete=models.CASCADE, verbose_name='Объект привязки')


class StepTemplates(models.Model):
    """
    Model template for create a step
    """
    name = models.CharField(max_length=255, verbose_name='Название схемы', db_index=True, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.SET_NULL, verbose_name='Кто создал', null=True)
    schema = models.JSONField(verbose_name='схема этапа')


class Step(models.Model):
    """
    Model step. show information about step, and what fields he has
    """
    name = models.CharField(max_length=255, verbose_name='Название этапа', db_index=True)
    placement = models.JSONField(verbose_name='Расположение')
    project_id = models.ForeignKey(to='MainProject', on_delete=models.CASCADE, verbose_name='id проекта',
                                   related_name='steps')
    noda_front = models.CharField(max_length=255, verbose_name='id ноды фронта')
    templates_schema = models.ForeignKey(to='StepTemplates', on_delete=models.SET_NULL, null=True,
                                         verbose_name='Схема для создания', related_name='steps')
    users_look = models.ManyToManyField(to=User, verbose_name='Те кто смотрят', blank=True, related_name='look')
    users_inspecting = models.ForeignKey(to=User, verbose_name='Тот кто проверяет', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='inspecting')
    users_editor = models.ForeignKey(to=User, verbose_name='Тот кто ответственен', on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='editor')
    responsible_persons_scheme = models.JSONField(verbose_name='Схема ответственных лиц', blank=True, default=dict)
    date_create = models.DateTimeField(verbose_name='Дата создание', auto_now_add=True)
    date_start = models.DateTimeField(verbose_name='Дата начала работы', blank=True, null=True)
    date_end = models.DateTimeField(verbose_name='Дата конца работы', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Steps'
        verbose_name = 'Step'
        verbose_name_plural = 'Steps'


class StepFields(models.Model):
    field = models.JSONField(verbose_name='Поле')
    step = models.ForeignKey(verbose_name='Связь с этапом', on_delete=models.CASCADE, to='Step', related_name='fields')

    class Meta:
        db_table = 'StepFields'
        verbose_name = 'StepField'
        verbose_name_plural = 'StepFields'


class FieldText(models.Model):
    """
    Text fild model step
    """
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Текст')
    text = models.CharField(max_length=255, verbose_name='Текст', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_text')


class FieldTextarea(models.Model):
    """
    Textarea fild model step
    """
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Большой текс')
    textarea = models.TextField(verbose_name='Большой текст', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_textarea')


class FieldDate(models.Model):
    """
    Date fild model step
    """
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Дата')
    time = models.DateField(verbose_name='Дата', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_date')


class FieldStartFinishTime(models.Model):
    """
    Start-Finish-Time fild model step
    """
    identify = models.CharField(max_length=255, verbose_name='Идентификатор поля', blank=True)
    name_field = models.CharField(max_length=255, verbose_name='Тип поля', default='Начало-Конец время')
    start = models.DateTimeField(verbose_name='Начало', blank=True)
    finish = models.DateTimeField(verbose_name='Конец', blank=True)
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_f_s_time')
