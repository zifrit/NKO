# Generated by Django 4.0 on 2023-10-17 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0053_alter_step_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldstartfinishtime',
            name='link_step',
        ),
        migrations.RemoveField(
            model_name='fieldtext',
            name='link_step',
        ),
        migrations.RemoveField(
            model_name='fieldtextarea',
            name='link_step',
        ),
        migrations.AlterField(
            model_name='step',
            name='responsible_persons_scheme',
            field=models.JSONField(blank=True, default={'users_editor': '', 'users_inspecting': '', 'users_look': []}, verbose_name='Схема ответственных лиц'),
        ),
        migrations.DeleteModel(
            name='FieldDate',
        ),
        migrations.DeleteModel(
            name='FieldStartFinishTime',
        ),
        migrations.DeleteModel(
            name='FieldText',
        ),
        migrations.DeleteModel(
            name='FieldTextarea',
        ),
    ]
