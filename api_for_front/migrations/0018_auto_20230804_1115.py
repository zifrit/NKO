# Generated by Django 3.2.5 on 2023-08-04 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0017_alter_steptemplates_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steptemplates',
            name='structure',
        ),
        migrations.RemoveField(
            model_name='steptemplates',
            name='structure_for_create',
        ),
        migrations.AddField(
            model_name='steptemplates',
            name='schema',
            field=models.JSONField(default=dict, verbose_name='схема этапа'),
        ),
        migrations.AddField(
            model_name='steptemplates',
            name='schema_for_create',
            field=models.JSONField(default=dict, verbose_name='схема для создания этапа'),
        ),
    ]