# Generated by Django 4.0 on 2023-10-18 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0064_stepschema_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steptemplates',
            name='name',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Название шаблона'),
        ),
    ]
