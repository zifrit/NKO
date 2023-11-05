from django.db import models
from django.contrib.auth.models import User


class MainKo(models.Model):
    """
    Model MainProject information about the main project
    """
    name = models.CharField(max_length=255, verbose_name='Название проекта', db_index=True, unique=True)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='Кто создал')
    template_ko = models.ForeignKey(to='TemplateMainKo', on_delete=models.PROTECT, verbose_name='Шаблон',
                                    related_name='ko')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')
    date_start = models.DateTimeField(verbose_name='Дата начала работы', blank=True, null=True)
    date_end = models.DateTimeField(verbose_name='Дата конца работы', blank=True, null=True)
    last_change = models.DateTimeField(auto_now=True, verbose_name='последние изменения')
    active = models.BooleanField(verbose_name='В процессе', default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'MainKo'
        verbose_name = 'MainKo'
        verbose_name_plural = 'MainKo'


class TemplateMainKo(models.Model):
    """
    Model TemplateMainProject
    """
    name = models.CharField(max_length=255, verbose_name='Название шаблона проекта', db_index=True, unique=True)
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='Кто создал')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')
    archive = models.BooleanField(verbose_name='Архив', default=False)
    finished = models.BooleanField(verbose_name='Законченность', default=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'TemplateMainKo'
        verbose_name = 'TemplateMainKo'
        verbose_name_plural = 'TemplatesMainKo'


class LinksStep(models.Model):
    """
    Model LinksStep information about the relationship between steps
    """
    start_id = models.PositiveIntegerField(verbose_name='начало связи')
    end_id = models.PositiveIntegerField(verbose_name='конец связи')
    description = models.CharField(max_length=255, verbose_name='описания', blank=True)
    project_id = models.PositiveIntegerField(verbose_name='id шаблона проекта', null=True)
    in_template = models.BooleanField(verbose_name='Относится ли к шаблону', default=True)
    data = models.JSONField(verbose_name='id фронта', default=dict)
    color = models.CharField(max_length=255, verbose_name='цвет', blank=True)

    class Meta:
        db_table = 'LinksStep'
        verbose_name = 'LinksStep'
        verbose_name_plural = 'LinksSteps'


class StepFiles(models.Model):
    """
    Model files step
    """
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to='file/%Y/%m-%d/', verbose_name='Файл')
    link_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, verbose_name='связь с этапом',
                                  related_name='step_files')
    link_field = models.ForeignKey(to='StepFields', on_delete=models.CASCADE, verbose_name='связь с полем',
                                   related_name='field_file')

    class Meta:
        db_table = 'StepFiles'
        verbose_name = 'StepFile'
        verbose_name_plural = 'StepFiles'


class StepImages(models.Model):
    """
    Model images step
    """
    file_name = models.CharField(verbose_name='Название файла', max_length=255)
    path_file = models.FileField(upload_to='images/%Y/%m.%d/', verbose_name='Файл')
    link_main_project = models.ForeignKey(to='TemplateMainKo', on_delete=models.CASCADE, verbose_name='Объект привязки')


class StepTemplates(models.Model):
    """
    Model Step templates
    """
    name = models.CharField(max_length=255, verbose_name='Название шаблона', db_index=True, unique=True)
    schema = models.OneToOneField(to='StepSchema', on_delete=models.CASCADE, verbose_name='схема')
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name='Кто создал', null=True)

    class Meta:
        db_table = 'StepTemplates'
        verbose_name = 'StepTemplates'
        verbose_name_plural = 'StepTemplates'


class StepSchema(models.Model):
    """
    Model schema for create a step
    """
    name = models.CharField(max_length=255, verbose_name='Название схемы', db_index=True)
    template_project = models.ForeignKey(to='TemplateMainKo', blank=True, null=True, verbose_name='Шаблона проекта',
                                         on_delete=models.CASCADE, related_name='step_schema')
    placement = models.JSONField(verbose_name='Расположение', default=dict)
    step_fields_schema = models.JSONField(verbose_name='схема полей этапа')
    responsible_persons_scheme = models.JSONField(verbose_name='Схема ответственных лиц', blank=True, default=dict({
        "users_editor": '',
        "users_look": [],
        "users_inspecting": ''
    }))
    first_in_project = models.BooleanField(verbose_name='Начинающий в проекте', default=False)
    last_in_project = models.BooleanField(verbose_name='Завершающий в проекте', default=False)
    original = models.BooleanField(verbose_name='Оригинал', default=False)
    noda_front = models.CharField(max_length=255, verbose_name='id ноды фронта', blank=True)

    class Meta:
        db_table = 'StepSchema'
        verbose_name = 'StepSchema'
        verbose_name_plural = 'StepSchemas'


class Step(models.Model):
    """
    Model step. show information about step, and what fields he has
    """
    name = models.CharField(max_length=255, verbose_name='Название этапа', db_index=True)
    placement = models.JSONField(verbose_name='Расположение')
    project = models.ForeignKey(to='MainKo', on_delete=models.CASCADE, verbose_name='id проекта',
                                related_name='steps', null=True, blank=True, )
    schema_step = models.PositiveIntegerField(verbose_name='id схемы этапа', blank=True, null=True)
    noda_front = models.CharField(max_length=255, verbose_name='id ноды фронта')
    users_look = models.ManyToManyField(to=User, verbose_name='Те кто смотрят', blank=True, related_name='look')
    users_inspecting = models.ForeignKey(to=User, verbose_name='Тот кто проверяет', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='inspecting')
    users_editor = models.ForeignKey(to=User, verbose_name='Тот кто ответственен', on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='editor')
    finished = models.BooleanField(verbose_name='Завершенность', default=False)
    active = models.BooleanField(verbose_name='В процессе', default=False)
    first_in_project = models.BooleanField(verbose_name='Начинающий в проекте', default=False)
    last_in_project = models.BooleanField(verbose_name='Завершающий в проекте', default=False)
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
