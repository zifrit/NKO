# Generated by Django 4.0 on 2023-09-22 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0026_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fields',
            name='step',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='api_for_front.step', verbose_name='связь с этапом'),
        ),
    ]