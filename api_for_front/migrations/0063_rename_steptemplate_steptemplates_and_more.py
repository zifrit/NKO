# Generated by Django 4.0 on 2023-10-18 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('api_for_front', '0062_stepschema_steptemplate_remove_stepsschema_creator_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StepTemplate',
            new_name='StepTemplates',
        ),
        migrations.AlterModelOptions(
            name='steptemplates',
            options={'verbose_name': 'StepTemplates', 'verbose_name_plural': 'StepTemplates'},
        ),
        migrations.AlterModelTable(
            name='steptemplates',
            table='StepTemplates',
        ),
    ]
