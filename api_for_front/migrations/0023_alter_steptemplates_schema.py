# Generated by Django 4.0 on 2023-09-21 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0022_alter_step_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='steptemplates',
            name='schema',
            field=models.JSONField(verbose_name='схема этапа'),
        ),
    ]