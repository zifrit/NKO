# Generated by Django 4.0 on 2023-11-04 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0080_alter_stepschema_template_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='schema_step',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='id схемы этапа'),
        ),
    ]
