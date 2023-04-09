# Generated by Django 3.2.5 on 2023-04-09 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identify', models.CharField(max_length=255, verbose_name='Идентификатор поля')),
                ('text', models.CharField(max_length=255, verbose_name='Текст')),
            ],
        ),
        migrations.CreateModel(
            name='FieldTextarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identify', models.CharField(max_length=255, verbose_name='Идентификатор поля')),
                ('textarea', models.TextField(verbose_name='Большой текст')),
            ],
        ),
        migrations.CreateModel(
            name='MainTableKO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название проекта')),
                ('stages_mass', models.CharField(max_length=255, verbose_name='Массив из id этапов')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кто создал')),
            ],
        ),
        migrations.CreateModel(
            name='KoStage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_create', models.DateTimeField(verbose_name='Дата создание')),
                ('date_start', models.DateTimeField(verbose_name='Дата начала работы')),
                ('date_end', models.DateTimeField(verbose_name='Дата конца работы')),
                ('text', models.ManyToManyField(to='api_for_front.FieldText', verbose_name='Текст')),
                ('textarea', models.ManyToManyField(to='api_for_front.FieldTextarea', verbose_name='Большой текст')),
            ],
        ),
        migrations.CreateModel(
            name='KoImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255, verbose_name='Название файла')),
                ('path_file', models.FileField(upload_to='images/%Y/%m.%d/', verbose_name='Файл')),
                ('ko', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_for_front.maintableko', verbose_name='Объект привязки')),
            ],
        ),
        migrations.CreateModel(
            name='KoFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255, verbose_name='Название файла')),
                ('path_file', models.FileField(upload_to='file/%Y/%m.%d/', verbose_name='Файл')),
                ('ko', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api_for_front.maintableko', verbose_name='Объект привязки')),
            ],
        ),
    ]
