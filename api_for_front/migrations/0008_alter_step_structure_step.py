# Generated by Django 3.2.5 on 2023-07-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0007_auto_20230720_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='structure_step',
            field=models.JSONField(default=dict, verbose_name='структура этапа'),
        ),
    ]
