# Generated by Django 4.0 on 2023-10-18 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0063_rename_steptemplate_steptemplates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stepschema',
            name='original',
            field=models.BooleanField(default=False, verbose_name='Оригинал'),
        ),
    ]
