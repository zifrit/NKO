# Generated by Django 4.0 on 2023-10-16 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_for_front', '0052_alter_step_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Название этапа'),
        ),
    ]
