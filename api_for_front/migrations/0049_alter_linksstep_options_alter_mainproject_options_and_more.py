# Generated by Django 4.0 on 2023-10-16 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0048_rename_project_id_step_project'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='linksstep',
            options={'verbose_name': 'LinksStep', 'verbose_name_plural': 'LinksSteps'},
        ),
        migrations.AlterModelOptions(
            name='mainproject',
            options={'verbose_name': 'MainProject', 'verbose_name_plural': 'MainProjects'},
        ),
        migrations.AlterModelOptions(
            name='stepfiles',
            options={'verbose_name': 'StepFile', 'verbose_name_plural': 'StepFiles'},
        ),
        migrations.AlterModelOptions(
            name='steptemplates',
            options={'verbose_name': 'StepTemplate', 'verbose_name_plural': 'StepTemplates'},
        ),
        migrations.AlterModelTable(
            name='linksstep',
            table='LinksStep',
        ),
        migrations.AlterModelTable(
            name='mainproject',
            table='MainProject',
        ),
        migrations.AlterModelTable(
            name='stepfiles',
            table='StepFiles',
        ),
        migrations.AlterModelTable(
            name='steptemplates',
            table='StepTemplates',
        ),
    ]
