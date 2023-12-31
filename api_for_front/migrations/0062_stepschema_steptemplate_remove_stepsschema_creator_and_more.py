# Generated by Django 4.0 on 2023-10-18 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api_for_front', '0061_stepsschema_template_project_templatemainproject'),
    ]

    operations = [
        migrations.CreateModel(
            name='StepSchema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название схемы')),
                ('template_project', models.PositiveIntegerField(blank=True, null=True, verbose_name='id шаблона проекта')),
                ('placement', models.JSONField(verbose_name='Расположение')),
                ('step_fields_schema', models.JSONField(verbose_name='схема полей этапа')),
                ('responsible_persons_scheme', models.JSONField(blank=True, default={'users_editor': '', 'users_inspecting': '', 'users_look': []}, verbose_name='Схема ответственных лиц')),
                ('first_in_project', models.BooleanField(default=False, verbose_name='Начинающий в проекте')),
                ('last_in_project', models.BooleanField(default=False, verbose_name='Завершающий в проекте')),
                ('noda_front', models.CharField(max_length=255, verbose_name='id ноды фронта')),
            ],
            options={
                'verbose_name': 'StepSchema',
                'verbose_name_plural': 'StepSchemas',
                'db_table': 'StepSchema',
            },
        ),
        migrations.CreateModel(
            name='StepTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Название схемы')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.user', verbose_name='Кто создал')),
                ('templates', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api_for_front.stepschema', verbose_name='схема')),
            ],
            options={
                'verbose_name': 'StepTemplate',
                'verbose_name_plural': 'StepTemplates',
                'db_table': 'StepTemplate',
            },
        ),
        migrations.RemoveField(
            model_name='stepsschema',
            name='creator',
        ),
        migrations.DeleteModel(
            name='StepTemplates',
        ),
        migrations.AlterField(
            model_name='step',
            name='step_schema',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='steps', to='api_for_front.stepschema', verbose_name='Схема для создания'),
        ),
        migrations.DeleteModel(
            name='StepsSchema',
        ),
    ]
