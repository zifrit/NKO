# Generated by Django 4.0 on 2023-09-21 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0020_step_metadata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='steptemplates',
            name='schema_for_create',
        ),
    ]
