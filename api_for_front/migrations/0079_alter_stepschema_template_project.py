# Generated by Django 4.0 on 2023-10-22 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0078_alter_stepschema_template_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stepschema',
            name='template_project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_for_front.templatemainko', verbose_name='Шаблона проекта'),
        ),
    ]
