# Generated by Django 4.0 on 2023-10-16 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0049_alter_linksstep_options_alter_mainproject_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='beginner_in_project',
            field=models.BooleanField(default=False, verbose_name='Начинающий в проекте'),
        ),
    ]
