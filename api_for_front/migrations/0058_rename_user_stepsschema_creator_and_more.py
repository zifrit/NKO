# Generated by Django 4.0 on 2023-10-18 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0057_rename_beginner_in_project_step_first_in_project_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stepsschema',
            old_name='user',
            new_name='creator',
        ),
        migrations.AddField(
            model_name='stepsschema',
            name='noda_front',
            field=models.CharField(default=1, max_length=255, verbose_name='id ноды фронта'),
            preserve_default=False,
        ),
    ]
