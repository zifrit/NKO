# Generated by Django 3.2.5 on 2023-06-06 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0002_auto_20230606_1412'),
    ]

    operations = [
        migrations.CreateModel(
            name='FieldDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identify', models.CharField(max_length=255, verbose_name='Идентификатор поля')),
                ('name_field', models.CharField(default='Дата', max_length=255, verbose_name='Имя поля')),
                ('time', models.DateField(verbose_name='Дата')),
            ],
        ),
        migrations.CreateModel(
            name='FieldStartFinishTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identify', models.CharField(max_length=255, verbose_name='Идентификатор поля')),
                ('name_field', models.CharField(default='Начало-Конец время', max_length=255, verbose_name='Имя поля')),
                ('start', models.DateField(verbose_name='Начало')),
                ('finish', models.DateField(verbose_name='Конец')),
            ],
        ),
        migrations.AddField(
            model_name='fieldtext',
            name='name_field',
            field=models.CharField(default='Текст', max_length=255, verbose_name='Имя поля'),
        ),
        migrations.AddField(
            model_name='fieldtextarea',
            name='name_field',
            field=models.CharField(default='Большой текс', max_length=255, verbose_name='Имя поля'),
        ),
        migrations.AddField(
            model_name='kostage',
            name='SF_time',
            field=models.ManyToManyField(blank=True, to='api_for_front.FieldStartFinishTime', verbose_name='Срок'),
        ),
        migrations.AddField(
            model_name='kostage',
            name='date',
            field=models.ManyToManyField(blank=True, to='api_for_front.FieldDate', verbose_name='Дата'),
        ),
    ]
